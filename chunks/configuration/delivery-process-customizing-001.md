---
schema_version: 1
id: configuration-delivery-process-customizing-001
title: "Delivery Process Customizing — Copying Control, Split Criteria, and Special Scenarios"
area: configuration
process_tags: [order-to-cash, delivery-processing, returns, stock-transfer]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "33-37"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - copying control delivery
  - control de copia entrega
  - delivery split criteria
  - criterios de división de entrega
  - order combination delivery
  - combinación de pedidos entrega
  - outbound delivery without reference
  - entrega de salida sin referencia
  - inbound delivery customizing
  - configuración entrega de entrada
  - confirmation category
  - categoría de confirmación
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-17
---

# Delivery Process Customizing — Copying Control, Split Criteria, and Special Scenarios

## Operational Summary
This chunk covers three interrelated Customizing areas: (1) the copying control table that governs how SD documents flow into deliveries; (2) delivery split and order combination logic; (3) specific Customizing for deliveries without order reference and inbound deliveries, which require additional configuration because they cannot inherit data from a sales order.

## Questions This Chunk Answers
- What does the copying control table control for deliveries?
- What criteria cause the system to split items into separate deliveries?
- Can multiple orders be combined into one delivery? How?
- How is a delivery without order reference configured?
- How is the inbound delivery Customizing set up when referencing a purchase order?

## What This Configuration Controls

### Copying Control
The copying control table defines:
- Which SD document types (order types) can be copied into which delivery types
- Which item categories are copied from the reference document to the delivery
- Under what conditions data is copied from the order to the outbound delivery
- Under what conditions several orders can be combined into one outbound delivery
- Which data fields are transferred
- Whether the reference is recorded in the document flow

## SPRO Path or Direct T-code
Logistics Execution → Shipping → Copying Control → Specify Copy Control for Deliveries

## Key Parameters

### Delivery Split Criteria
The system ships order items together if they are due for delivery and have identical delivery split criteria. **Mandatory split criteria** (always enforced):
- Shipping point
- Route
- Ship-to party

Optional split criteria defined in the standard system can be removed from the copying control table. Additional custom split criteria can also be added — if the defined fields differ between items, those items cannot be combined.

### Order Combination
When order combination is activated, the system groups together all orders or order items processed in the same delivery creation run, provided they match the delivery split criteria. Without order combination, each order generates a separate delivery.

### Customizing for Outbound Delivery Without Order Reference (LO)
When creating a delivery without order reference, the user must manually select the delivery type on the initial screen.

Required Customizing steps:
1. In the **delivery type** configuration, define a **default order type**. This provides access to order Customizing (since no real sales order exists).
2. Item category determination uses delivery type + item category group — same logic as order-independent items.
3. A corresponding order item category must exist for each delivery item category (needed for billing relevance and billing procedure).
4. To enable GI posting: the order item category must allow schedule lines; the schedule line category must define the movement type.

### Customizing for Inbound Delivery (EL and similar)
The delivery type of an inbound delivery is determined from the **confirmation category** Customizing (not from copying control).

Required Customizing steps:
1. In the confirmation category: define the delivery type (e.g., EL) and specify the preceding document type as purchase order.
2. In the delivery type (EL): define a **default order type** — required to access order Customizing for this process.
3. The default order type uses **copy control (Order Type → Delivery Type)** to transfer data from the PO to the delivery via data transfer routines.
4. Item category determination: uses item usage **V** (purchase order / stock transport).
5. A corresponding order item category must exist for the delivery item category (for the copying relationship between order and delivery).
6. For inbound delivery item categories of **SD document category 7** (e.g., ELN): the movement type for GR posting is maintained **directly in the delivery item category** (not in the schedule line category).

## Configuration Impact

| Scenario | Key Config Object | Where Movement Type Lives |
|---|---|---|
| Outbound delivery from sales order | Copying control (order type → delivery type) | Schedule line category |
| Outbound delivery without order ref | Default order type in delivery type config | Schedule line category |
| Inbound delivery from purchase order | Confirmation category → delivery type | Delivery item category (SD doc cat. 7) |

## Common Configuration Errors
- Missing default order type in delivery type → delivery without order reference cannot access billing and item category configuration.
- Missing order item category for a delivery item category → copying relationship between order and delivery not established; inbound delivery data transfer fails.
- Mandatory split criteria not aligned → unexpected delivery splits or combination failures.
- Movement type missing from delivery item category ELN → GR posting fails for inbound deliveries.

## Cross-References
- See also: configuration-sales-copying-control-001 (sales facet of copy control)
- See also: configuration-billing-copying-control-001 (billing facet of copy control)
- Supplementary: S4650 Unit 2 (phys 20-31) — unified cross-chain view of copy control across all three facets; S4650 is supplementary to these three authoritative chunks (density guardrail: not added as secondary source)
- Delivery type concept: configuration-delivery-type-001
- Delivery item category: configuration-delivery-item-category-001
- Shipping point and loading point: enterprise-structure-shipping-point-loading-point-001
