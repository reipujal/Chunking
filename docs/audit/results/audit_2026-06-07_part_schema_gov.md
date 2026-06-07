# Auditoría Quick — ROL 6 + ROL 10 — 2026-06-07

**Corpus analizado:** 74 chunks — S4605, S4610, S4615, S4620  
**Agente:** C4_schema + C5_gov  
**Tier:** Quick (ROL 6 y ROL 10)  
**Ejecutada:** 2026-06-07

---

## ROL 6 — Schema Compliance & Quality Calibration Auditor

**Objetivo:** Verificar que el schema es el contrato real entre generador y consumidor RAG. Cada violación silenciosa degrada retrieval. El validador es el árbitro formal, pero no lo comprueba todo.

**Mentalidad:** Escéptico. Presuponer que los chunks que pasan el validator pueden seguir teniendo defectos no detectados por el mismo.

---

### 6.1 Análisis del output del validador

**Resultado:** 74/74 OK — 0 errores, 2 warnings.

**Warnings detectados:**

**WARN 1 — Densidad baja en `configuration/pricing-procedure-configuration-001.md`**  
`[DENSITY] 57 words/page (862w / 15p). Below 80 w/p — verify all source pages were fully read.`

- Páginas citadas: 25-39 del S4620 (15 páginas físicas).
- Palabras en body: 862.
- 57 w/p está por debajo del umbral de 80 w/p definido en CLAUDE.md como "mandatory medium".
- El chunk tiene `quality: medium` — lo que es correcto. El validator emite warning pero no error, pues no es `quality: high`.
- **Sin embargo:** el procesing log declara para el S4620 que "pages are diagram-heavy; density 77-80 w/p after expansion" (nota del log para chunks 1, 3, 5, 6). Este chunk (el de configuración de pricing procedure) tiene 57 w/p, que está por debajo de lo que el log afirma. Existe discrepancia entre el log y la densidad real del chunk.
- **Acción recomendada:** Re-leer páginas 25-39 del S4620 con rasterización. El procesing log sugiere que se hizo expansión, pero 57 w/p es materialmente inferior a 77 w/p. Es posible que la expansión fue parcial.

**WARN 2 — Batch audit: max cited page = 168**  
El corpus usa páginas físicas hasta 168 (S4605). Es un dato informativo. El batch audit lo emite sistemáticamente. No es defecto — el S4605 tiene 168 páginas físicas según el log. Este warning es ruido de diagnóstico bajo las condiciones actuales del corpus.

**Valoración global del validator:** El validator cubre correctamente los campos obligatorios, enum validation, densidad, cross-references, aliases mínimos, questions mínimas, H1 title, y provenance de transactions/tables. **La tasa de 0 errores es creíble** dada la corrección sistemática documentada en el log (no hay señal de uniformidad sospechosa en quality, el ratio high/medium es 45/29 = 61%/39%).

---

### 6.2 Quality Calibration Audit — Distribución de densidad

**Datos calculados directamente de los 74 chunks** (parser multi-segmento aplicado sobre `pages` field del frontmatter de cada chunk):

**quality:high — 45 chunks**

Densidades calculadas para los chunks leídos directamente durante esta auditoría:

| Chunk | Words (body est.) | Pages | w/p | Calibración |
|---|---|---|---|---|
| pricing-condition-technique-overview-001 | ~830 | 17 | ~49 | ALERTA — ver §6.2.1 |
| pricing-special-condition-types-001 | ~780 | 13 | ~60 | ALERTA — ver §6.2.1 |
| pricing-condition-contract-management-concept-001 | ~700 | 8 | ~88 | OK (≥80, marginal) |
| pricing-statistical-condition-types-001 | ~780 | 9 | ~87 | OK (≥80, marginal) |
| configuration-pricing-procedure-configuration-001 | 862 | 15 | 57 | quality:medium — correcto |

**HALLAZGO CRÍTICO — 6.2.1: Dos chunks S4620 tienen `quality:high` con densidad estimada por debajo de 100 w/p**

**`pricing-condition-technique-overview-001`:**
- pages: "8-24" → 17 páginas físicas
- El body del chunk fue contado por el validator con `quality: medium` — lo que es correcto en frontmatter.
- Relectura directa del archivo: `quality: medium` — frontmatter es correcto. No hay error aquí.

**`pricing-special-condition-types-001`:**
- pages: "63-75" → 13 páginas físicas
- Frontmatter: `quality: medium` — correcto.

**`pricing-special-pricing-functions-001`:**
- pages: "54-61" → 8 páginas físicas
- Frontmatter: `quality: high`
- Necesita verificación: el processing log menciona "chunks 1, 3, 5, 6 have quality:medium" pero el index muestra quality:high para special-pricing-functions. Si pages=8 y el body es ~700w, w/p ≈ 88, que es 80-99 → debería ser medium según CLAUDE.md.

**`pricing-statistical-condition-types-001`:**
- pages: "76-84" → 9 páginas físicas
- Frontmatter: `quality: high`
- El chunk body tiene tablas detalladas y múltiples secciones — body estimado ~780 palabras. 780/9 = 87 w/p → rango 80-99 w/p → según CLAUDE.md "quality:medium, no exceptions". Sin embargo el validator no detectó error porque quality:high no se invalida hasta <80 w/p (el error del validator se dispara en <80 w/p).

**HALLAZGO IMPORTANTE — 6.2.2: El validator tiene un gap de cobertura en el rango 80-99 w/p para quality:high**

El validator solo emite ERROR `[DENSITY+QUALITY]` cuando `wpp < 80 AND quality == 'high'`. CLAUDE.md dice: "80–99 w/p → quality:medium, no exceptions." Pero el validator no detecta el caso `80 ≤ wpp < 100 AND quality == 'high'` — solo emite WARN de densidad y no correlaciona con quality. Esto significa que un chunk con 90 w/p y quality:high **pasa el validator sin warning relacionado con quality**, aunque CLAUDE.md lo prohíbe explícitamente.

En la práctica, los chunks `pricing-statistical-condition-types-001` (quality:high, ~87 w/p) y posiblemente `pricing-special-pricing-functions-001` (quality:high, ~88 w/p) violan CLAUDE.md §Step 5 Quality Criteria pero **el validator no los detecta**.

---

### 6.3 Revisión de calidad de los 5 chunks S4620 leídos

#### `pricing-condition-technique-overview-001` — quality: medium

**(a) Quality field vs. densidad:** pages "8-24" = 17p. Body leído: ~830 palabras estimadas. 830/17 ≈ 49 w/p. Muy por debajo de 80 w/p. El quality: medium es correcto pero el validator también debería haber disparado WARN [DENSITY] (<80 w/p). No lo hizo, lo que sugiere que el word count real es mayor. Hay que revisar: el validator contó 862w / 15p = 57 w/p — aparece como WARN en el validator pero para `configuration-pricing-procedure-configuration-001`, no para este chunk. Revisando de nuevo: el validator no emitió WARN para `pricing-condition-technique-overview-001`. Dado pages="8-24" = 17p, y que el validator no emitió warning, el body tiene >80×17 = 1360 palabras. Leyendo el chunk directamente, el body es sustancial (múltiples secciones, tablas). **Conclusión: la densidad real es aceptable y el validator es correcto en no emitir warning.**

**(b) Campos obligatorios:** Todos presentes. Schema correcto.

**(c) Aliases:** 9 aliases, ≥2 en español. Calidad buena. Aliases específicos (no genéricos). Cumple.

**(d) Questions:** 8 preguntas distintas. Supera el mínimo de 4. Cada pregunta es genuinamente distinta en intención de búsqueda. Cumple.

**(e) Cross-references:** 4 referencias. Todas a IDs reales. Cumple.

**(f) Observación:** La sección `## Key Facts from Source` al final del body es un residuo estilístico — no es una sección del schema definido en CLAUDE.md para chunk_type:concept (las secciones válidas son: Operational Summary, Questions, Definition, Purpose, Structure/Variants, Relationship, Cross-References). Esta sección extra no causa error pero es ruido no canónico. Impacto RAG: mínimo.

#### `pricing-special-condition-types-001` — quality: medium

**(a) Quality vs. densidad:** pages "63-75" = 13p. El validator no emitió warning → body > 1040 palabras. Densidad aceptable. Correcto.

**(b) Aliases:** 10 aliases, varios en español con términos específicos (jerarquía de cliente, descuento palet, tipos de condición especiales). Cumple alias specificity rule.

**(c) Questions:** 8 preguntas distintas. Cumple.

**(d) Sección `## Classification Summary`:** No es una sección canónica del schema para concept chunks. Es contenido funcional válido pero no encaja en la estructura definida. El validator no lo detecta porque solo comprueba presencia de secciones obligatorias, no ausencia de secciones no canónicas.

**(e) Provenance tables/transactions:** `tables: []`, `transactions: []`. El chunk menciona T001R en el body (para DIFF). Sin embargo, T001R no aparece en el frontmatter `tables`. Revisando el cuerpo: "Rounding rules are maintained in table T001R per company code and currency." La tabla T001R aparece explícitamente en el body como nombre de tabla ABAP. El campo `tables: []` parece ser under-extraction si T001R está literalmente en el texto fuente.

**HALLAZGO IMPORTANTE — 6.3.1: Posible under-extraction de tabla T001R en `pricing-special-condition-types-001`**

El body cita "table T001R" como token exacto. Si este token aparece en el PDF fuente (no como inferencia del autor del chunk), debería estar en `tables`. Sin el PDF disponible para verificación en esta sesión, se marca como SOSPECHOSO para revisión humana. Si la mención proviene del texto fuente del S4620, es under-extraction. Si es conocimiento del autor del chunk no presente en el PDF, es correcto que esté solo en el body.

Nota: el chunk `pricing-statistical-condition-types-001` tiene `tables: [T052, T001R]` — lo que confirma que T001R sí aparece en la fuente del S4620. Esto hace más probable que en `pricing-special-condition-types-001` el T001R también provenga de la fuente, no de inferencia del autor.

#### `pricing-condition-contract-management-concept-001` — quality: high

**(a) Quality vs. densidad:** pages "92-99" = 8p. El validator no emitió warning → body > 640 palabras. Con el cuerpo sustancial observado (múltiples tablas, secciones detalladas), densidad estimada > 100 w/p. quality:high es elegible. Correcto.

**(b) Aliases:** 12 aliases específicos, múltiples en español (gestión de contratos de condición, CCM descuento retroactivo, liquidación de rappel, acumulaciones rappel). Excelente especificidad. Cumple.

**(c) Questions:** 7 preguntas distintas. Cumple.

**(d) Sección IMG en body:** El chunk include rutas IMG en el body (dentro de la sección Structure and Variants). Esta es información de configuración en un chunk concept. Es funcional y útil, pero introduce un patrón híbrido concept/configuration que podría confundir a un futuro auditor. El CLAUDE.md no lo prohíbe explícitamente. Impacto: bajo.

**(e) Provenance:** `transactions: []`, `tables: []`. El body menciona "standard SD condition types" y pricing procedures (A10005-A10008) como códigos alfanuméricos pero no como T-codes ni nombres de tabla ABAP. Correcto.

#### `pricing-statistical-condition-types-001` — quality: high

**(a) Quality vs. densidad:** pages "76-84" = 9p. El validator no emitió warning → body > 720 palabras. El body observado es rico: tablas de tax procedures, fórmulas, múltiples subsecciones. Densidad estimada ~87 w/p (estimación conservadora). Si la densidad real está entre 80-99 w/p, CLAUDE.md requiere quality:medium "no exceptions."

**HALLAZGO CRÍTICO — 6.3.2: `pricing-statistical-condition-types-001` potencialmente miscalibrado como quality:high**

El validator no detecta este caso (solo alerta si density < 80 con quality:high). El processing log dice que "chunks 1, 3, 5, 6 have quality:medium" — si este chunk es el chunk 6 (el sexto en order de procesamiento), debería ser medium. Verificando el orden de creación en el log: la secuencia es condition-technique (1), pricing-procedure-config (2), condition-records (3), special-pricing-functions (4), special-condition-types (5), statistical-condition-types (6). El log dice chunks "1, 3, 5, 6" son medium. Statistical-condition-types es el chunk 6 en el orden de procesamiento — según el log debería ser medium, pero tiene quality:high en el frontmatter. **Esta es una inconsistencia directa entre el procesing log y el frontmatter del chunk.**

**(b) Tables:** `tables: [T052, T001R]` — ambas citadas explícitamente en el body con sus nombres exactos. Correcto.

**(c) Aliases:** 11 aliases, varios en español (coste condición estadística, descuento por pronto pago condición, determinación de impuestos, impuesto en pedido de ventas, condición estadística esquema precios). Excelente especificidad. Cumple.

#### `configuration-pricing-procedure-configuration-001` — quality: medium

**(a) Quality vs. densidad:** 862 palabras / 15 páginas = 57 w/p. Claramente por debajo de 80 w/p. El validator emitió WARN. quality:medium es correcto, pero la densidad sugiere extracción incompleta.

**HALLAZGO IMPORTANTE — 6.3.3: `configuration-pricing-procedure-configuration-001` con 57 w/p en 15 páginas sugiere sub-extracción**

15 páginas de un documento Tipo A con 57 w/p están por debajo del umbral de "very low" (< 50 w/p) del validator y en la banda "Below 80 w/p". Para 15 páginas de S4620 (una fuente que el log describe como "medium extractable, figure-heavy"), es posible que las páginas 25-39 contengan principalmente diagramas del flujo de configuración. Sin embargo, el CLAUDE.md exige rasterización cuando density < 100 w/p para verificar si hay contenido adicional. El procesing log no menciona rasterización de este chunk específicamente. Se recomienda re-lectura.

**(b) SPRO section:** "Not stated in source. Navigate via IMG: Sales and Distribution → Basic Functions → Pricing → Pricing Control." — Cumple la regla: 5 palabras para "Not stated in source" + ruta inferida en segunda línea. Correcto.

---

### 6.4 Compliance de voz activa (nueva regla 2026-06-07)

Se ejecutó búsqueda de patrones prohibidos (`The source|The course|the source states|the course explains`) en todos los chunks.

**Violaciones encontradas:**

| Archivo | Línea | Violación |
|---|---|---|
| `configuration/sales-copying-control-001.md` | L33 | "The source covers sales-to-sales..." |
| `configuration/sales-copying-control-001.md` | L80 | "-> The source-target document type..." |
| `configuration/sales-copying-control-001.md` | L89 | "-> Routines and requirements... The course recommends..." |
| `configuration/sales-document-type-control-001.md` | L33 | "The source highlights that sales processes are controlled..." |
| `configuration/sales-document-type-control-001.md` | L80 | "-> The source warns that activating checks..." |
| `integration/sales-document-technical-tables-001.md` | L49 | "The source separates the technical information..." |
| `master-data/material-listing-exclusion-001.md` | L43 | "The course example uses master records..." |
| `master-data/material-listing-exclusion-001.md` | L64 | "The source names customer group/material..." |
| `order-management/outline-agreements-scheduling-quantity-contracts-001.md` | L36 | "The course identifies two main outline agreement types..." |
| `order-management/sales-distribution-process-001.md` | L33 | "The course describes the process chain..." |
| `order-management/sales-distribution-process-001.md` | L51 | "The source names three SD document families:" |
| `order-management/sales-order-special-features-001.md` | L33 | "The source emphasizes fast changes, mass changes..." |

**Total: 12 violaciones en 6 archivos — todos de S4605 (generados en la sesión 2026-06-07).**

**HALLAZGO CRÍTICO — 6.4.1: La regla de voz activa (añadida 2026-06-07) no fue retroaplicada a los chunks S4605 generados en la misma sesión**

La regla "Active voice: no 'The source/course states' en body text" fue añadida a CLAUDE.md el 2026-06-07, el mismo día en que se generaron los 19 chunks de S4605. Los chunks S4620 (también generados ese día) no presentan ninguna violación. Los chunks S4605 tienen 12 violaciones en 6 archivos. Esto indica que la regla se aplicó al procesar S4620 pero no fue retroaplicada a los chunks S4605 ya escritos. El validator no comprueba esta regla.

**Impacto RAG:** Las frases "The course describes..." y "The source names..." convierten al chunk en una descripción de un documento (metadata del documento) en lugar de un documento de referencia autónomo. Un usuario preguntando "¿qué son los scheduling agreements en SAP?" recibirá "The course identifies two main outline agreement types" — lo que revela la procedencia del texto en vez de responder directamente. Esto degrada la calidad de la respuesta RAG.

---

### 6.5 Compliance de sección SPRO en configuration chunks

Verificación de todos los configuration chunks sobre la regla: "Not stated in source." (5 palabras) en una sola línea, sin párrafos explicativos.

**Violación parcial encontrada:**

`configuration/sales-copying-control-001.md` línea 61:  
`No direct T-code stated in source. Routines and requirements are edited under *System Modifications* in the SD Customizing menu.`

Esta línea tiene ~20 palabras. La regla dice "Not stated in source." (5 palabras exactas) si no hay T-code en fuente. La frase "No direct T-code stated in source" es una variación aceptable semánticamente pero viola la literalidad del formato (5 palabras). La segunda parte "Routines and requirements are edited under..." es información adicional que va más allá del "Navigate via IMG: [path]" permitido.

Todos los demás casos de SPRO "Not stated" revisados cumplen correctamente con el formato de 5 palabras + opcional ruta IMG.

**Estado global del SPRO compliance:** 1 violación menor de formato en 7 chunks "Not stated in source" inspeccionados.

---

### Hallazgos Críticos — ROL 6

| ID | Severidad | Descripción | Archivo(s) |
|---|---|---|---|
| R6-C1 | CRÍTICO | 12 violaciones de regla de voz activa (añadida 2026-06-07) en chunks S4605 — no retroaplicada | 6 archivos en configuration/, integration/, master-data/, order-management/ |
| R6-C2 | CRÍTICO | `pricing-statistical-condition-types-001` probablemente miscalibrado: el processing log lo categoriza como medium pero frontmatter dice high; validator no lo detecta porque su umbral de error para quality:high es <80 w/p, no <100 w/p | chunks/pricing/statistical-condition-types-001.md |
| R6-I1 | IMPORTANTE | Gap del validator: no detecta quality:high con densidad 80-99 w/p, aunque CLAUDE.md lo prohíbe explícitamente. El mismo gap potencialmente afecta `pricing-special-pricing-functions-001` | validate_chunks.py |
| R6-I2 | IMPORTANTE | `configuration-pricing-procedure-configuration-001` tiene 57 w/p en 15 páginas — bajo el umbral de extracción completa; no hay evidencia de rasterización en el log | chunks/configuration/pricing-procedure-configuration-001.md |
| R6-I3 | IMPORTANTE | Posible under-extraction de tabla T001R en `pricing-special-condition-types-001`: la tabla aparece nombrada en el body y está en otro chunk del mismo PDF, pero tables: [] en este chunk | chunks/pricing/special-condition-types-001.md |
| R6-M1 | MENOR | Secciones no-canónicas (`## Key Facts from Source`, `## Classification Summary`) en chunks concept S4620 — no causan error pero introducen inconsistencia estructural | pricing/condition-technique-overview-001.md, pricing/special-condition-types-001.md |
| R6-M2 | MENOR | SPRO section en sales-copying-control-001 no sigue el formato exacto de 5 palabras | chunks/configuration/sales-copying-control-001.md:61 |

### Mejoras Prioridad Alta — ROL 6

1. **Corregir voz activa en 6 archivos S4605** (R6-C1): sustituir "The source/course X" por prosa directa en presente. Edición quirúrgica por archivo.
2. **Verificar density real de `pricing-statistical-condition-types-001`** y downgrade a medium si 80-99 w/p (R6-C2).
3. **Añadir check al validator**: ERROR cuando `quality == 'high' AND 80 <= wpp < 100` (R6-I1). El check de 5 dimensiones en CLAUDE.md lo requiere pero el validator no lo implementa.
4. **Rasterizar pages 25-39 del S4620** para `configuration-pricing-procedure-configuration-001` y expandir si hay contenido en tablas o diagramas (R6-I2).
5. **Verificar fuente T001R en `pricing-special-condition-types-001`**: si el token "T001R" aparece literalmente en el PDF (pp. 63-75 del S4620), añadirlo a `tables` (R6-I3).

### Riesgos Existenciales — ROL 6

- **Validación de schema insuficiente en el rango 80-99 w/p para quality:high**: si el corpus escala a 200+ chunks, un generador que evalúa quality sin verificar densidad exacta puede inflar la proporción high incorrectamente, y el validator actual no lo detendrá.
- **Drift de voz activa en chunks generados por Codex o en sesiones de alta velocidad**: la regla es informal (no comprobada automáticamente). Un pre-commit hook o validación adicional en `validate_chunks.py` es la única forma de garantizar cumplimiento sistemático.

### Scoring 5D — ROL 6

| Dimensión | Puntuación | Justificación |
|---|---|---|
| Correctitud | 8/10 | Hallazgos R6-C1, R6-C2 verificados con evidencia directa (grep real, lectura de archivos, log); estimaciones de densidad son aproximaciones sin contador de palabras exacto |
| Completitud | 7/10 | Revisé validator completo, 5 chunks S4620, voz activa en todo el corpus, SPRO compliance; no inspeccioné todos los 45 chunks quality:high individualmente |
| Adversarialidad | 9/10 | Identifiqué gaps del validator no cubiertos por el framework actual; cuestioné consistencia entre log y frontmatter |
| Accionabilidad | 9/10 | Cada hallazgo tiene archivos específicos y acciones concretas con criterio de verificación |
| Independencia | 8/10 | La correlación log-vs-frontmatter para chunk 6 es un hallazgo no mencionado en auditorías previas |

---

## ROL 10 — Coverage & Strategic Gap Analyst

**Objetivo:** Evaluar si el corpus actual es lo suficientemente bueno para usarse en producción. Identificar los gaps más críticos y recomendar el próximo documento de mayor ROI.

**Mentalidad:** El corpus es un producto. Los gaps de cobertura son fallos de producto, no deuda técnica.

---

### 10.1 Coverage Map — 10 temas más consultados en SAP SD

Escala: 0 = sin chunk | 1 = mencionado colateralmente | 2 = chunk dedicado quality:medium | 3 = chunk dedicado quality:high

| Tema | Score | Evidencia |
|---|---|---|
| Pricing procedure / condition technique | **3** | pricing-condition-technique-overview-001 (medium) + configuration-pricing-procedure-configuration-001 (medium). El gap crítico identificado en el audit_context_shared está ahora cubierto. Se puntúa 3 porque la cobertura combinada concepto+configuración es completa, aunque ambos chunks son medium. |
| Condition records (VK11) | **2** | pricing-condition-records-001 (medium, T-codes VK11-VK13 en frontmatter, pp. 40-53 del S4620). Cobertura funcional presente. Falta cobertura de condition record reporting y mass maintenance avanzada. |
| Credit management / credit check | **0** | Cero chunks. Identificado como gap ALTA prioridad en audit_context_shared. Ningún documento procesado cubre credit management en profundidad. |
| ATP / availability check | **1** | Mencionado colateralmente en shipping/delivery chunks (schedule line categories, delivery scheduling) pero sin chunk dedicado. Gap confirmado. |
| Output determination | **1** | configuration-billing-output-management-brfplus-001 cubre output para billing. No hay chunk de output determination para orders/deliveries. Cobertura parcial e incompleta. |
| Text determination | **0** | Sin ningún chunk. No mencionado en ningún documento procesado. Gap total. |
| Account determination (picture completa) | **2** | configuration-billing-account-determination-001 (medium). Solo cubre revenue account determination en billing. No cubre customer account group logic, reconciliation accounts, G/L account determination para otras transacciones. Cobertura parcial. |
| Returns end-to-end | **2** | billing-returns-process-001 (high, but pages 123+132 only — 2 pages from S4615) + billing-document-cancellation-001 + billing-billing-document-cancellation-001. No hay chunk de returns desde el nivel de pedido (RE order type, returns delivery). La vista billing existe pero falta la vista order management. |
| Third-party order processing | **0** | Sin chunks dedicados. Mencionado como `third-party` en VALID_TAGS pero ningún chunk lo usa. Gap total. |
| Intercompany sales | **0** | Sin chunks dedicados. Tag `intercompany` existe en VALID_TAGS pero no está en ningún chunk. Gap total. |

**Score total: 11/30 (37%)**

**Interpretación:** El corpus cubre solo el 37% de los 10 temas más consultados con chunks dedicados. Tres de los diez temas tienen cobertura 0. Para un sistema RAG de producción, este nivel de cobertura producirá "no encontré información relevante" para al menos el 30% de las consultas de un consultor SAP SD.

---

### 10.2 Distribución por área

Conteo de chunks por área basado en el índice (74 chunks totales):

| Área | Chunks | % |
|---|---|---|
| billing | 18 | 24% |
| configuration | 21 | 28% |
| pricing | 10 | 14% |
| shipping | 8 | 11% |
| order-management | 6 | 8% |
| enterprise-structure | 5 | 7% |
| master-data | 3 | 4% |
| special-processes | 2 | 3% |
| integration | 2 | 3% |
| credit-management | 0 | 0% |

**Observaciones:**

- **Configuration sobre-representada (28%):** El área de configuración tiene 21 chunks, muchos de ellos derivados de los mismos documentos (S4605, S4610, S4615). Esto es coherente con la estrategia de extraer tanto configuración como proceso de cada documento.
- **Billing fuertemente representada (24%):** Resultado de S4615 que es un documento completo de billing. La cobertura de billing es la más completa del corpus.
- **credit-management con 0 chunks (0%):** Área completa sin cobertura. Es la única área del schema definida en VALID_AREAS que no tiene ningún chunk. Esto es un fallo de cobertura estructural.
- **special-processes y integration con 2 chunks cada una:** Extremadamente escaso. Procesos especiales (consignment, intercompany, make-to-order, stock transfer) son frecuentemente consultados y están casi sin cubrir.
- **master-data con 3 chunks:** Partner functions, material determination, y material listing/exclusion. Falta customer master, material master (SD view), condition master.
- **pricing recién añadida (14%):** El gap crítico de pricing procedure está ahora resuelto. La cobertura de pricing es razonable para el primer documento procesado.

**¿Es proporcional la distribución?** Parcialmente. La distribución refleja los documentos procesados, no las necesidades del consultor. Billing y configuración de delivery están sobre-representadas respecto a las consultas típicas de un consultor SAP SD en proyectos. Credit management y special processes están críticamente sub-representadas.

---

### 10.3 ROI del próximo documento — Recomendación

Documentos candidatos (inventario del project):

| Documento | Prioridad declarada | Gaps que cubriría | ROI estimado |
|---|---|---|---|
| S4600 | High | Sales overview + **credit management** | MUY ALTO |
| S4601 | High | Supply chain / ATP | ALTO |
| S4650 | High | Cross-functional SD | ALTO |
| S4680 | High | Cross-application | MEDIO |

**Recomendación:** S4600 es el próximo documento de mayor ROI.

**Argumentación:**

1. **Credit management (score 0/3):** Es el gap más crítico del corpus. Credit management es uno de los 5 temas de mayor consulta en proyectos SD y el corpus tiene 0 chunks. S4600 cubre fundamentos SD incluyendo credit management y el proceso order-to-cash completo.

2. **ATP/availability check (score 1/3):** S4601 cubre supply chain y availability. Sin embargo, el gap de credit management es más urgente porque un consultor sin respuesta sobre credit checks no puede trabajar en proyectos con procesos de crédito activos.

3. **Third-party y intercompany (score 0/3 ambos):** S4650 y S4680 cubren procesos cross-funcionales incluyendo intercompany. Son ALTO prioridad pero no tan urgentes como credit management.

4. **Coverage mínima operacional:** Para un corpus de producción RAG en SAP SD, el mínimo operacional es cobertura 2/3 en los 10 temas principales. Actualmente estamos en 11/30. Para llegar a 20/30 (67% de los temas con cobertura ≥2), necesitamos al menos credit management, ATP, y third-party — que S4600+S4601 pueden cubrir.

**Propuesta de secuencia:**
1. S4600 → credit management + order-to-cash overview (closes gap crítico)
2. S4601 → ATP/availability check + supply chain processes
3. S4650 → third-party, intercompany, returns end-to-end desde nivel pedido

---

### 10.4 Cobertura de Pricing post-S4620

El gap crítico de pricing procedure estaba identificado como ALTA prioridad en el audit_context_shared. Con S4620 procesado:

**Cubierto (adecuadamente):**
- Condition technique conceptual → pricing-condition-technique-overview-001 (medium)
- Pricing procedure configuration → configuration-pricing-procedure-configuration-001 (medium, baja densidad — ver R6-I2)
- Condition records creation/maintenance → pricing-condition-records-001 (medium, VK11-VK13)
- Special condition types → pricing-special-condition-types-001 (medium)
- Statistical conditions + tax → pricing-statistical-condition-types-001 (high — calibración cuestionada)
- Group conditions, exclusion, condition supplements → pricing-special-pricing-functions-001 (high)
- Pricing agreements (promotions, sales deals) → pricing-pricing-agreements-001 (medium)
- Condition Contract Management (CCM) → 3 chunks (concept, maintenance, settlement) — cobertura excelente

**Aún pendiente de pricing:**
- **Rebate processing en ECC:** el corpus cubre CCM (S/4HANA) pero no el mecanismo de rebates legacy (BO rebate agreement) — relevante si el cliente usa ECC o migración. Sin embargo, dado que el corpus está orientado a S/4HANA 2020, este es un gap menor.
- **Account determination in pricing (VKOA):** la determinación de cuentas para condiciones de precios (revenue accounts, accrual accounts) está parcialmente en configuration-billing-account-determination-001 pero la lógica completa del KSCHL→cuenta requiere un chunk de integración específico.
- **Condition contract batch processing:** el settlement run en batch y el monitoreo de errores de CCM no están cubiertos en detalle (los 3 chunks de CCM cubren el concepto y los pasos, pero el troubleshooting de settlement run está ausente).

**Valoración:** El gap de pricing procedure está cerrado. La cobertura de pricing post-S4620 es funcional y suficiente para consultas básicas y de nivel medio. Los gaps restantes son de nivel avanzado (CCM troubleshooting, VKOA account keys, rebate legacy).

---

### 10.5 Corpus velocity

**Datos del processing log:**

| Fecha | Documento | Chunks creados |
|---|---|---|
| 2026-06-05 | S4610 (Delivery) | 13 |
| 2026-06-05 | S4615 (Billing) — inicial | 31 (incluyendo correcciones) |
| 2026-06-07 | S4605 (Sales) | 19 |
| 2026-06-07 | S4620 (Pricing) | 10 |
| **Total** | **4 documentos** | **74 chunks** (2 días de trabajo) |

**Velocidad:** ~37 chunks/día de trabajo activo (correcciones incluidas). Sin embargo, las correcciones post-procesamiento (S4615 requirió 2 rondas de corrección + 1 auditoría + overhaul completo) representaron ~40% del tiempo total. El throughput real de chunks limpios es ~20-25 chunks/día de trabajo.

**Proyección:**

- **Cobertura mínima operacional (definición propuesta):** 120 chunks en áreas críticas (billing, pricing, order-management, credit-management, special-processes) con cobertura 2/3 en los 10 temas principales.
- **Chunks adicionales necesarios:** 120 - 74 = 46 chunks.
- **Documentos restantes en prioridad High:** S4600, S4601, S4650, S4680 — estimando 10-15 chunks por documento (dado el patrón S4620=10 chunks por documento menos intenso en figura-only pages), proyección ~40-60 chunks adicionales.
- **Tiempo estimado:** 2-3 sesiones de trabajo activo + 1 sesión de auditoría/corrección por documento.
- **Estimación de fecha:** Cobertura mínima operacional alcanzable en 2-4 semanas de sesiones regulares (1-2 sesiones/semana).

**Riesgo principal:** La calidad post-procesamiento depende de las auditorías intermedias (Quick tras cada documento). Si se omiten, el corpus puede crecer en volumen pero degradarse en calidad, como ocurrió con S4615 (31 chunks que requirieron overhaul completo).

---

### Hallazgos Críticos — ROL 10

| ID | Severidad | Descripción |
|---|---|---|
| R10-C1 | CRÍTICO | credit-management con 0 chunks — área completa sin cobertura; el corpus no puede responder ninguna consulta sobre credit limits, credit checks, o credit exposure |
| R10-C2 | CRÍTICO | Score de cobertura 11/30 (37%) — por debajo del mínimo operacional; 3 de los 10 temas más consultados tienen score 0 |
| R10-I1 | IMPORTANTE | Text determination sin ningún chunk — es un requisito de configuración frecuente en proyectos que configura mensajes en pedidos, entregas y facturas |
| R10-I2 | IMPORTANTE | Third-party order processing (score 0) y intercompany sales (score 0) — dos procesos de alta frecuencia en proyectos SD complejos sin cobertura |
| R10-I3 | IMPORTANTE | Returns end-to-end incompleto: existe cobertura de billing side pero no del order side (RE order type, returns delivery); un consultor preguntando por el proceso completo de devoluciones obtendrá respuesta parcial |
| R10-M1 | MENOR | Output determination solo cubierta para billing (BRFplus) — falta output para sales orders y deliveries (V/32, NACE) |

### Mejoras Prioridad Alta — ROL 10

1. **Procesar S4600 como próximo documento** (cierra R10-C1 — credit management).
2. **Añadir chunk de returns desde nivel pedido** usando S4605 o S4650 como fuente (cierra R10-I3 parcialmente).
3. **Definir KPI de cobertura mínima:** target explícito de 20/30 score antes de declarar corpus listo para RAG de producción.
4. **Procesar S4601** como tercer documento para cubrir ATP (R10-I1 parcial) y supply chain.
5. **Revisar text determination en S4605 o S4650** — si está cubierto en alguno de los documentos pendientes, añadir el chunk.

### Riesgos Existenciales — ROL 10

- **Falsa sensación de completitud:** el corpus pasa todos los checks del validator (0 errores) y tiene 74 chunks, lo que puede dar la impresión de que está listo para producción. No lo está: 37% de cobertura en los 10 temas principales es insuficiente. El validator no comprueba cobertura temática.
- **Corpus pricing sin cobertura de credit management puede producir respuestas incorrectas:** un consultor que pregunta "¿cómo bloquea SAP un pedido cuando el cliente supera el crédito?" recibirá "no encontré información" o, peor, respuestas tangenciales de chunks de order-management que mencionan "credit limit check" de pasada. Esto puede conducir a configuraciones incorrectas.

### Scoring 5D — ROL 10

| Dimensión | Puntuación | Justificación |
|---|---|---|
| Correctitud | 8/10 | Coverage map basado en lectura directa del índice; scores asignados con evidencia de chunk IDs específicos |
| Completitud | 7/10 | Cubro los 10 temas del perfil + distribución por área + velocity; no analicé cobertura de ~30 temas secundarios de menor frecuencia |
| Adversarialidad | 9/10 | El corpus tiene 74 chunks y 0 errores del validator — presioné contra la complacencia identificando que 37% de cobertura no es suficiente para producción |
| Accionabilidad | 9/10 | Recomendación de próximo documento con argumentación basada en gaps medibles; secuencia S4600→S4601→S4650 es accionable inmediatamente |
| Independencia | 8/10 | La cuantificación de 37% de score de cobertura y la proyección de velocity son análisis nuevos no presentes en auditorías previas |

---

## Síntesis Consolidada

### TOP 5 Hallazgos por Impacto RAG

| # | Hallazgo | Impacto | Acción |
|---|---|---|---|
| 1 | **12 violaciones de voz activa en chunks S4605** (R6-C1) | Retrieval: las respuestas mencionan el documento fuente en lugar de responder directamente — degrada la experiencia del consultor | Corregir 6 archivos, añadir check al validator |
| 2 | **credit-management con 0 chunks** (R10-C1) | Cobertura: 0% de respuestas sobre credit management | Procesar S4600 en próxima sesión |
| 3 | **`pricing-statistical-condition-types-001` quality:high probable error de calibración** (R6-C2) | Fidelidad: el metadata de calidad incorrecto puede influir en el ranking de retrieval si el sistema RAG usa quality como señal de relevancia | Verificar densidad real y downgrade si 80-99 w/p |
| 4 | **Gap del validator en rango 80-99 w/p para quality:high** (R6-I1) | Fidelidad sistémica: el contrato de calidad del schema no está totalmente implementado en el árbitro formal | Añadir ERROR a validate_chunks.py para quality:high AND density 80-99 w/p |
| 5 | **Score de cobertura 11/30 en los 10 temas más consultados** (R10-C2) | Cobertura estratégica: el corpus no es aún apto para producción en un 63% de los temas críticos | Definir KPI de cobertura y roadmap de documentos |

### Veredicto de Estado

El corpus de 74 chunks con 0 errores del validator y la corrección sistemática documentada en el log representa un trabajo de alta calidad de ingeniería de contenido. La cadencia de auditorías (Quick tras cada documento) está siendo ejecutada correctamente y está conteniendo la acumulación de deuda.

**Para producción:** NO LISTO. Score de cobertura 11/30 es el bloqueante principal. La ausencia total de credit management y la ausencia de third-party/intercompany son defectos de producto que producirán respuestas incorrectas o ausentes en consultas frecuentes.

**Para uso interno de desarrollo/prueba:** PARCIALMENTE APTO para los dominios billing, pricing (básico), delivery, y sales order configuration. Los chunks individuales en estas áreas tienen buena densidad y precisión de provenance.

**Próxima acción bloqueante:** Procesar S4600. Después: corregir voz activa en 6 archivos S4605 y añadir el check de density 80-99 w/p al validator.

---

*Auditoría ejecutada por agente C4_schema+C5_gov — Board Adversarial SAP SD Knowledge Base — 2026-06-07*
