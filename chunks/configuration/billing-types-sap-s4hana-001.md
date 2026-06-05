---
schema_version: 1
id: configuration-billing-types-sap-s4hana-001
title: "Standard Billing Types and Controls in SAP SD"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "21-22"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing type
  - clase de factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The *billing type* is the central control element for the whole billing document. SAP provides a predefined set of billing types to cover the full range of business transactions during billing processing, from standard invoices to cancellations and pro forma invoices.

## Questions This Chunk Answers
- What are the standard billing types available in SAP S/4HANA?
- What parameters does the billing type control?

## What This Configuration Controls
The billing type governs many control parameters that influence how the document is processed internally and how it interfaces with Financial Accounting. Key controls include:
- Number assignment (number range)
- Partners
- Texts
- Output determination
- Account determination
- Special features of the Financial Accounting interface (such as a posting block)

## Key Parameters
The following are common standard billing types available in the SAP system:

| Billing Type | Description |
|---|---|
| F2 | Invoice |
| F8 | Pro forma invoice |
| CS | Cash sale |
| G2 | Credit memo |
| L2 | Debit memo |
| RE | Returns |
| IV | Intercompany billing (invoice) |
| IG | Intercompany billing (credit memo) |
| S1 | Cancellation invoice |
| S2 | Cancellation credit memo |
| LR | Invoice list |
| LG | Credit memo list |

You can redefine existing billing types or create new ones to meet specific company requirements, such as controlling document types, negative postings, branch or head office logic, and value-dated credit memos.
