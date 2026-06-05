---
schema_version: 1
id: billing-document-table-structure-001
title: "Database Table Structure of the SD Billing Document"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "120-121"
    source_type: "A"
    role: "primary"
transactions: []
tables: [VBRK, VBRP, VBPA, SADR, VBFA, PRCD_COND, STXH, STXL, VBRL]
aliases:
  - table structure
  - estructura de tablas
level: technical
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
At the database tier, an SAP SD billing document spans across multiple specialized native tables, separating header attributes, item details, text lines, and underlying price conditions.

## Questions This Chunk Answers
- Which SAP database tables store billing document data?
- Where are the associated pricing conditions housed for an invoice?

## Database Tables
The underlying architecture of an SD standard billing document routes data across the following tables:

- `VBRK`: Billing document Header data
- `VBRP`: Billing document Item data
- `VBPA`: Partner definitions attached to the SD document
- `SADR`: Address data
- `VBFA`: SD document flow (linking the invoice historically to its predecessors)
- `PRCD_COND`: Price Condition data (formerly the `KONV` table structure)
- `STXH`: Header text properties
- `STXL`: Corresponding textual lines

For environments leveraging **Invoice Lists**, the architecture introduces an additional structural table:
- `VBRL`: Invoice List document structure traversing linked billing IDs.
