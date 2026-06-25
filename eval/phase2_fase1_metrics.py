"""
Fase 1 — Metrics computation (judge-free where possible).

Reads the new run output and computes:
- over-response per SRC + delta vs T2 baseline
- aggregate primary (6 SRCs)
- near-miss count pre vs post (ABSTENTION_PHRASE as substring but != exact)
- S4650 separate
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.eval_shared import ABSTENTION_PHRASE, is_pure_abstention

# T2 baseline (validated, pre-registered)
T2_BASELINE = {
    "S4600": {"n": 21, "pct_correct": 42.9, "pct_over": 57.1},
    "S4605": {"n": 31, "pct_correct": 38.7, "pct_over": 61.3},
    "S4610": {"n": 26, "pct_correct": 46.2, "pct_over": 53.8},
    "S4615": {"n": 30, "pct_correct": 40.0, "pct_over": 60.0},
    "S4620": {"n": 26, "pct_correct": 53.8, "pct_over": 46.2},
    "S4650": {"n": 14, "pct_correct": 35.7, "pct_over": 64.3},
    "S4680": {"n": 25, "pct_correct": 44.0, "pct_over": 56.0},
    "S4F30": {"n":  4, "pct_correct": 75.0, "pct_over": 25.0},
}
PRIMARY_SRCS = ["S4600", "S4605", "S4610", "S4615", "S4620", "S4680"]

# Old cache for near-miss pre-count
OLD_FULL  = Path("eval/results/faithfulness_full_2026-06-22.json")
OLD_COMPL = Path("eval/results/faithfulness_abstention_completion_2026-06-23.json")
NEW_RUN   = Path("eval/results/faithfulness_abstention_completion_2026-06-25.json")


def load_old_abstention():
    with open(OLD_FULL, encoding="utf-8") as f:
        full = json.load(f)
    with open(OLD_COMPL, encoding="utf-8") as f:
        compl = json.load(f)
    seen, records = set(), []
    for r in full["abstention_results"] + compl["abstention_results"]:
        if r["id"] not in seen:
            seen.add(r["id"])
            records.append(r)
    return records


def near_miss(response: str) -> bool:
    """Response contains ABSTENTION_PHRASE as substring but is not exact match."""
    stripped = response.strip()
    return (ABSTENTION_PHRASE in stripped) and (stripped != ABSTENTION_PHRASE)


def compute_metrics(records):
    by_src = {}
    for r in records:
        by_src.setdefault(r["src"], []).append(r)
    return by_src


def main(new_path: Path = NEW_RUN):
    if not new_path.exists():
        print(f"ERROR: {new_path} not found. Run faithfulness.py first.")
        sys.exit(1)

    with open(new_path, encoding="utf-8") as f:
        new_data = json.load(f)

    all_records_raw = new_data["abstention_results"]
    new_records = [r for r in all_records_raw if r.get("state") != "error"]
    n_errors_total = len(all_records_raw) - len(new_records)
    if n_errors_total:
        print(f"WARNING: {n_errors_total} error records excluded from all metrics (credit exhaustion).\n")
    old_records = load_old_abstention()

    all_by_src_raw = compute_metrics(all_records_raw)   # includes errors
    new_by_src = compute_metrics(new_records)
    # SRCs with zero errors in the raw run output
    complete_srcs_set = {
        src for src, recs in all_by_src_raw.items()
        if not any(r.get("state") == "error" for r in recs)
    }

    print("=" * 70)
    print("FASE 1 — OVER-RESPONSE PER SRC (judge-free, pure phrase only)")
    print("=" * 70)
    print(f"{'SRC':<8} {'n':>4}  {'old%':>6} {'new%':>6}  {'delta':>6}  {'direction'}")
    print("-" * 70)

    primary_old_correct = 0
    primary_new_correct = 0
    primary_n = 0

    for src in ["S4600", "S4605", "S4610", "S4615", "S4620", "S4650", "S4680", "S4F30"]:
        all_recs_raw = all_by_src_raw.get(src, [])
        new_recs = [r for r in all_recs_raw if r.get("state") != "error"]
        n_errors = len(all_recs_raw) - len(new_recs)
        n = len(new_recs)
        if len(all_recs_raw) == 0:
            print(f"{src:<8} {'—':>4}  {'—':>6} {'—':>6}  {'—':>6}")
            continue
        if n_errors > 0 and n == 0:
            print(f"{src:<8} {'ERR':>4}  {'—':>6} {'—':>6}  {'—':>6}  [ALL {n_errors} ERRORS — rerun needed]")
            continue
        if n_errors > 0:
            n_total = len(all_recs_raw)
            print(f"{src:<8} {'ERR':>4}  {'—':>6} {'—':>6}  {'—':>6}  [{n}/{n_total} valid — rerun needed]")
            continue

        new_correct  = sum(1 for r in new_recs if is_pure_abstention(r))
        new_over     = n - new_correct
        new_pct_over = 100 * new_over / n

        base = T2_BASELINE.get(src, {})
        old_pct_over = base.get("pct_over", 0)
        delta = new_pct_over - old_pct_over
        direction = "BETTER" if delta < -1 else ("WORSE" if delta > 1 else "FLAT")

        tag = " [PRIMARY]" if src in PRIMARY_SRCS else (" [OUTLIER]" if src == "S4650" else " [low-n]")
        print(f"{src:<8} {n:>4}  {old_pct_over:>5.1f}% {new_pct_over:>5.1f}%  {delta:>+6.1f}  {direction}{tag}")

        # Only include complete SRCs in primary aggregate (no errors)
        if src in PRIMARY_SRCS and n_errors == 0:
            primary_old_correct += round(base["n"] * base["pct_correct"] / 100)
            primary_new_correct += new_correct
            primary_n += n

    print("-" * 70)
    primary_old_over = primary_n - primary_old_correct
    primary_new_over = primary_n - primary_new_correct
    old_agg = 100 * primary_old_over / primary_n if primary_n else 0
    new_agg = 100 * primary_new_over / primary_n if primary_n else 0
    agg_delta = new_agg - old_agg
    passes_gate = agg_delta <= -15.0
    # Count which PRIMARY SRCs contributed (complete = zero errors in raw output)
    complete_primary = [src for src in PRIMARY_SRCS if src in complete_srcs_set]
    incomplete_primary = [s for s in PRIMARY_SRCS if s not in complete_primary]
    gate_label = "NOT EVALUABLE — incomplete data" if incomplete_primary else ("PASS" if passes_gate else "FAIL")
    print(f"\nAGREGADO PRIMARIO ({len(complete_primary)}/{len(PRIMARY_SRCS)} SRCs completos, n={primary_n})")
    if incomplete_primary:
        print(f"  PENDIENTE (rerun): {', '.join(incomplete_primary)}")
    print(f"  old over-response : {old_agg:.1f}%")
    print(f"  new over-response : {new_agg:.1f}%")
    print(f"  delta             : {agg_delta:+.1f} pts")
    print(f"  gate >=15 pts     : {gate_label}")

    # Near-miss analysis — compare only over SRCs complete in new run
    print("\n" + "=" * 70)
    print("NEAR-MISS (contains phrase as substring but != exact)")
    print("=" * 70)
    old_cmp = [r for r in old_records if r["src"] in complete_srcs_set]
    new_cmp = [r for r in new_records if r["src"] in complete_srcs_set]
    old_nm = sum(1 for r in old_cmp if near_miss(r["response"]))
    new_nm = sum(1 for r in new_cmp if near_miss(r["response"]))
    print(f"  scope    : SRCs {sorted(complete_srcs_set)} (complete data only)")
    print(f"  pre  (v1): {old_nm} / {len(old_cmp)} ({100*old_nm/len(old_cmp):.1f}%)" if old_cmp else "  pre  (v1): —")
    print(f"  post (v2): {new_nm} / {len(new_cmp)} ({100*new_nm/len(new_cmp):.1f}%)" if new_cmp else "  post (v2): —")
    if new_nm > old_nm:
        print(f"  WARNING: near-miss inflated by {new_nm - old_nm} — model reaches for phrase but violates 'y nada mas'")
    else:
        print(f"  OK: near-miss not inflated")

    # Cost
    print("\n" + "=" * 70)
    print("COST")
    print("=" * 70)
    print(f"  approx_cost_usd : ${new_data.get('approx_cost_usd', '?')}")
    print(f"  n_api_calls     : {new_data.get('n_api_calls', '?')}")

    print("\n" + "=" * 70)
    print("S4650 NOTE (outlier, not gated)")
    print("=" * 70)
    s4650 = new_by_src.get("S4650", [])
    if s4650:
        c = sum(1 for r in s4650 if is_pure_abstention(r))
        pct_over = 100 * (len(s4650) - c) / len(s4650)
        delta_s4650 = pct_over - T2_BASELINE["S4650"]["pct_over"]
        print(f"  n={len(s4650)}, new over-response={pct_over:.1f}%, delta={delta_s4650:+.1f} pts")
        print(f"  (Fase 3 type-a/b breakdown requires judge output — see JSON)")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else NEW_RUN
    main(path)
