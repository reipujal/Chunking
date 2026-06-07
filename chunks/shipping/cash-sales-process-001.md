---
schema_version: 1
id: shipping-cash-sales-process-001
title: "The Cash Sales Process in SAP SD"
area: shipping
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "122-123"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - cash sale
  - venta al contado
  - venta al contado SAP
  - CS order type
  - tipo de pedido CS
  - RD03 output type
  - cash settlement account
  - cuenta de liquidación en efectivo
  - SV cancellation
  - cash invoice
  - recibo de caja
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# The Cash Sales Process in SAP SD

## Operational Summary
A *cash sale* is a process where the customer orders, pays, and picks up goods simultaneously at the point of sale. SAP handles this with order type *CS*, which combines order and delivery creation in a single step, prints an immediate cash receipt via output type *RD03*, and posts the payment directly to a cash clearing account (not an open customer receivable). The goods issue is finalized asynchronously in a background program. Cash sale cancellations use billing type *SV*.

## Questions This Chunk Answers
- How does the cash sales process differ from a standard order-to-cash process?
- What order type is used for cash sales?
- When is the billing document created in a cash sale — before or after goods issue?
- Why is there no open customer receivable in a cash sale?
- How are cash sale cancellations processed?
- What output type prints the cash receipt immediately?

## When It Applies and Context
Cash sales apply to counter or walk-in sales where the customer pays immediately and takes the goods. There is no credit involved — payment is immediate and settlement goes directly to a cash account, not the customer's accounts receivable balance.

## Process Flow

1. **Order and Delivery in One Step**: When the cash sale order (type *CS*) is saved, the system automatically creates the outbound delivery at the same time. No separate delivery creation step is needed.
2. **Instant Cash Receipt**: The process uses order-related billing logic. Output type *RD03* prints an immediate cash receipt (invoice) directly from the order at the time of creation. Prices are fixed at this point.
3. **Postponed Goods Issue**: Because the customer picks up goods immediately, picking is typically not required. The goods issue posting is deferred and usually executed by a background program.
4. **Billing Update (CS)**: After goods issue is posted, a billing document is created using billing type *CS* to formally update the system. Note: the invoice is *not* printed again at this stage — only the billing status is updated.
5. **Financial Posting**: The posting goes to a *cash settlement account* (a G/L account defined specifically for cash sales), not to the customer's open receivables account.

For cancellations, use billing type *SV*.

## Conditions and Restrictions
- A G/L account for cash settlement must be configured in account determination; without it the cash sale posting fails.
- Picking is typically not relevant for cash sales since the customer takes goods immediately.
- The cash receipt is printed at order creation — no re-print occurs at billing.

## Common Errors

**Cash sale posting fails for cash settlement**
→ A G/L account for cash settlement must be configured. Set the account in account determination for the CS billing type and sales organization combination.

**Invoice printed twice (once at order, once at billing)**
→ Output for billing type CS must not have a print output type assigned (the receipt was already printed at order creation via RD03). Check output determination for billing type CS.

## Cross-References
- See also: billing-billing-document-creation-methods-001
- See also: configuration-billing-account-determination-001
- See also: shipping-goods-issue-ewm-001
