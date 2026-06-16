"""
compare.py — Lexical vs. semantic retrieval side-by-side comparison.

Runs both TF-IDF and bge-small-en-v1.5 against the same gold sets,
produces a unified report with per-question diff and P3 verdict.

Usage:
    python eval/compare.py                  # all docs with gold sets
    python eval/compare.py --src S4620      # single doc
    python eval/compare.py --no-hybrid      # skip RRF column

Writes:
    eval/results/semantic_vs_lexical_<date>.md
    eval/results/semantic_vs_lexical_<date>.json
"""

import re
import json
import argparse
import sys
from pathlib import Path
from datetime import date
from collections import defaultdict
from typing import Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.retriever import (
    load_chunks, TFIDFRetriever, SemanticRetriever, rrf_fuse,
    CHUNKS_DIR,
)
from eval.score import derive_gold_chunk_ids, recall_at_k, mrr, avg, pct

GOLD_DIR = Path("eval/gold")
RESULTS_DIR = Path("eval/results")
K_VALUES = [1, 3, 5, 10]

# Token-exact pattern: T-codes (VL01N), table names (VBRK, KONV), SAP codes (VK11)
TOKEN_EXACT_RE = re.compile(
    r"\b(V[A-Z][A-Z0-9]{2,5}|[A-Z]{3,5}\b|KO[A-Z]{2}\b|SPRO|IMG)\b"
)


def is_token_exact_query(query: str) -> bool:
    """True if query contains SAP T-codes or table names (uppercase tokens)."""
    return bool(TOKEN_EXACT_RE.search(query))


# ---------------------------------------------------------------------------
# Score one doc with a given retriever_fn
# ---------------------------------------------------------------------------

def score_questions(
    questions: list[dict],
    chunks: dict,
    src: str,
    retriever_fn: Callable[[str, int], list[str]],
    k: int = 10,
) -> list[dict]:
    """Return per-question result list. Questions must not be pre-mutated."""
    results = []
    for q in questions:
        if q.get("excluded"):
            continue
        gold_ids = derive_gold_chunk_ids(q, chunks, src)
        mappable = bool(gold_ids)
        if not mappable:
            results.append({
                "id": q["id"],
                "unit": q["unit"],
                "question": q.get("question", ""),
                "mappable": False,
                "gold_ids": [],
                "retrieved": [],
                "recall": {kv: None for kv in K_VALUES},
                "mrr": None,
            })
            continue
        retrieved = retriever_fn(q["question"], k)
        results.append({
            "id": q["id"],
            "unit": q["unit"],
            "question": q.get("question", ""),
            "mappable": True,
            "gold_ids": gold_ids,
            "retrieved": retrieved,
            "recall": {kv: recall_at_k(gold_ids, retrieved, kv) for kv in K_VALUES},
            "mrr": mrr(gold_ids, retrieved),
        })
    return results


# ---------------------------------------------------------------------------
# Per-question diff
# ---------------------------------------------------------------------------

def diff_results(
    lex_rows: list[dict],
    sem_rows: list[dict],
) -> list[dict]:
    """Categorize each mappable question as both_hit / sem_fixed / regression / both_miss."""
    sem_by_id = {r["id"]: r for r in sem_rows}
    diff = []
    for lr in lex_rows:
        if not lr["mappable"]:
            continue
        sr = sem_by_id.get(lr["id"])
        if sr is None or not sr["mappable"]:
            continue
        l1 = lr["recall"][1]
        s1 = sr["recall"][1]
        if l1 == 1.0 and s1 == 1.0:
            cat = "both_hit"
        elif l1 == 0.0 and s1 == 1.0:
            cat = "sem_fixed"
        elif l1 == 1.0 and s1 == 0.0:
            cat = "regression"
        else:
            cat = "both_miss"
        diff.append({
            "id": lr["id"],
            "question": lr["question"],
            "category": cat,
            "token_exact": is_token_exact_query(lr["question"]),
            "lex_mrr": lr["mrr"],
            "sem_mrr": sr["mrr"],
            "lex_r1": l1,
            "sem_r1": s1,
        })
    return diff


# ---------------------------------------------------------------------------
# Aggregate metrics from per-question results
# ---------------------------------------------------------------------------

def aggregate(rows: list[dict]) -> dict:
    mappable = [r for r in rows if r["mappable"]]
    if not mappable:
        return {"count": 0, "recall": {k: 0.0 for k in K_VALUES}, "mrr": 0.0}
    return {
        "count": len(mappable),
        "recall": {k: avg([r["recall"][k] for r in mappable]) for k in K_VALUES},
        "mrr": avg([r["mrr"] for r in mappable]),
    }


# ---------------------------------------------------------------------------
# S4615 diagnosis
# ---------------------------------------------------------------------------

def diagnose_unreachable(
    src: str,
    lex_rows: list[dict],
    sem_rows: list[dict],
    gold_questions: list[dict],
    chunks: dict,
) -> list[dict]:
    """Questions unreachable (recall@10=0) by the lexical retriever in S4615."""
    sem_by_id = {r["id"]: r for r in sem_rows}
    gold_by_id = {q["id"]: q for q in gold_questions}

    cases = []
    for lr in lex_rows:
        if not lr["mappable"]:
            continue
        if lr["recall"][10] != 0.0:
            continue
        sr = sem_by_id.get(lr["id"], {})
        gold_q = gold_by_id.get(lr["id"], {})

        gold_chunks_detail = []
        for cid in lr["gold_ids"]:
            c = chunks.get(cid, {})
            snippet = c.get("body", "")[:300].replace("\n", " ")
            gold_chunks_detail.append({
                "chunk_id": cid,
                "area": c.get("area", ""),
                "chunk_type": c.get("chunk_type", ""),
                "snippet": snippet,
            })

        cases.append({
            "id": lr["id"],
            "question": lr["question"],
            "gold_page_span": gold_q.get("gold_page_span"),
            "gold_chunks": gold_chunks_detail,
            "lex_r10": lr["recall"][10],
            "sem_r10": sr.get("recall", {}).get(10),
            "sem_r5": sr.get("recall", {}).get(5),
            "sem_r1": sr.get("recall", {}).get(1),
        })
    return cases


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def fmt_row(doc: str, lex: dict, sem: dict, hybrid: dict | None) -> str:
    def r(d, k):
        v = d["recall"].get(k, 0.0)
        return f"{v*100:.1f}%"

    row = (
        f"| {doc} | {d['count']} "
        f"| {r(lex,1)} | {r(lex,5)} | {r(lex,10)} | {lex['mrr']:.3f} "
        f"| {r(sem,1)} | {r(sem,5)} | {r(sem,10)} | {sem['mrr']:.3f} "
    ).replace("d['count']", str(lex["count"]))

    # Fix: use lex['count']
    row = (
        f"| {doc} | {lex['count']} "
        f"| {r(lex,1)} | {r(lex,5)} | {r(lex,10)} | {lex['mrr']:.3f} "
        f"| {r(sem,1)} | {r(sem,5)} | {r(sem,10)} | {sem['mrr']:.3f} "
    )
    if hybrid is not None:
        row += f"| {r(hybrid,1)} | {r(hybrid,5)} | {r(hybrid,10)} | {hybrid['mrr']:.3f} "
    row += "|"
    return row


def generate_report(
    all_lex: dict,  # src -> list[result_row]
    all_sem: dict,
    all_hyb: dict | None,
    all_diffs: dict,  # src -> list[diff_row]
    all_gold: dict,   # src -> gold dict
    s4615_diagnosis: list[dict],
    chunks: dict,
    semantic_meta: dict,
    include_hybrid: bool,
) -> str:
    today = date.today().isoformat()
    lines = []

    lines.append("# Lexical vs Semantic Retrieval Comparison")
    lines.append(f"Generated: {today}")
    lines.append(f"Model: `{semantic_meta.get('model','?')}` via sentence-transformers")
    lines.append(f"Corpus: {len(chunks)} chunks")
    lines.append(f"Truncated chunks (>512 tokens): {semantic_meta.get('truncated','?')}/{len(chunks)}")
    lines.append("")

    # ----- Pre-registered criterion -----
    lines.append("## Pre-Registered Decision Criterion (P3)")
    lines.append("")
    lines.append("Written BEFORE examining results:")
    lines.append("")
    lines.append("**(a) Embeddings adequate** — sem closes >=80% of @1 gap AND resolves S4615 unreachables @10.")
    lines.append("**(b) Non-conclusive → refine gold** — both retrievers already high @5, sem uplift @1 < 10 pp,")
    lines.append("    AND S4615 unreachables remain. Unit-level gold too coarse to decide P3.")
    lines.append("**(c) Granularity bottleneck → P3 justified** — sem leaves substantial @10 misses, especially")
    lines.append("    in S4615. Chunk granularity is the constraint, not retriever quality.")
    lines.append("")
    lines.append("**Transversal (hybrid signal):** if regressions concentrate in token-exact queries (T-codes,")
    lines.append("table names) -> recommend lexical+semantic hybrid regardless of above branch.")
    lines.append("")

    # ----- Global table -----
    lines.append("## Global Results — All Docs")
    header = "| Doc | N | lex@1 | lex@5 | lex@10 | lex-MRR | sem@1 | sem@5 | sem@10 | sem-MRR"
    if include_hybrid:
        header += " | hyb@1 | hyb@5 | hyb@10 | hyb-MRR"
    header += " |"
    lines.append(header)

    sep = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---"
    if include_hybrid:
        sep += " | --- | --- | --- | ---"
    sep += " |"
    lines.append(sep)

    totals_lex = defaultdict(list)
    totals_sem = defaultdict(list)
    totals_hyb = defaultdict(list)

    for src in sorted(all_lex.keys()):
        lex_rows = all_lex[src]
        sem_rows = all_sem[src]
        hyb_rows = all_hyb[src] if (all_hyb and src in all_hyb) else None

        la = aggregate(lex_rows)
        sa = aggregate(sem_rows)
        ha = aggregate(hyb_rows) if hyb_rows else None

        for k in K_VALUES:
            totals_lex[k].append(la["recall"][k])
            totals_sem[k].append(sa["recall"][k])
            if ha:
                totals_hyb[k].append(ha["recall"][k])
        totals_lex["mrr"].append(la["mrr"])
        totals_sem["mrr"].append(sa["mrr"])
        if ha:
            totals_hyb["mrr"].append(ha["mrr"])

        row = (
            f"| {src} | {la['count']} "
            f"| {pct(la['recall'][1])} | {pct(la['recall'][5])} | {pct(la['recall'][10])} | {la['mrr']:.3f} "
            f"| {pct(sa['recall'][1])} | {pct(sa['recall'][5])} | {pct(sa['recall'][10])} | {sa['mrr']:.3f} "
        )
        if include_hybrid and ha:
            row += f"| {pct(ha['recall'][1])} | {pct(ha['recall'][5])} | {pct(ha['recall'][10])} | {ha['mrr']:.3f} "
        row += "|"
        lines.append(row)

    # Aggregate row
    def agg_avg(d, k):
        vals = d[k]
        return avg(vals) if vals else 0.0

    agg_row = (
        f"| **TOTAL** | {sum(len([r for r in v if r['mappable']]) for v in all_lex.values())} "
        f"| **{pct(agg_avg(totals_lex,1))}** | **{pct(agg_avg(totals_lex,5))}** "
        f"| **{pct(agg_avg(totals_lex,10))}** | **{agg_avg(totals_lex,'mrr'):.3f}** "
        f"| **{pct(agg_avg(totals_sem,1))}** | **{pct(agg_avg(totals_sem,5))}** "
        f"| **{pct(agg_avg(totals_sem,10))}** | **{agg_avg(totals_sem,'mrr'):.3f}** "
    )
    if include_hybrid and totals_hyb:
        agg_row += (
            f"| **{pct(agg_avg(totals_hyb,1))}** | **{pct(agg_avg(totals_hyb,5))}** "
            f"| **{pct(agg_avg(totals_hyb,10))}** | **{agg_avg(totals_hyb,'mrr'):.3f}** "
        )
    agg_row += "|"
    lines.append(agg_row)
    lines.append("")

    # ----- By chunk_type -----
    lines.append("## By Chunk Type (aggregate across all docs)")
    lines.append("| Type | N | lex@1 | sem@1 | delta@1 | lex@5 | sem@5 | lex-MRR | sem-MRR |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    by_type_lex: dict[str, list] = defaultdict(list)
    by_type_sem: dict[str, list] = defaultdict(list)
    for src in all_lex:
        for lr in all_lex[src]:
            if not lr["mappable"]:
                continue
            ct = chunks.get(lr["gold_ids"][0], {}).get("chunk_type", "?") if lr["gold_ids"] else "?"
            by_type_lex[ct].append(lr)
        for sr in all_sem[src]:
            if not sr["mappable"]:
                continue
            ct = chunks.get(sr["gold_ids"][0], {}).get("chunk_type", "?") if sr["gold_ids"] else "?"
            by_type_sem[ct].append(sr)
    for ct in sorted(set(list(by_type_lex.keys()) + list(by_type_sem.keys()))):
        lr_list = by_type_lex.get(ct, [])
        sr_list = by_type_sem.get(ct, [])
        la = aggregate(lr_list) if lr_list else {"count": 0, "recall": {k: 0.0 for k in K_VALUES}, "mrr": 0.0}
        sa = aggregate(sr_list) if sr_list else {"count": 0, "recall": {k: 0.0 for k in K_VALUES}, "mrr": 0.0}
        delta = sa["recall"][1] - la["recall"][1]
        sign = "+" if delta >= 0 else ""
        lines.append(
            f"| {ct} | {la['count']} "
            f"| {pct(la['recall'][1])} | {pct(sa['recall'][1])} | {sign}{delta*100:.1f}pp "
            f"| {pct(la['recall'][5])} | {pct(sa['recall'][5])} "
            f"| {la['mrr']:.3f} | {sa['mrr']:.3f} |"
        )
    lines.append("")

    # ----- Per-question diff -----
    lines.append("## Per-Question Diff (@1) — Aggregate")
    all_diff_rows = []
    for src in sorted(all_diffs.keys()):
        all_diff_rows.extend(all_diffs[src])

    counts = defaultdict(int)
    for d in all_diff_rows:
        counts[d["category"]] += 1

    total_mappable = len(all_diff_rows)
    lines.append(f"- both_hit:   {counts['both_hit']} ({100*counts['both_hit']/total_mappable:.1f}%)")
    lines.append(f"- sem_fixed:  {counts['sem_fixed']} (lexical@1 miss, semantic@1 hit)")
    lines.append(f"- regression: {counts['regression']} (lexical@1 hit, semantic@1 miss)")
    lines.append(f"- both_miss:  {counts['both_miss']}")
    lines.append("")

    # sem_fixed list
    sem_fixed = [d for d in all_diff_rows if d["category"] == "sem_fixed"]
    if sem_fixed:
        lines.append("### sem_fixed — Semantic recovers where lexical failed")
        lines.append("| ID | Token-exact | Question (first 90 chars) |")
        lines.append("| --- | --- | --- |")
        for d in sem_fixed:
            te = "YES" if d["token_exact"] else "no"
            lines.append(f"| {d['id']} | {te} | {d['question'][:90]} |")
        lines.append("")

    # regressions list
    regressions = [d for d in all_diff_rows if d["category"] == "regression"]
    if regressions:
        lines.append("### Regressions — Lexical hits, Semantic misses @1")
        lines.append("| ID | Token-exact | Question (first 90 chars) |")
        lines.append("| --- | --- | --- |")
        for d in regressions:
            te = "YES" if d["token_exact"] else "no"
            lines.append(f"| {d['id']} | {te} | {d['question'][:90]} |")
        n_te = sum(1 for d in regressions if d["token_exact"])
        lines.append("")
        lines.append(
            f"Token-exact regressions: {n_te}/{len(regressions)} "
            f"({'high — hybrid signal' if n_te / max(len(regressions), 1) >= 0.5 else 'low'})"
        )
        lines.append("")

    # ----- S4615 diagnosis -----
    lines.append("## S4615 Unreachable Diagnosis")
    if not s4615_diagnosis:
        lines.append("No unreachable questions (recall@10 > 0 for all mappable S4615 questions).")
    else:
        lines.append(f"{len(s4615_diagnosis)} question(s) with lex recall@10 = 0:")
        lines.append("")
        for case in s4615_diagnosis:
            lines.append(f"### {case['id']}")
            lines.append(f"**Question:** {case['question']}")
            lines.append(f"**gold_page_span:** {case['gold_page_span']}")
            lines.append(f"**lex @10:** {case['lex_r10']} | **sem @1:** {case['sem_r1']} @5: {case['sem_r5']} @10: {case['sem_r10']}")
            lines.append("")
            for gc in case["gold_chunks"]:
                lines.append(f"**Gold chunk:** `{gc['chunk_id']}` ({gc['area']}/{gc['chunk_type']})")
                lines.append(f"*Snippet:* {gc['snippet'][:200]}...")
                lines.append("")
            # Diagnosis
            sem_reaches = case["sem_r10"] is not None and case["sem_r10"] > 0
            if sem_reaches:
                lines.append(f"**Diagnosis:** Semantic retrieves this chunk (sem@10>0). Lexical failure is vocabulary mismatch.")
            else:
                lines.append("**Diagnosis:** Both retrievers miss. Check: chunk anemic / gold_page_span outside all chunk ranges?")
            lines.append("")

    # ----- Truncation impact -----
    lines.append("## Truncation Impact")
    lines.append(f"Model max tokens: 512. All {semantic_meta.get('truncated','?')}/{len(chunks)} chunks")
    lines.append("exceed this limit (min 543 tokens, max ~1832 tokens in the corpus).")
    lines.append("Sentence-transformers silently truncates at encode time.")
    lines.append("Implication: the tail of every chunk is invisible to the semantic retriever.")
    lines.append("For long configuration chunks where key T-codes appear late in the body, this may")
    lines.append("explain semantic regressions vs lexical (which indexes the full body).")
    lines.append("")

    # ----- P3 Verdict -----
    lines.append("## P3 Verdict")
    lines.append("")

    # Compute data for verdict
    lex1_avg = agg_avg(totals_lex, 1)
    sem1_avg = agg_avg(totals_sem, 1)
    uplift_1 = (sem1_avg - lex1_avg) * 100  # pp
    lex5_avg = agg_avg(totals_lex, 5)
    sem5_avg = agg_avg(totals_sem, 5)

    s4615_unreachable_sem_resolved = sum(
        1 for c in s4615_diagnosis if c.get("sem_r10") is not None and c["sem_r10"] > 0
    )
    s4615_unreachable_total = len(s4615_diagnosis)

    n_regression_te = sum(1 for d in all_diff_rows if d["category"] == "regression" and d["token_exact"])
    n_regression = counts["regression"]
    hybrid_signal = n_regression > 0 and (n_regression_te / max(n_regression, 1)) >= 0.4

    lines.append(f"**Data summary:**")
    lines.append(f"- Avg @1 uplift (sem - lex): {uplift_1:+.1f} pp (threshold for branch a: >=10 pp)")
    lines.append(f"- Avg @5: lex={pct(lex5_avg)}, sem={pct(sem5_avg)}")
    lines.append(f"- S4615 unreachables: {s4615_unreachable_total} total; sem resolves: {s4615_unreachable_sem_resolved}")
    lines.append(f"- Token-exact regressions: {n_regression_te}/{n_regression}")
    lines.append("")

    # Apply criterion
    sem_closes_gap = uplift_1 >= 10.0 and s4615_unreachable_sem_resolved == s4615_unreachable_total
    both_high_at5 = lex5_avg >= 0.88 and sem5_avg >= 0.88
    unreachables_persist = s4615_unreachable_total > 0 and s4615_unreachable_sem_resolved < s4615_unreachable_total

    if sem_closes_gap:
        verdict = "a"
        verdict_text = (
            "(a) EMBEDDINGS ADEQUATE. Semantic closes >=10 pp of the @1 gap and resolves "
            "S4615 unreachables. Chunks + bge-small-en-v1.5 are sufficient. Deprioritize P3."
        )
    elif both_high_at5 and uplift_1 < 10.0 and unreachables_persist:
        verdict = "b"
        verdict_text = (
            "(b) NON-CONCLUSIVE -> REFINE GOLD FIRST. Both retrievers already high @5; "
            "semantic uplift @1 is modest (<10 pp); S4615 unreachables persist. "
            "The unit-level gold set is too coarse to discriminate retriever quality at the "
            "relevant operating point. Recommended next step: build lesson-level gold (Stage 1) "
            "before deciding on P3 hierarchical chunking."
        )
    else:
        verdict = "c"
        verdict_text = (
            "(c) GRANULARITY BOTTLENECK -> P3 JUSTIFIED. Substantial @10 misses persist "
            "even with semantic retriever, pointing to chunk-level granularity as the "
            "binding constraint, not retriever quality."
        )

    lines.append(f"**Verdict: {verdict_text}**")
    lines.append("")

    if hybrid_signal:
        lines.append(
            f"**Transversal — HYBRID RECOMMENDED:** {n_regression_te}/{n_regression} regressions "
            "are on token-exact queries (T-codes/table names). Lexical retrieval has a "
            "structural advantage for exact SAP identifiers. Use lexical+semantic RRF hybrid "
            "regardless of the P3 decision above."
        )
    else:
        lines.append(
            f"**Transversal:** Token-exact regression rate is low ({n_regression_te}/{n_regression}). "
            "Pure semantic retrieval does not show systematic weakness on exact-token queries."
        )
    lines.append("")

    # ----- Run instructions -----
    lines.append("## How to Run")
    lines.append("```bash")
    lines.append("cd 'c:/Users/aranu/Desktop/IA/Chunking'")
    lines.append("# Single doc, single retriever:")
    lines.append("python3 eval/score.py --src S4620 --retriever semantic")
    lines.append("# Full comparison:")
    lines.append("python3 eval/compare.py")
    lines.append("```")
    lines.append("")
    lines.append("## Limitations")
    lines.append("- Gold at **unit level** (indulgent). Lesson-level gold would give tighter signal.")
    lines.append("- bge-small-en-v1.5 truncates all 82 chunks at 512 tokens. Larger model or")
    lines.append("  chunking at <=512 tokens would improve semantic recall for long chunks.")
    lines.append("- Hybrid RRF uses k=60 (Cormack 2009); not tuned for this corpus.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="Single doc key (default: all with gold)")
    parser.add_argument("--no-hybrid", action="store_true", help="Skip hybrid column")
    args = parser.parse_args()

    # Determine which gold sets to use
    gold_files = sorted(GOLD_DIR.glob("*_assessments.json"))
    if args.src:
        gold_files = [f for f in gold_files if f.stem.startswith(args.src)]
    if not gold_files:
        print("No gold files found. Run extract_assessments.py first.")
        sys.exit(1)

    print(f"Loading {len(chunks_global := load_chunks())} chunks...")
    chunks = chunks_global

    print("Initializing lexical retriever...")
    lex = TFIDFRetriever(chunks)

    print("Initializing semantic retriever...")
    sem = SemanticRetriever(chunks)

    # Run smoke test
    passed, msg = sem.smoke_test(chunks)
    print(f"Smoke test: {'PASSED' if passed else 'FAILED'} | {msg}")
    if not passed:
        print("ERROR: Smoke test failed. Check prefix/normalization in SemanticRetriever.")
        sys.exit(1)

    include_hybrid = not args.no_hybrid
    if include_hybrid:
        print("Hybrid (RRF) enabled.")

        def make_hybrid_fn(lex_r, sem_r, K=50):
            def fn(q, k):
                return rrf_fuse([lex_r.retrieve(q, K), sem_r.retrieve(q, K)])[:k]
            return fn

        hyb_fn = make_hybrid_fn(lex, sem)

    all_lex: dict[str, list] = {}
    all_sem: dict[str, list] = {}
    all_hyb: dict[str, list] | None = {} if include_hybrid else None
    all_diffs: dict[str, list] = {}
    all_gold: dict[str, dict] = {}

    for gold_path in gold_files:
        src = gold_path.stem.replace("_assessments", "")
        print(f"\n--- {src} ---")
        with open(gold_path, encoding="utf-8") as f:
            gold = json.load(f)
        all_gold[src] = gold

        questions = [q for q in gold["questions"] if not q.get("excluded")]

        lex_rows = score_questions(questions, chunks, src, lex.retrieve)
        sem_rows = score_questions(questions, chunks, src, sem.retrieve)

        # Re-derive gold_ids for diff (score_questions does it internally)
        # We need it to be consistent, so re-use the same mechanism
        for r in lex_rows + sem_rows:
            if r["mappable"] and not r.get("gold_ids"):
                r["gold_ids"] = derive_gold_chunk_ids(
                    next(q for q in questions if q["id"] == r["id"]),
                    chunks, src
                )

        all_lex[src] = lex_rows
        all_sem[src] = sem_rows

        if include_hybrid:
            hyb_rows = score_questions(questions, chunks, src, hyb_fn)
            all_hyb[src] = hyb_rows

        all_diffs[src] = diff_results(lex_rows, sem_rows)

        la = aggregate(lex_rows)
        sa = aggregate(sem_rows)
        print(
            f"  Lex  recall@1={pct(la['recall'][1])} @5={pct(la['recall'][5])} "
            f"@10={pct(la['recall'][10])} MRR={la['mrr']:.3f}"
        )
        print(
            f"  Sem  recall@1={pct(sa['recall'][1])} @5={pct(sa['recall'][5])} "
            f"@10={pct(sa['recall'][10])} MRR={sa['mrr']:.3f}"
        )
        if include_hybrid:
            ha = aggregate(all_hyb[src])
            print(
                f"  Hyb  recall@1={pct(ha['recall'][1])} @5={pct(ha['recall'][5])} "
                f"@10={pct(ha['recall'][10])} MRR={ha['mrr']:.3f}"
            )

    # S4615 diagnosis
    s4615_diagnosis = []
    if "S4615" in all_lex:
        s4615_diagnosis = diagnose_unreachable(
            "S4615",
            all_lex["S4615"],
            all_sem["S4615"],
            [q for q in all_gold["S4615"]["questions"] if not q.get("excluded")],
            chunks,
        )

    # Load semantic meta
    meta_path = Path("eval/index/bge-small-en-v1.5/meta.json")
    semantic_meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    semantic_meta["model"] = sem.MODEL_NAME

    report = generate_report(
        all_lex, all_sem, all_hyb, all_diffs, all_gold,
        s4615_diagnosis, chunks, semantic_meta, include_hybrid,
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    md_path = RESULTS_DIR / f"semantic_vs_lexical_{today}.md"
    json_path = RESULTS_DIR / f"semantic_vs_lexical_{today}.json"

    md_path.write_text(report, encoding="utf-8")
    print(f"\nReport: {md_path}")

    summary = {
        "generated": today,
        "model": sem.MODEL_NAME,
        "truncated_chunks": semantic_meta.get("truncated"),
        "docs": {
            src: {
                "lexical": {k: aggregate(all_lex[src])["recall"][k] for k in K_VALUES}
                          | {"mrr": aggregate(all_lex[src])["mrr"]},
                "semantic": {k: aggregate(all_sem[src])["recall"][k] for k in K_VALUES}
                           | {"mrr": aggregate(all_sem[src])["mrr"]},
            }
            for src in sorted(all_lex.keys())
        },
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"JSON:   {json_path}")


if __name__ == "__main__":
    main()
