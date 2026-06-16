"""
score.py — Compute retrieval metrics for the eval gold set.

For each question:
  1. Derive gold_chunk_ids mechanically (page overlap, never by model)
  2. Run retriever → top-10 list
  3. Compute recall@k (k=1,3,5,10) and MRR (rank of first gold hit in top-10)

Aggregation: global + by area + by chunk_type.

Usage:
    python eval/score.py --src S4620
    python eval/score.py --src S4620 --gold eval/gold/S4620_assessments.json
"""

import re
import json
import argparse
from pathlib import Path
from datetime import date
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.retriever import retrieve, get_chunks, CHUNKS_DIR

GOLD_DIR = Path("eval/gold")
RESULTS_DIR = Path("eval/results")


# ---------------------------------------------------------------------------
# Page-overlap logic
# ---------------------------------------------------------------------------

def parse_page_range(pages_str: str) -> tuple[int, int] | None:
    """Parse '40-53' or '40' into (start, end). Returns None if unparseable."""
    pages_str = str(pages_str).strip().strip('"').strip("'")
    m = re.match(r"(\d+)\s*[-–]\s*(\d+)", pages_str)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r"(\d+)", pages_str)
    if m:
        p = int(m.group(1))
        return p, p
    return None


def ranges_overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def derive_gold_chunk_ids(
    question: dict,
    chunks: dict,
    src: str,
) -> list[str]:
    """
    Find chunks whose sources[] cite pages overlapping gold_page_span for src.
    gold_page_span and sources[].pages are all physical page numbers.
    """
    gold_span = question.get("gold_page_span")
    if not gold_span or len(gold_span) < 2:
        return []
    gold_range = (gold_span[0], gold_span[1])

    gold_ids = []
    for chunk_id, chunk in chunks.items():
        for source in chunk.get("sources", []):
            src_file = source.get("file", "")
            if src not in src_file:
                continue
            page_range = parse_page_range(source.get("pages", ""))
            if page_range and ranges_overlap(page_range, gold_range):
                gold_ids.append(chunk_id)
                break  # don't double-count same chunk

    return gold_ids


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def recall_at_k(gold_ids: list[str], retrieved: list[str], k: int) -> float:
    if not gold_ids:
        return 0.0
    gold_set = set(gold_ids)
    return 1.0 if any(r in gold_set for r in retrieved[:k]) else 0.0


def mrr(gold_ids: list[str], retrieved: list[str]) -> float:
    if not gold_ids:
        return 0.0
    gold_set = set(gold_ids)
    for rank, r in enumerate(retrieved, start=1):
        if r in gold_set:
            return 1.0 / rank
    return 0.0


def avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_dataset(
    gold_questions: list[dict],
    chunks: dict,
    src: str,
    k_values: list[int] = None,
) -> dict:
    if k_values is None:
        k_values = [1, 3, 5, 10]

    per_question = []
    no_gold_count = 0

    for q in gold_questions:
        if q.get("excluded"):
            continue

        gold_ids = derive_gold_chunk_ids(q, chunks, src)
        mappable = len(gold_ids) > 0

        # Update mappable flag on question record
        q["mappable"] = mappable
        q["gold_chunk_ids"] = gold_ids

        if not mappable:
            no_gold_count += 1
            per_question.append({
                "id": q["id"],
                "unit": q["unit"],
                "mappable": False,
                "gold_ids": [],
                "retrieved": [],
                "recall": {k: None for k in k_values},
                "mrr": None,
            })
            continue

        retrieved = retrieve(q["question"], k=max(k_values))

        recalls = {k: recall_at_k(gold_ids, retrieved, k) for k in k_values}
        mrr_val = mrr(gold_ids, retrieved)

        # Area / type from first gold chunk
        first_gold = chunks.get(gold_ids[0], {})
        area = first_gold.get("area", "unknown")
        chunk_type = first_gold.get("chunk_type", "unknown")

        per_question.append({
            "id": q["id"],
            "unit": q["unit"],
            "mappable": True,
            "gold_ids": gold_ids,
            "retrieved": retrieved,
            "recall": recalls,
            "mrr": mrr_val,
            "area": area,
            "chunk_type": chunk_type,
        })

    # Aggregate
    mappable_results = [r for r in per_question if r["mappable"]]

    global_recall = {
        k: avg([r["recall"][k] for r in mappable_results])
        for k in k_values
    }
    global_mrr = avg([r["mrr"] for r in mappable_results])

    # By area
    by_area: dict[str, list] = defaultdict(list)
    for r in mappable_results:
        by_area[r.get("area", "unknown")].append(r)

    area_metrics = {}
    for area, rows in by_area.items():
        area_metrics[area] = {
            "count": len(rows),
            "recall": {k: avg([r["recall"][k] for r in rows]) for k in k_values},
            "mrr": avg([r["mrr"] for r in rows]),
        }

    # By chunk_type
    by_type: dict[str, list] = defaultdict(list)
    for r in mappable_results:
        by_type[r.get("chunk_type", "unknown")].append(r)

    type_metrics = {}
    for ct, rows in by_type.items():
        type_metrics[ct] = {
            "count": len(rows),
            "recall": {k: avg([r["recall"][k] for r in rows]) for k in k_values},
            "mrr": avg([r["mrr"] for r in rows]),
        }

    return {
        "total_questions": len(gold_questions),
        "excluded": sum(1 for q in gold_questions if q.get("excluded")),
        "mappable": len(mappable_results),
        "not_mappable": no_gold_count,
        "global": {"recall": global_recall, "mrr": global_mrr},
        "by_area": area_metrics,
        "by_chunk_type": type_metrics,
        "per_question": per_question,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def format_report(src: str, gold: dict, results: dict) -> str:
    lines = []
    lines.append(f"# Retrieval Eval — {src}")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append(f"Gold: `eval/gold/{src}_assessments.json` (offset={gold['offset']})")
    lines.append("")

    lines.append("## Dataset Summary")
    lines.append(f"- Total questions extracted: {results['total_questions']}")
    lines.append(f"- Excluded (trivial/unparseable): {results['excluded']}")
    lines.append(f"- Mappable (≥1 gold chunk): {results['mappable']}")
    lines.append(f"- Not mappable (coverage gap): {results['not_mappable']}")
    lines.append("")

    g = results["global"]
    lines.append("## Global Metrics (mappable questions only)")
    lines.append(
        "| recall@1 | recall@3 | recall@5 | recall@10 | MRR |"
    )
    lines.append("| --- | --- | --- | --- | --- |")
    r = g["recall"]
    lines.append(
        f"| {pct(r[1])} | {pct(r[3])} | {pct(r[5])} | {pct(r[10])} | {g['mrr']:.3f} |"
    )
    lines.append("")

    if results["by_area"]:
        lines.append("## By Area")
        lines.append("| Area | N | recall@1 | recall@5 | MRR |")
        lines.append("| --- | --- | --- | --- | --- |")
        for area, m in sorted(results["by_area"].items()):
            lines.append(
                f"| {area} | {m['count']} | {pct(m['recall'][1])} | {pct(m['recall'][5])} | {m['mrr']:.3f} |"
            )
        lines.append("")

    if results["by_chunk_type"]:
        lines.append("## By Chunk Type")
        lines.append("| Type | N | recall@1 | recall@5 | MRR |")
        lines.append("| --- | --- | --- | --- | --- |")
        for ct, m in sorted(results["by_chunk_type"].items()):
            lines.append(
                f"| {ct} | {m['count']} | {pct(m['recall'][1])} | {pct(m['recall'][5])} | {m['mrr']:.3f} |"
            )
        lines.append("")

    lines.append("## Per-Question Results")
    lines.append(
        "| ID | Mappable | Gold chunks | recall@1 | recall@5 | MRR | Top-1 retrieved |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in results["per_question"]:
        if not r["mappable"]:
            lines.append(
                f"| {r['id']} | NO | — | — | — | — | — |"
            )
        else:
            top1 = r["retrieved"][0] if r["retrieved"] else "—"
            lines.append(
                f"| {r['id']} | YES | {len(r['gold_ids'])} | {pct(r['recall'][1])} | {pct(r['recall'][5])} | {r['mrr']:.3f} | {top1} |"
            )
    lines.append("")

    lines.append("## Coverage Notes")
    not_mappable = [r for r in results["per_question"] if not r["mappable"]]
    if not_mappable:
        lines.append(f"**{len(not_mappable)} questions not mapped to any chunk** — these represent coverage gaps:")
        for r in not_mappable:
            # Find original question
            q_match = next((q for q in gold["questions"] if q["id"] == r["id"]), {})
            lines.append(f"- `{r['id']}` ({r['unit']}): _{q_match.get('question','')[:80]}_")
    else:
        lines.append("All questions mapped to at least one chunk.")
    lines.append("")

    lines.append("## Limitations")
    lines.append(
        "- Gold is at **unit level** (indulgent): any chunk citing any page in the unit "
        "qualifies. Recall numbers are optimistic upper bounds. "
        "Lesson-level gold is the next refinement step."
    )
    lines.append(
        "- Retriever is **TF-IDF baseline** (lexical only). "
        "These numbers are the floor, not the ceiling."
    )
    lines.append(
        "- Metrics depend on correct offset detection. "
        f"Detected offset for {src}: {gold['offset']}."
    )
    lines.append(
        "- Questions where `correct` could not be inferred are included in retrieval "
        "eval (they don't need correct answers for recall/MRR)."
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Document key, e.g. S4620")
    parser.add_argument("--gold", help="Path to gold JSON (optional)")
    args = parser.parse_args()

    gold_path = Path(args.gold) if args.gold else GOLD_DIR / f"{args.src}_assessments.json"
    if not gold_path.exists():
        print(f"ERROR: gold file not found: {gold_path}")
        print("  Run: python eval/extract_assessments.py --src {args.src}")
        sys.exit(1)

    print(f"Loading gold: {gold_path}")
    with open(gold_path, encoding="utf-8") as f:
        gold = json.load(f)

    print(f"Loading chunks from {CHUNKS_DIR}...")
    chunks = get_chunks()
    print(f"  Loaded {len(chunks)} chunks")

    print(f"Scoring {len(gold['questions'])} questions...")
    results = score_dataset(gold["questions"], chunks, args.src)

    # Write results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    md_path = RESULTS_DIR / f"{args.src}_{today}.md"
    json_path = RESULTS_DIR / f"{args.src}_{today}.json"

    report = format_report(args.src, gold, results)
    md_path.write_text(report, encoding="utf-8")
    print(f"Report: {md_path}")

    # Write JSON (exclude verbose per_question retrieved lists to keep it readable)
    results_json = {k: v for k, v in results.items() if k != "per_question"}
    results_json["per_question_summary"] = [
        {
            "id": r["id"],
            "mappable": r["mappable"],
            "gold_ids": r.get("gold_ids", []),
            "recall_at_1": r["recall"].get(1) if r["mappable"] else None,
            "recall_at_5": r["recall"].get(5) if r["mappable"] else None,
            "mrr": r.get("mrr"),
        }
        for r in results["per_question"]
    ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=2, ensure_ascii=False)
    print(f"JSON:   {json_path}")

    # Print summary to console
    g = results["global"]
    r = g["recall"]
    print(f"\n=== {args.src} Retrieval Results ===")
    print(f"Mappable: {results['mappable']}/{results['total_questions'] - results['excluded']} available")
    print(f"recall@1={pct(r[1])}  recall@3={pct(r[3])}  recall@5={pct(r[5])}  recall@10={pct(r[10])}  MRR={g['mrr']:.3f}")


if __name__ == "__main__":
    main()
