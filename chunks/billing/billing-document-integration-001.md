---
schema_version: 1
id: billing-billing-document-integration-001
title: "Integration of Billing Documents in the SAP SD Process"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "18"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing document
  - factura
  - billing integration
  - integración de facturación
  - SD FI integration billing
  - integración SD FI facturación
  - order-to-cash final step
  - último paso order-to-cash
  - billing downstream effects
  - efectos de la facturación
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-07
---

# Integration of Billing Documents in the SAP SD Process

## Operational Summary
The *billing document* is the final step in the Sales and Distribution process chain. Creating a billing document triggers a cascade of automatic updates across multiple SAP components: it creates FI accounting documents, updates the billing status of the reference document, updates the credit exposure in the credit account, and feeds data to Profitability Analysis (CO-PA) and the Sales Information System (SIS).

## Questions This Chunk Answers
- What is the role of the billing document in the order-to-cash process?
- Which SAP modules are automatically updated when a billing document is created?
- Does creating a billing document update the credit account?
- What is the relationship between the billing document and Financial Accounting?
- How does the billing document affect Profitability Analysis?
- Can the billing document be created without a goods issue having been posted?

## Definition
The *billing document* is the SD document that formally concludes the customer transaction. It records the amount owed by the customer for goods delivered or services rendered and serves as the interface between SD and Financial Accounting. Unlike orders and deliveries, the billing document has direct financial consequences: it generates postings in the general ledger.

## Purpose in the SD Process
In the order-to-cash chain, billing is the revenue recognition step. It converts the logistics event (delivery, service) into a financial claim (receivable). Without a billing document, no FI posting occurs and no revenue is recognized. The billing document is also the basis for customer payment and any subsequent credit memo, debit memo, or return.

## Structure and Variants
Like all SD documents, billing documents have a header and items:
- **Header**: Payer, billing date, net value of the entire document.
- **Items**: Individual billed positions with material, quantity, and net value.

Billing document variants include standard invoices (F2), credit/debit memos, pro forma invoices, intercompany billing, invoice lists, and cancellation documents — all sharing the same structural design.

## Relationship with Other SAP SD Objects
Creating a billing document has the following effects:

| Effect | Description |
|---|---|
| Billing document | Created in SD (area: billing) |
| Document flow | SD document flow updated — reference documents show status *billed* |
| FI accounting document | Automatically created; G/L accounts posted for revenue, VAT, receivables |
| Credit account | Customer credit exposure updated |
| Billing status | Reference documents (order/delivery) updated to *fully billed* or *partially billed* |
| Sales Information System | SIS statistics updated |
| CO-PA | Data forwarded to Profitability Analysis |

## Goods Issue Dependency
Whether goods issue is required before billing depends on the *billing relevance* setting in the item category:
- **Order-related billing**: the billing document can be created directly from the sales order without a goods issue. Billing quantity is based on the order quantity.
- **Delivery-related billing**: goods issue must be posted before billing is possible. Billing quantity is based on the delivered (goods-issued) quantity.

This distinction is fundamental: a consultant checking why billing is blocked must first identify whether the item category requires delivery-related billing.

## Cross-References
- See also: billing-billing-document-structure-001
- See also: configuration-billing-account-determination-001
- See also: configuration-billing-fi-interface-controls-001
- See also: integration-general-billing-interface-001
