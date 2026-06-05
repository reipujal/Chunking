---
schema_version: 1
id: integration-general-billing-interface-001
title: "The General Billing Interface in SAP SD"
area: integration
process_tags: [order-to-cash, billing]
chunk_type: integration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "107"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - general billing interface
  - interfaz de facturación general
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Aside from the modern omnichannel convergent billing frameworks, companies can leverage the traditional user exit to invoke the *General Billing Interface*. This allows the SAP system to ingest and process external documents (orders and deliveries generated outside SAP).

## Questions This Chunk Answers
- How can legacy non-SAP orders be billed inside the SAP system?
- What formatting is required to use the general billing interface?

## Requirements
When utilizing the general billing interface to ingest external documents, you must formally prepare the data mapping correctly:
1. **Format**: Prepare the data rigorously in a sequential file of a specified format.
2. **Required Fields**: You must specify a minimum number of fundamentally required fields populated linearly from the data records (e.g., the customer master and the sales organization).
3. **Optional Fields**: Designate how the remaining optional fields (e.g., material master, specific price components) are filled—either definitively through the incoming data records or naturally adopted through standard system logic.

As part of the transfer, you can securely capture external reference numbers, preserving external delivery or order tracking attributes for traceability.
