# v16 — Cierre de línea over-response / abstención

**Fecha:** 2026-06-26
**Estado:** CERRADA (parked)

---

## Estado y motivo del cierre

La línea de trabajo de over-response/abstención queda aparcada. El motivo no es fracaso del experimento —el experimento fue correcto— sino que el eje de medición estaba mal orientado respecto al objetivo real del proyecto: un asistente de redacción de Valoraciones de Análisis de Elementos de Servicio (VAES). Para ese caso de uso, la abstención no es un fallo a suprimir: es la función que distingue lo que el corpus cubre de lo que el consultor debe aportar. Perseguir over-response como métrica de éxito perseguía el objetivo equivocado.

---

## Hallazgo final auditado (gate simétrico)

La auditoría completa incluyó los near-misses del baseline para los seis SRCs primarios (n=159). Los 17 near-misses de baseline de S4615/S4620/S4680 (del fichero `faithfulness_abstention_completion_2026-06-23.json`) fueron clasificados con el mismo criterio manual aplicado a v2 en Prompt 6: meta-commentary de abstención → LIMPIO; claim-respuesta sustantivo → COARTADA. Resultado: 16 LIMPIO, 1 COARTADA (`S4680-LA-U2-Q11`, gf=0.667, afirmación de billing type IV + shared pricing procedure logic).

### Tabla delta final — baseline simétrico (n=159)

| SRC | n | base_A | base_B | v2_A | v2_B | Δ_A | Δ_B |
|---|---|---|---|---|---|---|---|
| S4600 | 21 | 57.1% | 47.6% | 47.6% | 42.9% | −9.5pp | −4.8pp |
| S4605 | 31 | 61.3% | 38.7% | 54.8% | 22.6% | −6.5pp | −16.1pp |
| S4610 | 26 | 53.8% | 42.3% | 50.0% | 38.5% | −3.8pp | −3.8pp |
| S4615 | 30 | 60.0% | 46.7% | 56.7% | 26.7% | −3.3pp | −20.0pp |
| S4620 | 26 | 46.2% | 26.9% | 38.5% | 26.9% | −7.7pp | **+0.0pp** |
| S4680 | 25 | 56.0% | 28.0% | 44.0% | 16.0% | −12.0pp | −12.0pp |
| **AGG** | **159** | **56.0%** | **38.4%** | **49.1%** | **28.3%** | **−6.9pp** | **−10.1pp** |

```
Gate: delta_B_agg = −10.1pp  |  umbral = −15pp  →  FAIL  (gap = 4.9pp)
```

**S4620:** delta_B = 0.0pp. El modelo ya operaba al mismo nivel de decisión de abstención en T2; v2 cambió la forma de las respuestas (near-miss: 5→3) pero no la decisión (pure_ans = 7 en ambos runs). No hay mejora en over_B.

**Por qué el PASS de Prompt 6 era un artefacto:** el resultado previo (−20.1pp) comparó v2 auditado simétricamente contra un baseline sin auditar, donde `base_B = base_A` para S4615/S4620/S4680 (proxy conservador por ausencia aparente de datos T2 crudos). Al auditar el baseline correcto (`compl_2026-06-23`), esos tres SRCs tenían 17 near-misses LIMPIO que inflaban artificialmente el numerador de base_B. La corrección reduce `base_B_agg` de 48.4% a 38.4% (−10pp), encogiendo el delta aparente.

**Lección:** nunca medir la mejora de una métrica contra un baseline no auditado con el mismo criterio. La asimetría en la auditoría produce un delta ilusorio.

---

## Reencuadre: "un solo fallo" → tres fallos distintos con levers distintos

El over-response original (Phase 1: ~57% SRCs primarios) no era un único problema. Era la suma de tres componentes con levers independientes:

### 1. Fallo de decisión — ¿debe abstenerse?
- **Qué es:** el modelo responde cuando debería abstenerse (pure_ans indeseado).
- **Lever:** prompt (GENERATOR_SYSTEM v2).
- **Resultado medido:** débil. Delta_B simétrico = −10.1pp, sin alcanzar el umbral de −15pp. S4620 nulo. El prompt mueve la decisión en algunos SRCs (S4615: −20pp; S4605: −16pp) pero en conjunto no alcanza el gate.
- **Conclusión:** el lever de prompt para la decisión de abstención está cerca de su límite para este corpus. Mejoras adicionales requerirían cambios estructurales (retrieval, contexto, instrucción de rol).

### 2. Fallo de formato — near-miss (abstiene pero habla de más)
- **Qué es:** el modelo incluye la `ABSTENTION_PHRASE` pero la rodea de texto (meta-commentary, preámbulo de descarte). Clasificado como LIMPIO tras auditoría: es abstención de decisión con formato incorrecto.
- **Lever:** canonicalización determinista (`if ABSTENTION_PHRASE in response → output = ABSTENTION_PHRASE`), $0, sin regeneración.
- **Magnitud:** 33 near-miss-LIMPIO / 159 = 20.8pp de over_A en v2. Toda la brecha A−B es este fallo.
- **Estado:** NO hecho (ver deuda opcional abajo).

### 3. Fallo de fabricación — S4650 residual
- **Qué es:** el modelo responde con content no grounded en los chunks (gf < 0.5), sin base en el corpus.
- **Lever:** retrieval gating (reranking, filtrado de relevancia). Fuera de scope del experimento.
- **Resultado en S4650:** v2 redujo drásticamente los fallos type-a (distractor-grounded: 6→2, −67% absoluto); el residual vira a fabricación pura (type-b: 33.3%→66.7%). El prompt sí movió la composición, pero el residual de fabricación es inaccesible desde el prompt.
- **Estado:** parked junto con la línea.

---

## Activos vs andamiaje

### Reutilizable (no tocar, no borrar)
- **Corpus SD:** 95 chunks, content-hash estable, `chunks/`
- **Gold set de abstención:** preguntas fuera-de-scope por SRC, base para cualquier eval futura
- **Chunking pipeline:** clasificador, extractor, validador, log `chunks/_processing_log.md`
- **Retrieval + caché content-hash:** funcional, invalidación correcta (commit bb0a249, cerrado)
- **Scripts de eval:** `eval/phase2_bloque_ab.py` (compute_residuo fix), `eval/results/` (JSONs cacheados)

### Jubilado como headline
- **Harness de faithfulness (`eval/`):** útil para diagnóstico pero no como métrica de éxito del producto
- **Protocolo de frase-exacta:** demasiado frágil como contrato (near-miss inevitable con modelos generativos); si se retoma, canonicalizar en postproceso
- **over-response / grounded_fraction como KPI principal:** válido para caracterizar el corpus, no para guiar el desarrollo del producto

**Reubicación conceptual de la abstención:** pasa de "fallo a suprimir" a "función deseada". El sistema que abstiene cuando no sabe responde exactamente lo que un asistente de VAES debe hacer: delimitar lo que el estándar cubre y señalar lo que el consultor debe elicitar. La métrica de éxito futura no es "cuántas veces responde bien" sino "cuántas preguntas útiles genera para completar la VAE".

---

## Deuda opcional anotada (NO ejecutar ahora)

**Canonicalización determinista:** implementar postproceso `if ABSTENTION_PHRASE in response → output = ABSTENTION_PHRASE` en el pipeline de generación. Cerraría ~20.8pp del "fallo de formato" visible en over_A (33 near-miss-LIMPIO / 159) a coste $0, sin regeneración, sin cambios en retrieval ni chunks. No requiere nueva eval: el impacto es calculable analíticamente desde los JSONs cacheados.

Queda anotada aquí. No se hace en esta sesión. Si se retoma la línea, este es el primer paso de bajo riesgo.

---

## Pivote — siguiente línea de trabajo

El documento de objetivo VAES (`docs/context/`, a añadir por el usuario) definirá el rol de la capa 1 RAG. En ese marco:

- **Capa 1 (RAG de SD):** su función es recuperar lo que el estándar dice. Su éxito se mide por la calidad de las preguntas de elicitación que genera para completar una VAE, no por faithfulness.
- **Validación de la hipótesis:** un pilot de $0 con juicio humano (¿esta pregunta es útil para completar la VAE?) es el siguiente paso, no construir métricas automáticas.
- **No construir antes de validar:** el harness de eval se retoma solo si el pilot confirma la hipótesis y se necesita escalar el juicio humano.

---

## Caché content-hash

Resuelta en commit `bb0a249`. Invalidación correcta al cambiar contenido de chunk. Cerrada.

---

*Archivos de referencia:*
- `eval/results/faithfulness_abstention_completion_2026-06-23.json` — baseline T2 definitivo
- `eval/results/faithfulness_abstention_completion_2026-06-25_merged.json` — v2 completo (177 registros)
- `eval/phase2_bloque_ab.py` — compute_residuo fix + auditoría near-miss
- `eval/results/phase1_analysis_2026-06-23.json` — métricas Phase 1 (fuente T2_BASELINE)
