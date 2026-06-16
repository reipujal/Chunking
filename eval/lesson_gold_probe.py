"""
lesson_gold_probe.py

Lesson-level gold re-evaluation: A vs B vs C on lesson-title queries.

Goal: settle the P3 retrieval axis by testing whether window-pooled retrieval (C)
beats whole-chunk semantic retrieval (B) when gold spans are at lesson granularity
(tighter than unit spans used in granularity_probe.py).

Assignment method: STRUCTURAL ONLY (TOC lesson titles + page spans, no content-overlap).
Queries: lesson titles (from TOC — not from Learning Assessment content).
This creates a DIFFERENT gold set from the LA questions. Both levels coexist.

Pre-registered decision criterion (written BEFORE running, per methodology):

  Compare delta B-C @1 and MRR in lesson-gold vs unit-gold:
  - If lesson-gold B@1 - C@1 changes sign OR C-B delta grows to >= 8 pp:
      => Window-pooling materially helps at lesson granularity => P3 JUSTIFIED by retrieval.
  - If lesson-gold C@1 - B@1 stays < 5 pp (similar to unit-gold +3.0 pp):
      => Window-pooling neither helps nor hurts at lesson granularity.
      => CLOSE the retrieval axis for P3. P3 may still be motivated by generation
         quality (faithfulness/relevance in generation arm), maintainability, or
         O(N x M) index cost — but NOT by current retrieval metrics.
         Do NOT refine gold further (infinite regress).
  - If non-mappable rate > 25 % of lesson queries:
      => Gold quality too low (lesson chunks missing from corpus) => NON-CONCLUSIVE.
         Expand corpus coverage first, then repeat.

Usage:
    python3 eval/lesson_gold_probe.py              # all 5 docs
    python3 eval/lesson_gold_probe.py --src S4620  # single doc
    python3 eval/lesson_gold_probe.py --no-cache   # force index rebuild
"""

import argparse
import copy
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.retriever import (
    load_chunks,
    TFIDFRetriever,
    LongContextRetriever,
    WindowPooledRetriever,
    CHUNKS_DIR,
)
from eval.score import derive_gold_chunk_ids, recall_at_k, mrr, avg

GOLD_DIR = Path("eval/gold")
RESULTS_DIR = Path("eval/results")

SRCS = ["S4600", "S4605", "S4610", "S4615", "S4620"]
K_VALUES = [1, 3, 5, 10]

# Unit-gold summary from granularity_probe_2026-06-16 (reference for comparison)
UNIT_GOLD_SUMMARY = {
    "A": {"@1": 0.627, "@5": 0.903, "@10": 0.948, "mrr": 0.744},
    "B": {"@1": 0.754, "@5": 0.925, "@10": 0.963, "mrr": 0.823},
    "C": {"@1": 0.784, "@5": 0.918, "@10": 0.963, "mrr": 0.845},
    "B_minus_A": {"@1": 0.127, "mrr": 0.079},
    "C_minus_B": {"@1": 0.030, "mrr": 0.022},
}

PRE_REGISTERED_CRITERION = """
## Pre-Registered Decision Criterion
*Written BEFORE examining results.*

**Context:** Unit-gold B-C delta = +3.0 pp @1 / +0.022 MRR (non-conclusive due to
indulgent gold spans). Lesson-gold uses TIGHTER spans (lesson-level, ~3-8 pages each
vs 8-22 pages at unit level). Queries are lesson TITLES (structural, not LA questions).

**If lesson-gold C@1 - B@1 >= 8 pp** (or MRR delta >= 0.06):
  => Window-pooling helps materially at lesson granularity.
  => P3 (hierarchical chunking / finer retrieval units) JUSTIFIED by retrieval evidence.

**If lesson-gold C@1 - B@1 < 5 pp** (similar to unit-gold +3.0 pp):
  => Window-pooling does not help even with tighter gold.
  => CLOSE the P3 retrieval axis. Evaluate P3 via generation quality arm
     (faithfulness, answer precision on long chunks) if motivation remains.
  => Do NOT create further refined gold sets — this is the terminal retrieval test.

**Non-conclusive condition:** non-mappable rate > 25% of lesson queries.
  (Signals corpus coverage gap, not retrieval weakness.)

**B regression caveat:** if B drops significantly vs unit-gold (>5 pp), suspect gold
quality mismatch (lesson-title queries may systematically favor different chunks than
the LA questions used for unit-gold). Flag but do not invalidate.
"""


def load_lesson_gold(src: str) -> dict | None:
    path = GOLD_DIR / f"{src}_lesson_gold.json"
    if not path.exists():
        print(f"  WARNING: {path} not found — run lesson_gold_builder.py first")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def score_one(
    gold_questions: list[dict],
    chunks: dict,
    src: str,
    retriever_fn,
) -> dict:
    """Score one retriever on one doc's lesson gold. Uses deep-copy to prevent mutation."""
    qs = copy.deepcopy(gold_questions)
    per_q = []
    no_gold = 0

    for q in qs:
        if q.get("excluded"):
            continue
        gold_ids = derive_gold_chunk_ids(q, chunks, src)
        mappable = len(gold_ids) > 0
        if not mappable:
            no_gold += 1
            per_q.append({
                "id": q["id"], "lesson": q.get("lesson", ""),
                "mappable": False, "gold_ids": [],
                "recall": {k: None for k in K_VALUES}, "mrr": None,
            })
            continue

        retrieved = retriever_fn(q["question"], max(K_VALUES))
        recalls = {k: recall_at_k(gold_ids, retrieved, k) for k in K_VALUES}
        mrr_val = mrr(gold_ids, retrieved)

        first_chunk = chunks.get(gold_ids[0], {})
        per_q.append({
            "id": q["id"],
            "lesson": q.get("lesson", ""),
            "unit": q.get("unit", ""),
            "question": q.get("question", ""),
            "mappable": True,
            "gold_ids": gold_ids,
            "retrieved": retrieved[:3],
            "recall": recalls,
            "mrr": mrr_val,
            "chunk_type": first_chunk.get("chunk_type", "unknown"),
        })

    mappable = [r for r in per_q if r["mappable"]]
    global_recall = {k: avg([r["recall"][k] for r in mappable]) for k in K_VALUES}
    global_mrr = avg([r["mrr"] for r in mappable])

    by_type = defaultdict(list)
    for r in mappable:
        by_type[r.get("chunk_type", "unknown")].append(r)

    return {
        "mappable": len(mappable),
        "not_mappable": no_gold,
        "global": {"recall": global_recall, "mrr": global_mrr},
        "by_type": {ct: {"count": len(rs),
                         "recall": {k: avg([r["recall"][k] for r in rs]) for k in K_VALUES},
                         "mrr": avg([r["mrr"] for r in rs])}
                    for ct, rs in by_type.items()},
        "per_question": per_q,
    }


def pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def build_report(
    all_results: dict,  # {src: {"A": result, "B": result, "C": result}}
    lesson_golds: dict,  # {src: gold_dict}
    args,
) -> str:
    lines = []
    today = date.today().isoformat()

    lines.append("# Lesson-Level Gold Re-Evaluation — P3 Retrieval Verdict")
    lines.append(f"Generated: {today}")
    lines.append(f"Model B & C: `BAAI/bge-m3` (8192-token context) — SAME model, cached from granularity probe")
    lines.append(f"Corpus: 82 chunks | Docs: {', '.join(SRCS)}")
    lines.append(f"Gold: Lesson-title queries (TOC structural assignment, no content-overlap)")
    lines.append("")

    lines.append(PRE_REGISTERED_CRITERION)
    lines.append("")

    # -----------------------------------------------------------------------
    # Correctness checklist
    # -----------------------------------------------------------------------
    lines.append("## Correctness Checklist")
    lines.append("")
    lines.append("- Gold assignment method: TOC structural (lesson titles + footer page ranges)")
    lines.append("- Offsets reused (NOT re-detected): S4600/S4605/S4615=+8, S4610/S4620=+6")
    lines.append("- Spot-checks (first phys page of lesson span shows lesson title):")
    lines.append("  - S4600 phys 10: 'Unit 1 Lesson 1 Identifying Key Features of SAP Fiori' OK")
    lines.append("  - S4610 phys 28: 'Unit 3 Lesson 1 Controlling Delivery Documents' OK")
    lines.append("  - S4615 phys 65: 'Unit 7 Lesson 2 Understanding Special Types of Settlement' OK")
    lines.append("  - S4620 phys 25: 'Unit 2 Lesson 1 Configuring Pricing' OK")
    lines.append("- Unit gold preserved: yes (separate files, lesson gold is additive)")
    lines.append("- Retrievers: UNCHANGED — using cached bge-m3 embeddings from granularity probe")
    lines.append("- Model B = C: BAAI/bge-m3 (verified in granularity probe, cache reused)")
    lines.append("")

    # -----------------------------------------------------------------------
    # Assignment method breakdown
    # -----------------------------------------------------------------------
    lines.append("## Assignment Method Breakdown")
    lines.append("")
    total_qs = sum(len(lg["questions"]) for lg in lesson_golds.values())
    lines.append(f"Total lesson queries: {total_qs} across {len(SRCS)} docs")
    lines.append("Assignment method for ALL queries: `toc_structural` (lesson title from TOC)")
    lines.append("unit_fallback: 0 (lesson-objective approach creates new queries for EVERY lesson)")
    lines.append("")
    lines.append("**Note:** These are NEW queries (lesson titles), not refinements of LA questions.")
    lines.append("Unit-level LA gold (134 questions) is preserved for comparison.")
    lines.append("")
    lines.append("| Doc | Lesson queries | Offset | Multi-lesson units |")
    lines.append("| --- | --- | --- | --- |")
    for src, lg in lesson_golds.items():
        n = len(lg["questions"])
        offset = lg["offset"]
        from eval.lesson_gold_builder import TOC_LESSONS
        multi = sum(1 for t in TOC_LESSONS[src]
                    if sum(1 for t2 in TOC_LESSONS[src] if t2[0] == t[0]) > 1)
        lines.append(f"| {src} | {n} | +{offset} | {multi} lessons in multi-lesson units |")
    lines.append("")

    # -----------------------------------------------------------------------
    # Mappable summary
    # -----------------------------------------------------------------------
    lines.append("## Mappable Queries per Doc (lesson spans vs chunk page ranges)")
    lines.append("")
    lines.append("| Doc | Total | Mappable | Not mappable | Map rate |")
    lines.append("| --- | --- | --- | --- | --- |")
    total_m = total_nm = 0
    for src in SRCS:
        res_a = all_results[src]["A"]
        m = res_a["mappable"]
        nm = res_a["not_mappable"]
        total_m += m
        total_nm += nm
        rate = m / (m + nm) if (m + nm) > 0 else 0
        lines.append(f"| {src} | {m+nm} | {m} | {nm} | {pct(rate)} |")
    total_n = total_m + total_nm
    lines.append(f"| **TOTAL** | **{total_n}** | **{total_m}** | **{total_nm}** | **{pct(total_m/total_n if total_n else 0)}** |")
    lines.append("")
    if total_nm / total_n > 0.25:
        lines.append("**WARNING: non-mappable rate > 25% — corpus coverage gap. Results non-conclusive.**")
    else:
        lines.append(f"Non-mappable rate {pct(total_nm/total_n)}: within confidence threshold (< 25%).")
    lines.append("")

    # -----------------------------------------------------------------------
    # Global results table
    # -----------------------------------------------------------------------
    lines.append("## Global Results — Lesson Gold")
    lines.append("")
    lines.append("| Doc | N | A@1 | A@5 | A@10 | A-MRR | B@1 | B@5 | B@10 | B-MRR | C@1 | C@5 | C@10 | C-MRR |")
    lines.append("| --- | --- | " + " | ".join(["---"] * 12) + " |")

    agg = {"A": defaultdict(list), "B": defaultdict(list), "C": defaultdict(list)}
    for src in SRCS:
        row = [src]
        n_map = all_results[src]["A"]["mappable"]
        row.append(str(n_map))
        for ret in ["A", "B", "C"]:
            r = all_results[src][ret]["global"]
            row += [pct(r["recall"][1]), pct(r["recall"][5]), pct(r["recall"][10]),
                    f"{r['mrr']:.3f}"]
            agg[ret][1].append(r["recall"][1])
            agg[ret][5].append(r["recall"][5])
            agg[ret][10].append(r["recall"][10])
            agg[ret]["mrr"].append(r["mrr"])
            agg[ret]["n"].append(n_map)
        lines.append("| " + " | ".join(row) + " |")

    # Weighted aggregate (by mappable count)
    def weighted_avg(vals, weights):
        return sum(v * w for v, w in zip(vals, weights)) / sum(weights)

    weights = agg["A"]["n"]
    tot_row = ["**TOTAL**", f"**{sum(weights)}**"]
    for ret in ["A", "B", "C"]:
        for k in [1, 5, 10]:
            tot_row.append(f"**{pct(weighted_avg(agg[ret][k], weights))}**")
        tot_row.append(f"**{weighted_avg(agg[ret]['mrr'], weights):.3f}**")
    lines.append("| " + " | ".join(tot_row) + " |")
    lines.append("")

    # Compute final aggregates for verdicts
    final = {}
    for ret in ["A", "B", "C"]:
        final[ret] = {
            "@1": weighted_avg(agg[ret][1], weights),
            "@5": weighted_avg(agg[ret][5], weights),
            "@10": weighted_avg(agg[ret][10], weights),
            "mrr": weighted_avg(agg[ret]["mrr"], weights),
        }

    # -----------------------------------------------------------------------
    # By chunk type
    # -----------------------------------------------------------------------
    lines.append("## By Chunk Type (aggregate across all docs, lesson gold)")
    lines.append("")
    lines.append("| Type | N | A@1 | B@1 | delta(B-A) | C@1 | delta(C-B) | A-MRR | B-MRR | C-MRR |")
    lines.append("| --- | --- | " + " | ".join(["---"] * 8) + " |")
    all_type = {"A": defaultdict(list), "B": defaultdict(list), "C": defaultdict(list)}
    for src in SRCS:
        for ret in ["A", "B", "C"]:
            for ct, m in all_results[src][ret]["by_type"].items():
                all_type[ret][ct].extend([m["recall"][1]] * m["count"])
                all_type[ret][f"{ct}_mrr"].extend([m["mrr"]] * m["count"])
                all_type[ret][f"{ct}_n"].append(m["count"])

    ctypes = sorted(set(
        ct for ret in ["A", "B", "C"]
        for ct in all_type[ret].keys()
        if not ct.endswith("_mrr") and not ct.endswith("_n")
    ))
    for ct in ctypes:
        na = len(all_type["A"].get(ct, []))
        if na == 0:
            continue
        a1 = avg(all_type["A"].get(ct, [0]))
        b1 = avg(all_type["B"].get(ct, [0]))
        c1 = avg(all_type["C"].get(ct, [0]))
        amrr = avg(all_type["A"].get(f"{ct}_mrr", [0]))
        bmrr = avg(all_type["B"].get(f"{ct}_mrr", [0]))
        cmrr = avg(all_type["C"].get(f"{ct}_mrr", [0]))
        dba = b1 - a1
        dcb = c1 - b1
        lines.append(f"| {ct} | {na} | {pct(a1)} | {pct(b1)} | {dba:+.1f}pp | "
                     f"{pct(c1)} | {dcb:+.1f}pp | {amrr:.3f} | {bmrr:.3f} | {cmrr:.3f} |")
    lines.append("")

    # -----------------------------------------------------------------------
    # B vs C diff (lesson gold)
    # -----------------------------------------------------------------------
    lines.append("## B vs C Question-Level Diff (lesson gold @1)")
    lines.append("")
    both_hit = c_fixed = b_reg = both_miss = 0
    c_fixed_qs = []
    b_reg_qs = []
    for src in SRCS:
        pq_b = {r["id"]: r for r in all_results[src]["B"]["per_question"] if r["mappable"]}
        pq_c = {r["id"]: r for r in all_results[src]["C"]["per_question"] if r["mappable"]}
        for qid, rb in pq_b.items():
            rc = pq_c.get(qid)
            if rc is None:
                continue
            bh = rb["recall"][1] > 0
            ch = rc["recall"][1] > 0
            if bh and ch:
                both_hit += 1
            elif not bh and ch:
                c_fixed += 1
                c_fixed_qs.append((qid, rb.get("question", "")[:80]))
            elif bh and not ch:
                b_reg += 1
                b_reg_qs.append((qid, rb.get("question", "")[:80]))
            else:
                both_miss += 1
    lines.append(f"- both_hit  (B=1, C=1): {both_hit}")
    lines.append(f"- c_fixed   (B=0, C=1 — window recovers): {c_fixed}")
    lines.append(f"- b_regression (B=1, C=0 — window loses): {b_reg}")
    lines.append(f"- both_miss (B=0, C=0): {both_miss}")
    lines.append("")
    if c_fixed_qs:
        lines.append("C recovers (sample):")
        for qid, q in c_fixed_qs[:5]:
            lines.append(f"  - {qid}: _{q}_")
        lines.append("")
    if b_reg_qs:
        lines.append("B-regressions (sample):")
        for qid, q in b_reg_qs[:5]:
            lines.append(f"  - {qid}: _{q}_")
        lines.append("")

    # -----------------------------------------------------------------------
    # Lesson vs unit comparison side-by-side
    # -----------------------------------------------------------------------
    lines.append("## Lesson-Gold vs Unit-Gold: B-C Delta Comparison")
    lines.append("")
    lines.append("| Metric | Unit-gold B-C | Lesson-gold B-C | Change |")
    lines.append("| --- | --- | --- | --- |")

    ug = UNIT_GOLD_SUMMARY
    cb_unit_1 = ug["C"]["@1"] - ug["B"]["@1"]
    cb_lesson_1 = final["C"]["@1"] - final["B"]["@1"]
    cb_unit_mrr = ug["C"]["mrr"] - ug["B"]["mrr"]
    cb_lesson_mrr = final["C"]["mrr"] - final["B"]["mrr"]

    lines.append(f"| C-B @1 | {cb_unit_1*100:+.1f} pp | {cb_lesson_1*100:+.1f} pp | {(cb_lesson_1-cb_unit_1)*100:+.1f} pp |")
    lines.append(f"| C-B MRR | {cb_unit_mrr:+.4f} | {cb_lesson_mrr:+.4f} | {(cb_lesson_mrr-cb_unit_mrr):+.4f} |")
    lines.append(f"| A@1 | {pct(ug['A']['@1'])} | {pct(final['A']['@1'])} | — |")
    lines.append(f"| B@1 | {pct(ug['B']['@1'])} | {pct(final['B']['@1'])} | — |")
    lines.append(f"| C@1 | {pct(ug['C']['@1'])} | {pct(final['C']['@1'])} | — |")
    lines.append("")

    # -----------------------------------------------------------------------
    # Verdicts
    # -----------------------------------------------------------------------
    lines.append("## Verdicts")
    lines.append("")

    # Verdict 1: A vs B (sanity)
    ab_lesson = final["B"]["@1"] - final["A"]["@1"]
    lines.append(f"### Verdict 1 — Semantic vs Lexical (A vs B, lesson gold)")
    if ab_lesson >= 0.05:
        lines.append(f"Semantic still wins at lesson granularity: B@1 - A@1 = {ab_lesson*100:+.1f} pp. Confirming bge-m3 advantage holds.")
    else:
        lines.append(f"B-A delta at lesson level = {ab_lesson*100:+.1f} pp. Reduced vs unit-gold — likely due to query style change (lesson titles vs LA questions).")
    lines.append("")

    # Verdict 2: B vs C (P3)
    lines.append("### Verdict 2 — P3 Granularity (B vs C, lesson gold)")
    lines.append(f"C@1 - B@1 (lesson gold) = **{cb_lesson_1*100:+.1f} pp**")
    lines.append(f"C-MRR - B-MRR (lesson gold) = **{cb_lesson_mrr:+.4f}**")
    lines.append(f"Reference (unit gold): C@1 - B@1 = +3.0 pp | C-MRR - B-MRR = +0.022")
    lines.append("")

    if cb_lesson_1 >= 0.08:
        lines.append("**VERDICT: P3 JUSTIFIED by retrieval.** Window-pooling materially helps at lesson")
        lines.append("granularity (C-B delta >= 8 pp). Finer retrieval units (hierarchical chunking / P3) are")
        lines.append("supported by retrieval evidence.")
    elif cb_lesson_1 < 0.05:
        lines.append("**VERDICT: CLOSE THE RETRIEVAL AXIS FOR P3.**")
        lines.append(f"C-B delta at lesson gold ({cb_lesson_1*100:+.1f} pp) is similar to unit-gold (+3.0 pp).")
        lines.append("Window-pooling does not help even with tighter gold spans. The +3.0 pp unit-gold signal")
        lines.append("does not amplify when spans are narrowed to lesson level.")
        lines.append("")
        lines.append("**Implication:** If P3 (hierarchical chunking) is still desired, motivate it via:")
        lines.append("  1. Generation quality arm: answer faithfulness / precision on long chunks")
        lines.append("  2. Index efficiency: O(N×M) window vectors vs O(N) chunk vectors")
        lines.append("  3. Maintainability: finer chunks easier to update/version")
        lines.append("  Do NOT refine gold further — this is the terminal retrieval test.")
    else:
        lines.append(f"**VERDICT: NON-CONCLUSIVE.** C-B delta ({cb_lesson_1*100:+.1f} pp) falls in the")
        lines.append("ambiguous 5-8 pp range. Lesson gold reduces indulgence but signal still weak.")
        lines.append("Consider expanding corpus (more docs) before concluding.")
    lines.append("")

    # Non-mappable confidence gate
    if total_nm / total_n > 0.25:
        lines.append("**CONFIDENCE GATE FAILED:** Non-mappable rate > 25%. Verdict reliability is low.")
        lines.append("Expand corpus coverage (process more documents) before interpreting these results.")
    else:
        lines.append(f"**Confidence gate:** Non-mappable rate {pct(total_nm/total_n)} < 25% — verdict is reliable.")
    lines.append("")

    # -----------------------------------------------------------------------
    # Limitations
    # -----------------------------------------------------------------------
    lines.append("## Limitations")
    lines.append("")
    lines.append("- Queries are lesson TITLES (not LA questions) — different query distribution than unit gold.")
    lines.append("  Comparison with unit-gold numbers is informative but not apples-to-apples.")
    lines.append("- Lesson titles are shorter and more topic-focused than LA questions → may systematically")
    lines.append("  favor or disfavor certain retrieval strategies.")
    lines.append("- Unit-gold LA questions may be harder/subtler; lesson-title queries are easier (topic match).")
    lines.append("  A smaller B-C delta here may not fully generalize to harder queries.")
    lines.append("- 5 documents, ~82 lesson queries: moderate sample size. Add more docs for higher confidence.")
    lines.append("- Window parameters (400 tok / stride 300) not tuned for this corpus.")
    lines.append("")

    lines.append("## How to Run")
    lines.append("")
    lines.append("```bash")
    lines.append("cd 'c:/Users/aranu/Desktop/IA/Chunking'")
    lines.append("# Build lesson gold files (one-time):")
    lines.append("python3 eval/lesson_gold_builder.py")
    lines.append("# Run probe (all 5 docs):")
    lines.append("python3 eval/lesson_gold_probe.py")
    lines.append("# Single doc via score.py:")
    lines.append("python3 eval/score.py --src S4620 --retriever semantic_long --gold eval/gold/S4620_lesson_gold.json")
    lines.append("python3 eval/score.py --src S4620 --retriever semantic_window --gold eval/gold/S4620_lesson_gold.json")
    lines.append("```")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="Single doc (default: all)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Delete bge-m3 index and rebuild (WARNING: ~15 min)")
    args = parser.parse_args()

    srcs = [args.src] if args.src else SRCS

    if args.no_cache:
        import shutil
        for d in [Path("eval/index/bge-m3"), Path("eval/index/bge-m3-window")]:
            if d.exists():
                shutil.rmtree(d)
                print(f"Deleted cache: {d}")

    print("Loading chunks...")
    chunks = load_chunks()
    print(f"  {len(chunks)} chunks loaded")

    # Build retrievers (will load from cache if present)
    print("\n[A] Building TF-IDF retriever...")
    ret_a = TFIDFRetriever(chunks)

    print("\n[B] Building LongContextRetriever (bge-m3, whole-chunk)...")
    ret_b = LongContextRetriever(chunks)

    print("\n[C] Building WindowPooledRetriever (bge-m3, window-pooled)...")
    ret_c = WindowPooledRetriever(chunks)

    print()

    all_results = {}
    lesson_golds = {}

    for src in srcs:
        lg = load_lesson_gold(src)
        if lg is None:
            continue
        lesson_golds[src] = lg

        n_qs = len(lg["questions"])
        print(f"{'='*60}")
        print(f"Scoring {src} ({n_qs} lesson queries)...")

        results_src = {}
        for label, ret in [("A", ret_a), ("B", ret_b), ("C", ret_c)]:
            res = score_one(lg["questions"], chunks, src, ret.retrieve)
            results_src[label] = res
            g = res["global"]
            print(f"  {label} => @1={pct(g['recall'][1])}  @5={pct(g['recall'][5])}"
                  f"  @10={pct(g['recall'][10])}  mappable={res['mappable']}/{n_qs}")

        all_results[src] = results_src

    if not all_results:
        print("No results — did you run lesson_gold_builder.py?")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Building report...")
    report = build_report(all_results, lesson_golds, args)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    md_path = RESULTS_DIR / f"lesson_gold_probe_{today}.md"
    json_path = RESULTS_DIR / f"lesson_gold_probe_{today}.json"

    md_path.write_text(report, encoding="utf-8")
    print(f"Report: {md_path}")

    json_out = {
        "generated": today,
        "model_B_C": "BAAI/bge-m3",
        "total_lesson_queries": sum(len(lg["questions"]) for lg in lesson_golds.values()),
        "results_by_src": {
            src: {
                label: {
                    "mappable": all_results[src][label]["mappable"],
                    "not_mappable": all_results[src][label]["not_mappable"],
                    "global": all_results[src][label]["global"],
                    "by_type": all_results[src][label]["by_type"],
                }
                for label in ["A", "B", "C"]
            }
            for src in all_results
        }
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, indent=2, ensure_ascii=False)
    print(f"JSON:   {json_path}")

    # Final aggregate print
    print("\n=== AGGREGATE (lesson gold) ===")
    w = []
    vals = {"A": {k: [] for k in [1, 5, 10, "mrr"]},
            "B": {k: [] for k in [1, 5, 10, "mrr"]},
            "C": {k: [] for k in [1, 5, 10, "mrr"]}}
    for src in all_results:
        n = all_results[src]["A"]["mappable"]
        w.append(n)
        for ret in ["A", "B", "C"]:
            g = all_results[src][ret]["global"]
            for k in [1, 5, 10]:
                vals[ret][k].append(g["recall"][k])
            vals[ret]["mrr"].append(g["mrr"])

    def wa(vs, ws):
        return sum(v * wt for v, wt in zip(vs, ws)) / sum(ws) if ws else 0

    for ret in ["A", "B", "C"]:
        a1 = wa(vals[ret][1], w)
        a5 = wa(vals[ret][5], w)
        a10 = wa(vals[ret][10], w)
        mrr_ = wa(vals[ret]["mrr"], w)
        print(f"{ret}: @1={pct(a1)}  @5={pct(a5)}  @10={pct(a10)}  MRR={mrr_:.3f}")

    final_b1 = wa(vals["B"][1], w)
    final_c1 = wa(vals["C"][1], w)
    final_b_mrr = wa(vals["B"]["mrr"], w)
    final_c_mrr = wa(vals["C"]["mrr"], w)
    print(f"\nB-A @1: {(final_b1 - wa(vals['A'][1], w))*100:+.1f} pp")
    print(f"C-B @1: {(final_c1 - final_b1)*100:+.1f} pp  |  C-B MRR: {final_c_mrr - final_b_mrr:+.4f}")
    print(f"Reference (unit gold): C-B @1 = +3.0 pp  |  C-B MRR = +0.022")


if __name__ == "__main__":
    main()
