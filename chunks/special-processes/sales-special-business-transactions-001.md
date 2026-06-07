---
schema_version: 1
id: special-processes-sales-special-business-transactions-001
title: "Rush Orders, Cash Sales, Consignment, and Free-of-Charge Deliveries"
area: special-processes
process_tags: [order-to-cash, consignment, free-of-charge]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "81-87"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - rush order
  - venta al contado
  - consignacion
  - entrega gratuita
  - diferencia entre cash sales y rush order
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Rush Orders, Cash Sales, Consignment, and Free-of-Charge Deliveries

## Operational Summary
SAP SD includes special business transactions for immediate pickup, immediate payment, customer consignment stock, and free deliveries. The course compares *rush orders* and *cash sales*, then describes consignment fill-up, issue, pick-up, and return, plus delivery free-of-charge and subsequent delivery free-of-charge. These scenarios use specific sales document types and follow-on behavior to reflect whether goods are billed, whether ownership transfers, and whether delivery is created automatically.

## Questions This Chunk Answers
- What is the difference between a rush order and a cash sale?
- When does SAP automatically create a delivery for immediate sales processes?
- How does consignment fill-up differ from consignment issue?
- Which consignment processes are billing-relevant?
- Why should free-of-charge deliveries often be blocked for review?

## When It Applies and Context
Use these scenarios when a standard sales order does not fit the business process. *Rush orders* and *cash sales* apply when the customer picks up goods immediately. *Consignment processing* applies when goods are physically placed at the customer but remain company property until the customer consumes them. *Free-of-charge delivery* applies to samples or complaint-related replacement deliveries.

## Process Flow
### Rush Order
1. The user creates a rush order for immediate pickup from the plant or warehouse.
2. The sales document type has the immediate delivery switch and a configured delivery type.
3. When the rush order is saved, the system automatically creates a delivery.
4. After goods are withdrawn, picking and goods issue can begin.
5. Billing documents are created later, for example through collective processing, and invoices are sent to the customer.

### Cash Sale
1. The user creates a cash sale.
2. The sales document type has immediate delivery behavior and a cash-sale delivery type.
3. When saved, SAP automatically creates the delivery and prints a document that can be given to the customer as an invoice.
4. Goods are withdrawn, picked, and goods issue is posted.
5. Billing is order-related through the billing due list, but the invoice is not printed again during billing.
6. The billed amount posts directly to a cash account, so customer receivables do not arise as they do for rush or standard orders.

### Consignment
1. Consignment fill-up delivers goods to customer consignment stock without billing.
2. Consignment issue reduces both customer special stock and delivering plant stock and is billing-relevant.
3. Consignment pick-up represents customer return of consignment goods and is not billing-relevant.
4. Consignment return reverses a consignment issue and results in a credit memo.

## Conditions and Restrictions
Free-of-charge subsequent delivery requires a preceding document according to the course example. Copying controls must exist for each allowed preceding document. SAP can use delivery blocks in the sales document type so that free-of-charge deliveries are not released until reviewed. If the responsible employee rejects the free delivery, a reason for rejection can be maintained.

## Common Errors
**Cash sale expected to create receivables**
-> The course states that receivables do not occur for the customer because the invoice amount is posted directly to a cash account.

**Rush order expected to print an immediate invoice receipt**
-> The learning assessment clarifies that the customer receives such a document in cash sales, not in rush orders.

**Consignment fill-up is billed**
-> Fill-up is not billed because the consignment stock remains company property.

## Cross-References
- Prior step: configuration-sales-copying-control-001
- See also: shipping-cash-sales-process-001
- See also: pricing-free-goods-001
- See also: billing-returns-process-001
