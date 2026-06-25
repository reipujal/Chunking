"""
Fase 2 — False-abstention guardrail probe (~5/SRC, ~40 questions).

Runs positive questions with the current GENERATOR_SYSTEM (v2) to detect
whether the stricter abstention rule causes false abstentions when gold IS
in context. Judge is skipped — we only need to count pure abstentions.

Gate (pre-registered):
  pct_false_abstention <= 5%  -> PASS  (proceed to full positive re-gen)
  pct_false_abstention >= 15% -> STOP HARD
  5% < pct < 15%              -> report-and-stop, user decides

Usage:
    python eval/phase2_fase2_probe.py              # 5/SRC sample
    python eval/phase2_fase2_probe.py --n 10       # 10/SRC sample
    python eval/phase2_fase2_probe.py --srcs S4600,S4605
"""
import sys
import os
import json
import time
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.faithfulness import (
    load_chunks_extended,
    load_all_gold_questions,
    format_context,
    GENERATOR_SYSTEM,
)
from eval.retriever import make_retriever
from eval.score import derive_gold_chunk_ids
from eval.eval_shared import ABSTENTION_PHRASE, is_pure_abstention

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GENERATOR_MODEL = os.getenv("VAES_MODEL", "claude-sonnet-4-6")
RESULTS_DIR = Path("eval/results")
CHUNKS_DIR  = Path("chunks")

DEFAULT_N_PER_SRC = 5
DEFAULT_TOP_K     = 5

# Gate thresholds (pre-registered)
GATE_PASS_PCT  = 5.0
GATE_HARD_STOP_PCT = 15.0

PRIMARY_SRCS = ["S4600", "S4605", "S4610", "S4615", "S4620", "S4680"]

# ---------------------------------------------------------------------------
# Generator (no judge — probe only needs abstention count)
# ---------------------------------------------------------------------------

def _is_anthropic(model: str) -> bool:
    return model.startswith("claude")


def generate_answer(question: str, context: str) -> str:
    user_msg = f"Pregunta: {question}\n\nDocumentos de contexto:\n\n{context}"
    if _is_anthropic(GENERATOR_MODEL):
        from anthropic import Anthropic
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        for attempt in range(3):
            try:
                resp = client.messages.create(
                    model=GENERATOR_MODEL,
                    system=GENERATOR_SYSTEM,
                    messages=[{"role": "user", "content": user_msg}],
                    temperature=0.0,
                    max_tokens=600,
                )
                return resp.content[0].text.strip()
            except Exception as exc:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    return f"[GENERATION ERROR: {exc}]"
    else:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        for attempt in range(3):
            try:
                resp = client.chat.completions.create(
                    model=GENERATOR_MODEL,
                    messages=[
                        {"role": "system", "content": GENERATOR_SYSTEM},
                        {"role": "user",   "content": user_msg},
                    ],
                    temperature=0.0,
                    max_tokens=600,
                )
                return resp.choices[0].message.content.strip()
            except Exception as exc:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    return f"[GENERATION ERROR: {exc}]"


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------

def sample_questions(questions: list[dict], n_per_src: int, target_srcs: set | None) -> list[dict]:
    by_src: dict[str, list] = defaultdict(list)
    for q in questions:
        by_src[q["_src"]].append(q)
    sampled = []
    for src in sorted(by_src):
        if target_srcs and src not in target_srcs:
            continue
        sampled.extend(by_src[src][:n_per_src])
    return sampled


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=DEFAULT_N_PER_SRC,
                        help=f"Questions per SRC (default {DEFAULT_N_PER_SRC})")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--srcs", type=str, default=None,
                        help="Comma-separated SRC filter (default: all)")
    args = parser.parse_args()

    target_srcs = set(args.srcs.split(",")) if args.srcs else None

    print(f"Fase 2 — False-abstention guardrail probe")
    print(f"  Generator  : {GENERATOR_MODEL} (v2 GENERATOR_SYSTEM)")
    print(f"  Sample     : {args.n} per SRC")
    print(f"  Judge      : SKIPPED (probe only counts abstentions)")
    print(f"  Gate pass  : <= {GATE_PASS_PCT}% false abstention")
    print(f"  Gate stop  : >= {GATE_HARD_STOP_PCT}% false abstention")
    print()

    print("Loading chunks...")
    chunks = load_chunks_extended(CHUNKS_DIR)
    print(f"  {len(chunks)} chunks loaded")

    print("Loading retriever...")
    retriever = make_retriever("semantic_long", chunks)

    print("Loading questions...")
    all_questions = load_all_gold_questions()
    questions = sample_questions(all_questions, args.n, target_srcs)
    print(f"  {len(questions)} questions selected ({args.n}/SRC)")
    print()

    results = []
    n_api_calls = 0
    per_src_counts: dict[str, dict] = {}

    for i, q in enumerate(questions, 1):
        src   = q["_src"]
        q_id  = q.get("id", f"{src}-?-{i}")
        q_txt = q["question"]

        print(f"  [{i}/{len(questions)}] {q_id} ({src}) [positive]...", end="", flush=True)

        raw_retrieved   = retriever.retrieve(q_txt, k=args.top_k + 10)
        gold_chunk_ids  = derive_gold_chunk_ids(q, chunks, src)
        top_k_ids       = raw_retrieved[:args.top_k]
        gold_in_top_k   = any(gid in top_k_ids for gid in gold_chunk_ids)

        context  = format_context(top_k_ids, chunks)
        response = generate_answer(q_txt, context)
        n_api_calls += 1

        if response.startswith("[GENERATION ERROR:"):
            state = "error"
        elif response.strip() == ABSTENTION_PHRASE:
            state = "abstained"
        else:
            state = "answered"

        is_false_abs = (state == "abstained") and gold_in_top_k

        results.append({
            "id":              q_id,
            "question":        q_txt,
            "src":             src,
            "state":           state,
            "gold_chunk_ids":  gold_chunk_ids,
            "top_k_ids":       top_k_ids,
            "gold_in_top_k":   gold_in_top_k,
            "response":        response,
            "is_false_abstention": is_false_abs,
        })

        flag = " [FALSE ABS]" if is_false_abs else (" [ERROR]" if state == "error" else "")
        print(f" state={state}{flag}")

        # Accumulate per-src
        entry = per_src_counts.setdefault(src, {"n": 0, "false_abs": 0, "errors": 0, "answered": 0, "abstained": 0})
        entry["n"] += 1
        if state == "error":     entry["errors"] += 1
        if state == "answered":  entry["answered"] += 1
        if state == "abstained": entry["abstained"] += 1
        if is_false_abs:         entry["false_abs"] += 1

    # ── Summary ──────────────────────────────────────────────────────────────
    valid = [r for r in results if r["state"] != "error"]
    n_valid = len(valid)
    n_errors = len(results) - n_valid
    n_false_abs = sum(1 for r in valid if r["is_false_abstention"])
    pct_false_abs = 100 * n_false_abs / n_valid if n_valid else 0.0

    if n_errors:
        print(f"\nWARNING: {n_errors} errors (credit/API failure)")

    print()
    print("=" * 65)
    print("FASE 2 — FALSE-ABSTENTION GUARDRAIL RESULTS")
    print("=" * 65)
    print(f"{'SRC':<8}  {'n':>3}  {'err':>3}  {'answered':>8}  {'abstained':>9}  {'false_abs':>9}")
    print("-" * 65)
    for src in sorted(per_src_counts):
        e = per_src_counts[src]
        print(f"{src:<8}  {e['n']:>3}  {e['errors']:>3}  {e['answered']:>8}  {e['abstained']:>9}  {e['false_abs']:>9}")
    print("-" * 65)
    print(f"{'TOTAL':<8}  {len(results):>3}  {n_errors:>3}  {len([r for r in valid if r['state']=='answered']):>8}  {len([r for r in valid if r['state']=='abstained']):>9}  {n_false_abs:>9}")
    print()
    print(f"False abstention rate : {pct_false_abs:.1f}% ({n_false_abs}/{n_valid} valid questions)")
    print()

    if pct_false_abs <= GATE_PASS_PCT:
        gate = "PASS"
        action = "Proceed to full positive re-gen (v2 prompt safe for positive questions)."
    elif pct_false_abs >= GATE_HARD_STOP_PCT:
        gate = "STOP HARD"
        action = "Abort. v2 prompt causes unacceptable false abstentions. Revert or redesign."
    else:
        gate = "REPORT-AND-STOP"
        action = "Rate between 5-15%: report to user and await decision before full re-gen."

    print(f"Gate result : {gate}")
    print(f"Action      : {action}")

    if n_false_abs > 0:
        print()
        print("False abstentions detail:")
        for r in valid:
            if r["is_false_abstention"]:
                print(f"  [{r['id']}] gold_in_top_k=True, abstained")
                print(f"    Response: {r['response'][:80]}")

    # Save JSON
    RESULTS_DIR.mkdir(exist_ok=True)
    today = date.today().isoformat()
    out_path = RESULTS_DIR / f"phase2_fase2_probe_{today}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at":   today,
            "generator_model": GENERATOR_MODEL,
            "n_per_src":      args.n,
            "n_api_calls":    n_api_calls,
            "n_valid":        n_valid,
            "n_errors":       n_errors,
            "n_false_abstentions": n_false_abs,
            "pct_false_abstention": round(pct_false_abs, 1),
            "gate":           gate,
            "per_src":        per_src_counts,
            "results":        results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved: {out_path}")
    print(f"API calls    : {n_api_calls}")

    sys.exit(0 if gate == "PASS" else 1)


if __name__ == "__main__":
    main()
