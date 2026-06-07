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
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "109"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - value dated credit memo
  - nota de crédito con fecha valor
  - credit memo with value date
  - nota de crédito fecha base de pago
  - VALDT field
  - campo fecha valor
  - baseline payment date credit memo
  - fecha base de pago nota de crédito
  - credit memo payment synchronization
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Value Dated Credit Memos in SAP

## Operational Summary
Value dating for credit memos synchronizes the baseline payment date of a credit memo with the baseline payment date of the original invoice it corrects. Without value dating, the credit memo falls due immediately on its own billing date, creating a mismatch with the original invoice that makes automated payment run reconciliation difficult. When activated, the system copies the original invoice's baseline date into the credit memo's `VALDT` field.

## Questions This Chunk Answers
- Why are credit memos sometimes not synchronized with their original invoice in payment runs?
- How is value dating activated for credit memos?
- Where is the value date stored in the billing document?
- What happens if the original invoice's baseline date is earlier than the credit memo's billing date?
- Which billing type setting controls value dating behavior?
- When does copying of the baseline date get aborted?

## Definition
*Value dating* on a credit memo is the mechanism by which the system copies the baseline payment date from the originating invoice into the `VALDT` (Value Date) field of the credit memo. This ensures that when payment runs execute, the credit memo is netted against the original invoice using aligned dates, enabling clean clearing of the receivable.

## Purpose in the SD Process
In automated payment runs (e.g., payment program in FI), open items are matched and cleared. If a credit memo has a different baseline payment date than the original invoice, the two items are not aligned for clearing and the reconciliation produces a residual balance. Value dating eliminates this date mismatch, ensuring the credit memo cancels the original invoice cleanly in the payment run.

## Structure and Variants
The `Credit memo w/ ValDat` indicator in billing type settings controls the behavior:

| Indicator | Behavior |
|---|---|
| Blank | Credit memo falls due on its own billing date (no value date copied) |
| Active | Baseline payment date from the originating invoice is copied into the credit memo's VALDT field |

**Restriction**: The date is only copied if the original invoice's baseline payment date is **not earlier** than the credit memo's current billing date. If the original date predates the credit memo's billing date, copying is aborted to prevent retroactive dating.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Original Billing Document | Source of the baseline payment date (VALDT) |
| Credit Memo | Target document — VALDT field populated if indicator is active |
| FI Payment Run | Uses VALDT for clearing alignment between invoice and credit memo |
| Billing Type Customizing | Credit memo w/ ValDat indicator configured per billing type |

## Cross-References
- See also: billing-credit-debit-memo-process-001
- See also: configuration-billing-types-sap-s4hana-001
