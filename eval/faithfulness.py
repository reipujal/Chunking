#!/usr/bin/env python3
"""
eval/faithfulness.py — P-gen Phase 1: Faithfulness / Groundedness harness.

Measures whether RAG-generated answers are grounded in retrieved context.

Two question sets:
  positive   — full pipeline (retrieve → generate → judge). Measures grounding
               when answer is recoverable AND captures retrieval-miss behaviour.
  abstention — same questions but gold chunk excluded from context. Measures
               whether the system abstains vs hallucinates when evidence is absent.

Usage:
    python eval/faithfulness.py              # sample: 5 positive + 3 abstention
    python eval/faithfulness.py --full       # all mappable questions
    python eval/faithfulness.py --n-positive 10 --n-abstention 5
"""

import sys
import os
import json
import re
import time
import argparse
from collections import defaultdict
from pathlib import Path
from datetime import date

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.retriever import load_chunks, make_retriever, strip_frontmatter
from eval.score import derive_gold_chunk_ids

from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GENERATOR_MODEL = os.getenv("VAES_MODEL", "claude-sonnet-4-6")
JUDGE_MODEL      = os.getenv("JUDGE_MODEL", GENERATOR_MODEL)

GOLD_DIR    = Path("eval/gold")
RESULTS_DIR = Path("eval/results")
CHUNKS_DIR  = Path("chunks")

DEFAULT_TOP_K      = 5
DEFAULT_N_POSITIVE = 5
DEFAULT_N_ABSTENTION = 3

ABSTENTION_PHRASE = "No puedo responder con la documentación proporcionada."

# ---------------------------------------------------------------------------
# Prompts (verbatim from task spec)
# ---------------------------------------------------------------------------

GENERATOR_SYSTEM = (
    "Eres un asistente de SAP SD. Responde la pregunta USANDO SOLO los documentos "
    "de contexto. Reglas: (1) usa solo información presente en el contexto; NO uses "
    "conocimiento externo o previo. (2) Si el contexto no contiene la respuesta, "
    "responde EXACTAMENTE: 'No puedo responder con la documentación proporcionada.' "
    "y nada más. (3) No mezcles releases de SAP: si el contexto indica un release "
    "(p.ej. S/4HANA 1909 vs 2020), respétalo y no generalices entre releases. "
    "(4) Cita el/los id(s) de los documentos de contexto usados, en una línea final "
    "'Fuentes: <ids>'. (5) Sé conciso y preciso."
)

JUDGE_SYSTEM = (
    "Eres un evaluador estricto de grounding. Recibes una PREGUNTA, los DOCUMENTOS "
    "DE CONTEXTO dados a un asistente, y su RESPUESTA. Juzga SOLO si la respuesta "
    "está fundada en el contexto — NO uses tu propio conocimiento SAP, NO juzgues si "
    "es 'correcta' en general. Pasos: (1) descompón la RESPUESTA en afirmaciones "
    "atómicas. (2) Para cada afirmación, busca el fragmento textual del CONTEXTO que "
    "la respalda; cópialo VERBATIM en 'support'. Regla crítica: si no puedes citar un "
    "fragmento textual literal del CONTEXTO que respalde la afirmación, su label DEBE "
    "ser UNSUPPORTED — NO uses tu conocimiento propio para respaldarla. (3) clasifica: "
    "SUPPORTED (el 'support' lo respalda directamente), PARTIAL (parcial/sobre-afirmada "
    "— el contexto cubre parte pero no todo), UNSUPPORTED (no hay fragmento en el "
    "CONTEXTO). (4) determina si la respuesta es una abstención. (5) marca "
    "release-mixing (afirma hechos de un release ausentes del contexto, o mezcla "
    "releases). (6) calcula grounded_fraction = (SUPPORTED + 0.5*PARTIAL) / "
    "total_claims. Devuelve SOLO JSON válido: "
    '{"claims":[{"text":"...","label":"SUPPORTED|PARTIAL|UNSUPPORTED",'
    '"support":"<fragmento verbatim del CONTEXTO, o cadena vacía si UNSUPPORTED>"}],'
    '"is_abstention":bool,"release_mixing":bool,"grounded_fraction":float}. '
    "Sin prosa fuera del JSON."
)

# ---------------------------------------------------------------------------
# Chunk loading (extended with sap_release and title)
# ---------------------------------------------------------------------------

def load_chunks_extended(chunks_dir: Path = CHUNKS_DIR) -> dict:
    """Extends load_chunks() with sap_release and title fields."""
    chunks = load_chunks(chunks_dir)
    for chunk_id, chunk in chunks.items():
        raw = Path(chunk["path"]).read_text(encoding="utf-8")
        fm, _ = strip_frontmatter(raw)
        chunk["sap_release"] = fm.get("sap_release", "not specified")
        chunk["title"] = fm.get("title", chunk_id)
    return chunks

# ---------------------------------------------------------------------------
# Gold loading
# ---------------------------------------------------------------------------

def load_all_gold_questions() -> list[dict]:
    """Load all non-excluded, mappable questions from every *_assessments.json."""
    questions = []
    for gold_file in sorted(GOLD_DIR.glob("*_assessments.json")):
        data = json.loads(gold_file.read_text(encoding="utf-8"))
        src = data.get("doc", gold_file.stem.split("_")[0])
        for q in data.get("questions", []):
            if q.get("excluded"):
                continue
            if not q.get("mappable", True):
                continue
            q = dict(q)  # shallow copy to avoid mutating the original
            q["_src"] = src
            questions.append(q)
    return questions

# ---------------------------------------------------------------------------
# Context formatting
# ---------------------------------------------------------------------------

def format_context(chunk_ids: list[str], chunks: dict, max_body: int = 3000) -> str:
    parts = []
    for cid in chunk_ids:
        chunk = chunks.get(cid)
        if not chunk:
            continue
        release = chunk.get("sap_release", "not specified")
        body = chunk["body"][:max_body]
        parts.append(f"[ID: {cid} | Release: {release}]\n{body}")
    return "\n\n---\n\n".join(parts)

# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_answer(client: Anthropic, question: str, context: str) -> str:
    user_msg = f"Pregunta: {question}\n\nDocumentos de contexto:\n\n{context}"
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=GENERATOR_MODEL,
                system=GENERATOR_SYSTEM,
                messages=[
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
                max_tokens=600,
            )
            return resp.content[0].text.strip()
        except Exception as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return f"[GENERATION ERROR: {exc}]"

# ---------------------------------------------------------------------------
# Judge
# ---------------------------------------------------------------------------

def judge_answer(client: Anthropic, question: str, context: str, response: str) -> dict:
    user_msg = (
        f"PREGUNTA:\n{question}\n\n"
        f"DOCUMENTOS DE CONTEXTO:\n{context}\n\n"
        f"RESPUESTA DEL ASISTENTE:\n{response}"
    )
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=JUDGE_MODEL,
                system=JUDGE_SYSTEM,
                messages=[
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=1000,
            )
            raw = resp.content[0].text.strip()
            return _parse_judge_json(raw)
        except Exception as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return {
                    "error": str(exc),
                    "claims": [], "is_abstention": False,
                    "release_mixing": False, "grounded_fraction": 0.0,
                }


def _parse_judge_json(raw: str) -> dict:
    # Strip markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(raw.strip())
    except json.JSONDecodeError as exc:
        return {
            "parse_error": str(exc),
            "raw_response": raw[:500],
            "claims": [], "is_abstention": False,
            "release_mixing": False, "grounded_fraction": 0.0,
        }
    data.setdefault("claims", [])
    for claim in data["claims"]:
        claim.setdefault("support", "")
    data.setdefault("is_abstention", False)
    data.setdefault("release_mixing", False)
    data.setdefault("grounded_fraction", 0.0)
    return data

# ---------------------------------------------------------------------------
# Deterministic support verification
# ---------------------------------------------------------------------------

def verify_supports(judgment: dict, context: str) -> tuple[dict, int]:
    """Reclassify SUPPORTED/PARTIAL claims whose support span is not verbatim in context.

    Uses case-insensitive substring match. A support shorter than 8 chars is
    considered vacuous and triggers reclassification regardless.
    Recalculates grounded_fraction = (SUPPORTED + 0.5*PARTIAL) / n_claims.
    Returns (updated_judgment, n_reclassified).
    """
    context_lower = context.lower()
    n_reclassified = 0
    for claim in judgment.get("claims", []):
        label = claim.get("label", "UNSUPPORTED")
        support = claim.get("support", "").strip()
        if label in ("SUPPORTED", "PARTIAL"):
            # Reclassify if support is missing, too short, or not in context
            if not support or len(support) < 8 or support.lower() not in context_lower:
                claim["label"] = "UNSUPPORTED"
                claim["support"] = ""
                claim["_reclassified"] = True
                n_reclassified += 1
    # Recalculate grounded_fraction after reclassification
    claims = judgment.get("claims", [])
    if claims:
        gf = sum(
            1.0 if c.get("label") == "SUPPORTED" else
            0.5 if c.get("label") == "PARTIAL" else
            0.0
            for c in claims
        ) / len(claims)
        judgment["grounded_fraction"] = round(gf, 3)
    judgment["_n_support_reclassified"] = n_reclassified
    return judgment, n_reclassified


# ---------------------------------------------------------------------------
# Deterministic checks
# ---------------------------------------------------------------------------

def check_citations(response: str, top_k_ids: list[str], all_ids: set) -> dict:
    """Parse 'Fuentes: ...' line and validate IDs."""
    m = re.search(r"Fuentes:\s*(.+)$", response, re.MULTILINE | re.IGNORECASE)
    if not m:
        return {
            "has_citation_line": False,
            "cited_ids": [],
            "all_in_corpus": True,
            "all_in_top_k": True,
        }
    cited_ids = [x.strip() for x in re.split(r"[,;]", m.group(1)) if x.strip()]
    top_k_set = set(top_k_ids)
    return {
        "has_citation_line": True,
        "cited_ids": cited_ids,
        "all_in_corpus": all(cid in all_ids for cid in cited_ids),
        "all_in_top_k": all(cid in top_k_set for cid in cited_ids),
    }


def check_abstention_regex(response: str) -> bool:
    return ABSTENTION_PHRASE.lower() in response.lower()

# ---------------------------------------------------------------------------
# Single-question pipeline
# ---------------------------------------------------------------------------

def run_question(
    client: Anthropic,
    question_data: dict,
    chunks: dict,
    retriever,
    mode: str = "positive",
    top_k: int = DEFAULT_TOP_K,
) -> dict:
    """
    mode='positive'   — full top-k context
    mode='abstention' — gold chunk(s) excluded from context
    """
    q_text = question_data["question"]
    src    = question_data["_src"]
    q_id   = question_data["id"]

    # Retrieve with extra buffer so exclusion doesn't drop below top_k
    raw_retrieved = retriever.retrieve(q_text, k=top_k + 10)
    gold_chunk_ids = derive_gold_chunk_ids(question_data, chunks, src)
    gold_in_top_k  = any(gid in raw_retrieved[:top_k] for gid in gold_chunk_ids)

    if mode == "abstention":
        gold_set = set(gold_chunk_ids)
        top_k_ids = [cid for cid in raw_retrieved if cid not in gold_set][:top_k]
    else:
        top_k_ids = raw_retrieved[:top_k]

    context  = format_context(top_k_ids, chunks)
    response = generate_answer(client, q_text, context)
    judgment = judge_answer(client, q_text, context, response)
    judgment, n_reclassified = verify_supports(judgment, context)

    all_ids      = set(chunks.keys())
    cite_check   = check_citations(response, top_k_ids, all_ids)
    abstention_rx = check_abstention_regex(response)

    return {
        "id":                    q_id,
        "question":              q_text,
        "src":                   src,
        "mode":                  mode,
        "gold_chunk_ids":        gold_chunk_ids,
        "top_k_ids":             top_k_ids,
        "gold_in_top_k":         gold_in_top_k,
        "response":              response,
        "judgment":              judgment,
        "citation_check":        cite_check,
        "abstention_det":        abstention_rx,
        "n_support_reclassified": n_reclassified,
    }

# ---------------------------------------------------------------------------
# Aggregate metrics
# ---------------------------------------------------------------------------

def aggregate_positive(results: list[dict]) -> dict:
    n = len(results)
    if not n:
        return {}

    abstained_flags = [
        r["abstention_det"] or r["judgment"].get("is_abstention", False)
        for r in results
    ]
    answered = [r for r, a in zip(results, abstained_flags) if not a]
    gf_answered = [r["judgment"].get("grounded_fraction", 0.0) for r in answered]

    gitk = [r["gold_in_top_k"] for r in results]
    # citation validity only meaningful for answered responses
    cval = [r["citation_check"]["all_in_top_k"] for r in answered]
    rmix = [r["judgment"].get("release_mixing", False) for r in results]

    # False abstention: system abstained even though gold was in top-k
    false_abs = sum(
        1 for r, a in zip(results, abstained_flags) if a and r["gold_in_top_k"]
    )

    return {
        "n": n,
        "n_answered": len(answered),
        "n_abstained": sum(abstained_flags),
        "mean_grounded_fraction_answered": (
            round(sum(gf_answered) / len(gf_answered), 3) if gf_answered else None
        ),
        "pct_false_abstention":  round(100 * false_abs / n, 1),
        "gold_in_top_k_rate":    round(100 * sum(gitk) / n, 1),
        "n_retrieval_misses":    n - sum(gitk),
        "citation_validity_rate": (
            round(100 * sum(cval) / len(answered), 1) if answered else None
        ),
        "release_mixing_incidents": sum(rmix),
        "total_support_reclassified": sum(r.get("n_support_reclassified", 0) for r in results),
    }


def aggregate_abstention(results: list[dict]) -> dict:
    n = len(results)
    if not n:
        return {}
    correct = [
        r["abstention_det"] or r["judgment"].get("is_abstention", False)
        for r in results
    ]
    failures = [r for r, c in zip(results, correct) if not c]

    total_recl = sum(r.get("n_support_reclassified", 0) for r in results)
    # Abstention responses generate expected FP reclassifications (phrase not in context)
    abs_phrase_fp = sum(
        r.get("n_support_reclassified", 0) for r, c in zip(results, correct) if c
    )
    return {
        "n": n,
        "pct_correct_abstention":          round(100 * sum(correct) / n, 1),
        "pct_answered_when_should_abstain": round(100 * len(failures) / n, 1),
        "n_failures":                      len(failures),
        "total_support_reclassified":      total_recl,
        "n_reclassified_abstention_fp":    abs_phrase_fp,
    }


def aggregate_per_src(
    positive_results: list[dict],
    abstention_results: list[dict],
) -> dict:
    """Per-SRC breakdown of positive and abstention metrics."""
    srcs = sorted(set(
        r["src"] for r in (positive_results + abstention_results)
    ))
    per_src: dict = {}
    for src in srcs:
        pos  = [r for r in positive_results  if r["src"] == src]
        abs_ = [r for r in abstention_results if r["src"] == src]
        per_src[src] = {
            "positive":   aggregate_positive(pos)   if pos  else {},
            "abstention": aggregate_abstention(abs_) if abs_ else {},
        }
    return per_src

# ---------------------------------------------------------------------------
# Calibration report (human-readable)
# ---------------------------------------------------------------------------

def write_calibration(
    positive_results: list[dict],
    abstention_results: list[dict],
    pos_metrics: dict,
    abs_metrics: dict,
    path: Path,
    top_k: int,
) -> None:
    lines = [
        f"# Faithfulness Harness — Calibration Sample ({date.today().isoformat()})",
        "",
        (f"**Generator**: {GENERATOR_MODEL} | **Judge**: {JUDGE_MODEL} "
         f"| **top-k**: {top_k}"),
        "",
        "## Positive Set Metrics",
        "",
        f"| Metric | Value |",
        f"|---|---|",
    ]
    for k, v in pos_metrics.items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Abstention Set Metrics", "", "| Metric | Value |", "|---|---|"]
    for k, v in abs_metrics.items():
        lines.append(f"| {k} | {v} |")

    lines += ["", "---", "", "## Positive Questions (review grounding)", ""]
    for r in positive_results:
        j = r["judgment"]
        lines += [
            f"### {r['id']} ({r['src']})",
            f"**Q**: {r['question']}",
            f"**Gold chunks**: {', '.join(r['gold_chunk_ids'])}",
            f"**Gold in top-k**: {r['gold_in_top_k']} | "
            f"**top-k**: {', '.join(r['top_k_ids'][:3])}{'...' if len(r['top_k_ids'])>3 else ''}",
            "",
            "**Response**:",
            "```",
            r["response"],
            "```",
            "",
            f"**Judge** — grounded_fraction={j.get('grounded_fraction')} | "
            f"release_mixing={j.get('release_mixing')} | "
            f"is_abstention={j.get('is_abstention')}",
        ]
        for claim in j.get("claims", []):
            recl = " ⚑RECLASSIFIED" if claim.get("_reclassified") else ""
            sup  = claim.get("support", "")
            sup_str = f'  \n  > support: "{sup[:100]}{"..." if len(sup)>100 else ""}"' if sup else ""
            lines.append(f"- `[{claim.get('label')}]`{recl} {claim.get('text', '')}{sup_str}")
        lines += [
            f"**Reclassified supports**: {r.get('n_support_reclassified', 0)}",
            f"**Citations**: {r['citation_check']}",
            f"**Abstention regex**: {r['abstention_det']}",
            "",
        ]

    lines += ["---", "", "## Abstention Questions (review abstention)", ""]
    for r in abstention_results:
        j = r["judgment"]
        correct = r["abstention_det"] or j.get("is_abstention", False)
        lines += [
            f"### {r['id']} ({r['src']}) — ABSTENTION MODE",
            f"**Q**: {r['question']}",
            f"**Gold chunks excluded**: {', '.join(r['gold_chunk_ids'])}",
            f"**Context (no gold)**: {', '.join(r['top_k_ids'][:3])}{'...' if len(r['top_k_ids'])>3 else ''}",
            "",
            "**Response**:",
            "```",
            r["response"],
            "```",
            "",
            f"**Correct abstention**: {correct}",
            f"**Judge** — grounded_fraction={j.get('grounded_fraction')} | "
            f"is_abstention={j.get('is_abstention')}",
        ]
        for claim in j.get("claims", []):
            recl = " ⚑RECLASSIFIED" if claim.get("_reclassified") else ""
            sup  = claim.get("support", "")
            sup_str = f'  \n  > support: "{sup[:100]}{"..." if len(sup)>100 else ""}"' if sup else ""
            lines.append(f"- `[{claim.get('label')}]`{recl} {claim.get('text', '')}{sup_str}")
        lines += [f"**Reclassified supports**: {r.get('n_support_reclassified', 0)}", ""]

    lines += [
        "---",
        "",
        "## Limitations",
        "",
        "- **Judge bias**: generator and judge share the same model family (Anthropic). "
          "No cross-model independence — self-consistency risk.",
        "- **LÍMITE 2**: questions are SAP Learning Assessment (easy, single-lesson scope). "
          "Grounding score is a discipline floor, NOT a RAG quality proof.",
        "- **n**: small sample. Not statistically significant.",
        "- **parse_page_range**: fixed (commit 66e4862+). Comma-separated specs now "
          "parsed correctly; no known gold-chunk miss from page parsing.",
        "- **verify_supports / abstention claims**: the abstention phrase itself is not "
          "in the context by design, so verify_supports reclassifies abstention claims to "
          "UNSUPPORTED — these ⚑RECLASSIFIED labels on abstention responses are expected "
          "and do not indicate judge failure.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")

# ---------------------------------------------------------------------------
# Full-run report (abstention-primary, answered-only grounding, per-SRC)
# ---------------------------------------------------------------------------

def write_full_report(
    abstention_results: list[dict],
    pos_metrics: dict,
    abs_metrics: dict,
    per_src: dict,
    path: Path,
    top_k: int,
    n_api_calls: int,
    approx_cost_usd: float,
) -> None:
    today = date.today().isoformat()
    lines = [
        f"# P-gen Phase 1 — Full Faithfulness Run ({today})",
        "",
        (f"**Generator**: {GENERATOR_MODEL} | **Judge**: {JUDGE_MODEL} "
         f"| **top-k**: {top_k}"),
        (f"**N**: {pos_metrics.get('n')} positive + {abs_metrics.get('n')} abstention "
         f"| {len(per_src)} sources"),
        "",
        "> **LÍMITE 2**: All questions are SAP Learning Assessment (easy, single-lesson scope).",
        "> `mean_grounded_fraction_answered` is a **discipline floor** — it measures whether",
        "> the generator stays within its context. It is NOT a proof of RAG quality.",
        "> The real quality proof (LLM-only vs LLM+corpus, realistic consultant queries) is Phase 2.",
        "",
    ]

    # ── PRIMARY RISK: answered when should abstain ───────────────────────────
    pct_fail = abs_metrics.get("pct_answered_when_should_abstain", 0)
    n_fail   = abs_metrics.get("n_failures", 0)
    n_abs_total = abs_metrics.get("n", 0)
    lines += [
        "## ⚠ PRIMARY RISK — Answered When Should Abstain",
        "",
        (f"**{pct_fail}%** of abstention questions received an answer "
         f"({n_fail}/{n_abs_total}) — the system generated a response using "
         "irrelevant context instead of abstaining."),
        "A high `grounded_fraction` does **NOT** redeem these: they are product-risk failures.",
        "",
    ]
    failures = [
        r for r in abstention_results
        if not (r["abstention_det"] or r["judgment"].get("is_abstention", False))
    ]
    if failures:
        lines += ["### Failure detail", ""]
        lines += [
            "| # | ID (SRC) | top-1 retrieved | gf | Response (first 200 chars) |",
            "|---|---|---|---|---|",
        ]
        for i, r in enumerate(failures, 1):
            top1 = r["top_k_ids"][0] if r["top_k_ids"] else "—"
            gf   = r["judgment"].get("grounded_fraction", "?")
            resp = r["response"].replace("\n", " ")[:200]
            lines.append(
                f"| {i} | {r['id']} ({r['src']}) | {top1} | {gf} | {resp}… |"
            )
        lines += [""]
        for i, r in enumerate(failures, 1):
            lines += [
                f"#### Failure {i}: {r['id']} ({r['src']})",
                f"**Q**: {r['question']}",
                f"**Gold excluded**: {', '.join(r['gold_chunk_ids'])}",
                f"**Context top-3**: {', '.join(r['top_k_ids'][:3])}",
                "",
                "**Response**:",
                "```",
                r["response"],
                "```",
                "",
                f"**Judge**: grounded_fraction={r['judgment'].get('grounded_fraction')} "
                f"| is_abstention={r['judgment'].get('is_abstention')}",
            ]
            for c in r["judgment"].get("claims", []):
                recl = " ⚑" if c.get("_reclassified") else ""
                lines.append(f"- `[{c.get('label')}]`{recl} {c.get('text', '')}")
            lines += [""]
    else:
        lines += ["*No failures — all questions correctly abstained.*", ""]

    # ── GLOBAL METRICS ───────────────────────────────────────────────────────
    lines += ["## Global Metrics", "", "| Metric | Value |", "|---|---|"]
    lines += [
        f"| pct_correct_abstention (PRIMARY) | **{abs_metrics.get('pct_correct_abstention')}%** |",
        f"| pct_answered_when_should_abstain | **{abs_metrics.get('pct_answered_when_should_abstain')}%** |",
        f"| mean_grounded_fraction_answered (LÍMITE 2 — discipline floor) "
        f"| {pos_metrics.get('mean_grounded_fraction_answered')} |",
        f"| pct_false_abstention (pos set, abstained with gold in top-k) "
        f"| {pos_metrics.get('pct_false_abstention')}% |",
        f"| gold_in_top_k_rate (positive) | {pos_metrics.get('gold_in_top_k_rate')}% |",
        f"| n_retrieval_misses (positive) | {pos_metrics.get('n_retrieval_misses')} |",
        f"| citation_validity_rate (answered only) | {pos_metrics.get('citation_validity_rate')}% |",
        f"| release_mixing_incidents | {pos_metrics.get('release_mixing_incidents')} |",
        f"| total_support_reclassified (pos) | {pos_metrics.get('total_support_reclassified')} |",
        f"| total_support_reclassified (abs) | {abs_metrics.get('total_support_reclassified')} "
        f"(of which {abs_metrics.get('n_reclassified_abstention_fp')} expected FP from abstention phrase) |",
        f"| n_api_calls total (generator + judge) | {n_api_calls} |",
        f"| approx_cost_usd | ~${approx_cost_usd:.2f} |",
    ]
    lines += [""]

    # ── PER-SRC TABLE ────────────────────────────────────────────────────────
    lines += [
        "## Per-SRC Breakdown",
        "",
        "| SRC | n_pos | n_abs | gf_answered | false_abs% | correct_abs% | answered_should_abs% | gitk% |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for src, m in sorted(per_src.items()):
        pm = m.get("positive", {})
        am = m.get("abstention", {})
        lines.append(
            f"| {src} "
            f"| {pm.get('n', 0)} "
            f"| {am.get('n', 0)} "
            f"| {pm.get('mean_grounded_fraction_answered', '—')} "
            f"| {pm.get('pct_false_abstention', '—')}% "
            f"| {am.get('pct_correct_abstention', '—')}% "
            f"| {am.get('pct_answered_when_should_abstain', '—')}% "
            f"| {pm.get('gold_in_top_k_rate', '—')}% |"
        )
    lines += [""]

    # ── ANOMALIES ────────────────────────────────────────────────────────────
    anomalies = []
    for src, m in per_src.items():
        am = m.get("abstention", {})
        pct_aws = am.get("pct_answered_when_should_abstain", 0)
        global_aws = abs_metrics.get("pct_answered_when_should_abstain", 0)
        if pct_aws and pct_aws > global_aws + 20:
            anomalies.append(
                f"- **{src}**: pct_answered_when_should_abstain={pct_aws}% "
                f"(global avg {global_aws}%) — anomalously high"
            )
    if anomalies:
        lines += ["## Anomalies", ""] + anomalies + [""]

    # ── LIMITATIONS ─────────────────────────────────────────────────────────
    lines += [
        "## Limitations",
        "",
        "- **LÍMITE 2**: SAP Learning Assessment questions are easy, single-lesson scope. "
          "grounded_fraction is a discipline floor, not a RAG quality signal.",
        "- **Judge bias**: same model family (Anthropic) for generator and judge. "
          "Mitigated by verify_supports (deterministic span check), but self-consistency "
          "risk remains.",
        "- **Retrieval error ≠ hallucination**: the judge cannot detect 'correct answer "
          "from wrong chunk'. That failure mode appears in pct_answered_when_should_abstain "
          "with high gf — the content is grounded, but in irrelevant context.",
        "- **verify_supports FP on abstention phrase**: the exact abstention phrase is not "
          "in the context by design. Reclassified ⚑ claims in correct-abstention responses "
          "are expected false positives, not judge failures.",
        "- **Cost estimate**: rough, based on assumed token counts (~4000 input + ~600 "
          "output for generator; ~4600 input + ~1000 output for judge). Actual may vary.",
        "- **n per SRC**: see Per-SRC table. Sources with few questions (n<5) are not "
          "statistically meaningful.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="P-gen Phase 1: Faithfulness harness")
    parser.add_argument("--full",          action="store_true",
                        help="Run all mappable questions (not just sample)")
    parser.add_argument("--n-positive",    type=int, default=DEFAULT_N_POSITIVE)
    parser.add_argument("--n-abstention",  type=int, default=DEFAULT_N_ABSTENTION)
    parser.add_argument("--top-k",         type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--srcs",          type=str, default=None,
                        help="Comma-separated source IDs to include, e.g. S4600,S4F30")
    args = parser.parse_args()

    # ── API key ──────────────────────────────────────────────────────────────
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found. Check .env file.")
        sys.exit(1)
    client = Anthropic(api_key=api_key)
    print(f"Generator : {GENERATOR_MODEL}")
    print(f"Judge     : {JUDGE_MODEL}")
    print(f"top-k     : {args.top_k}")

    # ── Chunks + retriever ───────────────────────────────────────────────────
    print("\nLoading chunks...")
    chunks = load_chunks_extended()
    print(f"  {len(chunks)} chunks loaded")

    print("Loading retriever (semantic_long / bge-m3)...")
    retriever = make_retriever("semantic_long", chunks)

    # ── Gold questions ───────────────────────────────────────────────────────
    print("Loading gold questions...")
    raw_qs = load_all_gold_questions()
    mappable = []
    for q in raw_qs:
        gold_ids = derive_gold_chunk_ids(q, chunks, q["_src"])
        if gold_ids:
            q["_verified_gold_ids"] = gold_ids
            mappable.append(q)
    print(f"  {len(raw_qs)} questions in gold files -> {len(mappable)} verified mappable")

    # Optional source filter
    if args.srcs:
        src_filter = set(args.srcs.split(","))
        mappable = [q for q in mappable if q["_src"] in src_filter]
        print(f"  Source filter: {args.srcs} -> {len(mappable)} mappable")

    if args.full:
        positive_qs   = mappable
        abstention_qs = mappable          # full run: all questions in both sets
    else:
        # Stratified round-robin across sources so no single src dominates
        by_src: dict[str, list] = defaultdict(list)
        for q in mappable:
            by_src[q["_src"]].append(q)
        src_order = sorted(by_src.keys())
        src_iters = {s: iter(by_src[s]) for s in src_order}
        exhausted: set[str] = set()
        positive_qs = []
        src_cycle = list(src_order)
        idx = 0
        while len(positive_qs) < args.n_positive and len(exhausted) < len(src_order):
            s = src_cycle[idx % len(src_order)]
            idx += 1
            if s in exhausted:
                continue
            try:
                positive_qs.append(next(src_iters[s]))
            except StopIteration:
                exhausted.add(s)
        abstention_qs = positive_qs[:args.n_abstention]

    print(f"\nSample: {len(positive_qs)} positive + {len(abstention_qs)} abstention")

    # ── Positive set ─────────────────────────────────────────────────────────
    print("\n=== POSITIVE SET ===")
    positive_results = []
    for i, q in enumerate(positive_qs, 1):
        print(f"  [{i}/{len(positive_qs)}] {q['id']} ({q['_src']})...")
        r = run_question(client, q, chunks, retriever, mode="positive", top_k=args.top_k)
        gf = r["judgment"].get("grounded_fraction", "?")
        print(f"    grounded_fraction={gf}  gold_in_top_k={r['gold_in_top_k']}")
        positive_results.append(r)

    # ── Abstention set ───────────────────────────────────────────────────────
    print("\n=== ABSTENTION SET ===")
    abstention_results = []
    for i, q in enumerate(abstention_qs, 1):
        print(f"  [{i}/{len(abstention_qs)}] {q['id']} ({q['_src']}) [abstention]...")
        r = run_question(client, q, chunks, retriever, mode="abstention", top_k=args.top_k)
        correct = r["abstention_det"] or r["judgment"].get("is_abstention", False)
        print(f"    correct_abstention={correct}")
        abstention_results.append(r)

    # ── Aggregate ────────────────────────────────────────────────────────────
    pos_metrics = aggregate_positive(positive_results)
    abs_metrics = aggregate_abstention(abstention_results)
    per_src     = aggregate_per_src(positive_results, abstention_results)

    # API call count (1 generator + 1 judge per question, retries excluded)
    n_api_calls = (len(positive_results) + len(abstention_results)) * 2
    # Approximate cost: sonnet-4-6 ~$3/$15 per MTok in/out; opus-4-8 ~$15/$75
    # ~4000 tok in + 600 tok out generator; ~4600 tok in + 1000 tok out judge
    n_q = len(positive_results) + len(abstention_results)
    gen_cost  = n_q * (4000 * 3e-6 + 600 * 15e-6)
    judge_cost = n_q * (4600 * 15e-6 + 1000 * 75e-6)
    approx_cost_usd = round(gen_cost + judge_cost, 2)

    print(f"\n=== {'FULL' if args.full else 'SAMPLE'} METRICS ===")
    print("Positive:")
    for k, v in pos_metrics.items():
        if k != "n":
            print(f"  {k}: {v}")
    print("Abstention:")
    for k, v in abs_metrics.items():
        if k != "n":
            print(f"  {k}: {v}")
    print(f"\nAPI calls: {n_api_calls} | Approx cost: ~${approx_cost_usd}")

    print("\nPer-SRC:")
    for src, m in sorted(per_src.items()):
        pm = m.get("positive", {})
        am = m.get("abstention", {})
        print(
            f"  {src}: pos n={pm.get('n',0)} gf={pm.get('mean_grounded_fraction_answered')} "
            f"abs n={am.get('n',0)} correct_abs={am.get('pct_correct_abstention')}%"
        )

    # ── Save results ─────────────────────────────────────────────────────────
    today = date.today().isoformat()
    RESULTS_DIR.mkdir(exist_ok=True)
    suffix = "full" if args.full else "sample"

    results_payload = {
        "generated_at":       today,
        "generator_model":    GENERATOR_MODEL,
        "judge_model":        JUDGE_MODEL,
        "top_k":              args.top_k,
        "n_chunks_in_corpus": len(chunks),
        "positive_metrics":   pos_metrics,
        "abstention_metrics": abs_metrics,
        "per_src":            per_src,
        "n_api_calls":        n_api_calls,
        "approx_cost_usd":    approx_cost_usd,
        "positive_results":   positive_results,
        "abstention_results": abstention_results,
        "limitations": [
            "Same model family for generator and judge — self-bias risk.",
            "LÍMITE 2: Learning Assessment questions, easy single-lesson scope.",
            "parse_page_range fixed: comma-separated specs handled correctly.",
            "verify_supports FP: abstention phrase not in context by design.",
        ],
    }

    json_path   = RESULTS_DIR / f"faithfulness_{suffix}_{today}.json"
    report_path = RESULTS_DIR / f"faithfulness_{suffix}_{today}.md"

    json_path.write_text(
        json.dumps(results_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if args.full:
        write_full_report(
            abstention_results,
            pos_metrics, abs_metrics, per_src,
            report_path, args.top_k, n_api_calls, approx_cost_usd,
        )
    else:
        write_calibration(
            positive_results, abstention_results,
            pos_metrics, abs_metrics,
            report_path, args.top_k,
        )

    print(f"\nResults : {json_path}")
    print(f"Report  : {report_path}")
    if not args.full:
        print("\nPARA — review calibration before running full gold set (--full).")


if __name__ == "__main__":
    main()
