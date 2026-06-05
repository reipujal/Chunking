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
    pages: "108"
    source_type: "A"
    role: "primary"
transactions: []
tables: ["001"]
aliases:
  - negative posting
  - contabilización negativa
  - credit memo negative posting
  - nota de crédito contabilización negativa
  - reverse posting FI
  - contabilización inversa FI
  - inflated ledger credit memo
  - factura tabla 001 FI
  - FI table 001
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Negative Postings for Billing Documents

## Operational Summary
Negative postings cause cancellations and credit memos to reduce the **same side** of the general ledger account (rather than posting to the opposing credit/debit side), keeping ledger totals clean and intuitive. Without negative postings, a credit memo adds to both sides of the ledger (a debit entry and a credit entry), inflating both totals even though no net sale occurred. This feature is activated in the billing type and requires enabling in the FI company code settings (table `001`).

## Questions This Chunk Answers
- What is the difference between a standard credit memo posting and a negative posting?
- Why do credit memos without negative posting inflate both sides of the ledger?
- Where is the negative posting indicator configured in SD?
- What FI configuration is required for negative postings to take effect?
- Which billing types typically use negative postings?

## What This Configuration Controls
The negative posting indicator in the billing type controls whether the FI posting for that document type is made as a standard opposing-side entry (normal credit memo behavior) or as a **negative amount on the same side** as the original transaction (reducing the total instead of adding to both sides).

## SPRO Path or Direct T-code
Sales and Distribution → Billing → Billing Documents → Define Billing Types
(Field: *Negative posting* in the billing type settings)

FI prerequisite:
Financial Accounting → Financial Accounting Global Settings → Company Code → Enter Global Parameters
(Negative postings must also be permitted at company code level — controlled in FI table `001`)

## Key Parameters

| Setting | Behavior |
|---|---|
| Negative posting = blank in billing type | Standard opposing-side posting (normal credit memo behavior) |
| Negative posting = active in billing type | Negative amount on same side — requires FI company code to also permit negative postings |
| FI table `001` — negative posting permitted | Must be enabled in FI for the feature to take effect end-to-end |

## Configuration Impact
Negative postings are relevant for customers who run statutory financial reports that must show clean, unambiguous totals. Typical use: credit memos (G2), cancellation documents (S1, S2), and returns (RE). Without this configuration, high-volume credit activity inflates both debit and credit totals on revenue accounts, making period-end reconciliation more complex.

## Common Configuration Errors

**Negative posting indicator active in SD billing type, but behavior in FI is still standard**
→ The FI company code has not enabled negative postings in its global parameters (table `001`). Enable the setting at company code level.

**Negative postings enabled globally but unwanted for some billing types**
→ The negative posting indicator in SD is controlled per billing type — set it only for the credit memo and cancellation types, not for standard invoices.

## Cross-References
- See also: billing-credit-debit-memo-process-001
- See also: configuration-billing-fi-interface-controls-001
- See also: configuration-billing-types-sap-s4hana-001
