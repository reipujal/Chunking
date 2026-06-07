---
schema_version: 1
id: integration-sales-document-technical-tables-001
title: "Sales Document Technical Tables for Header and Item Data"
area: integration
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "166-168"
    source_type: A
    role: primary
transactions: []
tables: [VBAK, VBKD, VEDA, VBPA, VBUV, VBFA, STXH, STXL, VBAP, VBEP, VBBE]
aliases:
  - sales document tables
  - tablas documento de ventas
  - tablas VBAK VBAP VBEP
  - SD document flow table
  - donde estan los datos tecnicos del pedido de ventas
level: technical
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sales Document Technical Tables for Header and Item Data

## Operational Summary
The S4605 appendix lists core technical tables for SD sales documents at header and item level. These tables are useful for consultants who need to understand where document header data, item data, business data, contract data, partner data, incompletion logs, document flow, text headers, text lines, schedule lines, and individual requirements are stored. The table names below are included because they appear literally in the appendix source pages.

## Questions This Chunk Answers
- Which table stores sales document header data according to S4605?
- Which table stores sales document item data according to S4605?
- Which tables are named for business data, partner data, incompletion, and document flow?
- Which appendix tables relate to texts and schedule lines?
- Which table is named for individual requirements in the sales document item appendix?

## Definition
The appendix is a technical reference for table structures in Sales and Distribution. It does not describe transaction processing steps. Its purpose is to map common sales document concepts to the named database tables presented by the course.

## Purpose in the SD Process
Functional SD work often starts with document behavior: header, item, schedule line, partner, contract, and document flow. Technical analysis, reporting, integration mapping, and troubleshooting require knowing which table family holds those objects. The appendix connects the earlier process lessons to their technical storage structures.

## Structure and Variants
The source separates the technical information into header and item tables.

| Table | Source description | Level indicated by source |
|---|---|---|
| VBAK | Sales document: Header data | Header |
| VBKD | Sales document: Business data | Header and item |
| VEDA | Contract | Header and item |
| VBPA | Partner | Header and item |
| VBUV | Incompleteness log | Header and item |
| VBFA | SD document flow | Header and item |
| STXH | Texts: Header | Header |
| STXL | Texts: Lines | Header |
| VBAP | Sales document: Item data | Item |
| VBEP | Sales document: Schedule line | Item |
| VBBE | Individual requirements | Item |

The appendix lists VBKD, VEDA, VBPA, VBUV, and VBFA under both header and item sections. That means the course presents them as relevant to both levels of analysis rather than limiting them to one document layer.

## Relationship with Other SAP SD Objects
These tables correspond directly to concepts covered earlier in S4605. VBAK and VBAP map to the document header and item structure. VBEP maps to schedule lines, which control delivery dates, quantities, requirements transfer, and inventory movement behavior. VEDA relates to contracts and value contracts. VBPA relates to partner functions and partner determination. VBUV relates to the incompletion log. VBFA relates to document flow and create-with-reference processing. STXH and STXL support sales document texts.

This chunk is intentionally technical but bounded by the appendix. It does not infer additional tables or newer data models outside the source pages.

## Cross-References
- Prior step: pricing-free-goods-001
- See also: order-management-sales-distribution-process-001
- See also: order-management-sales-document-data-flow-001
- See also: configuration-sales-incompletion-check-001
