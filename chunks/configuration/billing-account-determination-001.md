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
    pages: "96-98"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - account determination
  - determinación de cuentas
  - G/L account SD billing
  - cuenta mayor facturación SD
  - revenue account determination
  - determinación cuenta de ingresos
  - account assignment group payer
  - grupo asignación de cuentas pagador
  - account assignment group material
  - grupo asignación de cuentas material
  - account key
  - clave de cuenta
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Account Determination for Billing in SAP SD

## Operational Summary
*Account determination* in SD billing identifies which General Ledger (G/L) accounts receive postings when a billing document is released to Financial Accounting. The system cross-references five criteria — chart of accounts, sales organization, account assignment group (payer), account assignment group (material), and account key — using the standard *condition technique*. VAT account determination is handled separately in FI, not in SD account determination.

## Questions This Chunk Answers
- How does SAP automatically determine which G/L account to post revenue to?
- What are the five criteria used in account determination?
- How does the condition technique apply to account determination?
- How are customer and material segments differentiated in account posting?
- Is the VAT G/L account determined in SD account determination?
- What is the account key and where is it defined?

## What This Configuration Controls
Account determination bridges SD billing events to FI G/L accounts for:
- Sales revenue (domestic vs. overseas, service vs. retail)
- Sales deductions (discounts, rebates)
- Cash settlement accounts (for cash sales — no customer receivable)
- Freight revenue (via account keys in pricing procedures)
- Reconciliation accounts (when different from the standard payer master)

## SPRO Path or Direct T-code
Sales and Distribution → Basic Functions → Account Assignment/Costing → Revenue Account Determination
- Sub-node: *Define And Assign Account Determination Procedures*
- Sub-node: *Define Access Sequences and Account Determination Types*

Note: G/L accounts for VAT are configured in FI (Financial Accounting Global Settings → Tax on Sales/Purchases → Posting → Define Tax Accounts) — not in SD account determination.

## Key Parameters

| Criterion | Purpose |
|---|---|
| Chart of accounts | Identifies the applicable G/L account master (one per company code) |
| Sales organization | Segregates accounts by sales structure (e.g., domestic vs. export org) |
| Account assignment group (payer) | Classifies customers: e.g., domestic vs. overseas revenue |
| Account assignment group (material) | Classifies goods: e.g., services vs. retail goods vs. trading goods |
| Account key | Assigned to condition types in pricing procedures; directs freight, rebates, surcharges to dedicated accounts |

The account assignment groups for payer are maintained in the payer's customer master record. The account assignment group for material is maintained in the material master (sales org data). Account keys are assigned in the pricing procedure Customizing.

## Configuration Impact
Account determination must be configured before billing documents can be released to accounting. Gaps in account determination (missing condition records, wrong account assignment groups) cause release errors. For cash sales specifically, a G/L account for cash settlement must be explicitly configured — there is no default open customer account posting for cash transactions.

## Common Configuration Errors

**"Account determination error" when releasing billing document to accounting**
→ The combination of chart of accounts + sales organization + account assignment group (payer) + account assignment group (material) + account key has no condition record in the account determination procedure. Maintain the missing record.

**Revenue posted to wrong G/L account**
→ Verify the account assignment group on the payer customer master and on the material master. An incorrect group maps to the wrong revenue account.

**VAT account missing — not found via SD account determination**
→ VAT accounts are defined in FI Customizing, not in SD. Check Tax on Sales/Purchases → Define Tax Accounts in FI.

## Cross-References
- See also: billing-billing-document-integration-001
- See also: configuration-billing-fi-interface-controls-001
- See also: shipping-cash-sales-process-001
