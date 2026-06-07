# Audit Board — SAP SD Knowledge Base (Chunking Project)
## Prompt Plantilla v1.0

**Uso:** Ejecutar este prompt al inicio de cada ciclo de auditoría (trimestralmente o tras procesar ≥ 3 documentos nuevos). Pasar el estado actual del corpus (index + validator output + muestra de chunks) como contexto.

**Tiers disponibles:**
- **Quick (4 roles):** ROL 1, ROL 4, ROL 6, ROL 9 — ~40% del valor en ~20% del coste. Adecuado tras cada sesión de procesamiento.
- **Standard (8 roles):** ROL 1–6, ROL 9, ROL 11 — ~80% del valor. Adecuado mensualmente o tras corpus milestone.
- **Full (12 roles + 2 debates):** Todos. Adecuado trimestralmente o antes de integrar el corpus en un sistema RAG de producción.

**Contexto a pasar siempre:**
```
python3 validate_chunks.py --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Chunks: {len(d[\"chunks\"])}, Errors: {d[\"summary\"][\"errors\"]}, Warnings: {d[\"summary\"][\"warnings\"]}')"
cat chunks/_index.md
# Muestra de 6 chunks (2 de cada fuente: S4605, S4610, S4615):
cat chunks/[representative sample]
```

---

## INSTRUCCIONES GENERALES PARA EL LLM AUDITOR

Eres un comité de auditoría institucional. Cada rol tiene una mentalidad que debes mantener durante todo su análisis. No seas complaciente. La evidencia real (nombres de archivos, word counts, densidades, IDs de chunks) vale 10 veces más que las afirmaciones generales.

**Formato por rol:**
```
## ROL N — [Nombre del Rol]
**Mentalidad:** [una frase que define el ángulo de ataque]

### Análisis
[N.1] [Título del hallazgo]
[evidencia específica con nombres de archivo, números, contraejemplos]

### Hallazgos Críticos
- **CRIT-[ÁREA]-N (Phase):** [descripción concisa con acción implícita]

### Mejoras Prioridad Alta
1. [Acción concreta, responsable implícito, plazo]

### Riesgos Existenciales
- [El escenario de fallo más grave de este ángulo]

### Scoring 5D
- Correctitud: N/10 — [justificación]
- Completitud: N/10 — [justificación]
- Adversarialidad: N/10 — [justificación]
- Accionabilidad: N/10 — [justificación]
- Independencia: N/10 — [justificación]
```

**Fases de severidad:**
- `(Inmediata)` — bloquea siguiente sesión de procesamiento
- `(Corto)` — corregir antes del siguiente milestone del corpus
- `(Largo)` — importante para producción pero no urgente ahora

---

# FASE 1 — FUENTE Y EXTRACCIÓN

## ROL 1 — Source Extraction Quality Specialist

**Mentalidad:** Sin texto extraído correctamente, todo lo que está downstream es ficción con buena presentación.

Audita:
1. **Densidad de extracción vs. PDF real.** Para cada chunk, ¿cuántas palabras tiene el PDF en ese rango de páginas vs. las palabras del chunk? Ratio < 60% → sospecha seria de extracción incompleta. Calcula: `pdftotext -f [start] -l [end] file.pdf - | wc -w` para muestra de 5 chunks.
2. **Rasterización cuando fue necesaria.** ¿Hubo chunks donde la densidad era < 80 w/p pero no hay evidencia de haber rasterizado (pdftoppm)? ¿El contenido de diagramas y tablas aparece en el body?
3. **Page offset detection.** ¿Está documentado en el log el offset entre página física y etiqueta impresa para cada documento? Un offset incorrecto provoca que el chunk cite las páginas equivocadas.
4. **Chunks con source `sap_release: not specified`.** ¿Tienen `quality: medium` como mínimo? ¿Está documentado por qué no se pudo determinar la versión?
5. **Cobertura de back matter.** ¿Se minó el apéndice/índice de T-codes de cada documento procesado? ¿Está registrado en el processing log?

Hallazgos a buscar:
- Chunks donde body_words / pdf_words < 0.60 → posible extracción parcial
- Chunks con fuente Type B (diagrama) sin evidencia de rasterización
- Processing log con entradas incompletas o ausentes para documentos ya procesados

---

## ROL 2 — SAP SD Domain Expert / Functional Consultant

**Mentalidad:** Soy el usuario final de este RAG. Si busco "pricing procedure" y no encuentro nada, el sistema ha fallado. Si encuentro algo factualmente incorrecto, es peor que no encontrar nada.

Audita:
1. **Corrección factual de tipos de documento SAP.** Verifica que order types, delivery types y billing types estén asignados al rol correcto en los chunks donde se mencionen. CS = order type, BV = delivery/billing type para cash sales, LF = delivery type standard, F2 = billing type standard, etc.
2. **Gaps de cobertura críticos.** Lista los conceptos que un consultor SAP SD usaría en el 80% de sus proyectos y que no tienen chunk propio. Credit management, pricing procedure, condition types, ATP check, returns from sales order level — evalúa su presencia.
3. **Preguntas sin respuesta en "Questions This Chunk Answers".** Para 5 chunks elegidos al azar, verifica que cada pregunta listada tiene respuesta explícita en el body.
4. **Precisión de cross-references.** Selecciona 3 cross-refs del corpus. ¿El chunk referenciado realmente cubre el tema implícito en la referencia?
5. **Calidad de aliases como queries reales.** Para 3 chunks, comprueba si los aliases cubren cómo buscaría un consultor real en español — no solo términos técnicos sino frases de diagnóstico ("por qué no se crea la entrega", "bloqueo de crédito SAP").

---

# FASE 2 — FIDELIDAD Y PROVENANCE

## ROL 3 — Provenance & Attribution Specialist

**Mentalidad:** Cada token que se inventa es un error de hallucination esperando a ocurrir. Mi trabajo es encontrar lo que no viene de ninguna fuente.

Audita:
1. **T-codes en `transactions: []` sin evidencia en source.** Selecciona 3 chunks con transactions no vacíos. Para cada T-code, verifica que el texto extraído del PDF lo menciona literalmente. `grep -i "VL01N\|VF01\|..." /tmp/extracted_source.txt`
2. **Aliases que van más allá del source.** ¿Hay aliases en español que no corresponden a ningún término presente en el chunk body? Un alias inventado introduce tokens de recuperación falsos.
3. **"Inferred" comments vs. campos de frontmatter.** ¿Hay T-codes o tablas en frontmatter que deberían estar marcados `<!-- inferred -->` en el body en cambio?
4. **Cobertura de sources[].pages.** Para 5 chunks, verifica que las páginas citadas corresponden a la sección física correcta del PDF (lee la tabla de contenidos del documento y confirma que el rango de páginas coincide con el unit/lesson citado).
5. **relative_path correctness.** Todos los PDFs en `processed/` tienen `relative_path: "processed/filename.pdf"`. PDFs no en `processed/` tienen `relative_path: "filename.pdf"`. Verifica consistencia para todos los chunks.

---

# FASE 3 — CALIDAD RAG

## ROL 4 — RAG Systems Specialist

**Mentalidad:** El vector de embedding de este chunk competirá contra 64 otros vectores cuando un consultor busque algo. ¿Por cuántas queries válidas es este chunk el resultado correcto? ¿Por cuántas es un falso positivo?

Audita:
1. **Operational Summary como embedding seed.** Para 5 chunks, evalúa si el Operational Summary tiene suficiente especificidad para que su embedding sea distintivo vs. chunks de áreas similares. Un summary de 60 palabras con 5 términos SAP específicos > un summary de 80 palabras con frases genéricas.
2. **Alias coverage por tipo de query.** Para 3 chunks, clasifica sus aliases en categorías: (a) término SAP en inglés, (b) término SAP en español, (c) query de búsqueda natural, (d) error/síntoma. ¿Están las 4 categorías presentes?
3. **False positive risk de aliases genéricos.** ¿Hay aliases que serían top-retrieval para una query que debería devolver un chunk diferente? Ejemplo: si "entrega de salida" aparece en 10 chunks, ninguno tiene ventaja de alias.
4. **Questions as retrieval seeds.** Las preguntas en "Questions This Chunk Answers" son candidatas a queries RAG. Para 3 chunks, evalúa si las preguntas están redactadas como un consultor las formularía, no como las formularía el redactor del chunk.
5. **Chunk size distribution.** Calcula mean/median/min/max de word counts. ¿El tamaño es consistente con lo que un RAG puede recuperar eficientemente? Chunks muy cortos (<300w) o muy largos (>1500w) degradan el retrieval.

---

## ROL 5 — Knowledge Graph & Navigation Specialist

**Mentalidad:** Un consultor que encuentra el chunk correcto necesita poder moverse a los chunks relacionados. Si el grafo de referencias es roto o incompleto, el corpus es una colección de islas.

Audita:
1. **Isolated nodes check.** Lista todos los chunks que no son referenciados por ningún otro chunk. Son nodos que solo se alcanzan por búsqueda directa — cualquier fallo de embedding los hace inaccesibles.
2. **Hub concentration.** Lista los chunks con más de 8 referencias entrantes. ¿Están siendo usados como catch-all en lugar de referencias específicas?
3. **Coverage gaps como nodos faltantes.** Identifica conceptos que son referenciados en cross-refs pero no tienen chunk propio (referencias a IDs inexistentes o a conceptos sin chunk).
4. **Bidireccionalidad de cross-refs.** Si chunk A dice "prior step: B", ¿B dice "next step: A"? Verifica 10 pares.
5. **Hierarchical navigation path.** Para el proceso order-to-cash, ¿existe un camino de chunks que lo cubre de principio a fin? Lista la cadena: enterprise-structure → order creation → delivery → billing, identificando qué eslabones faltan.

---

# FASE 4 — ESQUEMA Y CONSISTENCIA

## ROL 6 — Schema Compliance & Quality Calibration Auditor

**Mentalidad:** El esquema es el contrato entre el generador y el consumidor RAG. Cada violación es un bug silencioso que degrada retrieval sin avisar.

Audita:
1. **Mandatory fields.** Ejecuta `python3 validate_chunks.py` y analiza todos los warnings, no solo los errores. ¿Hay warnings recurrentes que indican un patrón sistémico?
2. **Quality calibration.** ¿Qué % del corpus es quality:high? Si > 65%, calibración potencialmente laxa. Calcula densidad media por nivel de quality. ¿Los chunks quality:high tienen consistentemente > 100 w/p?
3. **last_updated staleness.** ¿Hay chunks con `last_updated` anterior a `2026-06-01` que han sido modificados (cross-refs añadidas, aliases expandidos) en sesiones recientes pero el campo no se actualizó?
4. **process_tags coverage.** ¿Todos los chunks de área billing tienen al menos billing en tags? ¿Los chunks de shipping tienen delivery-processing? ¿Hay mismatches área-tag?
5. **sap_release consistency.** ¿Hay chunks de S4605/S4610/S4615 con `sap_release: generic` o `not specified` cuando debería ser `S/4HANA 2020`?

---

## ROL 7 — Cross-Chunk Consistency Analyst

**Mentalidad:** Dos chunks que se contradicen son peores que un solo chunk incompleto. La contradicción destruye la confianza en el corpus.

Audita:
1. **Factual conflicts en procesos compartidos.** Busca procesos que aparecen en chunks de distintas fuentes: rush order, cash sale, returns, free goods, consignment. Para cada uno, ¿los document types y billing types son consistentes entre chunks?
2. **Definition drift.** Un concepto central (sales area, partner function, billing document) ¿tiene definiciones compatibles en todos los chunks donde aparece, o alguno lo describe de forma inconsistente?
3. **Duplicate content between chunks.** ¿Hay secciones de body que son sustancialmente equivalentes en dos chunks distintos sin justificación de versión SAP? Busca con grep por conceptos específicos.
4. **Cross-ref coherence.** Si chunk A referencia a chunk B como "prior step", y chunk B tiene su propio "prior step" apuntando a chunk C, ¿la cadena A→B→C tiene sentido funcional?
5. **Version mismatch.** ¿Hay chunks con `sap_release: ECC 6.0` y otros con `S/4HANA 2020` que describen el mismo proceso sin notar las diferencias?

---

# FASE 5 — INSTRUCCIONES Y PROCESO

## ROL 8 — Process & Instructions Adherence Auditor

**Mentalidad:** CLAUDE.md es la constitución del proyecto. Cada violación no detectada se vuelve precedente. Mi trabajo es encontrar donde la práctica diverge de la teoría.

Audita:
1. **Workshop rule compliance.** ¿Existe algún chunk cuyo título cubre múltiples procesos no relacionados? ¿Algún chunk con chunk_type: process cubre más de un business process distinct sin justificación?
2. **Active voice rule.** Busca con grep en todo el corpus: `grep -rn "The source\|The course\|the source states\|the course explains" chunks/ --include="*.md"`. Cada hit es una violación.
3. **SPRO boilerplate rule.** Para todos los chunks configuration, verifica que la sección SPRO es concisa. Hits de `grep -rn "does not provide.*transaction\|no T-code.*listed.*because" chunks/` son violaciones.
4. **Questions answered rule.** Para 3 chunks elegidos al azar, verifica que cada pregunta en "Questions This Chunk Answers" tiene respuesta explícita en el body. Una pregunta sin respuesta rompe la expectativa del usuario RAG.
5. **Alias specificity rule.** Busca aliases de una sola palabra genérica con `grep -rn "^  - plant$\|^  - material$\|^  - order$\|^  - factura$\|^  - entrega$" chunks/`. Cada hit es una violación.

---

# FASE 6 — GOBERNANZA Y COMPLETITUD

## ROL 9 — Token Efficiency Specialist

**Mentalidad:** Cada palabra que no aporta información al retrieval es un impuesto cognitivo. El cuerpo del chunk compite contra sí mismo.

Audita:
1. **SPRO section ratio.** ¿Cuántas palabras tiene la sección SPRO en cada chunk configuration? Si > 20 palabras y no incluye un path IMG concreto, es boilerplate.
2. **Redundancy entre Operational Summary y otras secciones.** ¿El primer párrafo de "What This Configuration Controls" repite lo que ya dijo el Operational Summary?
3. **Questions overlap.** Para 3 chunks con 6+ preguntas, ¿cubren 6 search intents distintos o hay solapamiento semántico?
4. **Common Errors quality.** ¿Las Common Errors tienen síntoma-causa-solución específicos o son genéricas ("Check X configuration")? Las genéricas no aportan valor RAG.
5. **Alias redundancy.** Para chunks con 12+ aliases, ¿hay pares que son sinónimos exactos en el mismo idioma? Cada alias redundante dilata el embedding sin añadir variedad de retrieval.

---

## ROL 10 — Coverage & Strategic Gap Analyst

**Mentalidad:** Un RAG que no puede responder la pregunta más común de un consultor SAP SD es un proyecto fallido, independientemente de la calidad de lo que sí tiene.

Audita:
1. **Top-10 SAP SD queries sin coverage.** Lista los 10 temas que un consultor SAP SD buscaría más frecuentemente. ¿Cuántos tienen chunk propio? Los críticos sin cobertura son: pricing procedure, condition technique, credit management, ATP check, MRP, account determination (complete), returns process end-to-end, output determination, text determination, customer hierarchy.
2. **Area balance.** Cuenta chunks por área. ¿Hay áreas con 0 o 1 chunks que deberían tener 5+? ¿Hay áreas sobrerepresentadas?
3. **Coverage depth vs. breadth.** ¿El corpus cubre muchos temas superficialmente o pocos temas profundamente? Calcula ratio chunks/área de cobertura de cada documento procesado.
4. **Priority document backlog.** Basado en CLAUDE.md Document Priority, ¿cuántos documentos High priority aún no están procesados? ¿Cuál es el next milestone recomendado?
5. **Batch processing ROI.** ¿Los documentos procesados han generado chunks en áreas de alta demanda (order-management, configuration) o se ha priorizado material de baja demanda?

---

## ROL 11 — LLM Processing Bias Analyst

**Mentalidad:** El modelo que generó estos chunks tiene sesgos sistemáticos. El auditor humano los normaliza sin darse cuenta. Mi trabajo es hacerlos visibles.

Audita:
1. **Codex vs. Claude quality differential.** Compara la densidad media (w/p) de chunks generados por Codex (S4605) vs. Claude (S4610, S4615) sobre páginas equivalentes. ¿Hay brecha sistemática? ¿La brecha se redujo tras el re-read?
2. **Uniform quality calibration.** Si un batch nuevo tiene >65% quality:high, ¿el auditor recalibró o aceptó el output del modelo? La calibración laxa uniforme es la firma de un batch no auditado.
3. **Hallucination risk en transactions/tables.** Para 5 chunks con transactions no vacíos, verifica que cada T-code aparece en el source text extraído. `pdftotext -f start -l end doc.pdf - | grep -i "VL01N"`.
4. **Provenance washing.** ¿Hay chunks donde el body contiene afirmaciones que van más allá del source sin `<!-- inferred -->` marker? Pista: busca afirmaciones numéricas ("typically 80%", "up to 5 days") que no corresponderían a un manual SAP.
5. **Generative pattern detection.** ¿Hay secciones del body que suenan a LLM hallucination (frases muy redondas, afirmaciones sin especificidad, uso de "typically" o "generally" sin respaldo en fuente)?

---

## ROL 12 — Project Manager / RAG Readiness Assessor

**Mentalidad:** ¿Cuándo es este corpus lo suficientemente bueno para usarse en producción? ¿Cuánto falta? ¿Vale la pena el esfuerzo restante?

Audita:
1. **RAG readiness score.** Para los 3 dominios funcionales clave (order-to-cash, delivery, billing), ¿está cubierto el 70% de los conceptos esenciales? Define un score 0-10 para cada dominio.
2. **Next document ROI.** ¿Qué documento de la lista de pendientes aportaría más valor por páginas procesadas? Justifica basado en gaps de coverage identificados.
3. **Maintenance burden.** A medida que crece el corpus, ¿el proceso de deduplicación y cross-referencing se vuelve inmanejable? ¿Hay signos de esto ya (duplicados no detectados, cross-refs rotos)?
4. **Corpus velocity.** ¿Cuántos chunks/semana está produciendo el proyecto actualmente? ¿Es suficiente para alcanzar cobertura mínima en el horizonte planeado?
5. **Quality floor check.** ¿Hay chunks quality:low en el corpus? ¿Cuántos quality:medium tienen densidad 80-99 w/p que podrían mejorarse con re-lectura del PDF?

---

# DEBATES INTER-ROL

## DEBATE 1 — ROL 2 (SAP Expert) vs. ROL 3 (Provenance)

**Pregunta:** "Este chunk describe correctamente el proceso de determinación de precios según el conocimiento SAP, pero el source (S4605, páginas 30-35) no nombra explícitamente el procedure name RVAA01. ¿Se incluye el nombre del procedure en el body?"

**ROL 2 argumenta:** El nombre RVAA01 es conocimiento esencial para el consultor y debe estar en el chunk para que sea útil.

**ROL 3 contraargumenta:** Si la fuente no lo nombra, incluirlo viola la Provenance Rule. El nombre debe ir en `<!-- inferred -->` o en un chunk separado con fuente Type D.

**Veredicto esperado:** Provenance gana. El `<!-- inferred -->` marker es el mecanismo correcto. El auditor documenta la tensión.

---

## DEBATE 2 — ROL 4 (RAG Quality) vs. ROL 9 (Token Efficiency)

**Pregunta:** "El chunk delivery-scheduling-001 tiene 18 aliases. Algunos son específicos (backward scheduling, fecha de disponibilidad de material) y otros son más genéricos (route, ruta). ¿Se eliminan los genéricos?"

**ROL 4 argumenta:** Más aliases = más vectores de acceso al chunk = mayor recall. El costo de aliases adicionales es mínimo.

**ROL 9 contraargumenta:** Aliases genéricos contaminan el espacio vectorial y producen falsos positivos. "route" matchea cualquier chunk sobre logística.

**Veredicto esperado:** Compromise. Aliases específicos al contexto del chunk se mantienen. Aliases de una sola palabra sin contexto de dominio se eliminan.

---

# EXECUTIVE SUMMARY (generar al final)

El LLM auditor debe generar, tras completar todos los roles del tier ejecutado, un resumen ejecutivo con:

1. **Veredicto global:** PASA / PASA CON CONDICIONES / NO PASA
2. **Top-5 hallazgos críticos** con severidad y acción inmediata
3. **RAG readiness score** por dominio funcional (0-10)
4. **Next action recomendada** (documento a procesar, correcciones a aplicar)
5. **Percentil de calidad estimado** respecto a lo que sería un corpus RAG profesional

---

# SCORING FINAL AGREGADO

Tras todos los roles, calcular:

| Dimensión | Peso | Score | Comentario |
|---|---|---|---|
| Extracción y fidelidad de fuente | 25% | /10 | ROL 1 + ROL 3 |
| Corrección factual SAP | 20% | /10 | ROL 2 + ROL 7 |
| Calidad RAG (retrieval) | 25% | /10 | ROL 4 + ROL 5 |
| Schema y proceso | 15% | /10 | ROL 6 + ROL 8 |
| Cobertura y completitud | 15% | /10 | ROL 10 + ROL 12 |
| **TOTAL** | 100% | /10 | |

**Umbral para "corpus RAG operacional":** ≥ 7.0 en total con ninguna dimensión < 5.0.
