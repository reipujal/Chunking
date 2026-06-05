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
    pages: "115, 124"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - returns
  - devoluciones
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The returns process initiates when a dissatisfied customer physically sends back goods resulting in an inbound returns delivery. It ultimately yields a credit memo to compensate the customer seamlessly.

## Questions This Chunk Answers
- How is billing processed for customer returns?
- Which document does a standard return credit memo reference?

## Process Overview
1. **Returns Order**: A dedicated returns sales order is structurally created to register the impending inbound goods movement.
2. **Returns Delivery**: An inbound "returns delivery" is processed when the goods physically securely re-enter the stock.
3. **Credit Memo Generation**: Ultimately, a credit memo is generated to formally complete the compensation.

## Billing Reference Logic
Returns are systematically handled utilizing the exact same overarching rulesets applied to arbitrary credit memo requests. 

**Critical Rule:** While a physical returns delivery exists to log the inventory movement, the subsequent generating *credit memo is billed exclusively with direct reference to the parent order* (the return request document)—it does **not** reference the returns delivery document directly for billing.
