---
schema_version: 1
id: enterprise-structure-warehouse-org-units-ewm-001
title: "Warehouse Organizational Units in SAP S/4HANA — IM and EWM"
area: enterprise-structure
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "14-18"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - warehouse number
  - número de almacén
  - storage type
  - tipo de almacenamiento
  - storage section
  - sección de almacenamiento
  - storage bin
  - ubicación
  - activity area
  - área de actividad
  - quant
  - plant
  - centro
  - storage location
  - almacén
  - company code
  - sociedad
  - EWM organizational units
  - unidades organizativas EWM
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Warehouse Organizational Units in SAP S/4HANA — IM and EWM

## Operational Summary
SAP S/4HANA uses two overlapping organizational hierarchies for warehouse management: the Inventory Management (IM) hierarchy (client → company code → plant → storage location) and the EWM hierarchy (warehouse number → storage type → storage section → storage bin). The two are linked by assigning a plant and storage location to a warehouse number. Understanding both hierarchies is required to configure and operate delivery processing correctly.

## Questions This Chunk Answers
- What organizational hierarchy does SAP use for inventory management?
- What is a plant and what is a storage location?
- What is a warehouse number in EWM?
- How are storage types, storage sections, and storage bins related?
- What is an activity area and what is a quant?
- How does the EWM warehouse connect to the IM plant and storage location?

## Definition

### Inventory Management Hierarchy
Used to model the legal and physical structure of a corporate group:

| Level | Object | Description |
|---|---|---|
| 1 | Client | Represents the entire corporate group |
| 2 | Company Code | Legally independent accounting unit within the client |
| 3 | Plant | Physical location where inventory is stored (factory, DC). Central object in IM. Assigned to exactly one company code. |
| 4 | Storage Location | Sub-division of a plant. Enables differentiation of stock of the same material within a plant. Stock is managed at this level. |

A plant can have multiple storage locations. A plant belongs to exactly one company code.

### EWM Hierarchy
Used to model the internal physical structure of a warehouse:

| Level | Object | Description |
|---|---|---|
| 1 | Warehouse Number | Highest EWM level. Corresponds to a physical building or distribution center. Linked to a Supply Chain Unit (SCU). |
| 2 | Storage Type | Physical or logical subdivision of the warehouse complex. Defined by a 4-character code and a *storage type role*. Characterized by warehouse technology, space requirements, and organizational form/function. |
| 3 | Storage Section | Organizational subdivision of a storage type. Groups bins with similar attributes (e.g., heavy parts, hazardous materials, fast-moving items). Used during putaway bin determination. |
| 4 | Storage Bin | Smallest addressable unit in the warehouse. Represents the exact physical position where goods are stored. Storage bins are master data. |

## Purpose in the SD Process
The IM hierarchy determines which plant and storage location a delivery draws stock from. The EWM hierarchy controls where within the physical warehouse that stock is located and how picking and putaway tasks are routed.

## Structure and Variants

### Activity Areas
Storage bins — regardless of their storage type — are logically grouped into **activity areas**. One activity area is defined per warehouse activity:
- **Picking**: bins relevant for goods issue
- **Putaway**: bins relevant for goods receipt
- **Physical inventory**: bins to be counted

The same storage bin can belong to multiple activity areas. Activity areas determine the bin sorting sequence when warehouse orders are created.

### Quant
A **quant** represents the stock content of a single storage bin — the quantity of a specific product stored at a specific location. Quants are the lowest unit of stock management in EWM.

### Warehouse Number Configuration
Attributes defined at warehouse number level include:
- Weight, volume, and time units of measure
- Palletization data and packaging specification determination procedures

Recommendation: use one warehouse number per group of storage areas or buildings in the same geographical area. Physically separated warehouse complexes should have separate warehouse numbers.

## Connection Between IM and EWM

To activate EWM warehouse management for a given stock, a **plant + storage location** combination is assigned to a **warehouse number**. Multiple storage locations within the same plant can point to the same warehouse number, forming one warehouse complex from the IM perspective.

```
Plant ──┬── Storage Location A ──┐
        └── Storage Location B ──┴──► Warehouse Number ──► EWM hierarchy
```

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Outbound Delivery | Draws stock from plant + storage location; EWM generates warehouse order for picking |
| Shipping Point | Assigned to a plant; indirectly linked to the warehouse through the plant |
| *Transfer Order* / *Warehouse Order* | Created within the EWM hierarchy to execute picking and putaway |
| *Goods Issue* | Posted at plant/storage location level after EWM warehouse order is confirmed |

## Cross-References
- Shipping Point and Loading Point: enterprise-structure-shipping-point-loading-point-001
- Delivery document concept: shipping-delivery-document-concept-001
