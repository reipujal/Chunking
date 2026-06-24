"""
retriever.py — Chunk retrieval interface for eval harness.

Retrievers:
  TFIDFRetriever    — Baseline: TF-IDF over chunk body (frontmatter stripped).
  SemanticRetriever — Dense: BAAI/bge-small-en-v1.5 via sentence-transformers.
                      Cache: eval/index/<model-slug>/ (embeddings.npy + chunk_ids.json).

Public interface:
  retrieve(query, k)                          — lexical (module-level, backward-compat)
  make_retriever(kind, chunks) -> retriever   — factory for score.py
  rrf_fuse(ranked_lists) -> list[str]         — Reciprocal Rank Fusion helper

Corpus text indexed: chunk body (Markdown, frontmatter stripped). Same text for both
retrievers → apples-to-apples comparison.
"""

import re
import math
import json
import yaml
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import date as _date

CHUNKS_DIR = Path("chunks")
INDEX_DIR = Path("eval/index")


# ---------------------------------------------------------------------------
# Cache manifest helpers — shared by all three retriever classes.
# body_hashes keys on self._chunks[cid]["body"], the exact string passed to
# self._model.encode() before any windowing or truncation. Any body edit
# invalidates the cache by construction.
# ---------------------------------------------------------------------------

def _compute_manifest(chunks: dict, model_name: str, max_tokens: int, recipe_id: str) -> dict:
    return {
        "model_name": model_name,
        "max_tokens": max_tokens,
        "recipe_id": recipe_id,
        "body_hashes": {
            cid: hashlib.sha256(chunks[cid]["body"].encode("utf-8")).hexdigest()
            for cid in sorted(chunks)
        },
    }


def _manifest_valid(cached_meta: dict, manifest: dict) -> bool:
    return cached_meta.get("manifest") == manifest


# ---------------------------------------------------------------------------
# Chunk loading
# ---------------------------------------------------------------------------

def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Split a chunk file into (frontmatter_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2].strip()


def load_chunks(chunks_dir: Path = CHUNKS_DIR) -> dict[str, dict]:
    """Load all chunks. Returns {chunk_id: {id, body, sources, area, ...}}."""
    chunks: dict[str, dict] = {}
    for md_file in sorted(chunks_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue
        raw = md_file.read_text(encoding="utf-8")
        fm, body = strip_frontmatter(raw)
        chunk_id = fm.get("id")
        if not chunk_id:
            continue
        chunks[chunk_id] = {
            "id": chunk_id,
            "path": str(md_file),
            "body": body,
            "sources": fm.get("sources", []),
            "area": fm.get("area", ""),
            "chunk_type": fm.get("chunk_type", ""),
            "quality": fm.get("quality", ""),
        }
    return chunks


# ---------------------------------------------------------------------------
# TF-IDF baseline
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Lowercase + split on non-alphanumeric. Remove stopwords."""
    stopwords = {
        "the", "a", "an", "is", "are", "in", "of", "to", "and", "or",
        "for", "can", "you", "it", "this", "that", "be", "has", "have",
        "by", "with", "at", "on", "as", "from", "which", "these", "those",
        "will", "not", "if", "its", "their", "they", "we", "was", "were",
        "been", "being", "do", "does", "did", "so", "also", "only", "all",
        "when", "where", "how", "what", "who", "each", "more", "may",
        "used", "use", "using", "based", "per", "than", "into", "about",
    }
    tokens = re.findall(r"[a-z][a-z0-9/_-]*", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 1]


class TFIDFRetriever:
    def __init__(self, chunks: dict[str, dict]):
        self._chunks = chunks
        self._ids: list[str] = list(chunks.keys())
        self._tf: dict[str, dict[str, float]] = {}  # chunk_id -> {term: tf}
        self._df: dict[str, int] = defaultdict(int)  # term -> doc count
        self._n = len(self._ids)
        self._build()

    def _build(self):
        for cid, chunk in self._chunks.items():
            text = chunk["body"] + " " + " ".join(
                a if isinstance(a, str) else ""
                for a in chunk.get("sources", [])
            )
            tokens = _tokenize(text)
            if not tokens:
                self._tf[cid] = {}
                continue
            freq: dict[str, int] = defaultdict(int)
            for t in tokens:
                freq[t] += 1
            total = len(tokens)
            self._tf[cid] = {t: c / total for t, c in freq.items()}
            for t in freq:
                self._df[t] += 1

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        tokens = _tokenize(query)
        if not tokens:
            return []
        scores: dict[str, float] = defaultdict(float)
        for term in tokens:
            if term not in self._df:
                continue
            idf = math.log((self._n + 1) / (self._df[term] + 1)) + 1
            for cid, tf_map in self._tf.items():
                tf = tf_map.get(term, 0.0)
                scores[cid] += tf * idf
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [cid for cid, _ in ranked[:k]]


# ---------------------------------------------------------------------------
# Semantic retriever — BAAI/bge-small-en-v1.5
# ---------------------------------------------------------------------------

class SemanticRetriever:
    """Dense retriever using BAAI/bge-small-en-v1.5 via sentence-transformers.

    Model notes (bge-v1.5):
      - Query prefix:   "Represent this sentence for searching relevant passages: "
      - Passage prefix: none
      - Similarity:     cosine (= dot product after L2-norm)
      - Max tokens:     512
      - Embedding dim:  384

    Cache layout: eval/index/bge-small-en-v1.5/
      embeddings.npy   — float32 array (N, 384)
      chunk_ids.json   — list of N chunk IDs (row order matches embeddings)
      meta.json        — model, n_chunks, truncated, generated_at
    """

    MODEL_NAME = "BAAI/bge-small-en-v1.5"
    QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
    MAX_TOKENS = 512
    RECIPE_ID  = "bge-small-v1.5-whole-chunk"

    def __init__(self, chunks: dict[str, dict], model_name: str = MODEL_NAME):
        self._chunks = chunks
        self._model_name = model_name
        slug = model_name.split("/")[-1]
        self._cache_path = INDEX_DIR / slug
        self._chunk_ids: list[str] = []
        self._embeddings = None   # np.ndarray (N, dim) float32
        self._model = None
        self.truncated_count: int = 0
        self._build()

    # ------------------------------------------------------------------
    # Index build / cache
    # ------------------------------------------------------------------

    def _cache_valid(self) -> bool:
        emb_p  = self._cache_path / "embeddings.npy"
        ids_p  = self._cache_path / "chunk_ids.json"
        meta_p = self._cache_path / "meta.json"
        if not (emb_p.exists() and ids_p.exists() and meta_p.exists()):
            return False
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            return False
        manifest = _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID)
        return _manifest_valid(meta, manifest)

    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)

    def _build(self):
        import numpy as np

        emb_p = self._cache_path / "embeddings.npy"
        ids_p = self._cache_path / "chunk_ids.json"
        meta_p = self._cache_path / "meta.json"

        if self._cache_valid():
            self._chunk_ids = json.loads(ids_p.read_text(encoding="utf-8"))
            self._embeddings = np.load(str(emb_p))
            meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
            self.truncated_count = meta.get("truncated", -1)
            print(
                f"  [semantic] Cache loaded: {len(self._chunk_ids)} chunks, "
                f"{self.truncated_count} truncated — {self._cache_path}"
            )
            return

        print(f"  [semantic] Building index ({len(self._chunks)} chunks, model={self._model_name})...")
        self._load_model()

        self._chunk_ids = list(self._chunks.keys())
        texts = [self._chunks[cid]["body"] for cid in self._chunk_ids]

        # Count chunks that exceed MAX_TOKENS before truncation
        tokenizer = self._model.tokenizer
        self.truncated_count = 0
        for t in texts:
            toks = tokenizer(t, truncation=False)["input_ids"]
            if len(toks) > self.MAX_TOKENS:
                self.truncated_count += 1
        print(
            f"  [semantic] Chunks exceeding {self.MAX_TOKENS} tokens: "
            f"{self.truncated_count}/{len(texts)}"
        )

        # Passages: no prefix for bge-v1.5
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=32,
        )
        self._embeddings = np.array(embeddings, dtype=np.float32)

        # Persist cache
        self._cache_path.mkdir(parents=True, exist_ok=True)
        np.save(str(emb_p), self._embeddings)
        ids_p.write_text(json.dumps(self._chunk_ids), encoding="utf-8")
        meta_p.write_text(json.dumps({
            "model": self._model_name,
            "n_chunks": len(self._chunk_ids),
            "truncated": self.truncated_count,
            "generated_at": _date.today().isoformat(),
            "manifest": _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID),
        }, indent=2), encoding="utf-8")
        print(f"  [semantic] Index saved: {self._cache_path}")

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        import numpy as np

        if self._model is None:
            self._load_model()

        q_emb = self._model.encode(
            [self.QUERY_PREFIX + query],
            normalize_embeddings=True,
        )[0]
        # Cosine similarity = dot product (both L2-normalized)
        scores = self._embeddings @ q_emb
        top_idx = np.argsort(-scores)[:k]
        return [self._chunk_ids[i] for i in top_idx]

    def smoke_test(self, chunks: dict[str, dict]) -> tuple[bool, str]:
        """Return (passed, message). Query = first chunk title; expect rank-1 = that chunk."""
        if not chunks:
            return False, "no chunks"
        target_id = next(iter(chunks))
        # Extract H1 title from body
        body = chunks[target_id]["body"]
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if not title_match:
            return False, f"no H1 title in {target_id}"
        title = title_match.group(1).strip()
        top1 = self.retrieve(title, k=1)
        passed = bool(top1 and top1[0] == target_id)
        msg = (
            f"query='{title[:60]}' -> rank-1={top1[0] if top1 else 'none'} "
            f"(expected {target_id})"
        )
        return passed, msg


# ---------------------------------------------------------------------------
# Long-context whole-chunk retriever — jinaai/jina-embeddings-v2-base-en
# ---------------------------------------------------------------------------

class LongContextRetriever:
    """Dense retriever with 8192-token context (no truncation for SAP chunks).

    Model: BAAI/bge-m3
      - Context:   8192 tokens
      - Embedding: 1024-dim
      - Prefix:    none (symmetric; same text for queries and passages)
      - trust_remote_code: not required

    Cache: eval/index/bge-m3/
    """

    MODEL_NAME = "BAAI/bge-m3"
    MAX_TOKENS = 8192
    RECIPE_ID  = "bge-m3-whole-chunk"

    def __init__(self, chunks: dict[str, dict], model_name: str = MODEL_NAME):
        self._chunks = chunks
        self._model_name = model_name
        slug = model_name.split("/")[-1]
        self._cache_path = INDEX_DIR / slug
        self._chunk_ids: list[str] = []
        self._embeddings = None
        self._model = None
        self.max_tokens_found: int = 0
        self.truncated_count: int = 0
        self._build()

    def _cache_valid(self) -> bool:
        emb_p  = self._cache_path / "embeddings.npy"
        ids_p  = self._cache_path / "chunk_ids.json"
        meta_p = self._cache_path / "meta.json"
        if not (emb_p.exists() and ids_p.exists() and meta_p.exists()):
            return False
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            return False
        manifest = _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID)
        return _manifest_valid(meta, manifest)

    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)

    def _build(self):
        import numpy as np
        emb_p = self._cache_path / "embeddings.npy"
        ids_p = self._cache_path / "chunk_ids.json"
        meta_p = self._cache_path / "meta.json"

        if self._cache_valid():
            self._chunk_ids = json.loads(ids_p.read_text(encoding="utf-8"))
            self._embeddings = np.load(str(emb_p))
            meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
            self.max_tokens_found = meta.get("max_tokens_found", -1)
            self.truncated_count = meta.get("truncated", 0)
            print(
                f"  [long-ctx] Cache loaded: {len(self._chunk_ids)} chunks, "
                f"max_tokens={self.max_tokens_found}, {self.truncated_count} truncated"
                f" — {self._cache_path}"
            )
            return

        print(f"  [long-ctx] Building index ({len(self._chunks)} chunks, model={self._model_name})...")
        self._load_model()

        self._chunk_ids = list(self._chunks.keys())
        texts = [self._chunks[cid]["body"] for cid in self._chunk_ids]

        tokenizer = self._model.tokenizer
        token_counts = []
        for t in texts:
            toks = tokenizer(t, truncation=False)["input_ids"]
            token_counts.append(len(toks))
        self.max_tokens_found = max(token_counts)
        self.truncated_count = sum(1 for c in token_counts if c > self.MAX_TOKENS)
        print(
            f"  [long-ctx] Token counts: max={self.max_tokens_found}, "
            f"limit={self.MAX_TOKENS}, truncated={self.truncated_count}/{len(texts)}"
        )

        # Jina-v2: no prefix for passages
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=16,
        )
        self._embeddings = np.array(embeddings, dtype=np.float32)

        self._cache_path.mkdir(parents=True, exist_ok=True)
        np.save(str(emb_p), self._embeddings)
        ids_p.write_text(json.dumps(self._chunk_ids), encoding="utf-8")
        meta_p.write_text(json.dumps({
            "model": self._model_name,
            "n_chunks": len(self._chunk_ids),
            "max_tokens_found": self.max_tokens_found,
            "truncated": self.truncated_count,
            "generated_at": _date.today().isoformat(),
            "manifest": _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID),
        }, indent=2), encoding="utf-8")
        print(f"  [long-ctx] Index saved: {self._cache_path}")

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        import numpy as np
        if self._model is None:
            self._load_model()
        # Jina-v2: no query prefix
        q_emb = self._model.encode([query], normalize_embeddings=True)[0]
        scores = self._embeddings @ q_emb
        top_idx = np.argsort(-scores)[:k]
        return [self._chunk_ids[i] for i in top_idx]

    def smoke_test(self, chunks: dict[str, dict]) -> tuple[bool, str]:
        if not chunks:
            return False, "no chunks"
        target_id = next(iter(chunks))
        body = chunks[target_id]["body"]
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if not title_match:
            return False, f"no H1 title in {target_id}"
        title = title_match.group(1).strip()
        top1 = self.retrieve(title, k=1)
        passed = bool(top1 and top1[0] == target_id)
        msg = (
            f"query='{title[:60]}' -> rank-1={top1[0] if top1 else 'none'} "
            f"(expected {target_id})"
        )
        return passed, msg


# ---------------------------------------------------------------------------
# Window-pooled retriever — same model as LongContextRetriever
# B vs C: model identical, only granularity differs
# ---------------------------------------------------------------------------

class WindowPooledRetriever:
    """Window-pooled dense retriever. SAME model as LongContextRetriever.

    Each chunk body is split into overlapping windows of <=WINDOW_TOKENS model
    tokens with STRIDE_TOKENS stride (~25% overlap). Each window is encoded
    independently. At retrieval time:
      score(chunk) = max(sim(query_emb, window_emb)) over all chunk windows.

    This is the P3 granularity probe: B=whole-chunk vs C=window-pooled.
    Model is identical so the only variable is indexing granularity.

    Cache: eval/index/jina-embeddings-v2-base-en-window/
    """

    MODEL_NAME        = LongContextRetriever.MODEL_NAME  # SAME model as B — do not change
    WINDOW_TOKENS     = 400   # target window size (model tokens, without special)
    STRIDE_TOKENS     = 300   # 100-token overlap per step = ~25% of window
    MAX_WINDOW_TOKENS = 512   # hard cap for verification
    MAX_TOKENS        = MAX_WINDOW_TOKENS  # alias for manifest (_compute_manifest interface)
    RECIPE_ID         = "bge-m3-window-pooled"

    def __init__(self, chunks: dict[str, dict], model_name: str = MODEL_NAME):
        self._chunks = chunks
        self._model_name = model_name
        slug = model_name.split("/")[-1] + "-window"
        self._cache_path = INDEX_DIR / slug
        self._chunk_ids: list[str] = list(chunks.keys())
        self._window_embeddings = None   # np.ndarray (total_windows, dim)
        self._window_index: list[dict] = []
        self._windows_per_chunk: dict[str, list[int]] = {}  # chunk_id -> [global_idx, ...]
        self._model = None
        self.stats: dict = {}
        self._build()

    def _cache_valid(self) -> bool:
        emb_p  = self._cache_path / "window_embeddings.npy"
        idx_p  = self._cache_path / "window_index.json"
        meta_p = self._cache_path / "meta.json"
        if not (emb_p.exists() and idx_p.exists() and meta_p.exists()):
            return False
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            return False
        manifest = _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID)
        return _manifest_valid(meta, manifest)

    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)

    def _make_windows(self, text: str) -> list[str]:
        """Split text into overlapping windows using model tokenizer."""
        tokenizer = self._model.tokenizer
        token_ids = tokenizer(text, add_special_tokens=False, truncation=False)["input_ids"]
        windows = []
        start = 0
        while start < len(token_ids):
            end = min(start + self.WINDOW_TOKENS, len(token_ids))
            window_ids = token_ids[start:end]
            window_text = tokenizer.decode(window_ids, skip_special_tokens=True)
            windows.append(window_text)
            if end >= len(token_ids):
                break
            start += self.STRIDE_TOKENS
        return windows if windows else [text]

    def _build(self):
        import numpy as np
        emb_p = self._cache_path / "window_embeddings.npy"
        idx_p = self._cache_path / "window_index.json"
        meta_p = self._cache_path / "meta.json"

        if self._cache_valid():
            self._window_embeddings = np.load(str(emb_p))
            self._window_index = json.loads(idx_p.read_text(encoding="utf-8"))
            self._windows_per_chunk = {}
            for i, w in enumerate(self._window_index):
                self._windows_per_chunk.setdefault(w["chunk_id"], []).append(i)
            meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
            self.stats = meta
            print(
                f"  [window] Cache loaded: {self._window_embeddings.shape[0]} windows "
                f"from {len(self._windows_per_chunk)} chunks — {self._cache_path}"
            )
            return

        print(f"  [window] Building window index ({len(self._chunks)} chunks, model={self._model_name})...")
        self._load_model()

        all_window_texts: list[str] = []
        self._window_index = []
        self._windows_per_chunk = {}
        windows_counts: list[int] = []
        max_window_tokens_seen = 0
        tokenizer = self._model.tokenizer

        for cid in self._chunk_ids:
            body = self._chunks[cid]["body"]
            windows = self._make_windows(body)
            windows_counts.append(len(windows))
            for wnum, wtext in enumerate(windows):
                # Verify window token count including special tokens
                w_toks = tokenizer(wtext, truncation=False)["input_ids"]
                max_window_tokens_seen = max(max_window_tokens_seen, len(w_toks))
                widx = len(all_window_texts)
                all_window_texts.append(wtext)
                self._window_index.append({"chunk_id": cid, "window_num": wnum})
                self._windows_per_chunk.setdefault(cid, []).append(widx)

        total_windows = len(all_window_texts)
        avg_windows = sum(windows_counts) / len(windows_counts) if windows_counts else 0
        print(
            f"  [window] Total windows: {total_windows} | "
            f"per chunk: min={min(windows_counts)}, max={max(windows_counts)}, "
            f"avg={avg_windows:.1f}"
        )
        print(
            f"  [window] Max window tokens (incl special): {max_window_tokens_seen} "
            f"(limit={self.MAX_WINDOW_TOKENS})"
        )
        if max_window_tokens_seen > self.MAX_WINDOW_TOKENS:
            print(f"  [window] WARNING: {max_window_tokens_seen} > {self.MAX_WINDOW_TOKENS} — check stride/window size")

        # Jina-v2: no prefix for passages
        self._window_embeddings = np.array(
            self._model.encode(
                all_window_texts,
                normalize_embeddings=True,
                show_progress_bar=True,
                batch_size=32,
            ),
            dtype=np.float32,
        )

        self._cache_path.mkdir(parents=True, exist_ok=True)
        np.save(str(emb_p), self._window_embeddings)
        idx_p.write_text(json.dumps(self._window_index), encoding="utf-8")
        self.stats = {
            "model": self._model_name,
            "n_chunks": len(self._chunks),
            "total_windows": total_windows,
            "windows_min": min(windows_counts),
            "windows_max": max(windows_counts),
            "windows_avg": round(avg_windows, 1),
            "max_window_tokens": max_window_tokens_seen,
            "window_size_tokens": self.WINDOW_TOKENS,
            "stride_tokens": self.STRIDE_TOKENS,
            "generated_at": _date.today().isoformat(),
            "manifest": _compute_manifest(self._chunks, self._model_name, self.MAX_TOKENS, self.RECIPE_ID),
        }
        meta_p.write_text(json.dumps(self.stats, indent=2), encoding="utf-8")
        print(f"  [window] Index saved: {self._cache_path}")

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        import numpy as np
        if self._model is None:
            self._load_model()
        # Jina-v2: no query prefix
        q_emb = self._model.encode([query], normalize_embeddings=True)[0]
        # Score each window; aggregate to chunk via max-pool
        window_scores = self._window_embeddings @ q_emb
        chunk_scores: dict[str, float] = {}
        for cid, widx_list in self._windows_per_chunk.items():
            chunk_scores[cid] = float(np.max(window_scores[widx_list]))
        ranked = sorted(chunk_scores.items(), key=lambda x: -x[1])
        return [cid for cid, _ in ranked[:k]]

    def smoke_test(self, chunks: dict[str, dict]) -> tuple[bool, str]:
        if not chunks:
            return False, "no chunks"
        target_id = next(iter(chunks))
        body = chunks[target_id]["body"]
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if not title_match:
            return False, f"no H1 title in {target_id}"
        title = title_match.group(1).strip()
        top1 = self.retrieve(title, k=1)
        passed = bool(top1 and top1[0] == target_id)
        msg = (
            f"query='{title[:60]}' -> rank-1={top1[0] if top1 else 'none'} "
            f"(expected {target_id})"
        )
        return passed, msg


# ---------------------------------------------------------------------------
# Reciprocal Rank Fusion
# ---------------------------------------------------------------------------

def rrf_fuse(rankings: list[list[str]], rrf_k: int = 60) -> list[str]:
    """Fuse multiple ranked lists via Reciprocal Rank Fusion.

    rrf_k=60 is the standard constant (Cormack et al. 2009).
    """
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1.0 / (rrf_k + rank)
    return sorted(scores.keys(), key=lambda x: -scores[x])


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_retriever(kind: str, chunks: dict[str, dict]):
    """Return a retriever instance for *kind*.

    Kinds: 'lexical', 'semantic', 'semantic_long', 'semantic_window'
    """
    if kind == "semantic":
        return SemanticRetriever(chunks)
    if kind == "semantic_long":
        return LongContextRetriever(chunks)
    if kind == "semantic_window":
        return WindowPooledRetriever(chunks)
    return TFIDFRetriever(chunks)


# ---------------------------------------------------------------------------
# Backward-compat module-level API (used by score.py --retriever lexical)
# ---------------------------------------------------------------------------

_retriever: TFIDFRetriever | None = None
_chunks_cache: dict[str, dict] | None = None


def get_retriever(chunks_dir: Path = CHUNKS_DIR) -> TFIDFRetriever:
    global _retriever, _chunks_cache
    if _retriever is None:
        _chunks_cache = load_chunks(chunks_dir)
        _retriever = TFIDFRetriever(_chunks_cache)
    return _retriever


def retrieve(query: str, k: int = 10, chunks_dir: Path = CHUNKS_DIR) -> list[str]:
    """Public interface: retrieve top-k chunk IDs for a query (lexical)."""
    return get_retriever(chunks_dir).retrieve(query, k)


def get_chunks(chunks_dir: Path = CHUNKS_DIR) -> dict[str, dict]:
    get_retriever(chunks_dir)
    return _chunks_cache
