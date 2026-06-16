"""
retriever.py — Chunk retrieval interface for eval harness.

Baseline: TF-IDF over chunk body text (frontmatter stripped).
Interface: retrieve(query, k) -> list[chunk_id]

The retriever is swappable — replace build_index / retrieve_fn to use
embeddings or any other backend without touching score.py.
"""

import re
import math
import yaml
from pathlib import Path
from collections import defaultdict

CHUNKS_DIR = Path("chunks")


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


_retriever: TFIDFRetriever | None = None
_chunks_cache: dict[str, dict] | None = None


def get_retriever(chunks_dir: Path = CHUNKS_DIR) -> TFIDFRetriever:
    global _retriever, _chunks_cache
    if _retriever is None:
        _chunks_cache = load_chunks(chunks_dir)
        _retriever = TFIDFRetriever(_chunks_cache)
    return _retriever


def retrieve(query: str, k: int = 10, chunks_dir: Path = CHUNKS_DIR) -> list[str]:
    """Public interface: retrieve top-k chunk IDs for a query."""
    return get_retriever(chunks_dir).retrieve(query, k)


def get_chunks(chunks_dir: Path = CHUNKS_DIR) -> dict[str, dict]:
    get_retriever(chunks_dir)
    return _chunks_cache
