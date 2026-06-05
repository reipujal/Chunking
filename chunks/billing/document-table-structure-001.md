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
    pages: "128-129"
    source_type: "A"
    role: "primary"
transactions: []
tables: [VBRK, VBRP, VBPA, SADR, VBFA, PRCD_COND, STXH, STXL]
aliases:
  - billing table structure
  - estructura de tablas de facturación
  - VBRK
  - VBRP
  - billing database tables
  - tablas de base de datos facturación
  - PRCD_COND
  - VBFA document flow
  - flujo de documentos SD
level: technical
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Database Table Structure of the SD Billing Document

## Operational Summary
At the database tier, an SAP SD billing document is distributed across multiple specialized tables. The core tables are *VBRK* (header) and *VBRP* (items). Partner, address, document flow, pricing conditions, and text data are stored in separate tables linked to the billing document number. Understanding this structure is relevant for custom reporting, data migration, and debugging.

## Questions This Chunk Answers
- Which SAP database tables store billing document header and item data?
- Where are pricing conditions for an invoice stored in the database?
- Which table records the document flow between a delivery and its billing document?
- Where is partner data for a billing document stored?
- What table replaced KONV for pricing conditions in S/4HANA?
- Where are text lines of an invoice stored?

## Definition
The billing document's database representation follows the standard SAP SD pattern of separating header, item, partner, flow, and ancillary data across specialized tables. All tables link via the billing document number (*VBELN* for billing documents).

## Purpose in the SD Process
These tables are used by: SD reports and queries, FI reconciliation (via VBFA document flow), pricing analysis tools, and data migration projects. Knowledge of the table structure is required for ABAP development, BW/BI extraction, and troubleshooting account determination or pricing issues.

## Structure and Variants

| Table | Content |
|---|---|
| VBRK | Billing document **header** data (payer, billing date, net value, billing type) |
| VBRP | Billing document **item** data (material, quantity, net value per item) |
| VBPA | **Partner** data attached to the SD document (sold-to, payer, ship-to, etc.) |
| SADR | **Address** data |
| VBFA | **SD document flow** — links the billing document historically to predecessor documents (orders, deliveries) |
| PRCD_COND | **Pricing condition** data (formerly stored in table KONV in ECC; renamed in S/4HANA) |
| STXH | **Text header** properties (text IDs and object keys for long texts) |
| STXL | **Text lines** — the actual text content linked via STXH |

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Billing Document (SD) | Primary key: VBELN (billing document number) in VBRK and VBRP |
| Sales Order / Delivery | Linked via VBFA; predecessor document numbers stored in the flow table |
| FI Accounting Document | Not directly linked by table join; linked via FI posting reference derived at billing time |
| Pricing Procedure | Conditions for each item stored in PRCD_COND keyed by KNUMV (condition record number) |

## Cross-References
- See also: billing-billing-document-structure-001
- See also: configuration-billing-data-flow-001
