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
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "11"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - header
  - cabecera
  - item
  - posición
  - estructura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
All *billing documents* share a common structural design in SAP, consisting of a single header and any number of items. This two-tier structure separates general data applicable to the entire invoice from specific data relevant to individual products or services billed.

## Questions This Chunk Answers
- What is the structure of a billing document in SAP SD?
- What information is strictly kept at the header level versus the item level?

## Structure and Variants
A billing document is made up of two main levels:

1. **Header Level**
   The header contains general data that is valid for the entire billing document. Examples of header-level information include:
   - Customer number of the *payer*
   - Billing date
   - Net value of the entire billing document

2. **Item Level**
   The items contain data relevant specifically to each individual line item being billed. Examples of item-level information include:
   - Material number
   - Billing quantity
   - Net value of the individual item
