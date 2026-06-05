---
schema_version: 1
id: configuration-billing-account-determination-001
title: "Account Determination for Billing in SAP SD"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "88-90"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - account determination
  - determinación de cuentas
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
*Account Determination* establishes the exact bridge mapping SD billing events to specific general ledger (G/L) accounts in Financial Accounting (FI). This ensures sales revenue, sales deductions, cash settlements, and reconciliation accounts are accurately impacted.

## Questions This Chunk Answers
- How does the system automatically know which G/L account to post revenue to?
- What are the assignment criteria for account determination?

## Account Assignment Criteria
To successfully post an SD transaction to FI, the system cross-references several criteria to identify the target account:
1. **Chart of accounts**: Required to isolate the correct accounting ledger.
2. **Sales organization**: Segregates accounting per sales department structure.
3. **Account assignment group for payer**: Used to classify customers (e.g., domestic versus overseas revenue).
4. **Account assignment group for material**: Used to classify the goods being sold (e.g., service revenue versus retail goods revenue).
5. **Account key**: Found in pricing procedures, assigning condition types (like freight surcharges) to specialized revenue accounts.

## Mechanism: Condition Technique
Account determination leverages the standard SAP *condition technique*. 
- A *determination procedure* is assigned to a given billing type.
- The procedure utilizes *condition types*, each tied to an *access sequence*.
- The access sequence cascades through specific *condition tables*, extracting the matching G/L account based on the criteria mentioned above.

## Notes
- Cash sales feature unique handling. You must configure a G/L account explicitly for cash settlement instead of posting to an open customer account.
- The G/L account for posting Value-Added Tax (VAT) is **not** determined by this SD account determination logic; it is managed strictly in Financial Accounting (Tax on Sales/Purchases).
