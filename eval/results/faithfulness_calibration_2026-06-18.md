# Faithfulness Harness — Calibration Sample (2026-06-18)

**Generator**: gpt-4.1 | **Judge**: gpt-4.1 | **top-k**: 5

## Positive Set Metrics

| Metric | Value |
|---|---|
| n | 5 |
| mean_grounded_fraction | 0.833 |
| pct_with_any_unsupported | 0.0 |
| release_mixing_incidents | 0 |
| citation_validity_rate | 100.0 |
| gold_in_top_k_rate | 60.0 |
| n_retrieval_misses | 2 |
| pct_miss_abstained | 0.0 |

## Abstention Set Metrics

| Metric | Value |
|---|---|
| n | 3 |
| pct_correct_abstention | 33.3 |
| pct_hallucinated | 66.7 |

---

## Positive Questions (review grounding)

### S4600-LA-U1-Q1 (S4600)
**Q**: Which of the following apps gives you a visual overview of complex topics for monitoring or tracking purposes?
**Gold chunks**: configuration-sap-fiori-launchpad-001
**Gold in top-k**: True | **top-k**: order-management-sales-monitoring-analytics-001, configuration-sap-fiori-launchpad-001, billing-create-billing-documents-fiori-001...

**Response**:
```
The SAP Fiori analytical apps provide a visual overview of complex topics for monitoring or tracking purposes. These apps are specifically designed for monitoring and analytics, offering dashboards and KPI-driven exception management with drill-down capabilities for real-time insights.

Fuentes: configuration-sap-fiori-launchpad-001, order-management-sales-monitoring-analytics-001
```

**Judge** — grounded_fraction=0.5 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` The SAP Fiori analytical apps provide a visual overview of complex topics for monitoring or tracking purposes.
- `[PARTIAL]` These apps are specifically designed for monitoring and analytics, offering dashboards and KPI-driven exception management with drill-down capabilities for real-time insights.
**Citations**: {'has_citation_line': True, 'cited_ids': ['configuration-sap-fiori-launchpad-001', 'order-management-sales-monitoring-analytics-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

### S4600-LA-U1-Q2 (S4600)
**Q**: A user can personalize the home page in SAP Fiori launchpad by default.
**Gold chunks**: configuration-sap-fiori-launchpad-001
**Gold in top-k**: True | **top-k**: configuration-sap-fiori-launchpad-001, billing-create-billing-documents-fiori-001, pricing-condition-records-001...

**Response**:
```
Sí, por defecto un usuario puede personalizar la página de inicio en SAP Fiori Launchpad. El Launchpad proporciona funciones de personalización para los usuarios, permitiéndoles adaptar su experiencia según sus necesidades y preferencias.

Fuentes: configuration-sap-fiori-launchpad-001
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` por defecto un usuario puede personalizar la página de inicio en SAP Fiori Launchpad
- `[SUPPORTED]` El Launchpad proporciona funciones de personalización para los usuarios
- `[SUPPORTED]` permitiéndoles adaptar su experiencia según sus necesidades y preferencias
**Citations**: {'has_citation_line': True, 'cited_ids': ['configuration-sap-fiori-launchpad-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

### S4600-LA-U4-Q1 (S4600)
**Q**: The master data of customers and vendors is managed in SAP S/4HANA by using business partner master data.
**Gold chunks**: master-data-business-partner-master-data-001, master-data-material-master-sd-001
**Gold in top-k**: True | **top-k**: master-data-business-partner-master-data-001, enterprise-structure-shared-master-data-cross-division-001, order-management-sales-monitoring-analytics-001...

**Response**:
```
Sí, en SAP S/4HANA la gestión de los datos maestros de clientes y proveedores se realiza mediante el concepto unificado de Business Partner (BP). Esto reemplaza los registros maestros separados de cliente y proveedor que se usaban en SAP ECC. Un único registro de Business Partner puede representar tanto a un cliente como a un proveedor, y se le asignan roles específicos (por ejemplo, Customer, FI Customer, Vendor) que activan los campos de datos relevantes para cada contexto de negocio. Así se centraliza el mantenimiento de datos maestros y se evita la redundancia de datos en los módulos de Ventas, Compras y Finanzas.

Fuentes: master-data-business-partner-master-data-001, order-management-sales-order-source-of-data-001
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` En SAP S/4HANA la gestión de los datos maestros de clientes y proveedores se realiza mediante el concepto unificado de Business Partner (BP).
- `[SUPPORTED]` Esto reemplaza los registros maestros separados de cliente y proveedor que se usaban en SAP ECC.
- `[SUPPORTED]` Un único registro de Business Partner puede representar tanto a un cliente como a un proveedor, y se le asignan roles específicos (por ejemplo, Customer, FI Customer, Vendor) que activan los campos de datos relevantes para cada contexto de negocio.
- `[SUPPORTED]` Así se centraliza el mantenimiento de datos maestros y se evita la redundancia de datos en los módulos de Ventas, Compras y Finanzas.
**Citations**: {'has_citation_line': True, 'cited_ids': ['master-data-business-partner-master-data-001', 'order-management-sales-order-source-of-data-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

### S4600-LA-U4-Q2 (S4600)
**Q**: Which one of the following partner functions is applicable for a customer who receives the invoice?
**Gold chunks**: master-data-business-partner-master-data-001, master-data-material-master-sd-001
**Gold in top-k**: False | **top-k**: special-processes-intercompany-sales-process-001, billing-invoice-list-001, master-data-sd-partner-functions-001...

**Response**:
```
The applicable partner function for a customer who receives the invoice is the "bill-to party" partner function. In SAP SD, the bill-to party is the business partner who receives the invoice in a sales transaction. This is distinct from other partner functions such as sold-to party, ship-to party, and payer.

Fuentes: master-data-sd-partner-functions-001
```

**Judge** — grounded_fraction=1.0 | release_mixing=False | is_abstention=False
- `[SUPPORTED]` The applicable partner function for a customer who receives the invoice is the 'bill-to party' partner function.
- `[SUPPORTED]` In SAP SD, the bill-to party is the business partner who receives the invoice in a sales transaction.
- `[SUPPORTED]` This is distinct from other partner functions such as sold-to party, ship-to party, and payer.
**Citations**: {'has_citation_line': True, 'cited_ids': ['master-data-sd-partner-functions-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

### S4600-LA-U4-Q3 (S4600)
**Q**: The Customizing of sales document types includes some parameters that can be used to choose between division-specific and cross-division sales processing.
**Gold chunks**: master-data-business-partner-master-data-001, master-data-material-master-sd-001
**Gold in top-k**: False | **top-k**: configuration-sales-document-type-control-001, enterprise-structure-shared-master-data-cross-division-001, configuration-sales-copying-control-001...

**Response**:
```
Sí, en la Customizing del tipo de documento de ventas puedes controlar si el procesamiento de ventas es específico de división o cruzado entre divisiones. Esto se gestiona mediante el parámetro de "asignación de área de ventas" (*sales area assignment*), que define en qué organización de ventas, canal de distribución y división es válido el tipo de documento de ventas. Así, puedes restringir el tipo de documento a una división específica o permitir su uso en varias divisiones, habilitando el procesamiento cruzado de divisiones según la configuración elegida.

Fuentes: configuration-sales-document-type-control-001
```

**Judge** — grounded_fraction=0.666 | release_mixing=False | is_abstention=False
- `[PARTIAL]` En la Customizing del tipo de documento de ventas puedes controlar si el procesamiento de ventas es específico de división o cruzado entre divisiones.
- `[SUPPORTED]` Esto se gestiona mediante el parámetro de 'asignación de área de ventas' (sales area assignment), que define en qué organización de ventas, canal de distribución y división es válido el tipo de documento de ventas.
- `[PARTIAL]` Puedes restringir el tipo de documento a una división específica o permitir su uso en varias divisiones, habilitando el procesamiento cruzado de divisiones según la configuración elegida.
**Citations**: {'has_citation_line': True, 'cited_ids': ['configuration-sales-document-type-control-001'], 'all_in_corpus': True, 'all_in_top_k': True}
**Abstention regex**: False

---

## Abstention Questions (review abstention)

### S4600-LA-U1-Q1 (S4600) — ABSTENTION MODE
**Q**: Which of the following apps gives you a visual overview of complex topics for monitoring or tracking purposes?
**Gold chunks excluded**: configuration-sap-fiori-launchpad-001
**Context (no gold)**: order-management-sales-monitoring-analytics-001, billing-create-billing-documents-fiori-001, shipping-outbound-delivery-monitor-001...

**Response**:
```
The app that gives you a visual overview of complex topics for monitoring or tracking purposes is the *Sales Order Fulfillment* app, which provides a unified view of the current fulfillment situation and highlights orders that cannot be fulfilled. Additionally, *SAP Smart Business* provides KPI-driven dashboards for exception management and tracking. These tools are designed for monitoring and analytics in SAP S/4HANA Sales.

Fuentes: order-management-sales-monitoring-analytics-001
```

**Correct abstention**: False
**Judge** — grounded_fraction=1.0 | is_abstention=False
- `[SUPPORTED]` The app that gives you a visual overview of complex topics for monitoring or tracking purposes is the Sales Order Fulfillment app, which provides a unified view of the current fulfillment situation and highlights orders that cannot be fulfilled.
- `[SUPPORTED]` Additionally, SAP Smart Business provides KPI-driven dashboards for exception management and tracking.
- `[SUPPORTED]` These tools are designed for monitoring and analytics in SAP S/4HANA Sales.

### S4600-LA-U1-Q2 (S4600) — ABSTENTION MODE
**Q**: A user can personalize the home page in SAP Fiori launchpad by default.
**Gold chunks excluded**: configuration-sap-fiori-launchpad-001
**Context (no gold)**: billing-create-billing-documents-fiori-001, pricing-condition-records-001, master-data-sd-partner-functions-001...

**Response**:
```
No puedo responder con la documentación proporcionada.
```

**Correct abstention**: True
**Judge** — grounded_fraction=1.0 | is_abstention=True
- `[SUPPORTED]` No puedo responder con la documentación proporcionada.

### S4600-LA-U4-Q1 (S4600) — ABSTENTION MODE
**Q**: The master data of customers and vendors is managed in SAP S/4HANA by using business partner master data.
**Gold chunks excluded**: master-data-business-partner-master-data-001, master-data-material-master-sd-001
**Context (no gold)**: enterprise-structure-shared-master-data-cross-division-001, order-management-sales-monitoring-analytics-001, credit-management-credit-master-data-001...

**Response**:
```
Sí, en SAP S/4HANA 2020, los datos maestros de clientes y proveedores se gestionan utilizando el modelo de Business Partner (BP). El modelo de Business Partner es el punto de entrada central para crear, editar y visualizar los datos maestros de clientes y proveedores. Un Business Partner puede crearse en uno o más roles de BP, y los datos centrales como nombre, dirección y datos bancarios solo necesitan ingresarse una vez. Esto simplifica la gestión y evita la duplicidad de datos maestros para clientes y proveedores.

Fuentes: order-management-sales-order-source-of-data-001
```

**Correct abstention**: False
**Judge** — grounded_fraction=0.8 | is_abstention=False
- `[SUPPORTED]` En SAP S/4HANA 2020, los datos maestros de clientes y proveedores se gestionan utilizando el modelo de Business Partner (BP).
- `[SUPPORTED]` El modelo de Business Partner es el punto de entrada central para crear, editar y visualizar los datos maestros de clientes y proveedores.
- `[SUPPORTED]` Un Business Partner puede crearse en uno o más roles de BP.
- `[SUPPORTED]` Los datos centrales como nombre, dirección y datos bancarios solo necesitan ingresarse una vez.
- `[PARTIAL]` Esto simplifica la gestión y evita la duplicidad de datos maestros para clientes y proveedores.

---

## Limitations

- **Judge bias**: generator and judge share the same model family (OpenAI). No cross-model independence — self-consistency risk.
- **LÍMITE 2**: questions are SAP Learning Assessment (easy, single-lesson scope). Grounding score is a discipline floor, NOT a RAG quality proof.
- **n**: small sample. Not statistically significant.
- **parse_page_range**: comma-separated page specs (e.g. '23, 30-38') are partially parsed by score.py (only first number); may miss some gold chunks.