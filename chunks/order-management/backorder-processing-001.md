---
schema_version: 1
id: order-management-backorder-processing-001
title: "Backorder Processing (BOP) and ATP Scenarios in SAP SD"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "104-112"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - backorder processing
  - procesamiento de pedidos atrasados
  - BOP segment
  - BOP variant
  - BOP run
  - replenishment lead time
  - plazo de reaprovisionamiento
  - ATP scenario complete delivery
  - escenarios comprobación disponibilidad
  - qué pasa cuando el ATP no puede confirmar
  - confirmación parcial schedule line
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Backorder Processing (BOP) and ATP Scenarios in SAP SD

## Operational Summary
When the *available-to-promise* (ATP) check cannot confirm a sales order item for the customer's requested delivery date, SAP uses forward scheduling to find the earliest confirmable date. The system behavior depends on the delivery agreement (complete or partial) and the scope of check (whether replenishment lead time is included). Sales orders that cannot be confirmed become *backorders*. *Backorder processing* (BOP) provides a mechanism to reprioritize existing material confirmations across multiple demands, resolving backlog situations through configurable BOP segments, variants, and runs.

## Questions This Chunk Answers
- What happens when ATP cannot confirm the requested delivery date for a complete delivery order?
- How does SAP create schedule lines when partial deliveries are allowed and ATP can only partially confirm?
- What is the replenishment lead time and when does it allow ATP to confirm despite insufficient stock?
- What is a backorder in SAP S/4HANA and when does it arise?
- What are BOP segments, BOP variants, and BOP runs, and how do they interact?
- How does the first-come, first-served principle work, and how can it be overridden?

## When It Applies and Context
This process applies after a sales order item has been created or changed and the availability check runs. The source material uses a consistent initial state for all four scenarios: 100 units in stock, purchase orders for 50 and 60 units, existing sales orders consuming 100, 40, and 50 units.

## Process Flow — Four ATP Scenarios

### Scenario 1: ATP Confirms Completely
A new order arrives for 10 units; the customer does not require complete delivery; the requested delivery date is late enough that sufficient stock is available.

The system calculates the material availability date via backward scheduling. On that date, the ATP quantity is 10 units (the 50-unit purchase order covers the first 100-unit demand, leaving 10 units free). The system confirms the full quantity for the requested delivery date and generates one confirmed *schedule line* for the item.

### Scenario 2: Complete Delivery Required — ATP Fails, Forward Scheduling Finds Next Date
A new order arrives for 20 units; the customer requires complete delivery; the requested delivery date is early.

On the material availability date, the ATP quantity is 0 (the 100-unit stock is fully committed to an earlier demand). The system cannot confirm the requested date and switches to forward scheduling. Because complete delivery is required, the 20 units cannot be split. The system identifies the date when the second purchase order (60 units) arrives, which provides enough free quantity. It calculates a new delivery date using forward scheduling from that new material availability date.

Two *schedule lines* are created for the item: the first has the customer's requested delivery date with zero confirmed quantity; the second has the new (confirmable) delivery date with the full 20 units confirmed.

### Scenario 3: Partial Delivery Allowed — ATP Confirms in Two Batches
Same initial state; same order quantity (20 units) and early requested date; the customer allows partial deliveries.

The system cannot confirm the requested date (ATP quantity is 0). Because partial deliveries are allowed, the system distributes the 20 units across two availability dates: 10 units become available when the first purchase order arrives; the remaining 10 units become available when the second purchase order arrives.

Three *schedule lines* are created: the first has the requested delivery date with zero confirmed quantity; the second and third have two separate confirmed delivery dates with 10 units each.

### Scenario 4: Replenishment Lead Time — Confirms Despite Short-Term Shortage
Same initial state; order for 20 units; complete delivery required; early requested date. In this scenario, the scope of check includes the *replenishment lead time*.

The *replenishment lead time* represents the maximum time the system assumes the material will take to become available (for trading goods: planned delivery time + goods receipt processing time; for finished products: in-house production time). The system treats all demands with a material availability date beyond the replenishment lead time as automatically confirmable.

Because the material availability date for the new order falls after the replenishment lead time has expired, the system confirms the requested delivery date in full. This allows sales to commit to a delivery date even without specific open purchase or production orders, relying on the assumption that the material will be restocked within the replenishment horizon.

## Backorder Processing (BOP)

### Definition
A *backorder* is a sales order item for which the ATP check cannot confirm the requested quantity. Backorders arise when demand exceeds available supply within the relevant timeframe.

By default, the ATP check confirms demands on a first-come, first-served basis. This can create suboptimal situations where a high-priority customer order is unconfirmed while a low-priority order received earlier holds confirmed stock. Backorder processing addresses this by allowing authorized users to reallocate existing material confirmations.

### BOP Segment
A *BOP segment* contains:
- **Criteria**: define which requirements are included in the BOP run (for example, a specific sales organization or customer group)
- **Prioritizer**: a ranking rule that sorts requirements into a defined sequence before the BOP re-confirmation logic runs; this overrides the default first-come, first-served order

The prioritizer is central to BOP because it determines which demands receive confirmed stock when total demand exceeds supply.

### BOP Variant
A *BOP variant* is a collection of settings that defines:
- **Which requirements to process**: by referencing one or more BOP segments
- **How to handle them**: by specifying confirmation strategies that govern how the system reconfirms or deconfirms quantities

Each BOP run is based on exactly one BOP variant.

### BOP Run
A *BOP run* is the mass availability check execution that processes all requirements identified by the BOP variant's segments. It can be:
- Triggered **online** by an authorized user (for example, a fulfillment manager reviewing shortages)
- Scheduled as a **background job** (for example, after an MRP run or before creating the delivery due list)

The BOP run re-evaluates all included requirements in the priority sequence defined by the BOP segment's prioritizer. Requirements that were previously confirmed may be deconfirmed if a higher-priority demand needs the same stock. The result is a set of updated schedule lines reflecting the new confirmation distribution.

## Conditions and Restrictions
- BOP requires upfront configuration of BOP segments and variants before a run can be executed.
- Deconfirming a previously confirmed sales order schedule line affects the customer's expected delivery date; communication to the customer is a business process decision, not automatic.
- The replenishment lead time must be maintained in the material master for Scenario 4 logic to apply.
- Forward scheduling uses the same time components as backward scheduling (pick/pack time, loading time, transportation lead time, transit time from the shipping point and route).

## Common Errors
**Multiple schedule lines created unexpectedly**: partial delivery is allowed at item level; the system distributes the quantity across dates because complete confirmation is not possible on a single date. Verify the partial delivery agreement in the CMiR or business partner master.

**BOP run confirms less than expected**: the prioritizer in the BOP segment ranks the new demand lower than existing demands; confirm the BOP variant configuration and segment prioritizer logic.

## Cross-References
Prior step: order-management-availability-check-atp-001
See also: configuration-delivery-scheduling-001 (forward and backward scheduling mechanics)
See also: order-management-sales-order-source-of-data-001 (data flow into the sales order)
