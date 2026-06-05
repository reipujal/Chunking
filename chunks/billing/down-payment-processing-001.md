---
schema_version: 1
id: billing-down-payment-processing-001
title: "Down Payment Processing in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "83-88, 126"
    source_type: "A"
    role: "primary"
transactions: [F-29]
tables: []
aliases:
  - F-29
  - down payment
  - pago a cuenta
  - anticipo
  - FAZ
  - AZWR
  - down payment request
  - solicitud de pago anticipado
  - abono a cuenta
  - pago anticipado cliente
  - milestone billing down payment
  - facturación por hitos anticipo
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Down Payment Processing in SAP SD

## Operational Summary
Down payments are common in plant engineering and capital goods sales. SAP handles them by combining SD *milestone billing plans* with the condition type *AZWR* and a special G/L indicator in Financial Accounting. A down payment *request* document (billing type *FAZ*) is created first and sent to the customer; the actual incoming payment is posted in FI using transaction *F-29*; and when the partial or final invoice is issued, the system automatically deducts the down payment already received.

## Questions This Chunk Answers
- How is a down payment request generated in SAP SD?
- What billing type is used for down payment requests?
- Which condition type controls the down payment amount calculation?
- How is the incoming payment for a down payment posted in FI?
- How are down payments cleared when the final invoice is created?
- What happens to standard pricing conditions when a down payment condition is determined?

## When It Applies and Context
Down payment processing applies to orders with a *milestone billing plan* where partial advance payments are required before delivery. Typical in project business, construction, or capital goods. Requires specific billing plan dates configured with billing rule 4 (percentage) or rule 5 (value).

## Process Flow

### 1. Generating the Down Payment Request
Milestone billing plan dates with a down payment billing rule (rule 4 for percentage, rule 5 for fixed value) trigger the creation of a *down payment request* using billing type *FAZ*. This maps to a statistical (noted) FI document posted under special G/L indicator `F` — it does not create an open receivable yet.

### 2. Condition Type AZWR
Down payment items use the special condition type *AZWR*. When AZWR is determined (with calculation rule B for fixed amount), all other standard pricing conditions (such as PR00) are automatically set to inactive for that item. This ensures the down payment amount drives the line, not the regular price.

### 3. Incoming Payment (F-29)
The customer pays the requested down payment. The payment is posted in Financial Accounting using transaction *F-29*, assigning the amount to the down payment request under special G/L indicator `A`. The SD document flow shows the down payment request as *Cleared*.

### 4. Down Payment Clearing at Final Invoice
When a partial or final invoice is issued, the system detects all cleared down payments for the order and automatically appends a clearing item to the billing document. This item deducts the down payment from the gross receivable, showing the accurate outstanding balance owed.

## Conditions and Restrictions
- Requires a milestone billing plan on the sales order with billing rule 4 or 5.
- Condition type AZWR must be maintained in the pricing procedure.
- The F-29 payment posting must be complete before the down payment is detected as cleared at final invoicing.

## Common Errors

**Down payment request not created**
→ Verify that the milestone billing plan date exists, that billing type FAZ is assigned to the relevant billing plan date category, and that the date is due.

**Down payment amount incorrect on the invoice**
→ Check condition type AZWR on the pricing screen for the down payment clearing item. Its value can be manually adjusted if needed.

**Down payment not deducted from final invoice**
→ Confirm the down payment request has status *Cleared* in the document flow (F-29 payment must have been posted first).

## Cross-References
- Prior step: billing-billing-plans-concept-001
- See also: billing-installment-payments-001
- See also: configuration-billing-types-sap-s4hana-001
