---
schema_version: 1
id: enterprise-structure-shipping-point-loading-point-001
title: "Shipping Point and Loading Point in SAP SD"
area: enterprise-structure
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "13"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - shipping point
  - punto de expedición
  - loading point
  - punto de carga
  - goods receipt point
  - punto de recepción de mercancías
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Shipping Point and Loading Point in SAP SD

## Operational Summary
The *shipping point* is the key organizational unit that controls delivery processing in SAP SD. Every outbound delivery is processed from exactly one shipping point. The *loading point* is an optional sub-unit used to further structure operations within a shipping point. Both are defined in Customizing and assigned to plants.

## Questions This Chunk Answers
- What is a shipping point and what does it control?
- How is the shipping point determined on a delivery?
- Can one shipping point serve multiple plants?
- What is a loading point and how does it relate to the shipping point?
- Can a shipping point be used for goods receipts (inbound deliveries)?

## Definition

### Shipping Point
An independent organizational unit at a fixed physical location that processes and monitors outbound deliveries and goods issues. Key characteristics:

- Every outbound delivery is processed from **exactly one** shipping point.
- The responsible shipping point is **determined automatically at sales order item level** (based on shipping condition, loading group, and delivering plant).
- A single shipping point can process deliveries from **multiple plants**, provided the plants are geographically close.
- **Multiple shipping points** can be assigned to one plant — each with different loading equipment, processing times, or transport modes.
- The Customizing enterprise structure defines the allowed plant–shipping point combinations.

### Loading Point
An organizational sub-unit used to structure operations within a shipping point:

- Defined in Customizing for Logistics Execution.
- **Assigned manually** in the delivery document header (not automatically determined).
- Can optionally be included in delivery output documents.
- **Cardinality**: any number of loading points can be assigned to one shipping point, but each loading point belongs to exactly one shipping point.

## Purpose in the SD Process
The shipping point is the primary driver of delivery scheduling and workload distribution. It determines which warehouse team handles a delivery and which processing times (pick/pack/load durations) apply. Loading points allow further subdivision of work within a shipping point — for example, separating refrigerated goods handling from standard goods handling at the same dock.

## Structure and Variants

| Unit | Level | Assignment | Determination |
|---|---|---|---|
| *Shipping Point* | Independent org unit | Assigned to one or more plants | Automatic at sales order item level |
| *Loading Point* | Sub-unit of shipping point | Belongs to one shipping point | Manual in delivery header |

### Shipping Point as Goods Receipt Point
A shipping point can be configured as a **goods receipt point**, enabling it to process inbound deliveries as well. This allows the same physical location to handle both outbound and inbound flows.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order Item | Shipping point is determined here and copied to the delivery |
| Outbound Delivery Header | Carries the shipping point; cannot be changed once delivery is created |
| Inbound Delivery | Uses the shipping point when configured as a goods receipt point |
| Plant | One plant can have multiple shipping points; one shipping point can serve multiple plants |
| Delivery Scheduling | Processing times (pick, pack, load) are defined per shipping point |

## Cross-References
- Delivery document header data: shipping-delivery-document-structure-001
- Warehouse organizational units: enterprise-structure-warehouse-org-units-ewm-001
