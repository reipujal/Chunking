# Audit Board Profile — SAP SD Knowledge Base (Chunking)

> **Profile versión:** 1.0 — 2026-06-07
> **Framework:** `~/.claude/skills/audit-board/FRAMEWORK.md`
> **Para ejecutar:** invocar `/audit-board docs/audit/audit_board_profile.md`
> **Contexto compartido:** `docs/audit/audit_context_shared.md` (leer antes de cualquier rol)

---

## CONTEXTO OBLIGATORIO

Leer `docs/audit/audit_context_shared.md` antes de comenzar cualquier rol.
Contiene el estado actual del corpus, statistics, y hallazgos conocidos previos.

---

## REGLAS ADICIONALES DEL PROYECTO

> Añadir al final de las REGLAS ABSOLUTAS del framework cuando se ejecute este profile:

**REGLA 8 (Chunking):** Toda crítica debe ser categorizada por impacto RAG: ¿afecta al
retrieval (qué se encuentra), a la fidelidad (qué dice cuando se encuentra), o a la
cobertura (qué no se puede encontrar)? Un error de fidelidad en un chunk popular es más
grave que un chunk faltante en un área de baja demanda.

**REGLA 9 (Chunking):** Toda afirmación sobre el corpus debe basarse en evidencia directa
(leer archivos, ejecutar el validador, grep). Las afirmaciones generales sin referencia a
archivos específicos valen cero.

---

## CONTEXT BUNDLES POR CLUSTER

| Cluster | Archivos a leer |
|---------|----------------|
| `C1_fuente` | `docs/audit/audit_context_shared.md`, `chunks/_processing_log.md`, `docs/skills/1-classify.md`, `docs/skills/2-extract.md` + 4 chunks de S4605 (muestra) |
| `C2_contenido` | `docs/audit/audit_context_shared.md`, `chunks/_index.md`, CLAUDE.md §Step 3 y §Step 5 + 6 chunks representativos (2 por fuente) |
| `C3_rag` | `docs/audit/audit_context_shared.md`, `chunks/_index.md`, `validate_chunks.py` + 8 chunks de distintas áreas |
| `C4_schema` | `docs/audit/audit_context_shared.md`, `validate_chunks.py`, `CLAUDE.md` §Step 5 completo + output de `python3 validate_chunks.py` |
| `C5_gov` | `docs/audit/audit_context_shared.md`, `CLAUDE.md`, `chunks/_index.md`, `chunks/_processing_log.md` |

---

## CLUSTERS — ASIGNACIÓN DE ROLES (FASE 1)

| Cluster | Roles asignados | Output |
|---------|----------------|--------|
| `C1_fuente` | ROL 1, ROL 3 | `docs/audit/results/audit_FECHA_part_fuente.md` |
| `C2_contenido` | ROL 2, ROL 7 | `docs/audit/results/audit_FECHA_part_contenido.md` |
| `C3_rag` | ROL 4, ROL 5 | `docs/audit/results/audit_FECHA_part_rag.md` |
| `C4_schema` | ROL 6, ROL 8, ROL 9 | `docs/audit/results/audit_FECHA_part_schema.md` |
| `C5_gov` | ROL 10, ROL 11, ROL 12 | `docs/audit/results/audit_FECHA_part_gov.md` |

---

## TIERS PARA ESTE PROYECTO

| Tier | Roles incluidos | Trigger |
|------|----------------|---------|
| Quick | ROL 2, ROL 4, ROL 6, ROL 10 | Tras cada documento procesado |
| Standard | ROL 1, ROL 2, ROL 4, ROL 5, ROL 6, ROL 7, ROL 9, ROL 10 | Tras ≥3 documentos nuevos o mensual |
| Full | ROL 1–12 + debates + síntesis | Trimestral o antes de integrar en RAG de producción |

### ROL 1 — Source Extraction Quality Specialist
### ROL 2 — SAP SD Domain Expert / Functional Consultant
### ROL 3 — Provenance & Attribution Specialist
### ROL 4 — RAG Systems Specialist
### ROL 5 — Knowledge Graph & Navigation Specialist
### ROL 6 — Schema Compliance & Quality Calibration Auditor
### ROL 7 — Cross-Chunk Consistency Analyst
### ROL 8 — Process & Instructions Adherence Auditor
### ROL 9 — Token Efficiency Specialist
### ROL 10 — Coverage & Strategic Gap Analyst
### ROL 11 — LLM Processing Bias Analyst
### ROL 12 — Project Manager / RAG Readiness Assessor

---

## ROLES — FASE 1

========================================
### FASE 1A — FUENTE Y EXTRACCIÓN
========================================

### ROL 1 — Source Extraction Quality Specialist

**Objetivo:** Auditar la calidad de la extracción de texto de PDF, la completitud del contenido
extraído, la correcta detección del offset de páginas, y el uso de rasterización cuando es necesario.

**Mentalidad:** Sin texto extraído correctamente, todo lo que está downstream es ficción con
buena presentación. La densidad del chunk vs. la densidad del PDF es el único test objetivo.

**Preguntas específicas del proyecto:**
- Para una muestra de 5 chunks de S4605, ejecutar `pdftotext -f [start] -l [end] "docu sap/processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf" - | wc -w` y comparar con las palabras del chunk body. ¿Hay chunks donde la extracción fue < 60% del texto disponible?
- ¿El processing log documenta para cada documento: el offset físico/impreso, la cobertura de back matter (apéndice de T-codes), y un resumen de pages con contenido diagram-only?
- S4610 y S4615 fueron procesados por Claude; S4605 por Codex. ¿La densidad media (w/p) es sistemáticamente diferente entre ambos grupos? Calcular medias separadas.
- ¿Hay chunks de S4605 donde la densidad es < 80 w/p pero el quality es medium (aceptable) sin evidencia de que se rasterizó para confirmar que son páginas de solo diagramas?
- ¿Los sources[].pages de todos los chunks son páginas físicas del PDF (no etiquetas impresas)? Verificar 5 chunks comprobando que la página física corresponde al contenido esperado.

---

### ROL 3 — Provenance & Attribution Specialist

**Objetivo:** Verificar que todo contenido del chunk body tiene respaldo en el source text, y que
los campos `transactions` y `tables` solo contienen tokens que aparecen literalmente en el PDF.

**Mentalidad:** Cada token que se inventa es una alucinación esperando a ocurrir. El
campo `transactions: []` vacío es CORRECTO para el material conceptual S4605 — no es un defecto.

**Preguntas específicas del proyecto:**
- Para 5 chunks con `transactions` no vacíos: ejecutar `pdftotext -f [start] -l [end] [pdf] - | grep -i "[TCODE]"` para cada T-code listado. ¿Aparece literalmente en el extracted text?
- Buscar con `grep -rn "typically\|generally\|usually\|approximately\|often" chunks/ --include="*.md"` en el body text. Cada hit es sospechoso de afirmación inventada — verificar si tiene respaldo en el source.
- ¿Los aliases en español tienen equivalentes conceptuales en el body en inglés? Un alias en español que describe algo no mencionado en el body introduce falsos positivos RAG.
- Verificar coherencia de `relative_path` para todos los chunks: PDFs en `docu sap/processed/` → `relative_path: "processed/filename.pdf"`. Ejecutar: `grep -rn "relative_path:" chunks/ --include="*.md" | grep -v "processed/"` — cualquier hit es potencialmente incorrecto.
- Para 5 chunks, verificar que las páginas citadas en `sources[].pages` corresponden a la sección real del documento (TOC vs. páginas físicas del range).

---

========================================
### FASE 1B — CONTENIDO Y FIDELIDAD
========================================

### ROL 2 — SAP SD Domain Expert / Functional Consultant

**Objetivo:** Evaluar si el contenido de los chunks es factualmente correcto y suficientemente
completo para responder preguntas reales de un consultor SAP SD funcional.

**Mentalidad:** Soy el usuario final de este RAG. Si busco "pricing procedure" y no encuentro nada,
el sistema ha fallado. Si encuentro algo factualmente incorrecto, es peor que no encontrar nada.
Mi estándar de comparación es la experiencia de implementar SD en un proyecto real, no la teoría.

**Preguntas específicas del proyecto:**
- **Cash sales document types:** El corpus tiene dos chunks sobre cash sales (special-processes). ¿Usan los mismos tipos de documento (order type CS, delivery type BV, billing type BV)? ¿O hay discrepancias entre fuentes S4605 y S4615?
- **Pricing procedure gap:** El término "pricing procedure" aparece referenciado en al menos 6 chunks pero no tiene chunk propio. ¿Qué información esencial aporta CADA uno de esos chunks sobre pricing procedure? ¿Se puede inferir el concepto sin un chunk dedicado?
- **"Questions This Chunk Answers" test:** Para los chunks `configuration-sales-document-type-control-001`, `master-data-sd-partner-functions-001`, y `order-management-value-contracts-001`, verificar que cada pregunta listada tiene respuesta explícita en el body.
- **Credit management gap:** El área `credit-management/` tiene 0 chunks. ¿En cuántos chunks del corpus se menciona "credit management", "credit limit", "credit check", o "VKM1"? ¿Qué nivel de cobertura implícita existe?
- **Factual accuracy spot-check:** Para 3 procesos (rush order, consignment issue KE, incompletion check), verificar que los document types y transaction codes mencionados son correctos según SAP estándar.

---

### ROL 7 — Cross-Chunk Consistency Analyst

**Objetivo:** Detectar contradicciones factúales, redundancias, y definiciones inconsistentes
entre chunks del mismo corpus.

**Mentalidad:** Dos chunks que se contradicen son peores que un solo chunk incompleto. Una contradicción
destruye la confianza del usuario en TODO el corpus, no solo en los chunks implicados.

**Preguntas específicas del proyecto:**
- **Cash sales conflict check:** Ejecutar `grep -rn "billing type\|billing document type\|CS\|BV" chunks/special-processes/ --include="*.md"`. ¿Los dos chunks de cash sale describen el billing type de forma consistente?
- **Partner function descriptions:** El concepto "partner function" aparece en `master-data-sd-partner-functions-001` y probablemente en otros chunks. ¿Son compatibles las definiciones de sold-to party, ship-to party, payer, bill-to party entre chunks?
- **Delivery type references:** Buscar mentions de LF, BV, DF (delivery types) across chunks. ¿Se asignan consistentemente al proceso correcto?
- **Process step ordering:** Para el proceso order-to-cash, ¿los cross-refs de "prior step/next step" forman una secuencia coherente sin contradicciones de orden?
- **Version mismatch detection:** ¿Hay chunks de S4605 que describen el mismo proceso que chunks de S4615 con diferencias no documentadas como `## Differences from [version]`?

---

========================================
### FASE 1C — CALIDAD RAG
========================================

### ROL 4 — RAG Systems Specialist

**Objetivo:** Evaluar si el corpus es efectivamente recuperable por un sistema de vector search
para las queries reales de un consultor SAP SD.

**Mentalidad:** El vector de embedding de este chunk competirá contra 64 otros vectores cuando
un consultor busque algo. ¿Por cuántas queries válidas es este chunk el resultado correcto?
¿Por cuántas es un falso positivo?

**Preguntas específicas del proyecto:**
- **Operational Summary embedding quality:** Para 5 chunks de distintas áreas, evalúa si el Operational Summary (primeras 60-80 palabras) es lo suficientemente específico para generar un embedding que diferencie este chunk de sus vecinos del mismo área. Un summary que menciona "SAP SD" y el nombre del proceso es mejor que uno que menciona "the system" y "configuration".
- **Alias category coverage:** Para 5 chunks, clasifica CADA alias en: (A) término SAP inglés, (B) término SAP español, (C) query natural de búsqueda, (D) síntoma/error que lleva al consultor aquí. ¿Están las 4 categorías representadas?
- **False positive risk:** Ejecutar `grep -rn "^  - plant$\|^  - material$\|^  - order$\|^  - entrega$\|^  - factura$\|^  - delivery$" chunks/ --include="*.md"`. Cada hit es una alias single-word que matcheará en demasiados chunks.
- **Questions as retrieval seeds:** Para 5 chunks, reescribe las preguntas como queries que un consultor SAP escribiría en un chatbox. ¿Las preguntas del chunk coinciden con cómo buscaría el usuario, o están redactadas desde la perspectiva del chunk writer?
- **Chunk size distribution:** Calcula mean/median/min/max de word counts del corpus. Distribuye chunks por bucket (<400, 400-600, 600-900, 900-1200, >1200). ¿La distribución es coherente para RAG?

---

### ROL 5 — Knowledge Graph & Navigation Specialist

**Objetivo:** Evalitar la completitud y coherencia del grafo de cross-references, identificar
nodos aislados, hubs excesivos, y caminos de navegación rotos.

**Mentalidad:** Un consultor que encuentra el chunk correcto necesita poder moverse a los chunks
relacionados. Si el grafo de referencias es roto o incompleto, el corpus es una colección de islas.

**Preguntas específicas del proyecto:**
- **Isolated nodes:** Ejecutar `python3 validate_chunks.py --json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(c['label']) for c in d['chunks'] if c.get('isolated')]"`. ¿Cuántos nodos aislados hay? ¿Son el resultado de un área incompleta o un error de cross-referencing?
- **Hub analysis:** Ejecutar un script que cuente referencias entrantes por chunk. ¿Hay chunks con >8 referencias entrantes? Evalúa si esas referencias son todas apropiadas o si algunos chunks están siendo usados como "catch-all".
- **Order-to-cash path completeness:** Traza el camino conceptual desde enterprise structure → sales order creation → delivery → billing usando solo cross-refs del corpus. ¿Dónde se rompe la cadena?
- **Bidirectionality check:** Para 10 pares de chunks con relación prior/next, verifica que ambos extremos se referencian mutuamente. `grep -rn "prior step\|next step" chunks/ --include="*.md"` como punto de partida.
- **Broken references:** Ejecutar `python3 -c "[...]"` para extraer todos los IDs referenciados en Cross-References y verificar que existen como chunks reales. IDs referenciados que no existen son broken links.

---

========================================
### FASE 1D — ESQUEMA Y PROCESO
========================================

### ROL 6 — Schema Compliance & Quality Calibration Auditor

**Objetivo:** Verificar que todos los chunks cumplen el schema, que la calidad está correctamente
calibrada según las reglas de densidad, y que el validador no tiene falsos positivos/negativos.

**Mentalidad:** El schema es el contrato entre el generador y el consumidor RAG. Cada violación
silenciosa degrada el retrieval sin avisar. El validador es el árbitro — si pasa, ¿es porque
el chunk es correcto o porque el validador no está comprobando lo suficiente?

**Preguntas específicas del proyecto:**
- **Validator completeness:** Ejecutar `python3 validate_chunks.py` y analizar: (1) ¿hay warnings recurrentes que indican patrón sistémico no corregido? (2) ¿El validador detecta el patrón "The source states" en body text? (3) ¿El validador detecta questions sin respuesta en el body?
- **Quality calibration audit:** Calcular densidad media por nivel de quality. Si quality:high tiene media < 100 w/p o quality:medium tiene media > 100 w/p, hay calibración incorrecta. Ejecutar script para calcular densidad por chunk y agrupar por quality.
- **last_updated staleness:** `grep -rn "^last_updated:" chunks/ --include="*.md"` — ¿hay chunks con fecha anterior a 2026-06-01 que el log de git indica como modificados después de esa fecha?
- **process_tags correctness:** Para 5 chunks de distintas áreas, verificar que las tags reflejan el proceso que realmente cubre el chunk, no el área donde vive. Un chunk de `configuration/` sobre billing incompletion debería tener `[order-to-cash, delivery-processing, billing]`.
- **sap_release consistency:** ¿Todos los chunks de S4605 tienen `sap_release: S/4HANA 2020`? ¿Hay alguno con `generic` o `not specified` sin justificación en el log?

---

### ROL 8 — Process & Instructions Adherence Auditor

**Objetivo:** Verificar que los chunks cumplen fielmente las reglas de CLAUDE.md, identificar
dónde el agente de procesamiento (Codex o Claude) divergió de las instrucciones.

**Mentalidad:** CLAUDE.md es la constitución del proyecto. Cada violación no detectada se vuelve
precedente. Si las reglas no se aplican, no sirven para nada — peor, crean falsa seguridad.

**Preguntas específicas del proyecto:**
- **Active voice check:** `grep -rn "The source\|The course\|the source states\|the course explains\|the source notes\|the source describes" chunks/ --include="*.md"`. Cada resultado es una violación de la regla de voz activa añadida en 2026-06-07.
- **SPRO boilerplate check:** `grep -rn "does not provide.*transaction\|no T-code.*listed\|not provide a direct" chunks/ --include="*.md"`. Estos patrones largos violan la regla "Not stated in source." (≤5 palabras).
- **Questions answered check:** Para 5 chunks elegidos al azar, verificar que CADA pregunta en "Questions This Chunk Answers" tiene respuesta explícita. Una pregunta sin respuesta es evidencia directa de violación.
- **Alias specificity check:** `grep -rn "^  - plant$\|^  - material$\|^  - order$\|^  - delivery$\|^  - factura$\|^  - invoice$" chunks/ --include="*.md"`. Cada hit viola la alias specificity rule.
- **Workshop rule:** ¿Hay algún chunk cuyo título o contenido cubre múltiples procesos no relacionados? `grep -rn "^title:.*and.*and\|^title:.*,.*," chunks/ --include="*.md"` como pista.

---

### ROL 9 — Token Efficiency Specialist

**Objetivo:** Identificar dónde el corpus consume tokens sin aportar valor RAG y proponer
reducciones concretas.

**Mentalidad:** El corpus tiene ~50k palabras (~65k tokens). Cada palabra que no añade información
al retrieval es un impuesto cognitivo que diluye la señal del chunk.

**Preguntas específicas del proyecto:**
- **SPRO section word count:** Para todos los chunks configuration, extraer la sección SPRO y contar palabras. `grep -A 2 "^## SPRO" chunks/**/*.md`. ¿Hay secciones > 20 palabras sin un IMG path concreto?
- **Redundancy between Summary and Controls:** Para 5 chunks configuration, ¿el primer párrafo de "What This Configuration Controls" repite significativamente el Operational Summary? Cuantificar el overlap de conceptos.
- **Common Errors quality:** Para 5 chunks, evalúa las Common Errors. ¿Son específicas (síntoma → causa → solución con detalle SAP) o genéricas ("Check X configuration")? Las genéricas no aportan valor RAG.
- **Aliases redundancy:** Para chunks con > 12 aliases, ¿hay pares semánticamente equivalentes en el mismo idioma? Ejemplo: "billing document" y "billing doc" son el mismo alias.
- **Total token breakdown:** Calcular: tokens en frontmatter vs. tokens en body vs. tokens en aliases/questions vs. tokens en cross-refs. ¿Qué % del total es "overhead" (headers, boilerplate)?

---

========================================
### FASE 1E — GOBERNANZA Y COMPLETITUD
========================================

### ROL 10 — Coverage & Strategic Gap Analyst

**Objetivo:** Evaluar si el corpus cubre los dominios funcionales que un consultor SAP SD
necesita para su trabajo real, y priorizar qué documentos procesar a continuación.

**Mentalidad:** Un corpus perfecto en lo que tiene pero que no cubre el 40% de los temas
más consultados es un fracaso de producto. La cobertura es el gap más costoso porque
requiere procesar nuevos PDFs — no se arregla con edits.

**Preguntas específicas del proyecto:**
- **Top-10 SAP SD queries:** Evalúa cobertura para: (1) pricing procedure/condition technique, (2) credit management/credit check, (3) ATP/availability check, (4) output determination, (5) text determination, (6) account determination (complete), (7) customer hierarchy, (8) third-party order processing, (9) intercompany sales, (10) returns end-to-end. Score de cobertura 0-3 por tema.
- **Area distribution:** `grep "^| " chunks/_index.md | awk -F'|' '{print $5}' | sort | uniq -c | sort -rn`. ¿Qué área tiene más chunks? ¿Es proporcional a la importancia funcional?
- **Next document ROI:** Basado en los gaps identificados, ¿qué documento de la lista de pendientes (S4600, S4620, S4601, credit management docs) cerraría el mayor número de gaps por páginas procesadas?
- **Cross-area orphans:** ¿Hay chunks que referencian conceptos de un área no cubierta (ej. credit management) más de 3 veces? Esos son los puntos de máxima tensión del grafo.
- **Coverage vs. depth:** ¿Cuántos chunks tiene el área con más coverage? ¿Cuántos tiene la menos cubierta? El ratio ideal es que ningún área tenga 0 chunks y ninguna tenga > 30% del total.

---

### ROL 11 — LLM Processing Bias Analyst

**Objetivo:** Identificar sesgos sistemáticos introducidos por el modelo que procesó los PDFs
(Codex vs. Claude) y verificar que la calidad no depende del modelo usado.

**Mentalidad:** El modelo que generó estos chunks tiene sesgos que el auditor humano normaliza
sin darse cuenta. Mi trabajo es hacerlos cuantitativamente visibles.

**Preguntas específicas del proyecto:**
- **Codex vs. Claude extraction gap:** Calcula la densidad media (w/p) de todos los chunks S4605 (Codex) vs. S4610+S4615 (Claude). Controla por página count para que sea comparable. ¿Sigue habiendo brecha post-expansión, o se cerró con el re-read?
- **Uniform quality calibration:** En el batch Codex S4605 original, todos los chunks eran quality:high. Después del re-read, ¿cuántos son medium? ¿El % actual de high en S4605 es < 60%? Si sigue siendo > 70%, la recalibración puede no haber sido suficientemente agresiva.
- **Hallucination risk:** Para 5 chunks con body text que menciona cifras o procedimientos específicos ("15% discount", "background program"), verificar que esa información aparece en el PDF source correspondiente.
- **Stylistic patterns:** ¿Hay diferencias estilísticas sistemáticas entre chunks S4605 (Codex) y S4610/S4615 (Claude) que indiquen sesgos de escritura? (ej. frases más largas, más/menos aliases, secciones diferentes omitidas).
- **Consistency of CLAUDE.md application:** Las reglas de CLAUDE.md se actualizaron varias veces durante el procesamiento. ¿Los chunks más antiguos (S4615, procesada antes de S4605) incumplen reglas que se añadieron después?

---

### ROL 12 — Project Manager / RAG Readiness Assessor

**Objetivo:** Evaluar cuándo el corpus estará listo para uso en producción y cuál es el camino
crítico para llegar ahí.

**Mentalidad:** ¿Cuándo es este corpus lo suficientemente bueno para que un consultor lo use
realmente? ¿Cuánto tiempo falta? ¿Vale el esfuerzo restante o hay un camino más corto?

**Preguntas específicas del proyecto:**
- **RAG readiness score por dominio:** Para order-to-cash (30% del trabajo de un consultor), delivery processing (20%), billing (25%), configuration (15%), special processes (10%) — asigna una puntuación 0-10 de readiness basada en coverage, quality, y navigability.
- **Maintenance burden forecast:** A medida que el corpus crece de 64 a 150+ chunks, ¿el proceso de deduplicación y cross-referencing escala linealmente o exponencialmente? ¿Hay signos de complejidad creciente ya visible?
- **Processing velocity:** Basado en el processing log, ¿cuántos chunks por sesión se generan actualmente? ¿A ese ritmo, cuándo se alcanzaría cobertura mínima útil (estimación: 150 chunks, 5 documentos High priority procesados)?
- **Quality floor:** ¿Hay chunks quality:low en el corpus? ¿Cuántos quality:medium están en el rango 80-99 w/p que podrían mejorarse con re-lectura del PDF y convertirse a high?
- **Go/No-Go RAG:** Define los criterios mínimos para considerar el corpus "listo para producción" (ej. ≥ 80% de las top-10 queries tienen chunk con quality:high, 0 errores en validator, precio procedure cubierto). ¿Se cumplen actualmente?

---

## ROLES — FASE 2 (SÍNTESIS)

========================================
### SYNTHESIS ROLES (ejecutar en este orden)
========================================

### ROL 13 — Devil's Advocate / Crítico Sistemático

**Objetivo:** Atacar los findings de Fase 1. ¿Son realmente críticos? ¿O hay falsos positivos
entre los hallazgos? ¿Hay hallazgos de Fase 1 que se contradicen entre sí?

**Mentalidad:** Los auditores de Fase 1 también pueden equivocarse. Mi trabajo es encontrar
dónde los hallazgos son exagerados, incorrectos, o malinterpretan la intención del diseño.

Específico para este proyecto:
- ¿El ROL 9 (token efficiency) propone eliminar contenido que el ROL 4 (RAG quality) necesita?
- ¿El ROL 3 (provenance) es tan restrictivo que el ROL 2 (SAP expert) vería el corpus como incompleto?
- ¿Algún "crítico" de Fase 1 está aplicando un estándar imposible para un proyecto de una persona?

---

### ROL 14 — System Decomposition / Cross-Cutting Analysis

**Objetivo:** Identificar problemas que traversan múltiples clusters y que ningún rol individual
capturó completamente.

Preguntas cross-cutting:
- ¿Hay un patrón sistémico que explique la mayoría de los hallazgos? (ej. "todo viene del hecho de que Codex extrajo el 50% del texto")
- ¿Cuáles son las 3 invariantes más importantes del sistema que, si se rompen, todo lo demás falla?
- ¿Qué cambio de una sola línea en CLAUDE.md habría evitado el mayor número de hallazgos?

---

### ROL 15 — Attribution Analyst

**Objetivo:** Para cada hallazgo crítico, determinar su causa raíz: ¿es un fallo de instrucciones
(CLAUDE.md), del modelo (Codex/Claude), del proceso de revisión, o del diseño del schema?

Categorías de atribución:
- **CLAUDE.md**: la regla no existía, era ambigua, o estaba mal ubicada
- **Modelo (Codex)**: el modelo no siguió la instrucción existente
- **Modelo (Claude)**: Claude aplicó la instrucción incorrectamente
- **Proceso**: la revisión adversaria no detectó el problema a tiempo
- **Schema**: el diseño del schema no captura la restricción necesaria
- **Cobertura**: requiere nuevos PDFs, no tiene solución actual

---

## DEBATES — FASE 2

### DEBATE D1 — Provenance vs. Completeness

**Participantes:** ROL 3 (Provenance) vs. ROL 2 (SAP Expert)

**Pregunta:** "El chunk `configuration-sales-document-type-control-001` no menciona las
transacciones VOV8 (para editar tipos de documentos de ventas) ni las VOV4/VOV5 (asignación
de categorías). Una persona procesando ese chunk las habría incluido. ¿Se deberían añadir como
`<!-- inferred -->` o dejar el campo `transactions: []` vacío?"

**ROL 3 argumenta:** Si VOV8 no aparece en las páginas 47-53 del S4605, no va en `transactions`.
Puede ir en `<!-- inferred, pending validation -->` en el body. El campo queda vacío.

**ROL 2 contraargumenta:** Un consultor que busca "cómo configurar el tipo de documento de ventas"
necesita saber que la transacción es VOV8. Si el campo está vacío, el chunk es funcionalmente incompleto.

**Veredicto:** El campo `transactions: []` es correcto per provenance rule. Un `<!-- inferred -->` en el body con la T-code es el mecanismo correcto. La tensión entre fidelidad y utilidad es permanente: se resuelve procesando el back-matter appendix del documento donde sí aparecen las T-codes.

---

### DEBATE D2 — RAG Recall vs. Token Precision

**Participantes:** ROL 4 (RAG Systems) vs. ROL 9 (Token Efficiency)

**Pregunta:** "El chunk `configuration-delivery-scheduling-001` tiene 18 aliases, incluyendo
'route' y 'ruta'. ¿Se eliminan por demasiado genéricos o se mantienen porque mejoran recall?"

**ROL 4 argumenta:** En un corpus de 64 chunks sobre SAP SD logístico, "route" tiene un contexto
suficientemente restringido. El recall para queries sobre rutas mejora con el alias.

**ROL 9 contraargumenta:** "route" matcheará cualquier chunk de shipping o delivery. Es ruido puro.
El alias debería ser "route determination" o "route scheduling" para ser recuperable por la query
correcta sin contaminar otras.

**Veredicto:** ROL 9 gana: el alias mínimo específico que funciona como seed de retrieval vale más
que el alias genérico. "route determination" > "route". La regla de especificidad de aliases no es
solo sobre falsos positivos — es sobre forzar que el redactor piense en la intención de búsqueda real.

---

## META-REVIEW FINAL

El agente de síntesis produce al final:

```markdown
## EXECUTIVE SUMMARY

**Veredicto global:** PASA / PASA CON CONDICIONES / NO PASA
**Fecha:** YYYY-MM-DD
**Corpus:** N chunks, N errores, N warnings

### Top-5 Hallazgos Críticos
[con severidad y acción inmediata]

### RAG Readiness Score
| Dominio | Score | Bloqueante |
|---------|-------|-----------|
| Order-to-cash | /10 | |
| Delivery processing | /10 | |
| Billing | /10 | |
| Configuration | /10 | |
| Special processes | /10 | |

### Next Action Recomendada
[documento a procesar O correcciones a aplicar]

### Scoring Agregado
| Dimensión | Peso | Score |
|-----------|------|-------|
| Extracción y fidelidad | 25% | /10 |
| Corrección factual SAP | 20% | /10 |
| Calidad RAG | 25% | /10 |
| Schema y proceso | 15% | /10 |
| Cobertura | 15% | /10 |
| **TOTAL** | 100% | /10 |

**Umbral RAG operacional:** ≥ 7.0 total, ninguna dimensión < 5.0
```
