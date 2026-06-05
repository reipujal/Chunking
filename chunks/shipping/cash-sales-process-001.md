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
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "114-115"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - cash sale
  - venta al contado
  - CS
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
A *cash sale* involves the customer ordering, immediately paying for, and physically picking up goods simultaneously. Unlike standard operations, it prints a cash invoice (receipt) immediately upon order creation, and receivables are pushed directly to a cash clearing account instead of an open customer account.

## Questions This Chunk Answers
- How is the cash sales sequence structurally different from a standard order?
- What order type is used for cash sales?

## Process Flow and Characteristics
The cash sales sequence executes via specific synchronization steps utilizing the order type `CS`:

1. **Order and Delivery Sync**: The order and the delivery are generated virtually in a single step the moment the order is entered. 
2. **Instant Invoicing (Receipt)**: The process physically behaves as order-related billing. It utilizes a dedicated output type `RD03`, allowing the system to instantly print an invoice receipt deriving data straight from the order. Since the printed invoice confirms the price, there is no discrete subsequent price determination later.
3. **Postponed Goods Issue**: Because the customer picks up the goods instantly, picking is typically not relevant. The actual statistical posting of the goods issue is purposefully delayed and usually executed asynchronously via a background program later on.
4. **Billing Update (CS)**: After the goods issue is successfully posted, you create the final billing document formally using billing document type `CS`. Note strongly: despite triggering this update, the invoice document is intentionally *not* physically printed again. 
5. **Financial Postings**: Posting to FI deposits directly into a cash settlement account, not the traditional customer account. 

To process any cancellations associated functionally with cash sales, you explicitly utilize billing type `SV`.
