# Abstention Completion Run — 2026-06-23

**Generator**: claude-sonnet-4-6 | **Judge**: gpt-4.1-mini (provider: openai) | **top-k**: 5
**Mode**: abstention-only (positive set skipped)

## Abstention Metrics

| Metric | Value |
|---|---|
| n (total) | 99 |
| n_errors | 0 |
| n_valid (errors excluded) | 99 |
| pct_correct_abstention | **65.7%** |
| pct_answered_when_should_abstain | **34.3%** |
| n_failures | 34 |
| n_api_calls (gen only — judge skipped on abstained) | 153 |
| approx_cost_usd | ~$2.26 |

## Per-SRC Breakdown

| SRC | n | n_errors | n_valid | n_abstained | n_answered | pct_correct% | pct_answered_should_abs% |
|---|---|---|---|---|---|---|---|
| S4615 | 30 | 0 | 30 | 17 | 13 | 56.7% | 43.3% |
| S4620 | 26 | 0 | 26 | 19 | 7 | 73.1% | 26.9% |
| S4650 | 14 | 0 | 14 | 6 | 8 | 42.9% | 57.1% |
| S4680 | 25 | 0 | 25 | 19 | 6 | 76.0% | 24.0% |
| S4F30 | 4 | 0 | 4 | 4 | 0 | 100.0% | 0.0% |

## Failure Detail

| ID | SRC | state | top-1 | gf | Response (first 200 chars) |
|---|---|---|---|---|---|
| S4615-LA-U3-Q1 | S4615 | answered | billing-billing-document-integration-001 | 0.25 | Based on the provided documentation, a billing document **cannot** simultaneously reference both an order and a delivery.  The documentation explains that billing relevance is determined by the **item… |
| S4615-LA-U3-Q2 | S4615 | answered | billing-pro-forma-invoice-001 | 0.0 | ## Answer  Based on the context documents, the relevant billing document type to ensure that **goods have already been shipped before creating the billing document** is one created with reference to a… |
| S4615-LA-U4-Q1 | S4615 | answered | billing-billing-document-creation-methods-001 | 0.5 | ## Steps to Cancel a Billing Document  Based on the provided documentation, the specific step-by-step process to cancel an **individual** billing document is not detailed in the context documents.  Ho… |
| S4615-LA-U4-Q5 | S4615 | answered | configuration-billing-data-flow-001 | 0.5 | Based on the context documents, specifically the document on FI interface controls between SD Billing and Financial Accounting:  **No, a pro forma invoice billing document is NOT automatically transfe… |
| S4615-LA-U4-Q6 | S4615 | answered | shipping-inbound-delivery-ewm-001 | 1.0 | ## Goods Issue Before Delivery-Related Pro Forma Invoice  Yes, according to the context provided, **Goods Issue (GI) posting is the prerequisite for invoice creation**.  The document explicitly states… |
| S4615-LA-U5-Q1 | S4615 | answered | billing-billing-document-creation-methods-001 | 0.833 | ## Methods for Creating Billing Documents in SAP SD (S/4HANA 2020)  There are several methods available:  ### 1. Manual Creation — Transaction VF01 Enter the specific order or delivery document number… |
| S4615-LA-U6-Q1 | S4615 | answered | billing-invoice-list-001 | 0.4 | ## Options Available to Create an Invoice in SAP SD  Based on the provided documentation, the following invoice creation options are available:  ### 1. **Standard / Collective Invoice** The system att… |
| S4615-LA-U6-Q2 | S4615 | answered | billing-billing-plans-concept-001 | 0.333 | ## Creating Billing Documents Regularly on Specific Dates  To create billing documents regularly on specific dates, you use a **Periodic Billing Plan**.  ### How It Works  A **billing plan** is a sche… |
| S4615-LA-U7-Q1 | S4615 | answered | special-processes-intercompany-sales-process-001 | 0.25 | ## Delivery Split Criteria in SAP SD  Based on the context documents, the **mandatory split criteria** that cause an automatic invoice/delivery split are:  1. **Shipping point** 2. **Route** 3. **Ship… |
| S4615-LA-U8-Q4 | S4615 | answered | configuration-billing-relevance-item-category-001 | 0.0 | ## Respuesta  La afirmación es **incorrecta** según la documentación proporcionada.  El campo **billing relevance** (relevancia de facturación) en la categoría de posición **no** determina el tipo de … |
| S4615-LA-U10-Q1 | S4615 | answered | billing-billing-document-cancellation-001 | 0.8 | The statement is **True**, with an important nuance: once a billing document has been released to Financial Accounting, its data **cannot be overwritten or changed directly**. Instead, if the data is … |
| S4615-LA-U10-Q2 | S4615 | answered | configuration-delivery-process-customizing-001 | 0.0 | ## Setting Up Reference and Allocation Numbers in Customizing  Based on the context provided, the reference and allocation number configuration is mentioned in the **Copying Control in SAP SD Billing*… |
| S4615-LA-U11-Q1 | S4615 | answered | configuration-output-management-s4hana-001 | 0.333 | La afirmación mezcla dos conceptos distintos. Según la documentación proporcionada:  1. **BRFplus en Output Management**: Es correcto que SAP S/4HANA Output Management está basado en *Business Rule Fr… |
| S4620-LA-U1-Q1 | S4620 | answered | order-management-value-contracts-001 | 1.0 | La pregunta es si se puede limitar un acuerdo de precios a un período determinado.  Según el documento sobre Condition Contract Management, un *condition contract* incluye una **validez** (validity in… |
| S4620-LA-U1-Q3 | S4620 | answered | configuration-sales-item-category-control-001 | 0.75 | La afirmación es **parcialmente correcta, pero incompleta en su descripción**.  Según la documentación, **HM00** es una condición de cabecera que permite ingresar manualmente el valor total del pedido… |
| S4620-LA-U1-Q4 | S4620 | answered | configuration-pricing-procedure-configuration-001 | 0.0 | La afirmación es **correcta**.  Según la documentación, una **condition table** define los campos clave (*key fields*) que forman la clave única para los registros de condición (*condition records*). … |
| S4620-LA-U2-Q2 | S4620 | answered | pricing-condition-records-001 | 1.0 | La afirmación es **falsa**.  Un access sequence **no** se limita a una sola condition table. Según la documentación, el access sequence para un condition type puede buscar registros maestros utilizand… |
| S4620-LA-U3-Q1 | S4620 | answered | pricing-condition-contract-maintenance-001 | 0.769 | # What You Can Do With a Condition Record  Based on the provided documentation, the following actions and capabilities apply to condition records in SAP SD (S/4HANA 2020):  ## Create and Maintain - Co… |
| S4620-LA-U3-Q2 | S4620 | answered | pricing-pricing-agreements-001 | 0.0 | La afirmación es **verdadera**.  Según la documentación, los registros de condición tienen un **período de validez** que restringe el acuerdo a una ventana de tiempo específica, y explícitamente se in… |
| S4620-LA-U3-Q3 | S4620 | answered | pricing-condition-contract-management-concept-001 | 1.0 | Based on the context document on Condition Technique and Pricing Overview, besides the condition type based maintenance (VK11/VK12/VK13), there is an additional option:  **New Condition Maintenance In… |
| S4650-LA-U1-Q1 | S4650 | answered | enterprise-structure-sales-distribution-enterprise-structure-001 | 0.0 | ## Mandatory Organizational Elements in Sales and Distribution (SD)  Based on the provided documentation, the mandatory organizational elements in SAP SD are:  ### 1. **Sales Organization** Represents… |
| S4650-LA-U1-Q2 | S4650 | answered | master-data-business-partner-master-data-001 | 1.0 | La afirmación es correcta según la documentación proporcionada. El concepto de Business Partner (BP) en SAP S/4HANA centraliza el mantenimiento de datos maestros, de modo que información central como … |
| S4650-LA-U3-Q2 | S4650 | answered | master-data-material-master-sd-001 | 1.0 | Based on the context provided, the material master contains the following text source accessible in SD:  - **Sales Text** — this is a dedicated view in the material master (at the Sales Org + Distribu… |
| S4650-LA-U3-Q5 | S4650 | answered | pricing-condition-technique-overview-001 | 0.75 | La afirmación es **incorrecta** según la documentación proporcionada.  El **access sequence** (secuencia de acceso) se utiliza para que el sistema busque el **registro de condición** apropiado (condit… |
| S4650-LA-U4-Q2 | S4650 | answered | integration-general-billing-interface-001 | 0.5 | La pregunta es si una estrategia de comunicación puede usarse para comunicación externa.  Según el documento sobre funciones especiales en entregas de salida, la comunicación con socios externos se re… |
| S4650-LA-U4-Q3 | S4650 | answered | pricing-condition-technique-overview-001 | 0.0 | ## Evaluación de la afirmación  La afirmación dice que una secuencia de accesos siempre está configurada para buscar el registro **más específico al final** (*last*). Esto es **incorrecto** según la d… |
| S4650-LA-U4-Q6 | S4650 | answered | configuration-billing-output-management-brfplus-001 | 0.8 | ## How a BRFplus Output Decision Table is Processed  Based on the documentation, a BRFplus output decision table works as follows:  1. **Structure**: Each row in the decision table specifies:    - **C… |
| S4650-LA-U4-Q7 | S4650 | answered | configuration-billing-output-management-brfplus-001 | 0.75 | La afirmación es **incorrecta**.  Según la documentación proporcionada, **SAP S/4HANA Output Management** es precisamente el framework que **reemplaza** la determinación de salida basada en NAST (cond… |
| S4680-LA-U1-Q1 | S4680 | answered | configuration-delivery-field-determination-001 | 1.0 | Based on the context documents, specifically document [ID: configuration-sales-item-category-control-001], the item category determination in a sales order uses **four inputs**:  1. **Sales document t… |
| S4680-LA-U1-Q2 | S4680 | answered | configuration-schedule-line-category-control-001 | 0.688 | # Schedule Line Category CS – Configuration Settings for Third-Party Order Processing  Based on the provided documentation, the document with ID `configuration-schedule-line-category-control-001` desc… |
| S4680-LA-U2-Q8 | S4680 | answered | order-management-sales-monitoring-analytics-001 | 0.417 | ## Warehouse Management Solutions for Cross-Company Code Sales Process  Based on the context documents, the following information is available regarding warehouse management solutions for picking in S… |
| S4680-LA-U3-Q7 | S4680 | answered | configuration-delivery-item-category-001 | 0.667 | ## Item Category Determination for NL Outbound Delivery  The **NL** delivery type is the **Replenishment delivery**, which is an outbound delivery **without order reference** (order-independent). Base… |
| S4680-LA-U3-Q8 | S4680 | answered | configuration-delivery-item-category-001 | 0.6 | ## Schedule Line Category Assignment for NL Outbound Delivery Movement Type Determination  Based on the context documents, the schedule line category is **assigned to the item category** (and optional… |
| S4680-LA-U4-Q5 | S4680 | answered | special-processes-intercompany-sales-process-001 | 0.667 | ## Ways to Post the Internal Invoice as an Incoming Invoice in the Selling Company Code  According to the context, the internal invoice (billing type IV) issued by the delivering company code to the s… |