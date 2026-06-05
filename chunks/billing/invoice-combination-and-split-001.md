---
schema_version: 1
id: billing-invoice-combination-and-split-001
title: "Invoice Combination and Split in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "54-56"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - invoice split
  - partición de factura
  - invoice combination
  - combinación de facturas
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
By default, the SAP system attempts to combine all compatible transactions into a single collective billing document. Conversely, if necessary criteria do not match across the reference documents, the system triggers an automatic invoice split. 

## Questions This Chunk Answers
- When does the system combine multiple reference documents into a single collective invoice?
- What causes an automatic invoice split?
- Can you force an invoice split based on specific item fields like material group?

## Collective Billing Document Combinations
As a rule, the system attempts to combine reference objects. You can include both order-related items and delivery-related items originating from different preceding documents in the exact same billing document, provided their header-level attributes align.

## Invoice Splits
An automatic invoice split occurs whenever the header partners or critical data in the header fields are not identical across the items being billed. 

### Automatic Invoice Split (Header-Dependent)
All header partners and header fields in the billing document act as baseline split criteria. For example, if two orders belong to the same payer but feature different *terms of payment*, the system cannot merge them and automatically splits them into two distinct invoices.

### Item-Dependent Invoice Split
The system administrator can define additional *item-level* split requirements manually within Customizing for copying control. This prevents combining certain items even if their headers match.
- For example, separation can be strictly based on the material group or profit center.
- You can configure the system to create definitively one billing document for *each* sales document. This is done by specifying data transfer routine 3 in Customizing for copying control. The `VBRK-ZUKRI` field in the billing header is utilized to store these additional splitting criteria, and any fields forcing the split can be verified in a dedicated split analysis log.
