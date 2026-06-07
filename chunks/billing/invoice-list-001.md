---
schema_version: 1
id: billing-invoice-list-001
title: "Invoice Lists in SAP SD"
area: billing
process_tags: [order-to-cash, billing, invoice-list]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "65-66, 114, 125"
    source_type: "A"
    role: "primary"
transactions: [VF25, VF24]
tables: []
aliases:
  - VF25
  - VF24
  - invoice list
  - lista de facturas
  - LR billing type
  - LG billing type
  - RL00 condition type
  - MW15 condition type
  - factoring discount
  - descuento de factoring
  - purchasing association billing
  - facturación asociación de compras
  - head office invoice
  - factura central
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Invoice Lists in SAP SD

## Operational Summary
An *invoice list* collates multiple individual billing documents for different stores or delivery locations into a single consolidated document, settled periodically with the head office. The head office receives one invoice list instead of dozens of individual invoices. Invoice lists are created with transaction *VF25*; the corresponding worklist is processed with *VF24*. The invoice list's reference number overwrites the reference numbers of all underlying billing documents in Financial Accounting, linking the open items together.

## Questions This Chunk Answers
- What is an invoice list and when is it used?
- Which transactions are used to create and process invoice lists?
- What master data and Customizing configuration is required for invoice lists?
- How does a factoring discount work with invoice lists?
- What billing types are included in an invoice list?
- What happens to individual invoice reference numbers when an invoice list is created?

## Definition
An *invoice list* is a summary billing document that groups multiple individual invoices, credit memos, or debit memos for a specific payer (typically a head office) into a single settlement document issued on defined dates. It does not replace the individual billing documents — it consolidates them for payment purposes.

## Purpose in the SD Process
Invoice lists are primarily used in **purchasing association** scenarios, where a head office pays on behalf of multiple subsidiary stores. Instead of the head office reconciling hundreds of individual invoices, it receives a single invoice list on predefined dates (controlled by a factory calendar in the payer's customer master).

When the invoice list is created, its reference number is written into the reference fields of all underlying individual billing documents. This links the individual open items to the invoice list in Financial Accounting for efficient clearing.

## Structure and Variants

| Variant | Billing Type | Content |
|---|---|---|
| Invoice list for invoices/debit memos | LR | Standard invoices (F2), debit memos (L2) |
| Invoice list for credit memos | LG | Credit memos (G2) |

Factoring discounts (condition type *RL00*, with associated condition *MW15* for tax) can be agreed with the payer and applied at invoice list level.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Payer Customer Master | *InvoicingListDates* field (Billing Documents tab): factory calendar that defines when invoice lists are created |
| Individual Billing Documents | Included in the list; their FI reference numbers are overwritten with the invoice list reference |
| Output Condition Records | Types LR00 and RD01 must have condition records to control output routing |
| Billing Type Customizing | Each billing type to be included must be assigned to an invoice list type |
| RL00 / MW15 Condition Types | Factoring discount applied at invoice list level if agreed with the payer |

## Cross-References
- See also: billing-invoice-combination-and-split-001
- See also: enterprise-structure-head-office-branch-billing-001
- See also: configuration-billing-types-sap-s4hana-001
