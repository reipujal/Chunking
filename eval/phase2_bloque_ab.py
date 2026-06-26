"""
Fase 1 — Bloque A + B: Reclasificación near-miss (coste $0, sin API).

BLOQUE A: Clasificación determinista de near-miss en baseline y v2.
BLOQUE B: S4650 type-a/b desde grounded_fraction ya cacheado.
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.eval_shared import ABSTENTION_PHRASE

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_FULL   = Path("eval/results/faithfulness_full_2026-06-22.json")
BASE_COMPL  = Path("eval/results/faithfulness_abstention_completion_2026-06-23.json")
V2_MERGED   = Path("eval/results/faithfulness_abstention_completion_2026-06-25_merged.json")

T2_BASELINE = {
    "S4600": {"n": 21, "pct_correct": 42.9, "pct_over": 57.1},
    "S4605": {"n": 31, "pct_correct": 38.7, "pct_over": 61.3},
    "S4610": {"n": 26, "pct_correct": 46.2, "pct_over": 53.8},
    "S4615": {"n": 30, "pct_correct": 40.0, "pct_over": 60.0},
    "S4620": {"n": 26, "pct_correct": 53.8, "pct_over": 46.2},
    "S4680": {"n": 25, "pct_correct": 44.0, "pct_over": 56.0},
}
PRIMARY_SRCS = ["S4600", "S4605", "S4610", "S4615", "S4620", "S4680"]

# ---------------------------------------------------------------------------
# Near-miss detection
# ---------------------------------------------------------------------------
def is_near_miss(response: str) -> bool:
    s = response.strip()
    return (ABSTENTION_PHRASE in s) and (s != ABSTENTION_PHRASE)

def is_pure_abstention(response: str) -> bool:
    return response.strip() == ABSTENTION_PHRASE

# ---------------------------------------------------------------------------
# Residuo computation
# ---------------------------------------------------------------------------
def compute_residuo(response: str) -> str:
    # 1. Remove exact phrase (all occurrences)
    text = response.replace(ABSTENTION_PHRASE, "")
    # 2. Remove Fuentes/Sources lines
    lines = text.split("\n")
    lines = [l for l in lines if not re.match(r"^\s*(Fuentes?|Sources?):", l, re.IGNORECASE)]
    # 3. Per-line: strip structural markdown markers
    cleaned = []
    for line in lines:
        line = re.sub(r"^(\s*>\s*)+", "", line)   # blockquote >
        line = re.sub(r"^\s*#{1,6}\s*", "", line)  # headers # ## ###
        line = re.sub(r"^\s*[-*]\s+", "", line)    # unordered list - / *
        line = re.sub(r"^\s*\d+\.\s+", "", line)   # ordered list 1.
        cleaned.append(line)
    text = "\n".join(cleaned)
    # 4. Strip inline emphasis markers ** * __ _
    text = re.sub(r"\*{1,3}", "", text)
    text = re.sub(r"_{1,3}", "", text)
    # 5. Collapse excess blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

# ---------------------------------------------------------------------------
# Deterministic classifier
# ---------------------------------------------------------------------------

# Patterns that indicate the residuo is SAP-substantive (→ COARTADA)
_CLAIM_PATTERNS = [
    # Direct correctness judgment
    r"(?i)(the statement is|la (afirmaci[oó]n|respuesta|declaraci[oó]n) es)\s+(correc|incorrec|verdad|fals|true|false|incorrect|correct)",
    r"(?i)\b(correc|incorrec|verdader|fals)(to|ta|a|o|amente)\b",
    r"(?i)\b(the answer is|la respuesta (correcta )?es|la soluci[oó]n es)\b",
    r"(?i)\b(esto es (correcto|incorrecto|verdadero|falso))\b",
    # System / SAP behavioral claims
    r"(?i)(el sistema|the system)\s+(determina|crea|genera|procesa|usa|utiliza|establece|calcula|verifica)",
    r"(?i)(SAP\s+S/4HANA|S/4HANA)\s+(permite|uses?|requires?|determina)",
    r"(?i)(en cambio|instead|en realidad|actually|lo correcto|the correct (approach|behavior|answer))",
    # Transaction codes (2-4 uppercase letters + digits)
    r"\b[A-Z]{2,4}[0-9]{2,3}[A-Z]?\b",
    # "## Answer" / "## Analysis" with content
    r"(?i)^##\s+(answer|respuesta|analysis|an[aá]lisis)",
    # Specific SAP references with substantive content
    r"(?i)(la regla\s+\w+\s+(para|de)\s+|the rule\s+\w+\s+(for|of)\s+)",
    # Clear answering markers
    r"(?i)(based on the context.{0,60}(the answer|I can confirm|directly addressed|this is|the statement))",
    r"(?i)(el documento de contexto.{0,60}(indica|establece|confirma|muestra|demuestra))",
    r"(?i)(segun.{0,30}documento.{0,40}(es|son|indica|establece))",
]

# Patterns that indicate the residuo is meta-commentary (→ LIMPIO)
_META_PATTERNS = [
    r"(?i)^[\(\[]?(la|el|los|las)\s+(pregunta|contexto|documentos?|informaci[oó]n)",
    r"(?i)^[\(\[]?(the|this)\s+(question|context|document|provided context|information)",
    r"(?i)^(sin embargo|however|aunque|but|adem[aá]s|additionally|note that|nota)",
    r"(?i)(no (se menciona|contiene|incluye|proporciona|especifica|detalla|aborda|cubre|trata))",
    r"(?i)(does not (contain|include|mention|address|provide|specify|discuss))",
    r"(?i)(ninguno de los documentos|none of the (context )?documents)",
    r"(?i)(no (hay|existe|se encuentra|se menciona) (informaci[oó]n|detalle|referencia))",
    r"(?i)(the (provided|given|available) (context|documents?|information) (do(es)? not|doesn't|don't))",
    r"(?i)(the context (documents? )?(do(es)? not|doesn't|don't|only|discusses|covers|addresses))",
    r"(?i)^(i cannot|no puedo|no es posible)\s+(confirm|determine|verify|answer)",
    r"(?i)(la pregunta (hace referencia|trata|menciona|pregunta|habla) (a |sobre |de ))",
    r"(?i)(the question (asks?|refers?|mentions?|is about|discusses?))",
]

def classify_residuo(residuo: str) -> str:
    r = residuo.strip()

    if not r:
        return "LIMPIO"

    # Very short residuo without SAP claims → LIMPIO
    words = r.split()
    if len(words) <= 5 and not any(re.search(p, r) for p in _CLAIM_PATTERNS):
        return "LIMPIO"

    has_claim = any(re.search(p, r, re.MULTILINE) for p in _CLAIM_PATTERNS)
    has_meta  = any(re.search(p, r, re.MULTILINE) for p in _META_PATTERNS)

    if has_claim and not has_meta:
        return "COARTADA"
    if has_claim and has_meta:
        # Both signals: length is tie-breaker
        if len(words) > 40:
            return "COARTADA"
        return "AMBIGUO"
    if has_meta:
        return "LIMPIO"
    # No strong signal: short → LIMPIO, long → AMBIGUO
    if len(words) <= 25:
        return "LIMPIO"
    return "AMBIGUO"

# ---------------------------------------------------------------------------
# Load baseline T2 abstention records (deduped)
# ---------------------------------------------------------------------------
def load_baseline():
    with open(BASE_FULL, encoding="utf-8") as f:
        full = json.load(f)
    with open(BASE_COMPL, encoding="utf-8") as f:
        compl = json.load(f)
    seen, records = set(), []
    for r in full["abstention_results"] + compl["abstention_results"]:
        if r["id"] not in seen:
            seen.add(r["id"])
            records.append(r)
    return records

# ---------------------------------------------------------------------------
# Analyze one set of records
# ---------------------------------------------------------------------------
def analyze_set(records: list[dict]):
    nm_records = []
    for r in records:
        resp = r["response"]
        if is_near_miss(resp):
            residuo = compute_residuo(resp)
            cls = classify_residuo(residuo)
            # Corroboration: judge judgment
            j = r.get("judgment", {})
            judge_is_abs = j.get("is_abstention", None)
            gf = j.get("grounded_fraction", None)
            nm_records.append({
                "id":       r["id"],
                "src":      r["src"],
                "response": resp,
                "residuo":  residuo,
                "cls":      cls,
                "judge_is_abs": judge_is_abs,
                "gf":       gf,
                "gold_in_top_k": r.get("gold_in_top_k"),
            })
    return nm_records

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    baseline_recs = load_baseline()
    with open(V2_MERGED, encoding="utf-8") as f:
        v2_data = json.load(f)
    v2_recs = v2_data["abstention_results"]

    print(f"Loaded: baseline={len(baseline_recs)}, v2={len(v2_recs)}")
    print()

    baseline_nm = analyze_set(baseline_recs)
    v2_nm       = analyze_set(v2_recs)

    # ── A3: Full dump ──────────────────────────────────────────────────────
    sep = "=" * 70

    for label, nm_list in [("BASELINE T2", baseline_nm), ("V2", v2_nm)]:
        print(sep)
        print(f"VOLCADO NEAR-MISS — {label} ({len(nm_list)} registros)")
        print(sep)
        for i, nm in enumerate(nm_list, 1):
            print(f"\n[{i}] {nm['id']} ({nm['src']})  cls={nm['cls']}")
            print(f"     gf={nm['gf']}  judge_is_abs={nm['judge_is_abs']}  gold_in_top_k={nm['gold_in_top_k']}")
            print(f"  RESPONSE:")
            for line in nm["response"].split("\n"):
                print(f"    | {line}")
            print(f"  RESIDUO: {nm['residuo'][:300]!r}")
        print()

    # ── A4: Corroboration ─────────────────────────────────────────────────
    print(sep)
    print("A4 — CORROBORATION judge.is_abstention vs clasificación determinista")
    print(sep)
    for label, nm_list in [("BASELINE T2", baseline_nm), ("V2", v2_nm)]:
        agree = sum(1 for nm in nm_list
                    if (nm["cls"] == "LIMPIO") == bool(nm["judge_is_abs"]))
        disagree = len(nm_list) - agree
        print(f"\n{label} (n={len(nm_list)}):")
        for nm in nm_list:
            det_abs = nm["cls"] == "LIMPIO"
            jdg_abs = bool(nm["judge_is_abs"])
            flag = "" if det_abs == jdg_abs else " *** DISCREPANCIA ***"
            print(f"  {nm['id']}: det={'ABS' if det_abs else 'OVR'}  judge={'ABS' if jdg_abs else 'OVR'}{flag}")
        print(f"  Acuerdo: {agree}/{len(nm_list)}")
    print()

    # ── A1+A2: Counts ─────────────────────────────────────────────────────
    print(sep)
    print("A1+A2 — CONTEO NEAR-MISS POR CLASIFICACION")
    print(sep)
    for label, nm_list in [("BASELINE T2", baseline_nm), ("V2", v2_nm)]:
        from collections import Counter
        cnts = Counter(nm["cls"] for nm in nm_list)
        print(f"{label}: total={len(nm_list)}  LIMPIO={cnts['LIMPIO']}  COARTADA={cnts['COARTADA']}  AMBIGUO={cnts['AMBIGUO']}")
    print()

    # ── A5: Corrected aggregate ───────────────────────────────────────────
    print(sep)
    print("A5 — AGREGADO CORREGIDO SIMETRICO (6 SRCs primarios, n=159)")
    print(sep)

    # Build corrected counts per SRC for v2
    v2_by_src = defaultdict(list)
    for r in v2_recs:
        v2_by_src[r["src"]].append(r)

    # Build corrected counts per SRC for baseline
    base_by_src = defaultdict(list)
    for r in baseline_recs:
        base_by_src[r["src"]].append(r)

    # Build nm classification lookup
    v2_nm_cls   = {nm["id"]: nm["cls"] for nm in v2_nm}
    base_nm_cls = {nm["id"]: nm["cls"] for nm in baseline_nm}

    def corrected_counts(by_src, nm_cls_map, src):
        recs = by_src.get(src, [])
        pure_correct  = sum(1 for r in recs if is_pure_abstention(r["response"]))
        pure_over     = sum(1 for r in recs if not is_pure_abstention(r["response"]) and not is_near_miss(r["response"]))
        nm_limpio     = sum(1 for r in recs if is_near_miss(r["response"]) and nm_cls_map.get(r["id"]) == "LIMPIO")
        nm_coartada   = sum(1 for r in recs if is_near_miss(r["response"]) and nm_cls_map.get(r["id"]) in ("COARTADA", "AMBIGUO"))
        corr_correct  = pure_correct + nm_limpio
        corr_over     = pure_over + nm_coartada
        return {
            "n": len(recs),
            "pure_correct": pure_correct, "pure_over": len(recs) - pure_correct,
            "nm_limpio": nm_limpio, "nm_coartada": nm_coartada,
            "corr_correct": corr_correct, "corr_over": corr_over,
        }

    hdr = f"{'SRC':<8}  {'n':>3}  {'pure_over%':>10}  {'corr_base%':>11}  {'corr_v2%':>9}  {'pure_d':>7}  {'corr_d':>7}"
    print(hdr)
    print("-" * 75)

    agg = {k: 0 for k in ["n", "base_pure_correct", "base_corr_correct",
                            "v2_pure_correct", "v2_corr_correct"]}

    for src in PRIMARY_SRCS:
        base = T2_BASELINE[src]
        base_n = base["n"]
        base_pure_correct = round(base_n * base["pct_correct"] / 100)

        # For baseline corrected: need corrected_counts from baseline records
        bc = corrected_counts(base_by_src, base_nm_cls, src)
        # Baseline pure correct from T2 (pre-registered, use T2_BASELINE)
        # but near-miss correction from actual baseline records
        base_corr_correct = base_pure_correct + bc["nm_limpio"]

        vc = corrected_counts(v2_by_src, v2_nm_cls, src)
        v2_pure_correct  = sum(1 for r in v2_by_src.get(src, []) if is_pure_abstention(r["response"]))
        v2_corr_correct  = v2_pure_correct + vc["nm_limpio"]
        n_v2 = len(v2_by_src.get(src, []))

        pure_over_v2  = 100 * (n_v2 - v2_pure_correct) / n_v2 if n_v2 else 0
        base_pct_over = base["pct_over"]
        corr_base_pct = 100 * (base_n - base_corr_correct) / base_n if base_n else 0
        corr_v2_pct   = 100 * (n_v2 - v2_corr_correct) / n_v2 if n_v2 else 0
        pure_d   = pure_over_v2 - base_pct_over
        corr_d   = corr_v2_pct - corr_base_pct

        print(f"{src:<8}  {base_n:>3}  {pure_over_v2:>9.1f}%  {corr_base_pct:>10.1f}%  {corr_v2_pct:>8.1f}%  {pure_d:>+6.1f}  {corr_d:>+6.1f}")

        agg["n"]                += base_n
        agg["base_pure_correct"] += base_pure_correct
        agg["base_corr_correct"] += base_corr_correct
        agg["v2_pure_correct"]   += v2_pure_correct
        agg["v2_corr_correct"]   += v2_corr_correct

    n_agg = agg["n"]
    pure_over_agg_old  = 100 * (n_agg - agg["base_pure_correct"]) / n_agg
    pure_over_agg_v2   = 100 * (n_agg - agg["v2_pure_correct"])   / n_agg
    corr_over_agg_base = 100 * (n_agg - agg["base_corr_correct"])  / n_agg
    corr_over_agg_v2   = 100 * (n_agg - agg["v2_corr_correct"])    / n_agg
    pure_delta  = pure_over_agg_v2  - pure_over_agg_old
    corr_delta  = corr_over_agg_v2  - corr_over_agg_base

    print("-" * 75)
    print(f"{'TOTAL':<8}  {n_agg:>3}  {pure_over_agg_v2:>9.1f}%  {corr_over_agg_base:>10.1f}%  {corr_over_agg_v2:>8.1f}%  {pure_delta:>+6.1f}  {corr_delta:>+6.1f}")
    print()
    print(f"  pure_over (old baseline)  : {pure_over_agg_old:.1f}%")
    print(f"  pure_over (v2)            : {pure_over_agg_v2:.1f}%")
    print(f"  pure_delta                : {pure_delta:+.1f} pts")
    print(f"  corr_over (baseline)      : {corr_over_agg_base:.1f}%")
    print(f"  corr_over (v2)            : {corr_over_agg_v2:.1f}%")
    print(f"  corrected_delta           : {corr_delta:+.1f} pts")
    gate_pure = "FAIL" if pure_delta > -15.0 else "PASS"
    gate_corr = "FAIL" if corr_delta > -15.0 else "PASS"
    print(f"  gate >=15 pts (pure)      : {gate_pure}")
    print(f"  gate >=15 pts (corrected) : {gate_corr}")

    # ── BLOQUE B: S4650 ───────────────────────────────────────────────────
    print()
    print(sep)
    print("BLOQUE B — S4650 near-miss reclasificacion + type-a/b")
    print(sep)

    s4650_recs = [r for r in v2_recs if r["src"] == "S4650"]
    s4650_nm   = [nm for nm in v2_nm if nm["src"] == "S4650"]
    s4650_nm_cls = {nm["id"]: nm["cls"] for nm in s4650_nm}

    pure_abs  = [r for r in s4650_recs if is_pure_abstention(r["response"])]
    nm_limpio = [r for r in s4650_recs if is_near_miss(r["response"]) and s4650_nm_cls.get(r["id"]) == "LIMPIO"]
    nm_coat   = [r for r in s4650_recs if is_near_miss(r["response"]) and s4650_nm_cls.get(r["id"]) in ("COARTADA", "AMBIGUO")]
    pure_ans  = [r for r in s4650_recs if not is_pure_abstention(r["response"]) and not is_near_miss(r["response"])]
    over_genuine = pure_ans + nm_coat

    print(f"\nS4650 n=14:")
    print(f"  pure_abstained  : {len(pure_abs)}")
    print(f"  near_miss LIMPIO: {len(nm_limpio)}  (reclassify → abstained)")
    print(f"  near_miss COAT  : {len(nm_coat)}  (remains over)")
    print(f"  pure_answered   : {len(pure_ans)}")
    print(f"  over_genuine    : {len(over_genuine)}")
    print()

    # Type-a/b classification
    TYPE_A_GF = 0.5
    print("  Over-genuine records (type-a/b by gf):")
    type_a = []
    type_b = []
    for r in over_genuine:
        gf = r.get("judgment", {}).get("grounded_fraction", None)
        if gf is None:
            gf_val = 0.0
        else:
            gf_val = float(gf)
        typ = "type-a" if gf_val >= TYPE_A_GF else "type-b"
        if typ == "type-a": type_a.append(r)
        else: type_b.append(r)
        print(f"    {r['id']}: gf={gf_val:.3f}  -> {typ}  | {r['response'][:80]!r}")

    n_genuine = len(over_genuine)
    pct_a = 100 * len(type_a) / n_genuine if n_genuine else 0
    pct_b = 100 * len(type_b) / n_genuine if n_genuine else 0
    T3_TYPE_A = 66.7  # T3 baseline

    print()
    print(f"  type-a (gf>=0.5): {len(type_a)}/{n_genuine} = {pct_a:.1f}%  (T3 baseline: {T3_TYPE_A}%)")
    print(f"  type-b (gf<0.5) : {len(type_b)}/{n_genuine} = {pct_b:.1f}%")
    print()
    if n_genuine == 0:
        print("  VEREDICTO: S4650 sin over-response genuino tras reclasificación.")
    elif pct_a >= 50:
        print(f"  VEREDICTO: S4650 sigue type-a-dominante ({pct_a:.1f}% >= 50%).")
        print("  prompt-only FALSADO para distractor-grounded.")
        print("  Lever recomendado: retrieval gating (relevance threshold / score gating).")
        print("  Estado: fuera de scope actual, registrado como Fase-2 del proyecto.")
    else:
        print(f"  VEREDICTO: S4650 viró a type-b ({pct_b:.1f}% type-b). Revisar — inesperado.")

    # ── Cost confirmation ─────────────────────────────────────────────────
    print()
    print(sep)
    print("CONFIRMACION DE COSTE")
    print(sep)
    print("  Bloques A y B: $0.00  |  0 llamadas API")
    print("  Solo lectura de JSON ya cacheados + clasificación determinista.")
    print()

    # ── Decision gate ─────────────────────────────────────────────────────
    print(sep)
    print("GATE FASE 2")
    print(sep)
    print(f"  corrected_delta = {corr_delta:+.1f} pts")
    if corr_delta <= -10.0:
        print("  >= 10 pts mejora corregida → Fase 2 vale la pena (probe false-abstention).")
    else:
        print("  < 10 pts → v2 débil; evaluar si Fase 2 aporta valor antes de lanzarla.")

if __name__ == "__main__":
    main()
