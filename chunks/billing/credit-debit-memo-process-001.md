---
schema_version: 1
id: billing-credit-debit-memo-process-001
title: "Processing Credit and Debit Memos in SAP S/4HANA"
area: billing
process_tags: [order-to-cash, billing, credit-memo, debit-memo, complaints]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "30-32"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - credit memo
  - nota de crédito
  - nota de abono
  - debit memo
  - nota de débito
  - nota de cargo
  - credit memo request
  - solicitud de nota de crédito
  - debit memo request
  - solicitud de nota de débito
  - complaint billing
  - facturación por reclamación
  - WS00800286
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Processing Credit and Debit Memos in SAP S/4HANA

## Operational Summary
Credit and debit memos settle discrepancies or complaints with customers. They can be created with reference to a credit or debit memo *request* (a sales document used for the approval workflow), or directly from a billing document when no release procedure is needed. SAP S/4HANA provides a workflow app (*Manage Credit Memo Request Workflow*) to automate approval routing, including configurable automatic release thresholds and multi-level approver assignments.

## Questions This Chunk Answers
- How are credit and debit memos created in SAP SD?
- What is the difference between a credit memo request and the credit memo itself?
- When does the system set a billing block on a credit memo request?
- How is the workflow for credit memo approval managed in S/4HANA?
- Can credit memo requests be created without reference to a prior document?
- What happens to rejected items in a credit memo request?

## When It Applies and Context
Use credit memos when a customer has been overcharged or has returned goods and is owed compensation. Use debit memos when the customer was undercharged. The credit/debit memo request is the preliminary document that goes through an approval cycle before the actual billing document is created.

## Process Flow
1. **Create the Request**: Credit and debit memo requests can be created without any reference, with reference to a sales order, or with reference to a billing document.
2. **Billing Block (Optional)**: Customizing controls whether the system sets a billing block automatically on the request when it is created — this is the standard for credit memo requests that require approval.
3. **Approval/Release Workflow**: The responsible employee reviews the request and can:
   - **Release** it by removing the billing block, and adjust the amount or quantity to be credited.
   - **Reject** items by entering a reason for rejection. Rejected items are either copied into the credit memo with zero value or excluded entirely — controlled by the rejection reason configuration.
4. **Billing**: Once released (billing block removed), the credit or debit memo is created from the request in the same way as a standard invoice.

## Approval Workflows in SAP S/4HANA
The *Manage Credit Memo Request Workflow* app enables configurable approval workflows:
- Define conditions for **automatic release** (e.g., below a minimum value threshold — no human approval needed).
- Assign specific **approvers** for different value thresholds.
- Notifications go directly to the approver's *My Inbox* or *Notifications* tile.
- Approvers can approve, reject, or request rework without leaving Fiori.

The SAP standard workflow `WS00800286` must be activated before using this app.

## Conditions and Restrictions
- A credit memo request with an active billing block cannot be billed until the block is removed.
- Debit memo requests follow the same process and Customizing as credit memo requests.
- Item rejection reasons must be configured in Customizing to control the copy behavior (zero-value copy vs. complete exclusion).

## Common Errors

**Credit/debit memo request is blocked and cannot be billed**
→ The billing block is set (common by design for credit memos pending approval). Release the block via the approval process or manually if authorization permits.

**Rejected item still appears on the credit memo with full value**
→ The rejection reason configuration does not suppress the item. Check the reason for rejection settings to confirm they zero out or exclude the item during billing copy.

**Workflow notifications not reaching the approver**
→ Verify workflow `WS00800286` is activated and that the approver is correctly maintained in the workflow configuration.

## Cross-References
- See also: billing-invoice-correction-request-process-001
- See also: billing-returns-process-001
- See also: billing-value-dated-credit-memos-001
- See also: configuration-billing-negative-postings-001
- See also: configuration-billing-types-sap-s4hana-001
