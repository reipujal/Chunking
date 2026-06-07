# Roadmap a RAG profesional — prompts sucesivos para Sonnet

> Estado de partida: piloto SD, 74 chunks markdown, validador + audit + Skill 6 (coverage). Markdown es la **fuente de verdad** durante todo el piloto. Ningún prompt migra fuera de markdown hasta la Fase B.

## Principios de ejecución (aplican a TODOS los prompts)
- **Uno cada vez.** Ejecuta un prompt, commitea su salida, y solo entonces lanza el siguiente. Una sesión por workspace.
- **Pre-vuelo (ROL 0)** al inicio de cada uno: validador 0 errores, disco↔índice sincronizados, sin git lock. Si falla, parar.
- **Ejecución/medición, no decisión.** Donde hay una elección de arquitectura, el prompt **benchmarkea y reporta**; el humano decide con los datos.
- **Escritura atómica** (a `/tmp`, mover, re-leer) — el watcher trunca escrituras in-place.
- **Criterio de "hecho" verificable** al final de cada prompt; sin él, no está cerrado.
- Todo lo nuevo de retrieval/eval vive en una carpeta aparte (p.ej. `rag/`), **read-only sobre `chunks/`**. No tocar los chunks salvo que el prompt lo pida explícitamente.

---

# FASE A — Instrumentar el piloto (sigue en markdown)

## PROMPT A1 — Harness de evaluación de retrieval (la pieza clave)
**Objetivo:** dar señal de recuperación al piloto sin salir de markdown. Read-only sobre `chunks/`.

**Tarea:**
1. Construye un **gold-set de queries** en `rag/eval/gold_queries.jsonl`, cada línea `{query, lang, expected_chunk_ids[], source}`. Dos pools, claramente etiquetados:
   - *derived*: 1-2 por chunk a partir de "Questions This Chunk Answers" (traducidas a query natural).
   - *independent*: ≥30 queries estilo consultor, en **español**, redacción diagnóstica ("por qué no se crea la entrega", "bloqueo de crédito SAP"), escritas SIN mirar el body del chunk, con su(s) chunk(s) esperado(s). **Marca este pool**: es el que cuenta para la métrica honesta (los *derived* son softballs y sobre-estiman recall).
2. Implementa `rag/eval/run_eval.py`: parsea frontmatter+body de todos los chunks, embebe con un modelo **multilingüe local/barato** (p.ej. `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`), indexa en memoria (FAISS o numpy), y para cada query reporta **recall@1/3/5, MRR**, separado por pool y por `area`.
3. Salida: `rag/eval/baseline_<fecha>.md` con métricas + la **lista de queries con recall@5 = 0** (gaps de recuperación reales → alimentan contenido y chunking).

**Hecho:** el script corre end-to-end, reporta métricas separadas derived/independent, y existe el baseline con la lista de fallos. (Decisión humana posterior: ¿qué fallos son contenido faltante vs. chunking mejorable?)

## PROMPT A2 — Cerrar contenido instrumentado (loop por documento)
**Objetivo:** procesar los documentos pendientes prioritarios cerrando gaps medidos.

**Tarea:**
1. Pre-vuelo. Procesa el siguiente documento de mayor prioridad (empezar por **S4600** → credit management, el gap top). Usa el pipeline completo: Skills 1,2 → Steps 3-5 de CLAUDE.md → Skill 5 (validar) → **Skill 6 (coverage gate)**.
2. Tras cerrar el documento, **re-ejecuta A1** y compara: ¿bajó el nº de queries con recall@5=0? ¿el nuevo contenido es recuperable?
3. Registra en el log la entrada del documento + el delta de métricas de eval.

**Hecho:** documento `completed` por Skill 6 (0 errores, cobertura justificada) **y** delta de eval registrado. Repetir este prompt por cada documento pendiente.

## PROMPT A3 — Experimentos de estrategia de retrieval (aún read-only sobre markdown)
**Objetivo:** responder con evidencia si la estrategia de chunking/aliases es óptima (objetivo 1).

**Tarea:** usando A1 como banco de pruebas, ejecuta y reporta A/B sobre el pool *independent*:
1. **Qué embeber:** body vs. body+aliases vs. body+aliases+questions (multi-vector). Métrica por variante.
2. **Híbrido:** denso solo vs. denso + BM25/sparse para tokens exactos (T-codes VF01, tablas KONV/VBRK). Mide recall en queries con T-code.
3. **Filtrado por metadata:** ¿filtrar por `area`/`chunk_type` antes del denso mejora precisión sin perder recall?
4. **Tamaño de chunk:** identifica si los chunks >1200 o <350 palabras rinden peor; reporta correlación tamaño↔recall.

**Salida:** `rag/eval/strategy_experiments_<fecha>.md` con la configuración ganadora y, si procede, **recomendaciones concretas de cambio de chunking** (p.ej. "aliases mejoran recall +12% → reforzar la regla de aliases", o "chunks >1200w pierden recall → bajar el techo a 1000"). Estas recomendaciones se aplican a CLAUDE.md/skills (cierra objetivo 2 con evidencia).

**Hecho:** informe con métricas por variante y recomendaciones accionables. (Decisión humana: qué recomendaciones adoptar.)

---

# FASE B — Salir del piloto y construir el RAG (tras congelar estrategia)

## PROMPT B1 — Congelar estrategia + tier de validación humana
**Objetivo:** detener la deuda retroactiva y separar "draft" de "production-eligible".
**Tarea:** versiona la estrategia de chunking (tag/fecha en CLAUDE.md: "strategy v1 frozen"). Define el workflow de `status`: criterios para promover `draft`→`reviewed`→`validated`, y qué tier alimenta producción. Aplica la promoción a los chunks que un SME haya firmado (gate humano real; hoy los 74 son `draft` sin revisor). Añade al validador un check: solo `validated` es elegible para el índice de producción.
**Hecho:** estrategia congelada y documentada; criterios de promoción en CLAUDE.md; validador distingue tiers.

## PROMPT B2 — Ingesta a vector store de producción (markdown sigue siendo fuente de verdad)
**Objetivo:** índice de producción **derivado** del markdown, regenerable, nunca editado a mano.
**Tarea:** con la config ganadora de A3, construye `rag/ingest.py`: lee chunks `validated`, genera embeddings + metadata, carga en el vector store elegido (benchmarkear pgvector vs Qdrant en coste/latencia/filtros y **reportar** para decisión humana). El índice se regenera desde markdown; cualquier cambio en un chunk lo invalida.
**Hecho:** ingesta reproducible que reconstruye el índice desde cero; smoke test de retrieval pasa.

## PROMPT B3 — Capa de generación + grounding
**Objetivo:** que el sistema **responda**, con trazabilidad y sin alucinar.
**Tarea:** plantilla de generación que (1) cita la **página del PDF** de los chunks usados (la provenance ya está en frontmatter), (2) **rechaza** cuando ningún chunk supera un umbral de score (anti-alucinación), (3) pasa un check de **groundedness** (cada afirmación de la respuesta rastreable a un chunk recuperado). Evalúa faithfulness sobre el pool *independent*.
**Hecho:** dado un set de queries, responde con citas a página, rechaza las no cubiertas, y reporta faithfulness.

## PROMPT B4 — Ops/CI + bucle de observabilidad
**Objetivo:** pipeline profesional, reproducible y auto-mejorable.
**Tarea:** validador como gate de **CI/pre-commit** (no se commitea con errores); entorno de ingesta reproducible; logging de queries en producción y, sobre todo, **log de fallos de recuperación** (queries con recall 0 o respuesta rechazada) que se exporta como **gaps de cobertura** y re-alimenta el pipeline de chunking (cierra el loop objetivo 1↔2).
**Hecho:** CI bloquea corpus inválido; el log de fallos genera automáticamente una worklist de coverage.

---

# Nota para el audit board
Cuando A1 exista, añadir al profile un **ROL de evaluación de retrieval** (recall@k/MRR sobre el pool independent) y elevar la métrica de retrieval a dimensión de scoring. Hoy el audit mide salud de corpus (proxies); falta la dimensión de resultado.
