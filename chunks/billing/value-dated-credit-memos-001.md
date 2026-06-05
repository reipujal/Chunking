---
schema_version: 1
id: billing-value-dated-credit-memos-001
title: "Value Dated Credit Memos in SAP"
area: billing
process_tags: [order-to-cash, billing, credit-memo]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "101"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - value dated credit memo
  - nota de crédito con fecha valor
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Value dating for credit memos allows the system to harmonize the baseline payment date on a credit memo with the baseline payment date of the original invoice it stems from. This successfully synchronizes due dates to accurately reconcile the receivables and payables in the upcoming payment run.

## Questions This Chunk Answers
- Why are credit memos sometimes not synchronized with their original invoice in FI?
- How is the baseline payment date copied to a credit memo?

## Relationship with Other SAP SD Objects
Historically, when users created credit memo requests with reference to an existing billing document, the baseline dates for payment were completely decoupled and different. This disparity made it virtually impossible to cleanly reconcile the receivables against the payables efficiently.

## Activating Value Dating
You control this dynamic mechanism via the `Credit memo w/ ValDat` (credit memo with value date) indicator situated securely in the billing type settings.

- **Indicator Blank**: The credit memo falls due immediately on its own present billing date.
- **Indicator Active**: The baseline payment date from the originating invoice is actively populated directly into the `VALDT` (Value Date) field on the credit memo.

### Restriction
The date is copied conditionally. If the baseline date for payment from the originating historical invoice precedes the *current* billing date of the credit memo, copying is intentionally aborted, preventing retroactive dating paradoxes.
