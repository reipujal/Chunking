---
schema_version: 1
id: shipping-ewm-picking-process-001
title: "EWM Picking Process for Outbound Deliveries in SAP S/4HANA"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "71-74"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - EWM picking
  - picking EWM
  - warehouse task
  - tarea de almacén
  - outbound delivery order EWM
  - orden de entrega de salida EWM
  - warehouse management monitor
  - monitor de gestión de almacén
  - storage type sequence
  - secuencia de tipos de almacenamiento
  - stock removal rule
  - regla de retirada de stock
  - FIFO
  - wave processing
  - procesamiento de oleadas
  - production material request
  - solicitud de material de producción
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# EWM Picking Process for Outbound Deliveries in SAP S/4HANA

## Operational Summary
When an EWM-managed warehouse is involved, the LE outbound delivery is replicated to SAP EWM as an *outbound delivery order*, which drives the creation of *warehouse tasks* for picking. The physical picking is controlled by a storage type sequence and a stock removal rule (e.g., FIFO). The *Warehouse Management Monitor* provides a central control point for warehouse managers to track operations and execute corrective actions.

## Questions This Chunk Answers
- How does the EWM picking process connect to the LE outbound delivery?
- What documents are created in EWM for a sales order?
- How does the system find the correct stock (quant) for picking?
- What is the Warehouse Management Monitor and what can it do?
- How is picking handled for manufacturing orders vs. sales orders?

## When It Applies and Context
This process applies when the picking storage location is assigned to an EWM warehouse number. As of S/4HANA 1610, EWM is embedded in the core system and is the strategic path for warehouse management. Legacy WM (transfer orders) remains available but will not receive future development.

## Process Flow

### 1 — Source Documents
Picking and GI are triggered by different source documents depending on the business scenario:

| Scenario | Source Document |
|---|---|
| Customer order (SD) | Sales order → LE outbound delivery |
| Production supply | LE outbound delivery OR production material request (created directly in EWM) |
| Internal issue (cost center / internal order) | LE outbound delivery (can be created in IM or directly in EWM) |

Creating a production material request directly in EWM avoids creating an LE outbound delivery, reducing document volume in high-frequency production processes.

### 2 — Replication to EWM
For sales order items processed in an EWM warehouse, the LE outbound delivery is replicated to SAP EWM as an **outbound delivery order**. This EWM document triggers the creation of warehouse tasks for picking.

### 3 — Warehouse Number Determination
The EWM warehouse is activated when:
- The picking storage location is determined (via MALA or other rule)
- The combination of **plant + storage location** is assigned to an **EWM warehouse number**

### 4 — Warehouse Task Creation
Warehouse tasks control the physical movement of goods. For picking, the system determines which quants to pick using two elements:

**Storage type sequence**: ordered list of storage types in which the system searches for stock. The system checks the first storage type; if no stock is found, it moves to the next. For picking, the sequence can include a *storage type group* to evaluate quants from multiple storage types simultaneously.

**Stock removal rule (picking strategy)**: applied within the storage type(s) to select the specific quant. Examples:
- **FIFO** (first-in, first-out): selects the oldest quant from storage types in sequence
- **Stringent FIFO**: uses a storage type group to enforce FIFO across multiple storage types simultaneously

> A *quant* is a record of stock of a specific material in a specific storage bin. It is created during EWM putaway and deleted when the material is fully removed during picking.

### 5 — EWM Outbound Delivery (End of Process)
At the end of the EWM process, an additional EWM outbound delivery document is created. This document is required to handle potential delivery splits in case of partial deliveries (e.g., insufficient stock).

### Warehouse Management Monitor
The Warehouse Management Monitor is a central tool for warehouse managers providing:
- **Real-time visibility** into current warehouse status
- **Alert monitoring** for actual and potential problems, with exception-handling tools
- **Direct execution of functions**: create/confirm warehouse tasks and warehouse orders, change or block storage bins, trigger wave processing
- **Highly customizable**: standard nodes can be hidden; *variant nodes* can be created (standard nodes with specific selection criteria or layouts)
- **Display modes**: list view (ALV grid with sort/filter/print) and form view (HTML, detailed object information)

## Conditions and Restrictions
- EWM picking only applies when the picking storage location is linked to an EWM warehouse number.
- The LE outbound delivery must exist before EWM replication occurs (except for EWM-direct inbound delivery scenarios).
- Wave processing and other advanced EWM functions require additional Customizing.

## Common Errors
**Warehouse task not created**
→ Verify that the plant + storage location combination is assigned to the EWM warehouse number. Verify that the storage type sequence is configured for the picking area.

**Wrong quant selected**
→ Check stock removal rule (FIFO configuration) and whether the storage type group is correctly defined.

## Cross-References
- Warehouse organizational units (warehouse number, storage types, bins): enterprise-structure-warehouse-org-units-ewm-001
- Goods Issue posting in EWM: shipping-goods-issue-ewm-001
- Picking storage location determination: shipping-outbound-delivery-creation-process-001
- Outbound Delivery Monitor: shipping-outbound-delivery-monitor-001
