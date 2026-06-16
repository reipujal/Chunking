"""
granularity_probe.py — Granularity / truncation probe for the SAP SD eval harness.

Three retrieval variants compared across all 5 processed documents:
  A — Lexical (TF-IDF, full body). Baseline; re-run for apples-to-apples.
  B — Semantic whole-chunk, long context (jina-embeddings-v2-base-en, 8192 tokens).
      No truncation on SAP chunks (max ~1832 tokens << 8192).
  C — Semantic window-pooled (SAME model as B; windows ~400 tokens, ~25% overlap).
      Score(chunk) = max(sim(query, window)) — finer retrieval granularity.

Two comparisons isolating separate questions:
  A vs B — was the v4 borderline verdict (+9.9 pp) an artifact of truncation?
  B vs C — P3 granularity probe: do finer retrieval units help? (model identical)

Usage:
    cd "c:/Users/aranu/Desktop/IA/Chunking"
    python3 eval/granularity_probe.py
    python3 eval/granularity_probe.py --no-cache   # force rebuild indices
"""

import re
import sys
import json
import argparse
import copy
from pathlib import Path
from datetime import date
from collections import defaultdict
from typing import Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.retriever import (
    load_chunks, TFIDFRetriever, LongContextRetriever, WindowPooledRetriever,
    CHUNKS_DIR,
)
from eval.score import score_dataset

GOLD_DIR = Path("eval/gold")
RESULTS_DIR = Path("eval/results")

DOCS = ["S4600", "S4605", "S4610", "S4615", "S4620"]
K_VALUES = [1, 3, 5, 10]

# Reference lexical results from v4 (2026-06-16) — used to verify A re-run consistency
V4_LEX_REF = {
    "S4600": {"@1": 0.571, "@5": 0.857, "@10": 0.952, "mrr": 0.718},
    "S4605": {"@1": 0.613, "@5": 0.935, "@10": 0.968, "mrr": 0.747},
    "S4610": {"@1": 0.615, "@5": 0.923, "@10": 0.923, "mrr": 0.727},
    "S4615": {"@1": 0.700, "@5": 0.833, "@10": 0.900, "mrr": 0.762},
    "S4620": {"@1": 0.615, "@5": 0.962, "@10": 1.000, "mrr": 0.755},
    "TOTAL": {"@1": 0.623, "@5": 0.902, "@10": 0.949, "mrr": 0.742},
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def delta_str(a: float, b: float) -> str:
    d = (b - a) * 100
    sign = "+" if d >= 0 else ""
    return f"{sign}{d:.1f}pp"


def load_gold(src: str) -> dict:
    p = GOLD_DIR / f"{src}_assessments.json"
    if not p.exists():
        raise FileNotFoundError(f"Gold not found: {p}  (run extract_assessments.py first)")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def score_one(gold_questions: list[dict], chunks: dict, src: str,
              retriever_fn: Callable) -> dict:
    """Score one doc with one retriever. Uses a deep copy to avoid mutation leaks."""
    return score_dataset(
        copy.deepcopy(gold_questions), chunks, src,
        k_values=K_VALUES, retriever_fn=retriever_fn,
    )


def aggregate(results_by_doc: dict[str, dict]) -> dict:
    """Weighted aggregate of global metrics across docs."""
    total_n = 0
    acc_recall = defaultdict(float)
    acc_mrr = 0.0
    for src, res in results_by_doc.items():
        n = res["mappable"]
        total_n += n
        for k in K_VALUES:
            acc_recall[k] += res["global"]["recall"][k] * n
        acc_mrr += res["global"]["mrr"] * n
    if total_n == 0:
        return {"recall": {k: 0.0 for k in K_VALUES}, "mrr": 0.0, "n": 0}
    return {
        "recall": {k: acc_recall[k] / total_n for k in K_VALUES},
        "mrr": acc_mrr / total_n,
        "n": total_n,
    }


def aggregate_by_type(results_by_doc: dict[str, dict]) -> dict[str, dict]:
    """Aggregate by chunk_type across all docs."""
    type_acc: dict[str, dict] = defaultdict(lambda: {"n": 0, "r1": 0.0, "r5": 0.0, "mrr": 0.0})
    for src, res in results_by_doc.items():
        for ct, m in res.get("by_chunk_type", {}).items():
            n = m["count"]
            type_acc[ct]["n"] += n
            type_acc[ct]["r1"] += m["recall"][1] * n
            type_acc[ct]["r5"] += m["recall"][5] * n
            type_acc[ct]["mrr"] += m["mrr"] * n
    out = {}
    for ct, acc in type_acc.items():
        n = acc["n"]
        out[ct] = {
            "n": n,
            "recall_1": acc["r1"] / n if n else 0.0,
            "recall_5": acc["r5"] / n if n else 0.0,
            "mrr": acc["mrr"] / n if n else 0.0,
        }
    return out


def per_question_map(results_by_doc: dict[str, dict]) -> dict[str, dict]:
    """Flatten per-question results keyed by question ID."""
    out = {}
    for src, res in results_by_doc.items():
        for r in res.get("per_question", []):
            if r["mappable"]:
                out[r["id"]] = r
    return out


TOKEN_EXACT_RE = re.compile(
    r"\b([A-Z]{2}[A-Z0-9]{2,5}\d*|[A-Z]{3,6}\b)"  # T-codes: VL01N, VK11, VBRK, KONV, etc.
)


def is_token_exact(question: str) -> bool:
    return bool(TOKEN_EXACT_RE.search(question))


def diff_b_vs_c(b_map: dict[str, dict], c_map: dict[str, dict]) -> dict:
    both_hit = both_miss = b_fixed = c_fixed = 0
    c_fixed_qs = []
    b_fixed_qs = []
    both_miss_qs = []
    for qid, b_row in b_map.items():
        c_row = c_map.get(qid)
        if c_row is None:
            continue
        b_hit = b_row["recall"][1] >= 1.0
        c_hit = c_row["recall"][1] >= 1.0
        q_text = b_row.get("question", "")
        tok = is_token_exact(q_text)
        if b_hit and c_hit:
            both_hit += 1
        elif not b_hit and c_hit:
            c_fixed += 1
            c_fixed_qs.append({"id": qid, "token_exact": tok, "question": q_text})
        elif b_hit and not c_hit:
            b_fixed += 1
            b_fixed_qs.append({"id": qid, "token_exact": tok, "question": q_text})
        else:
            both_miss += 1
            both_miss_qs.append({"id": qid, "token_exact": tok, "question": q_text})
    return {
        "both_hit": both_hit, "c_fixed": c_fixed,
        "b_regression": b_fixed, "both_miss": both_miss,
        "c_fixed_qs": c_fixed_qs, "b_regression_qs": b_fixed_qs,
        "both_miss_qs": both_miss_qs,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(
    lex_by_doc, long_by_doc, win_by_doc,
    lex_agg, long_agg, win_agg,
    lex_type, long_type, win_type,
    correctness: dict,
    diff: dict,
    lex_mismatch: list[str],
) -> str:
    lines = []
    today = date.today().isoformat()

    lines.append("# Granularity Probe — Truncation Fix + P3 (Window-Pooled)")
    lines.append(f"Generated: {today}")
    lines.append(f"Model B & C: `{LongContextRetriever.MODEL_NAME}` (8192-token context)")
    lines.append(f"Corpus: 82 chunks | Docs: {', '.join(DOCS)}")
    lines.append("")

    # ------------------------------------------------------------------ #
    # Pre-registered criterion
    # ------------------------------------------------------------------ #
    lines.append("## Pre-Registered Decision Criterion")
    lines.append("")
    lines.append("*Written BEFORE examining results.*")
    lines.append("")
    lines.append("### A vs B — Truncation verdict")
    lines.append(
        "If B@1 − A@1 ≥ ~10 pp corpus-wide AND concept-type regression resolves "
        "(concept delta flips positive) → v4 borderline was a truncation artifact; "
        "whole-chunk long-context wins clearly."
    )
    lines.append("")
    lines.append("### B vs C — P3 granularity probe (model identical; only granularity varies)")
    lines.append(
        "**If C@1 − B@1 ≥ ~10 pp (or substantial at operative k)** → finer retrieval "
        "units help materially → P3 (hierarchical chunking) justified by retrieval evidence."
    )
    lines.append(
        "**If C@1 − B@1 is small (< ~3–5 pp)** → NON-CONCLUSIVE. Unit-level gold is "
        "indulgent (@5 already high); B≈C here does NOT rule out P3 benefit. "
        "Recommended next: build lesson-level gold and repeat B vs C before discarding P3."
    )
    lines.append("")

    # ------------------------------------------------------------------ #
    # Correctness checklist
    # ------------------------------------------------------------------ #
    lines.append("## Correctness Checklist")
    lines.append("")
    lines.append(f"- Model B (LongContextRetriever): `{LongContextRetriever.MODEL_NAME}`")
    lines.append(f"- Model C (WindowPooledRetriever): `{WindowPooledRetriever.MODEL_NAME}` ← SAME model")
    lines.append(f"- B = C model: {'YES ✓' if LongContextRetriever.MODEL_NAME == WindowPooledRetriever.MODEL_NAME else 'NO — BUG'}")
    lines.append(f"- B prefix: none ({LongContextRetriever.MODEL_NAME} symmetric — no instruction prefix)")
    lines.append(f"- C prefix: none (same)")
    lines.append(f"- B max_context: {LongContextRetriever.MAX_TOKENS} tokens")
    lines.append(f"- C window size: {WindowPooledRetriever.WINDOW_TOKENS} tokens, stride {WindowPooledRetriever.STRIDE_TOKENS} (~{int((1 - WindowPooledRetriever.STRIDE_TOKENS/WindowPooledRetriever.WINDOW_TOKENS)*100)}% overlap)")
    b_trunc = correctness.get('b_truncated', 0)
    b_trunc_label = "NO TRUNCATION OK" if b_trunc == 0 else f"TRUNCATED {b_trunc} chunks -- ISSUE"
    lines.append(f"- Max chunk tokens vs B context: {correctness.get('max_chunk_tokens', '?')} << {LongContextRetriever.MAX_TOKENS} -> {b_trunc_label}")
    lines.append(f"- Max window tokens (incl special): {correctness.get('max_window_tokens', '?')} ≤ {WindowPooledRetriever.MAX_WINDOW_TOKENS} → {'OK ✓' if correctness.get('max_window_tokens', 999) <= WindowPooledRetriever.MAX_WINDOW_TOKENS else 'EXCEEDS LIMIT — ISSUE'}")
    lines.append(f"- Total windows: {correctness.get('total_windows', '?')} across {correctness.get('n_chunks', '?')} chunks (avg {correctness.get('avg_windows', '?')} windows/chunk)")
    lines.append(f"- Smoke test B: {'PASS ✓' if correctness.get('smoke_b_pass') else 'FAIL — check prefix/norm'} | {correctness.get('smoke_b_msg', '')}")
    lines.append(f"- Smoke test C: {'PASS ✓' if correctness.get('smoke_c_pass') else 'FAIL — check prefix/norm'} | {correctness.get('smoke_c_msg', '')}")
    if lex_mismatch:
        lines.append(f"- Lexical A re-run vs v4 reference: MISMATCH on {', '.join(lex_mismatch)} — gold or chunks changed")
    else:
        lines.append("- Lexical A re-run vs v4 reference: matches ✓")
    lines.append("")

    # ------------------------------------------------------------------ #
    # Global table
    # ------------------------------------------------------------------ #
    lines.append("## Global Results — All Docs")
    lines.append("")
    hdr = "| Doc | N | A@1 | A@5 | A@10 | A-MRR | B@1 | B@5 | B@10 | B-MRR | C@1 | C@5 | C@10 | C-MRR |"
    sep = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    lines.append(hdr)
    lines.append(sep)
    for src in DOCS:
        la = lex_by_doc[src]["global"]
        lb = long_by_doc[src]["global"]
        lc = win_by_doc[src]["global"]
        n = lex_by_doc[src]["mappable"]
        lines.append(
            f"| {src} | {n} "
            f"| {pct(la['recall'][1])} | {pct(la['recall'][5])} | {pct(la['recall'][10])} | {la['mrr']:.3f} "
            f"| {pct(lb['recall'][1])} | {pct(lb['recall'][5])} | {pct(lb['recall'][10])} | {lb['mrr']:.3f} "
            f"| {pct(lc['recall'][1])} | {pct(lc['recall'][5])} | {pct(lc['recall'][10])} | {lc['mrr']:.3f} |"
        )
    # Aggregate row
    la, lb, lc = lex_agg, long_agg, win_agg
    lines.append(
        f"| **TOTAL** | **{la['n']}** "
        f"| **{pct(la['recall'][1])}** | **{pct(la['recall'][5])}** | **{pct(la['recall'][10])}** | **{la['mrr']:.3f}** "
        f"| **{pct(lb['recall'][1])}** | **{pct(lb['recall'][5])}** | **{pct(lb['recall'][10])}** | **{lb['mrr']:.3f}** "
        f"| **{pct(lc['recall'][1])}** | **{pct(lc['recall'][5])}** | **{pct(lc['recall'][10])}** | **{lc['mrr']:.3f}** |"
    )
    lines.append("")

    # ------------------------------------------------------------------ #
    # By chunk_type
    # ------------------------------------------------------------------ #
    lines.append("## By Chunk Type (aggregate across all docs)")
    lines.append("")
    lines.append("| Type | N | A@1 | B@1 | delta(B-A) | C@1 | delta(C-B) | A-MRR | B-MRR | C-MRR |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    all_types = sorted(set(list(lex_type.keys()) + list(long_type.keys()) + list(win_type.keys())))
    for ct in all_types:
        la_t = lex_type.get(ct, {})
        lb_t = long_type.get(ct, {})
        lc_t = win_type.get(ct, {})
        n = la_t.get("n", lb_t.get("n", 0))
        a1 = la_t.get("recall_1", 0.0)
        b1 = lb_t.get("recall_1", 0.0)
        c1 = lc_t.get("recall_1", 0.0)
        lines.append(
            f"| {ct} | {n} "
            f"| {pct(a1)} | {pct(b1)} | {delta_str(a1, b1)} "
            f"| {pct(c1)} | {delta_str(b1, c1)} "
            f"| {la_t.get('mrr', 0):.3f} | {lb_t.get('mrr', 0):.3f} | {lc_t.get('mrr', 0):.3f} |"
        )
    lines.append("")

    # ------------------------------------------------------------------ #
    # A vs B — Truncation analysis
    # ------------------------------------------------------------------ #
    lines.append("## A vs B — Truncation Analysis")
    lines.append("")
    lines.append(f"*A = TF-IDF (indexes full body). B = {LongContextRetriever.MODEL_NAME} whole-chunk (8192 ctx, no truncation).*")
    lines.append(f"*v4 bge-small truncated 82/82 chunks. {LongContextRetriever.MODEL_NAME} truncates {correctness.get('b_truncated', '?')}/82.*")
    lines.append("")
    b_minus_a_1 = (long_agg["recall"][1] - lex_agg["recall"][1]) * 100
    lines.append(f"- Global B@1 − A@1: **{b_minus_a_1:+.1f} pp** (threshold ≥ ~10 pp for 'clear win')")
    lines.append(f"- Global B@5 − A@5: {(long_agg['recall'][5] - lex_agg['recall'][5])*100:+.1f} pp")
    lines.append(f"- Global B-MRR − A-MRR: {(long_agg['mrr'] - lex_agg['mrr']):+.3f}")
    lines.append("")
    lines.append("### Concept-type regression status (key signal)")
    lines.append("v4 concept delta was −5.8 pp (semantic bge-small WORSE than lexical on concept queries).")
    ct_la = lex_type.get("concept", {})
    ct_lb = long_type.get("concept", {})
    concept_delta = (ct_lb.get("recall_1", 0.0) - ct_la.get("recall_1", 0.0)) * 100
    if concept_delta > 0:
        lines.append(
            f"Under Jina-v2 (no truncation), concept delta = **{concept_delta:+.1f} pp** → "
            f"regression **resolved** — was a truncation artifact. ✓"
        )
    elif concept_delta > -3:
        lines.append(
            f"Under Jina-v2, concept delta = **{concept_delta:+.1f} pp** → "
            f"regression reduced but still slightly negative. May be vocabulary-match advantage for lexical on concept queries."
        )
    else:
        lines.append(
            f"Under Jina-v2, concept delta = **{concept_delta:+.1f} pp** → "
            f"regression persists. NOT a truncation artifact — semantic is genuinely weaker on concept queries."
        )
    lines.append("")

    # Per-doc deltas A vs B
    lines.append("### Per-doc A@1 vs B@1")
    lines.append("| Doc | A@1 | B@1 | delta |")
    lines.append("| --- | --- | --- | --- |")
    for src in DOCS:
        a1 = lex_by_doc[src]["global"]["recall"][1]
        b1 = long_by_doc[src]["global"]["recall"][1]
        lines.append(f"| {src} | {pct(a1)} | {pct(b1)} | {delta_str(a1, b1)} |")
    lines.append("")

    # ------------------------------------------------------------------ #
    # B vs C — P3 granularity probe
    # ------------------------------------------------------------------ #
    lines.append("## B vs C — P3 Granularity Probe")
    lines.append("")
    lines.append("*B = whole-chunk (1 vector/chunk). C = window-pooled (max-pool over windows).*")
    lines.append(f"*Model B = C: {LongContextRetriever.MODEL_NAME}. Only variable: indexing granularity.*")
    lines.append("")
    c_minus_b_1 = (win_agg["recall"][1] - long_agg["recall"][1]) * 100
    c_minus_b_5 = (win_agg["recall"][5] - long_agg["recall"][5]) * 100
    lines.append(f"- Global C@1 − B@1: **{c_minus_b_1:+.1f} pp**")
    lines.append(f"- Global C@5 − B@5: **{c_minus_b_5:+.1f} pp**")
    lines.append(f"- Global C-MRR − B-MRR: {win_agg['mrr'] - long_agg['mrr']:+.3f}")
    lines.append("")

    lines.append("### Per-doc B@1 vs C@1")
    lines.append("| Doc | B@1 | C@1 | delta |")
    lines.append("| --- | --- | --- | --- |")
    for src in DOCS:
        b1 = long_by_doc[src]["global"]["recall"][1]
        c1 = win_by_doc[src]["global"]["recall"][1]
        lines.append(f"| {src} | {pct(b1)} | {pct(c1)} | {delta_str(b1, c1)} |")
    lines.append("")

    lines.append("### Per-question diff B vs C (@1)")
    lines.append(f"- both_hit (B=1, C=1): {diff['both_hit']}")
    lines.append(f"- c_fixed  (B=0, C=1 — window-pool recovers): {diff['c_fixed']}")
    lines.append(f"- b_regression (B=1, C=0 — window-pool loses): {diff['b_regression']}")
    lines.append(f"- both_miss (B=0, C=0): {diff['both_miss']}")
    lines.append("")

    if diff["c_fixed_qs"]:
        lines.append("#### C recovers (window-pool finds, whole-chunk misses)")
        lines.append("| ID | Token-exact | Question (first 90 chars) |")
        lines.append("| --- | --- | --- |")
        for row in diff["c_fixed_qs"]:
            lines.append(
                f"| {row['id']} | {'YES' if row['token_exact'] else 'no'} "
                f"| {row['question'][:90]} |"
            )
        lines.append("")

    if diff["b_regression_qs"]:
        lines.append("#### B-regressions (whole-chunk finds, window-pool loses)")
        lines.append("| ID | Token-exact | Question (first 90 chars) |")
        lines.append("| --- | --- | --- |")
        for row in diff["b_regression_qs"]:
            lines.append(
                f"| {row['id']} | {'YES' if row['token_exact'] else 'no'} "
                f"| {row['question'][:90]} |"
            )
        lines.append("")

    # ------------------------------------------------------------------ #
    # Verdicts
    # ------------------------------------------------------------------ #
    lines.append("## Verdicts")
    lines.append("")

    # Truncation verdict
    lines.append("### Verdict 1 — Truncation (A vs B)")
    if b_minus_a_1 >= 10.0 and concept_delta > 0:
        lines.append(
            f"**CLEAR WIN for embeddings.** B@1 − A@1 = {b_minus_a_1:+.1f} pp (≥ 10 pp threshold). "
            f"Concept regression resolved ({concept_delta:+.1f} pp). "
            "The v4 borderline result was a truncation artifact from bge-small's 512-token limit. "
            "Long-context whole-chunk embeddings outperform TF-IDF clearly."
        )
    elif b_minus_a_1 >= 10.0 and concept_delta <= 0:
        lines.append(
            f"**PARTIAL WIN.** B@1 − A@1 = {b_minus_a_1:+.1f} pp (≥ 10 pp threshold). "
            f"However concept regression persists ({concept_delta:+.1f} pp) — semantic is weaker on "
            "concept queries regardless of truncation. Consider hybrid for concept chunks."
        )
    elif b_minus_a_1 >= 5.0:
        lines.append(
            f"**MODEST IMPROVEMENT.** B@1 − A@1 = {b_minus_a_1:+.1f} pp (< 10 pp threshold). "
            "Embeddings improve over TF-IDF but not conclusively. Concept delta "
            f"{'resolved (' + f'{concept_delta:+.1f}' + ' pp)' if concept_delta > 0 else f'persists ({concept_delta:+.1f} pp)'}."
        )
    else:
        lines.append(
            f"**NON-CONCLUSIVE.** B@1 − A@1 = {b_minus_a_1:+.1f} pp. "
            "Long-context embeddings do not clearly outperform TF-IDF at @1 on this corpus."
        )
    lines.append("")

    # P3 verdict
    lines.append("### Verdict 2 — P3 Granularity (B vs C)")
    if c_minus_b_1 >= 10.0:
        lines.append(
            f"**P3 JUSTIFIED BY RETRIEVAL.** C@1 − B@1 = {c_minus_b_1:+.1f} pp (≥ 10 pp). "
            "Window-pooled retrieval materially outperforms whole-chunk at @1. "
            "Finer retrieval granularity helps even with the current unit-level gold. "
            "Recommendation: implement hierarchical chunking (P3)."
        )
    elif c_minus_b_1 >= 3.0:
        lines.append(
            f"**POSSIBLE P3 SIGNAL.** C@1 − B@1 = {c_minus_b_1:+.1f} pp (3–10 pp range). "
            "Window-pooled shows some advantage but unit-level gold is too coarse to confirm. "
            "Recommendation: build lesson-level gold and repeat B vs C before deciding P3."
        )
    elif c_minus_b_1 >= -3.0:
        lines.append(
            f"**NON-CONCLUSIVE (B ≈ C).** C@1 − B@1 = {c_minus_b_1:+.1f} pp. "
            "Window-pooling neither helps nor hurts materially at this gold granularity. "
            "Unit-level gold is indulgent — B≈C here does NOT rule out P3. "
            "Recommended next step: build lesson-level gold (Stage 1) and repeat B vs C."
        )
    else:
        lines.append(
            f"**WINDOW-POOL REGRESSES.** C@1 − B@1 = {c_minus_b_1:+.1f} pp. "
            "Splitting into windows hurts retrieval. Whole-chunk indexing is better for this corpus. "
            "P3 via window-pooling is NOT recommended."
        )
    lines.append("")

    # ------------------------------------------------------------------ #
    # How to run
    # ------------------------------------------------------------------ #
    lines.append("## How to Run")
    lines.append("")
    lines.append("```bash")
    lines.append("cd 'c:/Users/aranu/Desktop/IA/Chunking'")
    lines.append("# Full probe (all 5 docs, all 3 retrievers):")
    lines.append("python3 eval/granularity_probe.py")
    lines.append("# Single doc, single retriever (via score.py):")
    lines.append("python3 eval/score.py --src S4620 --retriever semantic_long")
    lines.append("python3 eval/score.py --src S4620 --retriever semantic_window")
    lines.append("# Force index rebuild:")
    lines.append("python3 eval/granularity_probe.py --no-cache  # deletes eval/index/bge-m3* and rebuilds")
    lines.append("```")
    lines.append("")

    lines.append("## Limitations")
    lines.append(
        "- Gold at **unit level** (indulgent). Lesson-level gold would give tighter B vs C signal."
    )
    lines.append(
        f"- First run downloads {LongContextRetriever.MODEL_NAME} (~1.2 GB). Subsequent runs use cache."
    )
    lines.append(
        f"- Window parameters: {WindowPooledRetriever.WINDOW_TOKENS} tokens, "
        f"stride {WindowPooledRetriever.STRIDE_TOKENS}. Not tuned for this corpus."
    )
    lines.append(
        "- Max-pool aggregation is a simple heuristic; mean-pool or learned-pool could differ."
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Delete jina-* index dirs and rebuild from scratch",
    )
    args = parser.parse_args()

    if args.no_cache:
        import shutil
        for p in Path("eval/index").glob("jina*"):
            print(f"Removing cache: {p}")
            shutil.rmtree(p, ignore_errors=True)

    print(f"\n{'='*60}")
    print("Loading chunks...")
    chunks = load_chunks(CHUNKS_DIR)
    print(f"  {len(chunks)} chunks loaded")

    # ------------------------------------------------------------------
    # Build retrievers once
    # ------------------------------------------------------------------
    print("\n[A] TF-IDF (lexical baseline)")
    ret_a = TFIDFRetriever(chunks)

    print("\n[B] LongContextRetriever (jina-v2, whole-chunk, no truncation)")
    ret_b = LongContextRetriever(chunks)

    print("\n[C] WindowPooledRetriever (jina-v2, window-pooled, same model as B)")
    ret_c = WindowPooledRetriever(chunks)

    # ------------------------------------------------------------------
    # Correctness checklist
    # ------------------------------------------------------------------
    print("\nRunning smoke tests...")
    smoke_b_pass, smoke_b_msg = ret_b.smoke_test(chunks)
    smoke_c_pass, smoke_c_msg = ret_c.smoke_test(chunks)
    print(f"  Smoke B: {'PASS' if smoke_b_pass else 'FAIL'} — {smoke_b_msg}")
    print(f"  Smoke C: {'PASS' if smoke_c_pass else 'FAIL'} — {smoke_c_msg}")

    correctness = {
        "max_chunk_tokens": ret_b.max_tokens_found,
        "b_truncated": ret_b.truncated_count,
        "max_window_tokens": ret_c.stats.get("max_window_tokens", -1),
        "total_windows": ret_c.stats.get("total_windows", -1),
        "n_chunks": ret_c.stats.get("n_chunks", -1),
        "avg_windows": ret_c.stats.get("windows_avg", -1),
        "smoke_b_pass": smoke_b_pass,
        "smoke_b_msg": smoke_b_msg,
        "smoke_c_pass": smoke_c_pass,
        "smoke_c_msg": smoke_c_msg,
    }

    # ------------------------------------------------------------------
    # Score all docs × all retrievers
    # ------------------------------------------------------------------
    lex_by_doc: dict[str, dict] = {}
    long_by_doc: dict[str, dict] = {}
    win_by_doc: dict[str, dict] = {}

    for src in DOCS:
        print(f"\n{'='*60}")
        print(f"Scoring {src}...")
        try:
            gold = load_gold(src)
        except FileNotFoundError as e:
            print(f"  SKIP: {e}")
            continue

        questions = gold["questions"]
        print(f"  A — lexical")
        lex_by_doc[src] = score_one(questions, chunks, src, ret_a.retrieve)
        print(f"    @1={pct(lex_by_doc[src]['global']['recall'][1])}  "
              f"@5={pct(lex_by_doc[src]['global']['recall'][5])}  "
              f"@10={pct(lex_by_doc[src]['global']['recall'][10])}")

        print(f"  B — semantic_long")
        long_by_doc[src] = score_one(questions, chunks, src, ret_b.retrieve)
        print(f"    @1={pct(long_by_doc[src]['global']['recall'][1])}  "
              f"@5={pct(long_by_doc[src]['global']['recall'][5])}  "
              f"@10={pct(long_by_doc[src]['global']['recall'][10])}")

        print(f"  C — semantic_window")
        win_by_doc[src] = score_one(questions, chunks, src, ret_c.retrieve)
        print(f"    @1={pct(win_by_doc[src]['global']['recall'][1])}  "
              f"@5={pct(win_by_doc[src]['global']['recall'][5])}  "
              f"@10={pct(win_by_doc[src]['global']['recall'][10])}")

    # ------------------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------------------
    lex_agg = aggregate(lex_by_doc)
    long_agg = aggregate(long_by_doc)
    win_agg = aggregate(win_by_doc)
    lex_type = aggregate_by_type(lex_by_doc)
    long_type = aggregate_by_type(long_by_doc)
    win_type = aggregate_by_type(win_by_doc)

    # ------------------------------------------------------------------
    # Verify lexical re-run vs v4 reference
    # ------------------------------------------------------------------
    lex_mismatch: list[str] = []
    for src in DOCS:
        if src not in lex_by_doc:
            continue
        ref = V4_LEX_REF.get(src, {})
        got = lex_by_doc[src]["global"]["recall"][1]
        if abs(got - ref.get("@1", got)) > 0.01:
            lex_mismatch.append(src)
    total_got_1 = lex_agg["recall"][1]
    if abs(total_got_1 - V4_LEX_REF["TOTAL"]["@1"]) > 0.01:
        lex_mismatch.append("TOTAL")

    # ------------------------------------------------------------------
    # Per-question diff B vs C
    # ------------------------------------------------------------------
    b_map = per_question_map(long_by_doc)
    c_map = per_question_map(win_by_doc)
    diff = diff_b_vs_c(b_map, c_map)

    # ------------------------------------------------------------------
    # Build and write report
    # ------------------------------------------------------------------
    report = build_report(
        lex_by_doc, long_by_doc, win_by_doc,
        lex_agg, long_agg, win_agg,
        lex_type, long_type, win_type,
        correctness, diff, lex_mismatch,
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    md_path = RESULTS_DIR / f"granularity_probe_{today}.md"
    md_path.write_text(report, encoding="utf-8")

    # JSON summary
    json_data = {
        "generated": today,
        "model_b_c": LongContextRetriever.MODEL_NAME,
        "correctness": correctness,
        "lex_mismatch": lex_mismatch,
        "aggregate": {
            "A": {"recall": lex_agg["recall"], "mrr": lex_agg["mrr"], "n": lex_agg["n"]},
            "B": {"recall": long_agg["recall"], "mrr": long_agg["mrr"], "n": long_agg["n"]},
            "C": {"recall": win_agg["recall"], "mrr": win_agg["mrr"], "n": win_agg["n"]},
        },
        "by_doc": {
            src: {
                "A": lex_by_doc.get(src, {}).get("global"),
                "B": long_by_doc.get(src, {}).get("global"),
                "C": win_by_doc.get(src, {}).get("global"),
                "n": lex_by_doc.get(src, {}).get("mappable"),
            }
            for src in DOCS if src in lex_by_doc
        },
        "by_type": {
            ct: {
                "A": lex_type.get(ct),
                "B": long_type.get(ct),
                "C": win_type.get(ct),
            }
            for ct in sorted(set(list(lex_type) + list(long_type) + list(win_type)))
        },
        "diff_b_vs_c": {k: v for k, v in diff.items() if not k.endswith("_qs")},
    }
    json_path = RESULTS_DIR / f"granularity_probe_{today}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Report: {md_path}")
    print(f"JSON:   {json_path}")
    print(f"\n=== AGGREGATE ===")
    print(f"A (lexical):        @1={pct(lex_agg['recall'][1])}  @5={pct(lex_agg['recall'][5])}  @10={pct(lex_agg['recall'][10])}  MRR={lex_agg['mrr']:.3f}")
    print(f"B (sem_long):       @1={pct(long_agg['recall'][1])}  @5={pct(long_agg['recall'][5])}  @10={pct(long_agg['recall'][10])}  MRR={long_agg['mrr']:.3f}")
    print(f"C (sem_window):     @1={pct(win_agg['recall'][1])}  @5={pct(win_agg['recall'][5])}  @10={pct(win_agg['recall'][10])}  MRR={win_agg['mrr']:.3f}")
    delta_ba = (long_agg["recall"][1] - lex_agg["recall"][1]) * 100
    delta_cb = (win_agg["recall"][1] - long_agg["recall"][1]) * 100
    print(f"B-A @1: {delta_ba:+.1f} pp  |  C-B @1: {delta_cb:+.1f} pp")
    if not lex_mismatch:
        print("Lexical re-run matches v4 reference OK")
    else:
        print(f"WARNING: lexical mismatch vs v4 on {lex_mismatch}")


if __name__ == "__main__":
    main()
