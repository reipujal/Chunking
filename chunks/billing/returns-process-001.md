---
schema_version: 1
id: billing-returns-process-001
title: "The Returns Process in SAP SD Billing"
area: billing
process_tags: [order-to-cash, billing, returns]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "123, 132"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - returns
  - devoluciones
  - customer return
  - devolución de cliente
  - returns credit memo
  - nota de crédito por devolución
  - returns order
  - pedido de devolución
  - returns delivery
  - entrega de devolución
  - RE billing type
  - goods return billing
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# The Returns Process in SAP SD Billing

## Operational Summary
The returns process handles goods physically sent back by a dissatisfied customer. It involves three successive documents: a *returns order* (to record the return request), a *returns delivery* (to process the inbound goods movement), and a *credit memo* (to compensate the customer financially). A critical rule governs the billing step: the credit memo is created with reference to the *returns order*, not the *returns delivery*.

## Questions This Chunk Answers
- What is the complete document sequence for processing a customer return?
- Which document does the returns credit memo reference — the returns order or the returns delivery?
- Does the returns delivery affect the billing process?
- What billing type is used for returns in the standard system?
- How does the returns process relate to the credit memo request process?

## When It Applies and Context
Use the returns process when a customer sends goods back and expects financial compensation (credit to their account). The returns delivery records the physical goods receipt into stock. The credit memo settles the financial obligation. Both logistics and billing dimensions are handled in separate documents.

## Process Flow
1. **Returns Order**: A dedicated returns sales order is created to register the incoming goods and authorize the return. This is the anchor document for the credit memo.
2. **Returns Delivery**: When the goods physically re-enter stock, an inbound *returns delivery* is processed and goods receipt is posted. This affects inventory but does not trigger billing.
3. **Credit Memo Generation**: A credit memo is created to financially compensate the customer. In the standard system, billing type *RE* is used.

## Billing Reference Logic
The credit memo for a return follows the same rules as a standard credit memo request.

**Critical Rule**: The credit memo is created **with reference to the returns order** — not the returns delivery. The returns delivery exists solely for the inventory/warehouse movement; it is not a billing reference for the credit memo.

This means the credit memo copies pricing, quantities, and partner data from the returns order, not from the delivery document.

## Conditions and Restrictions
- The returns order must exist and be in a billable status before the credit memo can be created.
- Billing relevance for the returns item category must be set to order-related billing (since billing references the order, not the delivery).
- A billing block may be set automatically on the returns order, requiring release before billing.

## Common Errors

**Credit memo created but references wrong document**
→ The credit memo for a return must reference the *returns order*, not the returns delivery. Verify the reference document type in copying control for the RE billing type.

**Returns credit memo not appearing in billing due list**
→ The returns order has a billing block set. Release the block on the order before processing the credit memo.

## Cross-References
- See also: billing-credit-debit-memo-process-001
- See also: billing-invoice-correction-request-process-001
- See also: shipping-inbound-delivery-ewm-001
