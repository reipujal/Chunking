# Faithfulness Harness — Calibration Sample (2026-06-22)

**Generator**: claude-sonnet-4-6 | **Judge**: claude-opus-4-8 | **top-k**: 5

## Positive Set Metrics

| Metric | Value |
|---|---|
| n | 5 |
| mean_grounded_fraction | 0.967 |
| pct_with_any_unsupported | 0.0 |
| release_mixing_incidents | 0 |
| citation_validity_rate | 80.0 |
| gold_in_top_k_rate | 100.0 |
| n_retrieval_misses | 0 |
| pct_miss_abstained | None |
| total_support_reclassified | 0 |

## Abstention Set Metrics

| Metric | Value |
|---|---|
| n | 3 |
| pct_correct_abstention | 66.7 |
| pct_hallucinated | 33.3 |

---

## Positive Questions (review grounding)

### S4600-LA-U1-Q1 (S4600)
**Q**: Which of the following apps gives you a visual overview of complex topics for monitoring or tracking purposes?
**Gold chunks**: configuration-sap-fiori-launchpad-001
**Gold in top-k**: True | **top-k**: order-management-sales-monitoring-analytics-001, configuration-sap-fiori-launchpad-001, billing-create-billing-documents-fiori-001...

**Response**:
```
La pregunta hace referencia a una aplicación que proporciona una **visión visual general de temas complejos** con fines de monitoreo o seguimiento.

Según la documentación proporcionada, las **Analytical Apps** de SAP Fiori son las que cumplen esta función. El documento sobre SAP Fiori Launchpad describe tres tipos de aplicaciones Fiori que cubren diferentes necesidades de interacción:

- **Transaction apps**: para ejecución de procesos
- **Analytical apps**: para **monitoreo** (*monitoring*)
- **Factsheets**: para exploración de datos

Las **Analytical Apps** son específicamente las diseñadas para proporcionar una visión general visual de temas complejos con propósitos de monitoreo o seguimiento.

Fuentes: configuration-sap-fiori-launchpad-001
```

**Judge** — grounded_fraction=0.833 | release_mixing=False | is_abstention=False
- `[PARTIAL]` Las Analytical Apps de SAP Fiori son las que proporcionan una visión visual general de temas complejos con fines de monitoreo.  
  > support: "*analytical apps* for monitoring"
- `[SUPPORTED]` SAP Fiori Launchpad describe tres tipos de aplicaciones Fiori que cubren diferentes necesidades de interacción.  
  > support: "Three types of Fiori apps cover different interaction needs: *transaction apps* for process executio..."
- `[SUPPORTED]` Transaction apps: para ejecución de procesos.  
  > support: "*transaction apps* for process execution"
- `[SUPPORTED]` Analytical apps: para monitoreo.  
  > support: "*analytical apps* for monitoring"
- `[SUPPORTED]` Factsheets: para exploración de datos.  
  > support: "*factsheets* for data exploration"
- `[PARTIAL]` Las Analytical Apps son específicamente las diseñadas para proporcionar una visión general visual de temas complejos con propósitos de monitoreo o seguimiento.  
  > support: "*analytical apps* for monitoring"
**Reclassified supports**: 0
**Citations**: {'has_citation_line': True, 'cited_ids': ['configuration-sap-fiori-launchpad-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

### S4F30-LA-U2-Q1 (S4F30)
**Q**: Choose three components which are part of Advanced Credit Management but are not part of Basic Credit Management.
**Gold chunks**: credit-management-credit-check-sd-integration-001, credit-management-credit-master-data-001, credit-management-credit-rules-engine-001
**Gold in top-k**: True | **top-k**: credit-management-credit-master-data-001, special-processes-advanced-returns-management-001, credit-management-credit-check-sd-integration-001...

**Response**:
```
# Componentes de Advanced Credit Management no presentes en Basic Credit Management

Basándome en los documentos de contexto, los tres componentes que forman parte de **Advanced Credit Management** pero **no** de Basic Credit Management son:

1. **Credit Scoring Rule (Regla de Puntuación de Crédito):** Calcula automáticamente el score crediticio del business partner y deriva la clase de riesgo correspondiente, incluyendo fórmulas configurables con datos del BP, datos transaccionales y calificaciones de agencias externas.

2. **Credit Limit Rule (Regla de Límite de Crédito):** Calcula y propone automáticamente un límite de crédito por segmento de crédito, mediante fórmulas definibles por el usuario.

3. **Credit Eventing (Eventos de Crédito):** Mecanismo que permite construir cadenas de procesos donde un evento crediticio (por ejemplo, cambio en la clase de riesgo o expiración del score) dispara automáticamente actividades de seguimiento.

> *Nota:* El documento también menciona la **integración con agencias externas de crédito** y las **Credit Limit Requests** como capacidades adicionales de Advanced Credit Management. Sin embargo, las tres reglas del Rules Engine (Scoring, Limit y Check Rule) junto con el eventing son explícitamente identificados como parte de Advanced Credit Management y **no disponibles en Basic Credit Management**.

**Fuentes:** credit-management-credit-rules-engine-001, credit-management-credit-master-data-001
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` Credit Scoring Rule calcula automáticamente el score crediticio del business partner y deriva la clase de riesgo correspondiente  
  > support: "The scoring rule automatically calculates the business partner's *credit score* and derives the corr..."
- `[SUPPORTED]` Credit Scoring Rule incluye fórmulas configurables con datos del BP, datos transaccionales y calificaciones de agencias externas  
  > support: "A scoring formula can combine:
- SAP Business Partner master data (preconfigured field selection)
- ..."
- `[SUPPORTED]` Credit Limit Rule calcula y propone automáticamente un límite de crédito por segmento de crédito, mediante fórmulas definibles por el usuario  
  > support: "the *Credit Limit Rule* (calculates and proposes a credit limit per credit segment)"
- `[SUPPORTED]` Credit Eventing es un mecanismo que permite construir cadenas de procesos donde un evento crediticio dispara automáticamente actividades de seguimiento  
  > support: "An *eventing* mechanism allows process chains to be built so that credit events (such as a change in..."
- `[SUPPORTED]` El cambio en la clase de riesgo o expiración del score son ejemplos de eventos crediticios  
  > support: "When the score expires or is invalidated, a credit event is triggered."
- `[SUPPORTED]` Estas reglas (Scoring, Limit, Check Rule) y el eventing son parte de Advanced Credit Management y no disponibles en Basic Credit Management  
  > support: "These capabilities are part of Advanced Credit Management and are not available in Basic Credit Mana..."
- `[SUPPORTED]` El documento también menciona la integración con agencias externas de crédito y las Credit Limit Requests como capacidades adicionales de Advanced Credit Management  
  > support: "*Advanced Credit Management*, which adds formula-based scoring and limit calculation, credit eventin..."
**Reclassified supports**: 0
**Citations**: {'has_citation_line': True, 'cited_ids': ['** credit-management-credit-rules-engine-001', 'credit-management-credit-master-data-001'], 'all_in_corpus': False, 'all_in_top_k': False}
**Abstention regex**: False

### S4600-LA-U1-Q2 (S4600)
**Q**: A user can personalize the home page in SAP Fiori launchpad by default.
**Gold chunks**: configuration-sap-fiori-launchpad-001
**Gold in top-k**: True | **top-k**: configuration-sap-fiori-launchpad-001, billing-create-billing-documents-fiori-001, pricing-condition-records-001...

**Response**:
```
El documento de contexto [ID: configuration-sap-fiori-launchpad-001] menciona que el SAP Fiori Launchpad ofrece capacidades de **personalización** ("personalization"), pero **no especifica si esta funcionalidad está habilitada por defecto para el usuario o si requiere configuración adicional por parte del administrador**.

Por lo tanto, no puedo confirmar ni negar con precisión si un usuario puede personalizar la página de inicio **por defecto** basándome únicamente en la documentación proporcionada.

No puedo responder con la documentación proporcionada.
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=True
- `[SUPPORTED]` El SAP Fiori Launchpad ofrece capacidades de personalización.  
  > support: "a shell that hosts Fiori apps, displays live KPI tiles, and provides navigation, personalization, an..."
- `[SUPPORTED]` El contexto no especifica si esta funcionalidad está habilitada por defecto para el usuario o si requiere configuración adicional por parte del administrador.  
  > support: "a shell that hosts Fiori apps, displays live KPI tiles, and provides navigation, personalization, an..."
- `[SUPPORTED]` No puedo confirmar ni negar si un usuario puede personalizar la página de inicio por defecto basándome únicamente en la documentación proporcionada.  
  > support: "How can users personalize the SAP Fiori Launchpad?"
**Reclassified supports**: 0
**Citations**: {'has_citation_line': False, 'cited_ids': [], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: True

### S4F30-LA-U2-Q2 (S4F30)
**Q**: Which process-relevant relationship types can be maintained in SAP Credit Management?
**Gold chunks**: credit-management-credit-check-sd-integration-001, credit-management-credit-master-data-001
**Gold in top-k**: True | **top-k**: credit-management-credit-master-data-001, credit-management-credit-rules-engine-001, master-data-business-partner-master-data-001...

**Response**:
```
## Process-Relevant Relationship Types in SAP Credit Management

Based on the provided documentation, the context does **not** contain specific information about "process-relevant relationship types" that can be maintained in SAP Credit Management.

The documents cover topics such as:
- The BP role **UKM000** and credit profile/segment structure
- Credit Rules Engine (scoring, limit, and check rules)
- SD integration and credit check triggers
- Documented Credit Decisions (DCDs)

However, none of these documents explicitly describe or list "process-relevant relationship types" as a configurable or maintainable element within SAP Credit Management.

No puedo responder con la documentación proporcionada.
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=True
- `[SUPPORTED]` The context does not contain specific information about process-relevant relationship types that can be maintained in SAP Credit Management.  
  > support: "How can customer hierarchies be modelled in SAP Credit Management?"
- `[SUPPORTED]` The documents cover the BP role UKM000 and credit profile/segment structure.  
  > support: "credit-specific data is maintained in the BP using the dedicated role **UKM000** (*SAP Credit Manage..."
- `[SUPPORTED]` The documents cover the Credit Rules Engine (scoring, limit, and check rules).  
  > support: "provides three types of configurable rules that automate credit evaluation: the *Credit Scoring Rule..."
- `[SUPPORTED]` The documents cover SD integration and credit check triggers.  
  > support: "At which points in the SD process is the credit check triggered?"
- `[SUPPORTED]` The documents cover Documented Credit Decisions (DCDs).  
  > support: "a *Documented Credit Decision* (DCD) is created in Credit Management for structured review and relea..."
- `[SUPPORTED]` None of these documents explicitly describe or list process-relevant relationship types as a configurable or maintainable element within SAP Credit Management.  
  > support: "How can customer hierarchies be modelled in SAP Credit Management?"
**Reclassified supports**: 0
**Citations**: {'has_citation_line': False, 'cited_ids': [], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: True

### S4600-LA-U4-Q1 (S4600)
**Q**: The master data of customers and vendors is managed in SAP S/4HANA by using business partner master data.
**Gold chunks**: master-data-business-partner-master-data-001, master-data-material-master-sd-001
**Gold in top-k**: True | **top-k**: master-data-business-partner-master-data-001, enterprise-structure-shared-master-data-cross-division-001, order-management-sales-monitoring-analytics-001...

**Response**:
```
La afirmación es **correcta**. En SAP S/4HANA, los datos maestros de clientes y proveedores se gestionan mediante el concepto unificado de **Business Partner (BP)**. Este enfoque reemplaza los registros maestros separados de clientes y proveedores que existían en SAP ECC. Un único registro de business partner puede representar tanto a un cliente como a un proveedor, con los datos relevantes activados mediante la asignación de **roles** específicos (por ejemplo, el rol *Customer* para procesos SD y el rol *Vendor* para compras). Los datos centrales como nombre, dirección y datos bancarios se introducen una sola vez, evitando redundancia y mejorando la integridad de los datos.

Fuentes: master-data-business-partner-master-data-001, order-management-sales-order-source-of-data-001
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` En SAP S/4HANA, los datos maestros de clientes y proveedores se gestionan mediante el concepto unificado de Business Partner (BP).  
  > support: "In SAP S/4HANA, customer and vendor master data is managed through the unified *Business Partner* (B..."
- `[SUPPORTED]` Este enfoque reemplaza los registros maestros separados de clientes y proveedores que existían en SAP ECC.  
  > support: "This replaces the separate customer and vendor master records used in SAP ECC."
- `[SUPPORTED]` Un único registro de business partner puede representar tanto a un cliente como a un proveedor.  
  > support: "a single business partner record can represent both a customer and a vendor, avoiding data redundanc..."
- `[SUPPORTED]` Los datos relevantes son activados mediante la asignación de roles específicos (por ejemplo, el rol Customer para procesos SD y el rol Vendor para compras).  
  > support: "| Customer | SD sales processes | Sales area data, ordering, shipping, billing, partner functions |
..."
- `[SUPPORTED]` Los datos centrales como nombre, dirección y datos bancarios se introducen una sola vez, evitando redundancia y mejorando la integridad de los datos.  
  > support: "Central data such as name, address, and bank details only needs to be entered once."
**Reclassified supports**: 0
**Citations**: {'has_citation_line': True, 'cited_ids': ['master-data-business-partner-master-data-001', 'order-management-sales-order-source-of-data-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

---

## Abstention Questions (review abstention)

### S4600-LA-U1-Q1 (S4600) — ABSTENTION MODE
**Q**: Which of the following apps gives you a visual overview of complex topics for monitoring or tracking purposes?
**Gold chunks excluded**: configuration-sap-fiori-launchpad-001
**Context (no gold)**: order-management-sales-monitoring-analytics-001, billing-create-billing-documents-fiori-001, shipping-outbound-delivery-monitor-001...

**Response**:
```
La pregunta hace referencia a una app que proporciona una **visión visual general de temas complejos** con fines de monitoreo o seguimiento.

Según el documento de contexto, **SAP Smart Business** es la herramienta que proporciona dashboards basados en KPIs con indicadores visuales (por ejemplo, indicadores en rojo para excepciones), permitiendo a los usuarios monitorear situaciones complejas de un vistazo y navegar directamente a las transacciones subyacentes para actuar.

El documento describe SAP Smart Business como una herramienta de gestión de excepciones orientada a KPIs con enlaces directos de acción, donde los tiles alertan al manager con indicadores visuales y permiten hacer drill-down hacia los datos subyacentes.

Fuentes: order-management-sales-monitoring-analytics-001
```

**Correct abstention**: False
**Judge** — grounded_fraction=0.625 | is_abstention=False
- `[SUPPORTED]` SAP Smart Business proporciona dashboards basados en KPIs con indicadores visuales (por ejemplo, indicadores en rojo para excepciones)  
  > support: "If the issue is a KPI-level exception (for example, revenue gap vs. plan), *SAP Smart Business* tile..."
- `[PARTIAL]` SAP Smart Business permite a los usuarios monitorear situaciones complejas de un vistazo y navegar directamente a las transacciones subyacentes para actuar  
  > support: "The manager clicks the tile to drill down to the underlying data and navigates to the transaction to..."
- `[SUPPORTED]` El documento describe SAP Smart Business como una herramienta de gestión de excepciones orientada a KPIs con enlaces directos de acción  
  > support: "*SAP Smart Business* provides KPI-driven exception management with direct action links"
- `[UNSUPPORTED]` ⚑RECLASSIFIED Los tiles alertan al manager con indicadores visuales y permiten hacer drill-down hacia los datos subyacentes
**Reclassified supports**: 1

### S4F30-LA-U2-Q1 (S4F30) — ABSTENTION MODE
**Q**: Choose three components which are part of Advanced Credit Management but are not part of Basic Credit Management.
**Gold chunks excluded**: credit-management-credit-check-sd-integration-001, credit-management-credit-master-data-001, credit-management-credit-rules-engine-001
**Context (no gold)**: special-processes-advanced-returns-management-001, special-processes-third-party-order-processing-001, pricing-condition-contract-management-concept-001...

**Response**:
```
No puedo responder con la documentación proporcionada.
```

**Correct abstention**: True
**Judge** — grounded_fraction=0.0 | is_abstention=True
- `[UNSUPPORTED]` ⚑RECLASSIFIED No puedo responder con la documentación proporcionada.
**Reclassified supports**: 1

### S4600-LA-U1-Q2 (S4600) — ABSTENTION MODE
**Q**: A user can personalize the home page in SAP Fiori launchpad by default.
**Gold chunks excluded**: configuration-sap-fiori-launchpad-001
**Context (no gold)**: billing-create-billing-documents-fiori-001, pricing-condition-records-001, master-data-sd-partner-functions-001...

**Response**:
```
No puedo responder con la documentación proporcionada.
```

**Correct abstention**: True
**Judge** — grounded_fraction=0.0 | is_abstention=True
- `[UNSUPPORTED]` ⚑RECLASSIFIED No puedo responder con la documentación proporcionada.
**Reclassified supports**: 1

---

## Limitations

- **Judge bias**: generator and judge share the same model family (Anthropic). No cross-model independence — self-consistency risk.
- **LÍMITE 2**: questions are SAP Learning Assessment (easy, single-lesson scope). Grounding score is a discipline floor, NOT a RAG quality proof.
- **n**: small sample. Not statistically significant.
- **parse_page_range**: comma-separated page specs (e.g. '23, 30-38') are partially parsed by score.py (only first number); may miss some gold chunks.