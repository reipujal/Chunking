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
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "62-64"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - invoice split
  - partición de factura
  - invoice combination
  - combinación de facturas
  - split criteria
  - criterios de partición
  - VBRK-ZUKRI
  - collective billing document
  - factura colectiva
  - automatic split
  - partición automática
  - one invoice per order
  - una factura por pedido
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Invoice Combination and Split in SAP SD

## Operational Summary
By default, SAP attempts to combine all compatible billing items — from multiple orders or deliveries — into a single collective billing document. When header-level data (payer, terms of payment, destination country) differs across items, the system automatically splits them into separate invoices. Additional item-level split rules can be configured in copying control to force splits even when headers match. The `VBRK-ZUKRI` field holds the additional split criteria and can be inspected in a split analysis log.

## Questions This Chunk Answers
- When does the system combine multiple reference documents into a single collective invoice?
- What triggers an automatic invoice split?
- Can you force an invoice split based on item-level attributes like material group or profit center?
- How do you configure one billing document per sales order?
- What field stores additional item-level split criteria in the billing header?
- How can you diagnose why two items ended up in different invoices?

## Definition
*Invoice combination* is the system's default behavior of merging compatible billing items (from different orders or deliveries) into one collective billing document to reduce document volume. *Invoice split* is the automatic or configured separation of items into multiple invoices when combination is not possible or not desired.

## Purpose in the SD Process
Combination reduces the number of billing documents and simplifies payment processing for customers (one payment for many deliveries). Splits are necessary when legal, financial, or commercial rules require separate invoices (different tax jurisdictions, different terms of payment, different payers).

## Structure and Variants

### Automatic Invoice Split (Header-Dependent)
All header-level partners and fields act as baseline split criteria. If any of the following differ across items being billed, the system automatically creates separate invoices:
- Payer
- Terms of payment
- Destination country
- Any other billing header field that is defined as a split criterion

### Item-Dependent Invoice Split (Configured)
The system administrator can define additional item-level split rules in **copying control**. This forces splits even when all header fields match:
- Example: one invoice per profit center, or separate invoices per material group.
- To create exactly **one billing document per sales document**, specify data transfer routine `3` in copying control. The `VBRK-ZUKRI` field in the billing header stores these additional criteria.

A **split analysis log** is available to diagnose why items ended up in different invoices — it shows which field triggered the split.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Copying Control | Item-level split criteria configured here (data transfer routine, VBRK-ZUKRI) |
| Billing Due List | Combination attempts are made per billing run — items in the same run but with different criteria are split automatically |
| Payer Master | If two items have different payers, they will never combine |
| Invoice List | Separate invoices (after split) can be grouped in an invoice list for consolidated settlement |

## Cross-References
- See also: billing-invoice-list-001
- See also: configuration-billing-copying-control-001
- See also: billing-billing-document-creation-methods-001
