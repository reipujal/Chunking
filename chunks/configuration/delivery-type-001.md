---
schema_version: 1
id: configuration-delivery-type-001
title: "Delivery Type in SAP SD — Concept and Configuration"
area: configuration
process_tags: [order-to-cash, delivery-processing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "29-30"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivery type
  - tipo de entrega
  - LF
  - RE
  - EL
  - NL
  - LO
  - delivery document type
  - tipo de documento de entrega
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Delivery Type in SAP SD — Concept and Configuration

## Operational Summary
The *delivery type* is the primary control object of the delivery document. It is visible in the delivery header and governs the entire delivery processing. Each business transaction in shipping and goods receipt is modelled using a distinct delivery type. The delivery type is derived from the sales order type via copying control.

## Questions This Chunk Answers
- What is a delivery type and what does it control?
- What standard delivery types exist in SAP SD?
- How does the system determine which delivery type to use?
- Can delivery types be customized?

## What This Configuration Controls
The delivery type controls the entire delivery document end to end: how it is created, which item categories it proposes, how copying control maps from preceding documents, and which billing type follows after goods issue.

## SPRO Path or Direct T-code
Logistics Execution → Shipping → Deliveries → Define Delivery Types

## Key Parameters

| Delivery Type | Description |
|---|---|
| LF | Standard outbound delivery (from sales order) |
| EL | Inbound delivery — shipping notification (from purchase order) |
| LB | Delivery for subcontract order |
| LO | Outbound delivery without order reference |
| LP | Delivery from project |
| RE | Returns delivery |
| NL | Replenishment delivery |

Additional control elements per delivery type allow configuring specific processing behaviour. The standard delivery types can be adjusted for business requirements. If major changes are needed, SAP recommends creating a new delivery type.

## Configuration Impact

### Determination from Order Type (Copying Control)
The delivery type of an outbound delivery is derived from the order type of the originating order. In copying control, each order type is linked to the allowed delivery types. When creating a delivery, the system proposes the delivery type defined in copying control. It is possible to manually select a different delivery type within the allowed alternatives.

### Shipping-Relevant Settings in Sales Order Type
The sales order type Customizing includes the following delivery-relevant fields:
- **Proposed delivery type**: which delivery type the system defaults for the outbound delivery
- **Delivery date proposal**: whether the system proposes a delivery date in the requested delivery date field and how far in the future
- **Automatic delivery creation**: whether the system creates the outbound delivery automatically in the background when the order is saved

### Delivery Relevance and Schedule Lines
- Delivery relevance for text and value items is set at the order item category level.
- For normal items, delivery relevance is controlled at the schedule line level.
- Schedule lines must be allowed for the order item category to enable inventory management posting (GI).
- The movement type for GI is defined in the schedule line category.

## Common Configuration Errors
- Order type not linked to a delivery type in copying control → delivery creation fails.
- Schedule lines not allowed for item category → delivery items cannot post GI.
- Movement type missing in schedule line category → goods movement type cannot be determined.

## Cross-References
- Delivery item category determination: configuration-delivery-item-category-001
- Copying control and delivery split: configuration-delivery-process-customizing-001
- Delivery document structure: shipping-delivery-document-structure-001
