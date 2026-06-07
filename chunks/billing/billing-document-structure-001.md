---
schema_version: 1
id: billing-billing-document-structure-001
title: "Billing Document Structure in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "19"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing document structure
  - estructura de documento de facturación
  - header billing
  - cabecera de factura
  - item billing
  - posición de factura
  - payer
  - pagador
  - billing date
  - fecha de facturación
  - billing quantity
  - cantidad facturada
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Billing Document Structure in SAP SD

## Operational Summary
All *billing documents* in SAP share a common two-level structure: a single header and any number of items. The header holds data valid for the entire document; each item holds data specific to a single billed position. This structure is consistent across all billing document types — invoices, credit memos, cancellations, and pro forma invoices.

## Questions This Chunk Answers
- What is the structure of a billing document in SAP SD?
- What data is stored at the header level versus the item level?
- Is the billing date stored on the header or the item?
- Where is the payer recorded in the billing document?
- Does the billing document have schedule lines like a sales order?
- How many items can a billing document have?

## Definition
A billing document is an SAP SD document that records the financial claim against the customer for goods or services. Its two-tier structure separates general commercial data (header) from product-specific data (items), enabling the billing of multiple materials or services within a single document.

## Purpose in the SD Process
The billing document is the culmination of the order-to-cash process. Its structure ensures that: (1) commercial terms applicable to the whole transaction (payer, billing date) are captured once at header level; and (2) product-specific data (quantities, materials, values) is captured per item, allowing detailed invoice line presentation and downstream accounting by item.

## Structure and Variants

### Header Level
Contains data that applies to the **entire billing document**:
- Customer number of the *payer* (the partner responsible for payment)
- Billing date
- Net value of the entire billing document (sum of all items)
- Output and partner determination data

### Item Level
Contains data specific to **each individual billed position**:
- Material number
- Billing quantity
- Net value of the individual item
- Pricing conditions for that item

Unlike a sales order, a billing document has **no schedule lines**. Billing quantities come from the reference document (delivery quantity or order quantity depending on billing relevance).

A billing document can contain any number of items, including items from different reference documents when combination rules allow it.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order / Delivery | Billing document created with reference; quantities and prices copied per copying control |
| FI Accounting Document | Automatically created from billing document; header maps to accounting header, items to line items |
| Pricing Conditions | Item-level conditions determine net value, tax, and freight per item |
| Payer Master | Partner function PAYER provides the bill-to partner at header level |

## Cross-References
- See also: billing-billing-document-integration-001
- See also: billing-document-table-structure-001
- See also: configuration-billing-copying-control-001
- See also: billing-billing-document-creation-methods-001
