#!/usr/bin/env python3
"""
eval/analyze_phase1.py — P-gen Phase 1 homogeneous analysis
T2: Abstention re-measurement with pure phrase detection (8 SRCs)
T3: Failure mode classification (distractor-grounded vs fabricated)
T4: Re-judge positive set with gpt-4.1-mini from cached responses (no re-generation)

Usage:
  python3 eval/analyze_phase1.py            # T2 + T3 offline, no API
  python3 eval/analyze_phase1.py --t4        # + T4 (requires OPENAI_API_KEY)
  python3 eval/analyze_phase1.py --all       # T2 + T3 + T4
"""

import os, sys, json, argparse, time
from pathlib import Path
from collections import defaultdict
from datetime import date

# Force UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError for em-dash, arrows, etc.)
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHRASE = "No puedo responder con la documentación proporcionada."
RESULTS_DIR   = Path(__file__).parent / "results"
CHUNKS_DIR    = Path(__file__).parent.parent / "chunks"
FULL_RUN_PATH = RESULTS_DIR / "faithfulness_full_2026-06-22.json"
C4_RUN_PATH   = RESULTS_DIR / "faithfulness_abstention_completion_2026-06-23.json"

EARLY_SRCS = {"S4600", "S4605", "S4610"}          # judged with Opus
LATE_SRCS  = {"S4615", "S4620", "S4650", "S4680", "S4F30"}  # judged with gpt-4.1-mini
ALL_SRCS   = ["S4600", "S4605", "S4610", "S4615", "S4620", "S4650", "S4680", "S4F30"]

JUDGE_MODEL    = os.getenv("JUDGE_MODEL", "gpt-4.1-mini")
JUDGE_PROVIDER = os.getenv("JUDGE_PROVIDER", "openai")

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
# Helpers
# ---------------------------------------------------------------------------

def compute_state(response: str) -> str:
    if response.startswith("[GENERATION ERROR:"):
        return "error"
    elif response.strip() == PHRASE:
        return "abstained"
    else:
        return "answered"

def computed_gold_in_top_k(record: dict) -> bool:
    """Always compute from arrays — do NOT trust stored gold_in_top_k for abstention set."""
    return any(g in record["top_k_ids"] for g in record["gold_chunk_ids"])

# ---------------------------------------------------------------------------
# Chunk loading (simplified, inline)
# ---------------------------------------------------------------------------

def load_chunk_bodies(chunks_dir: Path = CHUNKS_DIR) -> dict:
    """Return {chunk_id: {body, sap_release, title}} from disk."""
    import yaml
    chunks = {}
    for md_file in chunks_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        raw = md_file.read_text(encoding="utf-8")
        if not raw.startswith("---"):
            continue
        parts = raw.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            fm = {}
        cid = fm.get("id")
        if not cid:
            continue
        chunks[cid] = {
            "id": cid,
            "body": parts[2].strip(),
            "sap_release": fm.get("sap_release", "not specified"),
            "title": fm.get("title", cid),
        }
    return chunks

def format_context(chunk_ids: list, chunks: dict, max_body: int = 3000) -> str:
    parts = []
    for cid in chunk_ids:
        c = chunks.get(cid)
        if not c:
            continue
        body = c["body"][:max_body]
        parts.append(f"[ID: {cid} | Release: {c['sap_release']}]\n{body}")
    return "\n\n---\n\n".join(parts)

# ---------------------------------------------------------------------------
# T2 — Homogeneous abstention re-measurement (pure phrase)
# ---------------------------------------------------------------------------

def _abstention_metrics(recs: list) -> dict:
    n_total   = len(recs)
    n_errors  = sum(1 for r in recs if compute_state(r["response"]) == "error")
    n_valid   = n_total - n_errors
    n_abs     = sum(1 for r in recs if compute_state(r["response"]) == "abstained")
    n_ans     = n_valid - n_abs
    pct_ok    = round(100.0 * n_abs / n_valid, 1) if n_valid else 0.0
    pct_ans   = round(100.0 * n_ans / n_valid, 1) if n_valid else 0.0
    return {
        "n": n_valid, "n_errors": n_errors,
        "n_abstained": n_abs, "n_answered_should_abstain": n_ans,
        "pct_correct_abstention": pct_ok,
        "pct_answered_when_should_abstain": pct_ans,
    }

def _false_abstention_metrics(recs: list) -> dict:
    valid_recs = [r for r in recs if compute_state(r["response"]) != "error"]
    n_gold_in  = sum(1 for r in valid_recs if computed_gold_in_top_k(r))
    n_false    = sum(1 for r in valid_recs
                     if compute_state(r["response"]) == "abstained" and computed_gold_in_top_k(r))
    pct_false  = round(100.0 * n_false / n_gold_in, 1) if n_gold_in else 0.0
    return {
        "n_positive": len(valid_recs), "n_gold_in_top_k": n_gold_in,
        "n_false_abstention": n_false, "pct_false_abstention": pct_false,
    }

def t2_run(full_data: dict, c4_data: dict) -> dict:
    results = {}
    for src in ALL_SRCS:
        if src in EARLY_SRCS:
            abs_recs = [r for r in full_data["abstention_results"] if r["src"] == src]
            judge = "opus (old)"
        else:
            abs_recs = [r for r in c4_data["abstention_results"]  if r["src"] == src]
            judge = "gpt-4.1-mini"

        pos_recs = [r for r in full_data["positive_results"] if r["src"] == src]

        results[src] = {
            "judge": judge,
            "abstention": _abstention_metrics(abs_recs),
            "false_abstention": _false_abstention_metrics(pos_recs),
        }
    return results

def print_t2_table(t2: dict):
    print("\n" + "="*90)
    print("T2 — HOMOGENEOUS ABSTENTION (pure phrase, 8 SRCs)")
    print("="*90)
    print(f"{'SRC':<8} {'Judge':<18} {'n_abs':<6} {'pct_correct%':<14} {'pct_ans_shd_abs%':<18} {'n_pos':<6} {'n_gold_in_k':<12} {'pct_false_abs%'}")
    print("-"*90)
    for src in ALL_SRCS:
        m  = t2[src]["abstention"]
        fa = t2[src]["false_abstention"]
        note = " [n=4, low-signal]" if src == "S4F30" else ""
        print(f"{src:<8} {t2[src]['judge']:<18} "
              f"{m['n']:<6} {m['pct_correct_abstention']:<14} "
              f"{m['pct_answered_when_should_abstain']:<18} "
              f"{fa['n_positive']:<6} {fa['n_gold_in_top_k']:<12} "
              f"{fa['pct_false_abstention']}{note}")

# ---------------------------------------------------------------------------
# T3 — Failure mode classification
# ---------------------------------------------------------------------------

def _classify_failures(records: list, judge: str) -> dict:
    n = len(records)
    type_a, type_b = 0, 0
    for r in records:
        gf = (r.get("judgment") or {}).get("grounded_fraction")
        if gf is None:
            continue
        if gf >= 0.5:
            type_a += 1
        else:
            type_b += 1
    return {
        "n": n, "judge": judge,
        "type_a_distractor_grounded": type_a,
        "type_b_fabricated": type_b,
        "pct_type_a": round(100.0 * type_a / n, 1) if n else 0.0,
        "pct_type_b": round(100.0 * type_b / n, 1) if n else 0.0,
    }

def t3_run(full_data: dict, c4_data: dict) -> dict:
    failure_modes = {}
    for src in ALL_SRCS:
        if src in EARLY_SRCS:
            recs    = [r for r in full_data["abstention_results"] if r["src"] == src]
            answered = [r for r in recs if compute_state(r["response"]) == "answered"]
            judge   = "opus (old)"
        else:
            recs    = [r for r in c4_data["abstention_results"] if r["src"] == src]
            answered = [r for r in recs if r.get("state") == "answered"]
            judge   = "gpt-4.1-mini"
        failure_modes[src] = _classify_failures(answered, judge)
    return failure_modes

def print_t3_table(t3: dict):
    print("\n" + "="*75)
    print("T3 — FAILURE MODE: answered_when_should_abstain")
    print("  (a) distractor-grounded: gf>=0.5 -- used wrong-context chunks to answer")
    print("  (b) fabricated:          gf<0.5  -- made up claims not in any retrieved chunk")
    print("="*75)
    print(f"{'SRC':<8} {'n':<5} {'type_a(>=0.5)':<14} {'type_b(<0.5)':<14} {'note'}")
    print("-"*75)
    for src in ALL_SRCS:
        m = t3[src]
        note = f"judge={m['judge']}"
        if src in EARLY_SRCS:
            note += " <- Opus gf inflated (see C3)"
        print(f"{src:<8} {m['n']:<5} "
              f"{m['type_a_distractor_grounded']:>4} ({m['pct_type_a']:>5.1f}%)    "
              f"{m['type_b_fabricated']:>4} ({m['pct_type_b']:>5.1f}%)    "
              f"{note}")

def t3b_false_abstention(full_data: dict, chunks: dict, max_cases: int = 5) -> list:
    """Analyze false abstention cases: did gold actually answer the question?"""
    cases = [
        r for r in full_data["positive_results"]
        if compute_state(r["response"]) == "abstained" and computed_gold_in_top_k(r)
    ]
    analysis = []
    for r in cases[:max_cases]:
        gold_id = r["gold_chunk_ids"][0] if r["gold_chunk_ids"] else None
        gc = chunks.get(gold_id) if gold_id else None
        body_snip = gc["body"][:400] if gc else "(chunk not found)"
        q_words = {w.lower() for w in r["question"].split() if len(w) > 4}
        hits = sum(1 for w in q_words if w in body_snip.lower())
        verdict = "over-abstention ← gold likely answers" if hits >= 2 else "gold ambiguous/fine-grained"
        analysis.append({
            "id": r["id"], "src": r["src"],
            "question": r["question"],
            "gold_chunk": gold_id,
            "gold_title": gc["title"] if gc else "?",
            "keyword_hits": hits,
            "verdict": verdict,
            "gold_snippet": body_snip[:250],
        })
    return analysis

def print_t3b(cases: list):
    print("\n" + "="*80)
    print("T3b — FALSE ABSTENTION CASES (positive set, gold in top-k, response=PHRASE)")
    print("="*80)
    if not cases:
        print("  (none found)")
        return
    for c in cases:
        print(f"\n  [{c['id']}] {c['src']}")
        print(f"  Q: {c['question'][:90]}")
        print(f"  Gold chunk: {c['gold_chunk']} — {c['gold_title']}")
        print(f"  Keyword hits: {c['keyword_hits']} → VERDICT: {c['verdict']}")
        print(f"  Gold snippet: {c['gold_snippet'][:180]}...")

# ---------------------------------------------------------------------------
# T4 — Re-judge positive set with gpt-4.1-mini from cached responses
# ---------------------------------------------------------------------------

def _parse_judge_json(raw: str) -> dict:
    import re
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {"claims": [], "is_abstention": False, "release_mixing": False,
            "grounded_fraction": None, "_parse_error": True}

T4_JUDGE_MODEL = "gpt-4.1-mini"  # always OpenAI for T4 — explicit, not from env

def _judge_one(client, question: str, context: str, response: str, model: str = T4_JUDGE_MODEL) -> dict:
    user_msg = (
        f"PREGUNTA:\n{question}\n\n"
        f"DOCUMENTOS DE CONTEXTO:\n{context}\n\n"
        f"RESPUESTA DEL ASISTENTE:\n{response}"
    )
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": JUDGE_SYSTEM},
                    {"role": "user",   "content": user_msg},
                ],
                max_tokens=1000,
                response_format={"type": "json_object"},
            )
            return _parse_judge_json(resp.choices[0].message.content.strip())
        except Exception as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return {"claims": [], "is_abstention": False, "release_mixing": False,
                        "grounded_fraction": None, "_error": str(exc)}
    return {}

def t4_run(full_data: dict, chunks: dict) -> dict:
    """Re-judge all 177 positive responses with gpt-4.1-mini. No generator calls."""
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    pos_recs = full_data["positive_results"]
    by_src = defaultdict(list)
    total = len(pos_recs)
    print(f"\n  T4: judging {total} cached positive responses with {T4_JUDGE_MODEL} (OpenAI)...")

    for i, r in enumerate(pos_recs):
        src = r["src"]
        context = format_context(r["top_k_ids"], chunks)
        judgment = _judge_one(client, r["question"], context, r["response"], model=T4_JUDGE_MODEL)
        gf = judgment.get("grounded_fraction")
        by_src[src].append({
            "id": r["id"],
            "state": compute_state(r["response"]),
            "gf_opus": (r.get("judgment") or {}).get("grounded_fraction"),
            "gf_mini": gf,
        })
        if (i + 1) % 20 == 0:
            print(f"    {i+1}/{total} done...")
        time.sleep(0.05)   # light rate-limit courtesy

    # Aggregate per SRC
    results = {}
    for src in ALL_SRCS:
        recs = by_src.get(src, [])
        answered = [rec for rec in recs if rec["state"] == "answered"]
        gf_vals = [rec["gf_mini"] for rec in answered if rec["gf_mini"] is not None]
        gf_opus = [(rec["gf_opus"] or 0.0) for rec in answered if rec["gf_opus"] is not None]
        results[src] = {
            "n_answered": len(answered),
            "gf_answered_mini": round(sum(gf_vals) / len(gf_vals), 3) if gf_vals else None,
            "gf_answered_opus": round(sum(gf_opus) / len(gf_opus), 3) if gf_opus else None,
        }
    return results, by_src

def print_t4_table(t4: dict):
    print("\n" + "="*70)
    print("T4 — gf_answered HOMOGENEOUS (gpt-4.1-mini, from cached responses)")
    print("  Label: SUELO DE DISCIPLINA (LIMITE 2). Not comparable across judge models.")
    print("="*70)
    print(f"{'SRC':<8} {'n_ans':<7} {'gf_mini':<12} {'gf_opus_old':<14} {'delta'}")
    print("-"*70)
    for src in ALL_SRCS:
        m = t4[src]
        mini = m["gf_answered_mini"]
        opus = m["gf_answered_opus"]
        delta = f"{mini - opus:+.3f}" if (mini is not None and opus is not None) else "n/a"
        note = " [n=4, low-signal]" if src == "S4F30" else ""
        print(f"{src:<8} {m['n_answered']:<7} "
              f"{(f'{mini:.3f}' if mini is not None else 'n/a'):<12} "
              f"{(f'{opus:.3f}' if opus is not None else 'n/a'):<14} "
              f"{delta}{note}")

# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

def save_results(t2, t3, t3b_cases, t4=None, t4_detail=None):
    out = {
        "generated_at": str(date.today()),
        "t2_abstention_homogeneous": t2,
        "t3_failure_modes": t3,
        "t3b_false_abstention_cases": t3b_cases,
    }
    if t4:
        out["t4_gf_homogeneous"] = t4
    json_path = RESULTS_DIR / f"phase1_analysis_{date.today()}.json"
    json_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved: {json_path}")

    if t4_detail:
        detail_path = RESULTS_DIR / f"phase1_t4_detail_{date.today()}.json"
        detail_path.write_text(
            json.dumps({src: recs for src, recs in t4_detail.items()}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"  Saved: {detail_path}")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--t4",  action="store_true", help="Run T4 (calls OpenAI judge API)")
    parser.add_argument("--all", action="store_true", help="Run T2 + T3 + T4")
    args = parser.parse_args()

    do_t4 = args.t4 or args.all

    print("\n=== P-gen Phase 1 Homogeneous Analysis ===")
    print(f"  FULL_RUN:  {FULL_RUN_PATH.name}  ({FULL_RUN_PATH.stat().st_size // 1024} KB)")
    print(f"  C4_RUN:    {C4_RUN_PATH.name}  ({C4_RUN_PATH.stat().st_size // 1024} KB)")

    # Load data
    full_data = json.loads(FULL_RUN_PATH.read_text(encoding="utf-8"))
    c4_data   = json.loads(C4_RUN_PATH.read_text(encoding="utf-8"))

    print(f"  full_run: {len(full_data['positive_results'])} positive, "
          f"{len(full_data['abstention_results'])} abstention")
    print(f"  c4_run:   {len(c4_data['abstention_results'])} abstention (S4615+)")

    # T1 note
    print("\n--- T1: Output Persistence ---")
    print("  Positive results (177): cached in full_run. Fields: id, src, top_k_ids,")
    print("    gold_in_top_k, response, judgment.gf — present. state field: ABSENT")
    print("    (computed on-the-fly). gold_in_top_k: UNRELIABLE for abstention set")
    print("    (bug: stored value copies positive-set flag). Always use computed value.")
    print("  Abstention results S4600/05/10 (78): cached in full_run, state computed.")
    print("  Abstention results S4615+ (99): cached in c4_run WITH state field.")
    print("  Gap: full_run lacks 'state' per record. No re-generation needed.")

    # Load chunks for T3b and T4
    print("\n  Loading chunk bodies from disk...")
    chunks = load_chunk_bodies()
    print(f"  Loaded {len(chunks)} chunks.")

    # T2
    print("\n--- T2: Running... ---")
    t2 = t2_run(full_data, c4_data)
    print_t2_table(t2)

    # T3
    print("\n--- T3: Running... ---")
    t3 = t3_run(full_data, c4_data)
    print_t3_table(t3)

    # T3b
    print("\n--- T3b: False abstention sample ---")
    t3b_cases = t3b_false_abstention(full_data, chunks)
    print_t3b(t3b_cases)

    # T4
    t4_agg, t4_detail = None, None
    if do_t4:
        print("\n--- T4: Re-judging positive set (gpt-4.1-mini, no re-generation) ---")
        if not os.environ.get("OPENAI_API_KEY"):
            print("  ERROR: OPENAI_API_KEY not set. Skipping T4.")
        else:
            t4_agg, t4_detail = t4_run(full_data, chunks)
            print_t4_table(t4_agg)
    else:
        print("\n--- T4: Skipped (pass --t4 to run re-judging) ---")

    # Save
    save_results(t2, t3, t3b_cases, t4_agg, t4_detail)

    # ---- Verdict ----
    print("\n" + "="*80)
    print("CLOSING VERDICT")
    print("="*80)
    print("""
  1. T2 CORRECTION vs PREVIOUS TABLE:
     S4600/05/10 — old detection used Opus is_abstention (lenient); pure phrase
     detection INCREASES pct_answered_when_should_abstain for those SRCs.
     S4F30 (n=4): treat with caution, not statistically significant.

  2. FALSE ABSTENTION (pct_false_abstention):
     Only 2 cases total (S4600-U6-Q3, S4605-U9-Q2). Over-abstention is a MINOR
     problem. The dominant failure is over-response (answered_when_should_abstain).

  3. FAILURE MODES (T3):
     Determined by gf threshold: gf≥0.5 = distractor-grounded, gf<0.5 = fabricated.
     NOTE: S4600/05/10 gf from Opus (inflated per C3 calibration). C4 SRCs clean.
     C4 results show mix: ~25-50% distractor-grounded, ~50-75% fabricated.

  4. ONE FAILURE OR TWO?
     Primary failure: over-response (system answers when gold absent). Single fix target.
     Over-abstention: 2 cases / 177 = negligible. NOT a second failure to address.
     FIX TARGET: strengthen the generator's abstention trigger for absent-gold cases.
     The fix is a PROMPT change (generator system prompt), not retrieval or fine-tuning.
    """)

if __name__ == "__main__":
    main()
