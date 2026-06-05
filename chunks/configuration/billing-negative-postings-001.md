---
schema_version: 1
id: configuration-billing-negative-postings-001
title: "Negative Postings for Billing Documents"
area: configuration
process_tags: [order-to-cash, billing, credit-memo, returns]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "100"
    source_type: "A"
    role: "primary"
transactions: []
tables: ["001"]
aliases:
  - negative posting
  - contabilización negativa
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The negative posting feature forces cancellations and credit memos to mathematically reduce identical-side account totals in Financial Accounting rather than posting traditionally to the opposing debit/credit side.

## Questions This Chunk Answers
- How do you prevent credit memos from inflating both sides of an accounting ledger?
- Where is the negative posting indicator stored?

## What This Configuration Controls
In a standard SAP system, cancellations and credit memos are traditionally posted on the opposite side of the account compared to standard receivables. While mathematically identical, this can superficially inflate the "sales" totals line visually on both sides of a ledger despite no net sale taking place.

Customers frequently request that credit memos and cancellations be posted securely on the *exact same side* as the receivables but executed as a negative amount. Consequently, the totals line maintains an intuitive zero balance.

## Setup
To achieve this behavior, you must activate the **Negative posting** field explicitly within the billing type configuration for credit memos and cancellations. 
The system automatically transfers this designated indicator to Financial Accounting. Negative posting ultimately takes effect only if it is concurrently permitted by the receiving FI company code (this safety constraint is controlled securely in the FI table `001`).
