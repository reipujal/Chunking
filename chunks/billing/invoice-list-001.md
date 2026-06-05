---
schema_version: 1
id: billing-invoice-list-001
title: "Invoice Lists in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "57-58, 106"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - invoice list
  - lista de facturas
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
An *invoice list* is a mechanism by which multiple individual billing documents for varying locations or stores are collated and settled together at specific time intervals, typically directed to a head office acting on behalf of a purchasing association.

## Questions This Chunk Answers
- What are invoice lists used for?
- What configuration steps and master data are required to enable invoice lists?

## Purpose in the SD Process
Invoice lists are prominently used by purchasing associations. In this scenario, the head office settles billing documents for all subsidiary stores. Rather than the head office receiving dozens of individual invoices, it receives a single consolidated invoice list on specific dates. The list can encompass standard invoices, credit memos, and debit memos for a particular payer. 

When the invoice list is created, its reference number overwrites the reference numbers of the underlying individual billing documents, linking the open items together in Financial Accounting.

## Relationship with Other SAP SD Objects
To deploy invoice lists, the system administrator must configure specific data in Customizing and Master Data:
- **Factory Calendar**: Define a factory calendar dictating when invoice lists are created, and assign this calendar to the `InvoicingListDates` field on the Billing Documents tab of the payer's customer master record.
- **Factoring Discounts**: If a factoring discount is agreed upon, maintain the condition type `RL00` (factoring discount) as well as the related condition type `MW15` for the payer.
- **Output Types**: Create output condition records for the types `LR00` and `RD01` to physically route the documents properly.
- **Invoice List Types**: Every billing type to be included must be assigned securely to an invoice list type (e.g., standard SAP types `LG` for credit memos and `LR` for invoices/debit memos).
