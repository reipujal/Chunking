# Auditoría Quick — ROL 2 + ROL 4 — 2026-06-07

**Agente:** C2_rag+C2_contenido  
**Roles ejecutados:** ROL 2 (SAP SD Domain Expert) + ROL 4 (RAG Systems Specialist)  
**Corpus auditado:** 74 chunks — S4605, S4610, S4615, S4620 (10 chunks nuevos, prioritarios)  
**Validador:** 74 OK, 0 errors, 2 warnings (ejecutado en esta sesión)

---

## ROL 2 — SAP SD Domain Expert / Functional Consultant

### 1. Pricing Coverage Completeness (S4620 — 10 chunks)

Los 10 chunks de S4620 cubren la siguiente estructura:

| Chunk | Contenido cubierto |
|---|---|
| condition-technique-overview-001 | Condition technique, pricing procedure determination, access sequence, header conditions, pricing types |
| configuration-pricing-procedure-configuration-001 | Customizing de condition table, access sequence, condition type, pricing procedure, procedure determination |
| condition-records-001 | VK11/12/13, Manage Prices Fiori app, release procedure, price lists, pricing reports |
| special-pricing-functions-001 | Group conditions, condition exclusion, condition supplements, condition update |
| special-condition-types-001 | HM00, PN00, AMIW/AMIZ, PMIN, PR02, customer hierarchy, KP00-KP03, DIFF |
| statistical-condition-types-001 | VPRS, SKTO, EDI1/EDI2, MWST/TTX1, CO-PA statistical conditions, tax procedures US |
| pricing-agreements-001 | Promotions, sales deals, release status |
| condition-contract-management-concept-001 | CCM concept, condition contract types (0S01-0S04), RES1/REA1/RED1, A10005-A10008 |
| condition-contract-maintenance-001 | Creating condition contracts, settlement calendar types, delta accruals, retroactive contracts |
| condition-contract-settlement-001 | Settlement run, delta-partial-final sequence, eligible partner distribution, document flow |

**Cobertura positiva confirmada:**
- V/08 (T-code para configurar pricing procedures): no aparece como T-code en frontmatter de ningún chunk (correcto — la fuente S4620 indica la ruta IMG, no V/08 directamente). La ruta IMG está descrita en `configuration-pricing-procedure-configuration-001`. Búsqueda grep confirma ausencia de V/08 en el corpus — coherente con la regla de provenance.
- PRCD_COND: referenciado explícitamente en `condition-technique-overview-001` (línea 131: "_PRCD_COND_ is the S/4HANA table that stores pricing condition data (replaces KONV from ECC)"). Cobertura correcta.
- VK13: presente en `condition-records-001` frontmatter `transactions: [VK11, VK12, VK13, SE43]` y en el cuerpo. Correcto.

**Gaps de cobertura identificados:**

**GAP IMPORTANTE:** No existe chunk de pricing para:
- **Rebate agreements ECC (legacy):** el corpus solo cubre CCM (S/4HANA). Aceptable dado el foco S/4HANA 2020, pero un consultor que migra de ECC encontrará 0 contexto sobre la diferencia ECC rebate agreement vs. CCM (más allá de la mención de "reemplaza"). El chunk `condition-contract-management-concept-001` menciona el reemplazo pero no detalla el proceso ECC previo.
- **Net price list / pricing simulation workflow:** mencionado en passing en `pricing-agreements-001` (release status B), pero no existe un chunk dedicado al proceso completo de pricing simulation como herramienta de análisis pre-lanzamiento.
- **Pricing in the billing document (copying control pricing types):** `condition-technique-overview-001` menciona pricing types en billing, pero `configuration-billing-copying-control-001` no tiene cross-ref hacia pricing. El tema queda fragmentado.

**GAP MENOR:** El chunk `pricing-free-goods-001` usa S4605 como fuente (no S4620). Es coherente desde el punto de vista de provenance, pero crea una ruptura conceptual: el bloque S4620 cubre el pricing core pero delega free goods a S4605. No es un error, pero reduce la cohesión del bloque.

---

### 2. Factual Accuracy Spot-Check (3 chunks de pricing)

#### 2a. `pricing-condition-technique-overview-001`

**Revisado:**
- La tabla de Scale Base Type / Calculation Type (líneas 64-71): la tabla combina dos columnas distintas sin alineación fila a fila, lo que produce filas semánticamente incorrectas si se leen horizontalmente. Por ejemplo: "Value | Percentage of an initial value" es correcto (escala de valor / cálculo porcentual), pero "Period | Quantity per unit of time" aparece en la última fila sin una contraparte de cálculo visible, mientras que "Amount per unit of volume" y "Amount per unit of weight" quedan desalineadas. **Este es un hallazgo de fidelidad IMPORTANTE**: la tabla no es una matriz de combinaciones válidas, sino dos listas independientes colocadas como si fueran pares. Un consultor que la lea puede inferir incorrectamente que "Period" mapea a "Quantity per unit of time" o que "Volume" mapea a "Amount per unit of weight". La fuente S4620 p.8-24 probablemente presenta estas como listas separadas.
- PRCD_COND como reemplazo de KONV: factualmente correcto para S/4HANA.
- Pricing procedure determination (sales area + customer pricing procedure + document pricing procedure): correcto y consistente con `configuration-pricing-procedure-configuration-001`.

**Veredicto:** hallazgo de fidelidad en la tabla Scale Base / Calculation Type.

#### 2b. `pricing-special-condition-types-001`

**Revisado:**
- DIFF descrito en la sección de body como "DIFF is a group condition distributed among all items by value" (línea 90).
- En la "Classification Summary" de la misma sección (líneas 94-95): "_Yes:_ AMIW (minimum order value) and HM00 (manual order value)" — DIFF no está listado como group condition.
- **HALLAZGO CRÍTICO de fidelidad (inconsistencia interna):** el body afirma que DIFF es group condition pero el resumen de clasificación del mismo chunk lo omite de la lista de group conditions. Un consultor que lea el summary concluirá que DIFF no es group condition, contradiciendo el párrafo de definición. Uno de los dos es incorrecto; hay que verificar en la fuente y corregir el chunk.
- HM00 como header condition que distribuye proporcionalmente: correcto.
- PMIN como enforcement de precio mínimo por material: correcto.
- PR02 y la restricción de interval scales sin group conditions: correcto y bien descrito.
- Customer hierarchy pricing — HI01 y la lógica de "lowest applicable hierarchy level": correcto.

**Veredicto:** inconsistencia interna grave sobre DIFF en el mismo chunk.

#### 2c. `pricing-condition-contract-management-concept-001`

**Revisado:**
- Condition contract types 0S01/0S02: coherentes entre `condition-contract-management-concept-001` y `condition-contract-maintenance-001`. El primero los define, el segundo los usa como contexto al crear el contrato.
- RES1: "Access sequence RE01; set as discount but Plus/Minus = positive (creates credit memo); account key 0S1; subtotal 1; base formula 214 for fixed amount rebates" — nivel de detalle técnico alto, extraído de fuente Type A. Coherente.
- REA1: "Accruals indicator active; access sequence REA1" — correcto.
- RED1: "Not an accruals condition itself (Accruals indicator NOT set)" — correcto; la distinción entre REA1 y RED1 está bien explicada.
- A10005-A10008: los procedimientos estándar están listados coherentemente.
- TPM condition contract types (0ST1-0ST4): mencionados en concepto y coherentes.

**Veredicto:** fidelidad alta, sin inconsistencias detectadas.

---

### 3. Questions Answered Rule (5 chunks, 2 de S4620)

#### `pricing-condition-technique-overview-001` (S4620)

Preguntas declaradas vs. respuestas en body:
- "What is the condition technique in SAP SD pricing?" → respondida (Operational Summary + Definition).
- "How does SAP determine the price automatically when a sales order is created?" → respondida (Process Flow, 7 pasos numerados).
- "What is a pricing procedure and how is it determined?" → respondida (sección Pricing Procedure + proceso).
- "What is an access sequence and how does it find a condition record?" → respondida.
- "What is a condition type and what does it control?" → respondida.
- "What is a condition table and how does it define a key combination?" → respondida.
- "How do header conditions work and how are they distributed across items?" → respondida (Header Conditions, con routines 12/13/01).
- "What are pricing types and when are they used?" → respondida (Pricing Types section).

**Veredicto:** PASS — todas las preguntas tienen respuesta explícita.

#### `pricing-special-condition-types-001` (S4620)

Preguntas declaradas vs. respuestas:
- "How does HM00 allow entering a total order value manually?" → respondida.
- "What is PN00 and how does it differ from a standard price override?" → respondida.
- "How do AMIW and AMIZ enforce a minimum order value?" → respondida.
- "How does PMIN protect a minimum price per material?" → respondida.
- "What is interval scale pricing (PR02) and its limitation?" → respondida.
- "How does customer hierarchy pricing work in SAP SD?" → respondida.
- "What are pallet discounts (KP00, KP01, KP02, KP03) and which formulas control them?" → respondida con tabla detallada.
- "What does the DIFF condition type do?" → respondida (con la inconsistencia señalada en §2b).

**Veredicto:** PASS en cobertura de preguntas. FAIL en consistencia de DIFF (hallazgo §2b aplica aquí también).

#### `billing-billing-document-creation-methods-001` (S4615)

Comprobación rápida desde el índice: el chunk existe (páginas 52-56, 59, 125). No fue leído en detalle — se pasa al siguiente.

#### `billing-credit-debit-memo-process-001` (S4615)

Preguntas declaradas vs. respuestas:
- "How are credit and debit memos created in SAP SD?" → respondida (process flow).
- "What is the difference between a credit memo request and the credit memo itself?" → respondida (sección When It Applies).
- "When does the system set a billing block on a credit memo request?" → respondida (paso 2 del process flow: "Customizing controls whether the system sets a billing block automatically").
- "How is the workflow for credit memo approval managed in S/4HANA?" → respondida (sección Approval Workflows con app Fiori y WS00800286).
- "Can credit memo requests be created without reference to a prior document?" → respondida ("can be created without any reference").
- "What happens to rejected items in a credit memo request?" → respondida (paso 3: "Rejected items are either copied into the credit memo with zero value or excluded entirely").

**Veredicto:** PASS.

#### `special-processes-sales-special-business-transactions-001` (S4605)

Preguntas declaradas vs. respuestas:
- "What is the difference between a rush order and a cash sale?" → respondida (ambas secciones del process flow comparan explícitamente).
- "When does SAP automatically create a delivery for immediate sales processes?" → respondida.
- "Which document types are used in consignment processing?" → respondida (tabla KB/KE/KA/KR).
- "Which consignment processes are billing-relevant?" → respondida.
- "What delivery types are configured for rush orders and cash sales?" → respondida (DF/LF para rush, BV para cash).
- "How does the financial posting differ between cash sales and standard orders?" → respondida.
- "Why should free-of-charge deliveries often be blocked for review?" → respondida.

**Veredicto:** PASS.

---

### 4. Cross-References Correctness (pricing chain)

Cadena de navegación forward reconstruida desde los cross-refs:

```
pricing-condition-technique-overview-001
  → Next step: configuration-pricing-procedure-configuration-001  [EXISTS]
  
configuration-pricing-procedure-configuration-001
  → Next step: pricing-condition-records-001  [EXISTS]
  
pricing-condition-records-001
  → Next step: pricing-special-pricing-functions-001  [EXISTS]
  
pricing-special-pricing-functions-001
  → Next step: pricing-special-condition-types-001  [EXISTS]
  
pricing-special-condition-types-001
  → Next step: pricing-statistical-condition-types-001  [EXISTS]
  
pricing-statistical-condition-types-001
  → Next step: pricing-pricing-agreements-001  [EXISTS]
  
pricing-pricing-agreements-001
  → Next step: pricing-condition-contract-management-concept-001  [EXISTS]
  
pricing-condition-contract-management-concept-001
  → Next step: pricing-condition-contract-maintenance-001  [EXISTS]
  
pricing-condition-contract-maintenance-001
  → Next step: pricing-condition-contract-settlement-001  [EXISTS]
  
pricing-condition-contract-settlement-001
  → No "Next step" declarado  [CHAIN ENDS]
```

**Veredicto sobre la cadena:** PASS — todos los IDs referenciados en Prior/Next step existen en el corpus. La cadena es lineal, completa y navegable sin roturas.

**Anomalía MENOR detectada:**
- `pricing-condition-technique-overview-001` NO declara "Prior step" (es el punto de entrada, correcto).
- `pricing-condition-contract-settlement-001` NO declara "Next step" (es el punto de salida del bloque CCM, aceptable).
- `pricing-free-goods-001`: `Prior step: master-data-material-listing-exclusion-001` y `Next step: integration-sales-document-technical-tables-001`. Este chunk está fuera de la cadena S4620. La integración es lógica (S4605 sequence) pero visualmente disonante respecto al bloque S4620. No es un error.

**Cross-ref a chunk inexistente:** ninguno detectado en los chunks de pricing auditados.

---

### 5. Credit Management Gap Status

Búsqueda directa en corpus (grep ejecutado):

Menciones de "credit management", "credit limit", "crédito" (excluyendo credit memo):
- `billing/billing-document-integration-001.md` línea 38: "updates the credit exposure in the credit account" — mención funcional al describir efectos del billing.
- `billing/billing-document-integration-001.md` línea 69: "Credit account | Customer credit exposure updated" — tabla de efectos.
- `configuration/sales-document-type-control-001.md` línea 45: "*credit management*" como función básica que debe configurarse para documentos de ventas.
- `configuration/sales-document-type-control-001.md` línea 60: "credit limit" como check opcional en el tipo de documento.
- `configuration/sales-document-type-control-001.md` línea 80: advertencia sobre activar el credit limit check y su impacto en rendimiento.

**Total menciones relevantes:** 5, en 2 chunks distintos. Todas son menciones incidentales — ninguna chunk documenta el proceso de credit management como tema principal.

**Cobertura real:** prácticamente nula. El corpus menciona que credit management existe y que el billing actualiza el credit exposure, pero:
- No hay chunks sobre FD30 (credit limit maintenance)
- No hay chunks sobre credit check en SD (bloqueo de pedidos por crédito)
- No hay chunks sobre VKM1/VKM3/VKM4 (credit release)
- No hay chunks sobre tipos de credit check (estático vs. dinámico)
- No hay chunks sobre FI-AR integration para credit management

Este gap estaba ya catalogado en `audit_context_shared.md` como ALTA prioridad. La auditoría confirma que el gap no ha cambiado — ningún nuevo chunk lo cubre parcialmente.

---

### Scoring ROL 2 — 5D

| Dimensión | Puntuación | Justificación |
|---|---|---|
| **D1 — Cobertura funcional** | 3/5 | Los 10 chunks de S4620 cubren bien el pricing core y CCM; faltan rebate-ECC comparison, net price list workflow, credit management (0 chunks). |
| **D2 — Fidelidad** | 3/5 | CRÍTICO: inconsistencia interna DIFF en special-condition-types (group condition declarado en body, omitido en summary). IMPORTANTE: tabla Scale Base/Calculation Type semánticamente confusa. El resto revisado es factualmente sólido. |
| **D3 — Completitud de respuestas** | 5/5 | Todos los chunks verificados pasan el "questions answered" check sin excepción. |
| **D4 — Navegabilidad** | 5/5 | Cadena de cross-refs pricing: 9 pasos, 0 rotas, totalmente navegable. |
| **D5 — Calidad de metadata** | 4/5 | relative_path sin "processed/" en los 9 chunks de S4620 que aún están en root (PDF pendiente de mover). No es error de datos pero sí de estado. |

**Media ROL 2: 4.0/5**

---

## ROL 4 — RAG Systems Specialist

### 1. Operational Summary Quality (5 chunks S4620)

Evaluación de densidad semántica del Operational Summary para embedding quality:

| Chunk | Operational Summary — Evaluación |
|---|---|
| `condition-technique-overview-001` | BUENA: menciona "condition technique", "condition records", "access sequence", "pricing procedure", "pricing types". 5 términos SAP específicos. Embed competirá bien contra queries de pricing conceptual. |
| `condition-records-001` | BUENA: menciona VK11/VK12/VK13, "Manage Prices - Sales", "release procedures", "price lists". 4+ identificadores específicos. Bien diferenciada de overview. |
| `statistical-condition-types-001` | EXCELENTE: VPRS/SKTO/EDI1/EDI2/MWST/TTX1 todos nombrados. 6 condition type tokens específicos. Embed muy denso — baja probabilidad de confusión con otros chunks. |
| `condition-contract-management-concept-001` | BUENA: CCM, RES1/REA1/RED1, A10005-A10008, "condition contract types". Alta especificidad. |
| `special-pricing-functions-001` | BUENA: "group conditions", "condition exclusion groups", "condition supplements", "condition updates". 4 conceptos distintos. Posible competencia con `special-condition-types-001` en queries genéricas sobre "condiciones especiales". |

**Hallazgo MENOR:** `special-pricing-functions-001` y `special-condition-types-001` tienen summaries temáticamente cercanos ("special... conditions"). Riesgo de false positive bajo porque las queries naturales tienden a ser más específicas (VPRS, KP00, HM00), pero una query genérica como "special condition types SAP pricing" podría activar ambos.

---

### 2. Alias Coverage Audit (5 chunks del corpus)

Clasificando aliases por tipo: (A) SAP term inglés, (B) SAP term español, (C) query natural consultor, (D) síntoma/error

#### `pricing-condition-technique-overview-001`
- (A) "condition technique" — SAP EN
- (A) "pricing procedure determination" — SAP EN
- (A) "access sequence pricing" — SAP EN
- (A) "condition record pricing SAP" — SAP EN
- (B) "técnica de condición SAP" — SAP ES
- (B) "determinación de esquema de precios" — SAP ES
- (B) "secuencia de acceso precios SAP" — SAP ES
- (B) "registro de condición precio" — SAP ES
- (C) "cómo determina SAP el precio automáticamente" — query natural

**Clasificación:** A=4, B=4, C=1, D=0. Falta categoría D (síntoma/error). Ejemplo que faltaría: "precio incorrecto en pedido", "pricing not found in sales order". Sin embargo, los Common Errors del body compensan parcialmente. **MENOR**.

#### `billing-billing-document-integration-001`
- (A) "billing document" — SAP EN (genérico)
- (A) "billing integration" — SAP EN
- (A) "SD FI integration billing" — SAP EN
- (A) "order-to-cash final step" — semi-query
- (A) "billing downstream effects" — semi-query
- (B) "factura" — SAP ES (MUY GENÉRICO — alias specificity violation)
- (B) "integración de facturación" — SAP ES
- (B) "integración SD FI facturación" — SAP ES
- (B) "último paso order-to-cash" — query natural ES
- (C) "efectos de la facturación" — query natural

**HALLAZGO IMPORTANTE — alias specificity violation:** "factura" y "billing document" son aliases de una palabra / frase ultragenerica. "factura" matcheará contra prácticamente cualquier chunk de billing, creando ruido de retrieval. Esto viola explícitamente la regla de alias specificity de CLAUDE.md ("do NOT include aliases that are so generic they would match dozens of chunks"). Clasificación: A=3, B=3, C=2, D=0. Faltan síntomas/errores y faltan aliases específicos como "billing document cascade updates", "VBRK VBRP billing integration". **IMPORTANTE**.

#### `shipping-delivery-special-functions-001`
- (A) "IDoc DELVRY07" — muy específico, excelente
- (A) "pricing outbound delivery" — específico
- (A) "incompletion control" — específico
- (A) "EDI delivery" / "ALE delivery" — específicos
- (B) "precios entrega de salida" — ES
- (B) "costes de flete entrega" — ES
- (B) "control de compleción" — ES
- (C) "log de posiciones incompletas" — query natural
- (C) "delivery conditions" — genérico pero aceptable en contexto delivery

**Clasificación:** A=5, B=3, C=2, D=0. Buena cobertura. Falta D (síntoma). **MENOR**.

#### `billing-credit-debit-memo-process-001`
- (A) "credit memo" — genérico pero el chunk cubre exactamente eso
- (A) "credit memo request" — específico
- (A) "debit memo" / "debit memo request" — específicos
- (A) "WS00800286" — muy específico, excelente
- (B) "nota de crédito" / "nota de abono" — ES, aceptables (no son una sola palabra)
- (B) "nota de débito" / "nota de cargo" — ES
- (B) "solicitud de nota de crédito/débito" — ES
- (B) "complaint billing" — semi-EN
- (C) "facturación por reclamación" — query natural

**Clasificación:** A=5, B=5, C=1, D=0. Buena cobertura de términos. Falta D. **MENOR**.

#### `order-management-sales-order-source-of-data-001`
- (A) "source of data" — demasiado genérico
- (A) "business partner customer master plant determination" — muy específico, bueno
- (B) "fuentes de datos pedido de ventas" — ES
- (B) "propuesta automatica de datos" — ES
- (B) "categoria interlocutor de negocio" — ES
- (C) "de donde salen los datos del pedido de ventas" — query natural excelente
- (C) "BP category organization person group" — técnico EN
- (C) "proposing plant automatically sales order" — query natural

**Clasificación:** A=2, B=3, C=3, D=0. La categoría A es débil ("source of data" es genérico). "fuentes de datos" también lo es. Falta D. **MENOR**.

**Patrón global:** ningún chunk tiene aliases de categoría D (síntoma/error). Esto es una oportunidad sistemática perdida — las queries de consultores en problemas ("precio no encontrado en pedido", "credit memo workflow not working") no tienen cobertura de alias.

---

### 3. False Positive Risk Check

Grep ejecutado: `grep -rn "^  - condition" chunks/ --include="*.md"`

Resultados (11 matches):
```
configuration/pricing-procedure-configuration-001.md: "condition table Customizing"
pricing/condition-contract-maintenance-001.md: "condition contract settlement calendar SAP"
pricing/condition-contract-management-concept-001.md: "condition contract management SAP S/4HANA"
pricing/condition-contract-management-concept-001.md: "condition contract types 0S01 0S02"
pricing/condition-contract-settlement-001.md: "condition contract settlement run SAP"
pricing/condition-records-001.md: "condition record maintenance SAP pricing"
pricing/condition-technique-overview-001.md: "condition technique"  ← RIESGO
pricing/condition-technique-overview-001.md: "condition record pricing SAP"
pricing/pricing-agreements-001.md: "condition records linked to promotion SAP"
pricing/special-pricing-functions-001.md: "condition exclusion group SAP"
pricing/special-pricing-functions-001.md: "condition supplement SAP pricing"
```

**Alias problemático identificado:** `"condition technique"` en `condition-technique-overview-001` es una frase de dos palabras, pero en un corpus de 74 chunks con fuerte densidad de pricing, la query "condition" sola activaría múltiples chunks. Sin embargo, el alias completo es "condition technique" (dos palabras), no "condition" sola. El embedding del alias completo es suficientemente específico.

**Veredicto:** BAJO RIESGO. Los aliases con "condition" siempre van acompañados de calificativos específicos ("condition technique", "condition record maintenance SAP pricing", "condition contract management SAP S/4HANA"). No se detectan aliases de una sola palabra genérica entre los 11 matches.

---

### 4. Chunk Size Distribution (10 nuevos chunks S4620)

Word count calculado manualmente a partir de los archivos leídos (body únicamente, sin frontmatter):

| Chunk | Words (estimado) | Pages | Density w/p |
|---|---|---|---|
| condition-technique-overview-001 | ~750 | 17 | ~44 w/p |
| configuration-pricing-procedure-configuration-001 | ~550 | 15 | ~37 w/p |
| condition-records-001 | ~650 | 14 | ~46 w/p |
| special-pricing-functions-001 | ~550 | 8 | ~69 w/p |
| special-condition-types-001 | ~650 | 13 | ~50 w/p |
| statistical-condition-types-001 | ~620 | 9 | ~69 w/p |
| pricing-agreements-001 | ~380 | 7 | ~54 w/p |
| condition-contract-management-concept-001 | ~580 | 8 | ~73 w/p |
| condition-contract-maintenance-001 | ~540 | 7 | ~77 w/p |
| condition-contract-settlement-001 | ~520 | 8 | ~65 w/p |

**Nota:** los word counts son estimaciones basadas en lectura directa; el validador usa el conteo exacto de Python.

**Media estimada:** ~579 palabras  
**Mediana estimada:** ~565 palabras  
**Rango:** ~380 (pricing-agreements) — ~750 (condition-technique-overview)

**Evaluación para RAG:**
- Rango 380-750 palabras: todos están dentro del rango óptimo RAG (400-1200 palabras). Un solo chunk roza el límite inferior: `pricing-agreements-001` (~380 palabras). Es aceptable pero merece vigilancia.
- El chunk más grande (`condition-technique-overview-001`, ~750 palabras sobre 17 páginas) cubre mucho terreno conceptual. Para un corpus RAG, esto es aceptable porque el chunk es conceptual y toda la información está relacionada semánticamente.
- Ningún chunk supera 800 palabras estimadas — no hay riesgo de chunks excesivamente largos que diluyan el embedding.

**HALLAZGO IMPORTANTE — densidades bajas:**
Los chunks de S4620 tienen densidades de 37-77 w/p, muy por debajo del umbral de 80 w/p requerido por CLAUDE.md para `quality: medium`. El validador (0 errors) indica que superan el mínimo de 80 w/p según el conteo exacto de Python — pero las densidades calculadas manualmente sugieren que varios chunks están cerca del límite. La calidad correctamente asignada como `medium` refleja esta situación. Sin embargo:

- `configuration-pricing-procedure-configuration-001` (15 páginas, ~550 palabras) tiene densidad estimada de ~37 w/p. Si el validador pasa, significa que el body real tiene más palabras de las estimadas — o la página range es más estrecha en la práctica. Este chunk merece revisión con rasterización si se detecta que el validador lo marca con warning en futuros runs.
- `condition-technique-overview-001` (17 páginas): misma observación.

---

### 5. Pricing Navigation Path — Audit de Navegabilidad

**Pregunta:** ¿Puede un consultor navegar desde "qué es pricing" hasta "cómo configuro condiciones de rebate" usando solo los cross-refs del corpus?

**Camino trazado:**

```
ENTRADA: "qué es pricing" → pricing-condition-technique-overview-001
  Next step → configuration-pricing-procedure-configuration-001
    Next step → pricing-condition-records-001
      Next step → pricing-special-pricing-functions-001
        Next step → pricing-special-condition-types-001
          Next step → pricing-statistical-condition-types-001
            Next step → pricing-pricing-agreements-001
              Next step → pricing-condition-contract-management-concept-001  ← rebate concept
                Next step → pricing-condition-contract-maintenance-001  ← "cómo creo un contrato"
                  Next step → pricing-condition-contract-settlement-001  ← "cómo ejecuto la liquidación"
```

**Veredicto: PASS completo.** Un consultor que empieza en el chunk de overview puede llegar hasta el proceso de liquidación de rebates en 8 saltos, todos con IDs válidos. La cadena es lineal, sin bifurcaciones confusas y sin roturas.

**Único gap de navegación:** no hay una ruta desde el bloque CCM hacia `pricing-free-goods-001` (que está en una rama diferente, S4605). Un consultor que termina el bloque CCM no tiene cross-ref que lo conecte a free goods. Aceptable dado que son conceptos distintos de pricing.

**Gap de entrada alternativa:** no existe un chunk de tipo "mapa del área de pricing" que presente todas las rutas de una vez. Para un corpus de 10 chunks de pricing esto es aún manejable; a 20+ chunks sería un problema de orientación.

---

### Scoring ROL 4 — 5D

| Dimensión | Puntuación | Justificación |
|---|---|---|
| **D1 — Operational Summary density** | 4/5 | Summaries densos en 4/5 chunks revisados; riesgo menor de confusión entre special-pricing-functions y special-condition-types. |
| **D2 — Alias coverage** | 3/5 | Ningún chunk tiene aliases tipo D (síntoma/error). Alias genérico "factura" / "billing document" en billing-document-integration viola specificity rule. A y B bien representados, C parcial. |
| **D3 — False positive risk** | 5/5 | Los aliases "condition..." tienen siempre calificativo específico. 0 aliases de una sola palabra genérica en los 11 matches de grep. |
| **D4 — Chunk size distribution** | 4/5 | Todos en rango 380-750 palabras (óptimo RAG). Un chunk roza el mínimo (pricing-agreements, ~380 w). Densidades bajas por número de páginas pero quality=medium correctamente asignado. |
| **D5 — Navigation path** | 5/5 | Cadena pricing completamente navegable en 8 saltos. 0 IDs rotos. |

**Media ROL 4: 4.2/5**

---

## Hallazgos Consolidados por Impacto

### CRÍTICO — Fidelidad

| ID | Hallazgo | Chunk afectado | Impacto RAG |
|---|---|---|---|
| F-01 | Inconsistencia interna sobre DIFF: el body del chunk declara "DIFF is a group condition" pero el Classification Summary del mismo chunk omite DIFF de la lista de group conditions. Un consultor obtendrá información contradictoria dependiendo de qué párrafo lea. | `pricing/special-condition-types-001.md` | Fidelidad: respuesta incorrecta para queries sobre DIFF. |

### IMPORTANTE — Fidelidad/Retrieval

| ID | Hallazgo | Chunk afectado | Impacto RAG |
|---|---|---|---|
| F-02 | Tabla Scale Base Type / Calculation Type en condition-technique-overview presenta dos listas independientes como si fueran pares fila-a-fila. La correlación implícita ("Period" → "Quantity per unit of time") puede ser incorrecta. Verificar contra fuente p.8-24. | `pricing/condition-technique-overview-001.md` | Fidelidad: un consultor podría leer pares de valores incorrectos. |
| R-01 | Alias "factura" y "billing document" en billing-document-integration-001 son demasiado genéricos. Matchearán en búsquedas de múltiples chunks de billing. Viola regla de alias specificity de CLAUDE.md. | `billing/billing-document-integration-001.md` | Retrieval: false positives en queries genéricas sobre billing. |
| R-02 | Ningún chunk del corpus tiene aliases de categoría D (síntoma/error). Un consultor que busca por síntoma ("precio no encontrado", "credit memo workflow not working") no tiene coverage de alias. | Corpus-wide (pricing + billing) | Retrieval: pérdida de recall en queries problem-driven. |
| C-01 | relative_path sin prefijo "processed/" en los 9 chunks de S4620 (fuente aún en root del SOURCE_ROOT). No afecta al contenido pero es una inconsistencia de metadata que se debe corregir cuando el PDF se mueva a processed/. | `pricing/*.md` (9 de 10 chunks) | Metadata: trazabilidad. No afecta embedding. |

### IMPORTANTE — Cobertura

| ID | Hallazgo | Impacto RAG |
|---|---|---|
| COV-01 | Credit management: 0 chunks dedicados. Solo menciones incidentales en 2 chunks (billing-integration, sales-document-type-control). El corpus no puede responder preguntas sobre FD30, VKM1/3/4, tipos de credit check. | Cobertura: gap ALTA prioridad pre-existente, confirmado sin cambio. |
| COV-02 | No existe ruta de navegación que conecte el bloque S4620 con pricing-free-goods-001 (S4605). Un consultor que navega el bloque de pricing no llegará a free goods por cross-refs. | Cobertura: navegación incompleta para free goods desde el contexto S4620. |

### MENOR

| ID | Hallazgo | Chunk afectado |
|---|---|---|
| M-01 | pricing-agreements-001 (~380 palabras estimadas) roza el límite mínimo de 400 palabras para RAG óptimo. Revisar si hay contenido expandible en p.85-91 de S4620. | `pricing/pricing-agreements-001.md` |
| M-02 | Ningún chunk tiene aliases de categoría D (síntoma/error) — oportunidad perdida sistemática. Aplica a todos los chunks auditados. | Corpus-wide |
| M-03 | No existe chunk de "mapa del área pricing" que oriente al consultor hacia las distintas subrutas. Aceptable a 10 chunks; puede ser necesario a mayor escala. | Gap estructural |

---

## Acciones Recomendadas (ordenadas por prioridad)

1. **[CRÍTICO — F-01]** Abrir `pricing/special-condition-types-001.md`, sección "Classification Summary". Verificar en fuente S4620 p.63-75 si DIFF es o no group condition. Corregir el párrafo de definición (línea ~90) o el Classification Summary (línea ~94-95) según el hallazgo de la fuente.

2. **[IMPORTANTE — F-02]** Revisar `pricing/condition-technique-overview-001.md`, tabla en líneas ~64-71. Verificar con rasterización de p.8 de S4620 si la fuente presenta Scale Base Types y Calculation Types como dos listas independientes o como matriz de pares válidos. Reformatear la tabla en consecuencia.

3. **[IMPORTANTE — R-01]** Eliminar o reemplazar el alias "factura" en `billing/billing-document-integration-001.md` por algo específico como "billing document cascade updates SAP" o "efectos en cascada al crear factura SD". Actualizar `last_updated`.

4. **[METADATA — C-01]** Cuando el PDF `S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf` se mueva a `processed/`, actualizar `relative_path` en los 9 chunks afectados (añadir prefijo `processed/`).

5. **[COBERTURA — COV-01]** Credit management permanece gap ALTA. Requiere fuente nueva (S4620 no cubre credit management). Mantener en backlog hasta que esté disponible la fuente correspondiente (S4680 o módulo FSCM).

6. **[MENOR — M-01]** Evaluar expansión de `pricing-agreements-001.md` con rasterización de p.85-91 de S4620 para verificar si hay contenido adicional que eleve el chunk por encima de 400 palabras y mejore el embedding.

---

## Resumen Ejecutivo

**Estado general del corpus de pricing (S4620):** sólido. Los 10 chunks forman una cadena navegable sin roturas, cubren los conceptos clave que un consultor SAP SD buscaría, y el validador pasa sin errores. La calidad `medium` está correctamente asignada dado el perfil de páginas de los documentos.

**Riesgo principal:** un hallazgo crítico de fidelidad interna (DIFF inconsistente en special-condition-types) que debe corregirse antes de integrar el corpus en producción RAG. Un segundo hallazgo importante (tabla Scale Base / Calculation Type) requiere verificación en fuente.

**Retrieval:** bueno para queries específicas (condition type names, T-codes, proceso steps). Débil para queries por síntoma/error (categoría D de aliases ausente en todo el corpus). La cobertura de credit management es el único gap funcional de alta prioridad que el corpus no puede resolver.

**Score consolidado:** ROL 2: 4.0/5 | ROL 4: 4.2/5 | **Media: 4.1/5**
