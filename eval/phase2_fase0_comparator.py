"""
Fase 0 — Comparator validity check (zero generation cost).

Compares cached top_k_ids for every abstention question against
retriever.retrieve() on the current clean index. Single variable check:
if top-k is identical, the cached baselines are valid comparators for
the generator-only experiment.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.retriever import load_chunks, make_retriever

CHUNKS_DIR = Path("chunks")
TOP_K      = 5
GOLD_BUFFER = 10  # faithfulness.py uses top_k + 10 for raw retrieval

FULL_CACHE  = Path("eval/results/faithfulness_full_2026-06-22.json")
COMPL_CACHE = Path("eval/results/faithfulness_abstention_completion_2026-06-23.json")


def load_abstention_records():
    with open(FULL_CACHE, encoding="utf-8") as f:
        full = json.load(f)
    with open(COMPL_CACHE, encoding="utf-8") as f:
        compl = json.load(f)
    seen = set()
    records = []
    for r in full["abstention_results"] + compl["abstention_results"]:
        if r["id"] not in seen:
            seen.add(r["id"])
            records.append(r)
    return records


def retrieve_top_k(retriever, question: str, gold_ids: list[str], top_k: int) -> list[str]:
    """Mirrors faithfulness.py evaluate_one() with mode='abstention' exactly.
    Gold is ALWAYS excluded from context (line 336-337 of faithfulness.py),
    regardless of whether it appears in raw retrieval.
    """
    raw = retriever.retrieve(question, k=top_k + GOLD_BUFFER)
    gold_in_top_k = any(gid in raw[:top_k] for gid in gold_ids)
    gold_set = set(gold_ids)
    # abstention mode: always exclude gold
    ids = [cid for cid in raw if cid not in gold_set][:top_k]
    return ids, gold_in_top_k


def main():
    print("Loading chunks...")
    chunks = load_chunks(CHUNKS_DIR)
    print(f"  {len(chunks)} chunks loaded")

    print("Loading retriever (semantic_long / bge-m3)...")
    retriever = make_retriever("semantic_long", chunks)

    print("Loading abstention records...")
    records = load_abstention_records()
    print(f"  {len(records)} unique abstention records\n")

    mismatches = []
    total = len(records)
    by_src_total = {}
    by_src_match = {}

    for i, r in enumerate(records):
        src = r["src"]
        by_src_total[src] = by_src_total.get(src, 0) + 1

        cached_ids   = r["top_k_ids"]
        cached_gold  = r["gold_in_top_k"]

        live_ids, live_gold = retrieve_top_k(
            retriever, r["question"], r["gold_chunk_ids"], TOP_K
        )

        if cached_ids == live_ids:
            by_src_match[src] = by_src_match.get(src, 0) + 1
        else:
            mismatches.append({
                "id":         r["id"],
                "src":        src,
                "cached_ids": cached_ids,
                "live_ids":   live_ids,
                "cached_gold": cached_gold,
                "live_gold":   live_gold,
            })

        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{total}] processed...")

    n_match = total - len(mismatches)
    print(f"\n{'='*60}")
    print(f"FASE 0 RESULTS")
    print(f"{'='*60}")
    print(f"Total abstention questions : {total}")
    print(f"Exact top_k match         : {n_match}  ({100*n_match/total:.1f}%)")
    print(f"Mismatches                : {len(mismatches)}")
    print()
    print("Per-SRC breakdown:")
    for src in sorted(by_src_total):
        t = by_src_total[src]
        m = by_src_match.get(src, 0)
        flag = "" if m == t else "  *** MISMATCH ***"
        print(f"  {src}: {m}/{t} match{flag}")

    if mismatches:
        print("\nMismatched records (need re-baseline in Fase 1):")
        for mm in mismatches:
            print(f"  {mm['id']} ({mm['src']})")
            print(f"    cached : {mm['cached_ids']}")
            print(f"    live   : {mm['live_ids']}")
            print(f"    gold_in_top_k cached={mm['cached_gold']} live={mm['live_gold']}")
    else:
        print("\nAll top_k_ids identical — cached baselines are valid comparators.")
        print("Single variable = GENERATOR_SYSTEM confirmed.")

    print(f"{'='*60}")
    return mismatches


if __name__ == "__main__":
    mismatches = main()
    sys.exit(0 if not mismatches else 1)
