---
schema_version: 1
id: shipping-outbound-delivery-monitor-001
title: "Outbound Delivery Monitor in SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "62-63"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - outbound delivery monitor
  - monitor de entregas de salida
  - inbound delivery monitor
  - monitor de entregas de entrada
  - delivery worklist
  - lista de trabajo de entregas
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Outbound Delivery Monitor in SAP SD

<!-- inferred transactions, pending validation: VL06O (outbound delivery monitor), VL06I (inbound delivery monitor) — the source describes both monitors by function only and does not print the T-codes -->

## Operational Summary
The *Outbound Delivery Monitor* is a central transaction for monitoring and executing all delivery-related activities. It displays all outbound deliveries — both pending and completed — and allows executing subsequent functions directly from the list, including picking transfer order creation and goods issue posting in collective background processing. An equivalent *Inbound Delivery Monitor* exists for inbound delivery activities.

## Questions This Chunk Answers
- What does the Outbound Delivery Monitor display?
- What functions can be executed from the monitor?
- Can the monitor be personalized for specific users or teams?
- Is there an equivalent monitor for inbound deliveries?

## Definition
The Outbound Delivery Monitor displays all deliveries that are still to be processed or have already been processed. From the resulting list, users can perform subsequent functions on individual or groups of deliveries.

## Purpose in the SD Process
The monitor serves as the operational control centre for the shipping department. It provides visibility into all active deliveries and enables collective background processing of repetitive tasks — eliminating the need to process each delivery individually.

## Structure and Variants

### Selection and Display
- Users can define **user-specific selection variants** to filter deliveries by criteria such as shipping point, route, delivery date, or processing status.
- **Display variants** control which columns are visible in the list view.
- The list can be sorted, filtered, and summed using standard ALV functionality.

### Functions Available from the List
From the Outbound Delivery Monitor, users can execute the following in collective background processing:
- **Creation of transfer orders** for picking (WM)
- **Posting of goods issue**

Additional document navigation is also available: branching directly to individual delivery documents from the list.

### Inbound Delivery Monitor
The inbound delivery monitor provides the same capabilities for monitoring and executing inbound delivery activities (goods receipt processing, putaway, etc.).

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Outbound Delivery | Primary object displayed and processed in the outbound delivery monitor |
| Transfer Order (WM) | Can be created in background from the outbound delivery monitor for picking |
| *Goods Issue* | Can be posted in background from the outbound delivery monitor |
| Inbound Delivery | Monitored and processed via the inbound delivery monitor |

## Cross-References
- Delivery creation via Delivery Due List: shipping-outbound-delivery-creation-process-001
- EWM picking process: shipping-ewm-picking-process-001
- Goods Issue posting in EWM: shipping-goods-issue-ewm-001
