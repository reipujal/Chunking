---
schema_version: 1
id: configuration-billing-copying-control-001
title: "Copying Control in SAP SD Billing"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "36-39"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - copying control
  - control de copia
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The copying control table determines how data is transferred during the billing process. The system administrator configures controls at both the header and item levels to define exact behavior for reference documents, billing quantities, and pricing updates.

## Questions This Chunk Answers
- How is the transfer of data from an order or delivery to a billing document configured?
- What are the common pricing behavior types during billing copying control?

## What This Configuration Controls
Copying control specifies a Source document type to a Target billing type. It is configured at multiple levels:

### Header Level Controls
- **Reference document**: Specifies the documents that may be used as a reference for billing.
- **Determination**: Includes rules for foreign trade data, allocation numbers, reference numbers, and item number assignment.

### Item Level Controls
- **Target matching**: The Target billing type mapped against the source sales document type and the specific *item category*.
- **Billing quantity**: Defines which quantity should be invoiced. Common permutations include:
  - Based on an order: Order quantity minus quantity already billed.
  - Based on a delivery: Quantity already delivered minus quantity already billed.
  - Based on a pro forma invoice (F5): Order quantity.
  - Based on a pro forma invoice (F8): Delivery quantity.
- **Pricing and exchange rate**: Determines whether pricing should be carried out again or simply copied from the order, defining the *pricing type* and exchange rate behavior.

## Pricing Types in Billing
The system administrator assigns a pricing type to dictate how prices are adopted:
- **A**: Elements are copied from the reference document and updated according to a scale.
- **B**: Pricing is carried out again (redetermined entirely).
- **C**: Manual pricing elements are copied; pricing applies again for the others.
- **D**: Pricing elements are copied unchanged from the reference document.
- **G**: Elements are copied unchanged, but tax conditions are determined again.
- **H**: Elements are copied unchanged, but freight is determined again.
