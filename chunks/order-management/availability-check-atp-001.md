---
schema_version: 1
id: order-management-availability-check-atp-001
title: "Availability Check (ATP) in SAP SD — Concept and Configuration"
area: order-management
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "97-103"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - availability check
  - comprobación de disponibilidad
  - ATP check
  - verificación de disponibilidad
  - material availability date
  - fecha de disponibilidad de material
  - transfer of requirements
  - transferencia de necesidades MRP
  - partial delivery agreement
  - acuerdo entrega parcial
  - complete delivery SAP
  - cómo configura SAP la comprobación de disponibilidad
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Availability Check (ATP) in SAP SD — Concept and Configuration

## Operational Summary
The *availability check* determines whether the requested quantity of a material can be confirmed for a customer's requested delivery date at the time of sales order entry. The most important strategy is *available-to-promise* (ATP). The check runs at item level, at plant level, and is controlled by both material master settings and Customizing control tables. The result of the check directly influences the *schedule lines* generated for the sales order item.

## Questions This Chunk Answers
- What is the availability check (ATP) and how does it work in SAP SD?
- What is the *material availability date* and how is it calculated?
- At what organizational level does the availability check run?
- What stock types and movements can be included in the scope of the availability check?
- What is the *transfer of requirements* and what process does it trigger?
- How are complete delivery and partial delivery agreements configured, and what priority rules apply?

## Definition
The *availability check* is the function SAP executes when a sales order item is created or changed to verify that sufficient stock will exist on the *material availability date*. If the check confirms the ordered quantity, a confirmed *schedule line* is generated. If it cannot confirm, the system attempts to find the earliest date when confirmation is possible, using forward scheduling.

*Available-to-promise* (ATP) is the standard strategy: the system calculates the ATP quantity on the material availability date by netting current stock against existing demand (open sales orders, reservations) and planned supply (purchase orders, production orders), filtered by the scope of check defined in Customizing.

## Purpose in the SD Process
Without a reliable availability check, sales orders are confirmed without knowing whether the material can actually be delivered. The ATP check allows the sales organization to:
- Confirm realistic delivery dates to customers
- Detect shortages immediately at order entry
- Feed confirmed requirements to materials planning (MRP) so that procurement or production is initiated proactively

## Control Mechanisms

### Material Master Control
The *Availability check* field on the *Sales: General/Plant Data* tab page of the material master controls whether and how the check is performed for that material. Different materials can have different check configurations — for example, a standard finished product might use a full ATP check while a service material uses no check.

### Customizing Control Tables
In addition to the material master field, Customizing control tables define the *scope of check*: which stock categories and movements are considered. The scope can be configured to include or exclude:
- **Stock types**: unrestricted-use stock, safety stock, stock in quality inspection, stock in transfer
- **Inward movements**: purchase orders, production orders
- **Outward movements**: existing sales orders, material reservations from inventory management

The combination of the material master setting and the Customizing scope of check determines precisely what the ATP quantity calculation takes into account on the material availability date.

## Material Availability Date
The *material availability date* is the date on which sufficient material must be physically available in the warehouse (ready for picking and packing) to meet the customer's confirmed delivery date. It is calculated by *delivery and transportation scheduling*, which works backward from the customer's requested delivery date, subtracting pick/pack time, loading time, transportation lead time, and transit time. The availability check then runs against this calculated date — not against the requested delivery date directly.

## Check at Plant Level
The availability check runs at the level of the *delivering plant* assigned to the sales order item. The plant is determined automatically using the following access sequence:
1. Customer-material info record
2. Ship-to party business partner master record
3. Material master record

If no valid plant can be found, the document becomes incomplete and the availability check cannot run.

## Transfer of Requirements
When a customer orders material and the sales order is created, the corresponding material quantities are automatically transferred to *material requirements planning* (MRP) as individual requirements. MRP uses these requirements to decide how to procure or produce the material — through purchase orders or production orders. Existing open requirements from other sales orders influence the ATP quantity on any given date, which is why the order in which demands are confirmed matters for backorder scenarios.

## Complete and Partial Delivery Agreements
The system checks the delivery agreement for each sales order item when evaluating whether a partial or complete confirmation is possible.

**Complete delivery (header level):** maintained in the business partner master data (Sales area data, *Shipping* tab). When active, all items of all orders for that customer must be fully confirmed before a delivery document can be created.

**Partial delivery agreement (item level):** controls whether a single item can be split across multiple deliveries. The customer-material info record (CMiR) has higher priority than the business partner master record when determining the applicable setting. Available options:
- Multiple partial deliveries allowed
- Only one delivery to be created, even if the ordered quantity cannot be fulfilled
- Only a complete delivery per item is allowed
- No limit on subsequent deliveries

When partial deliveries are allowed, the system can distribute the ordered quantity across multiple confirmed schedule lines with different dates. When only a complete delivery is allowed, the system waits until the full quantity is available on a single date.

## Conditions and Restrictions
- The availability check requires a *delivering plant* on the sales order item; without a plant, no check is possible.
- The check runs at the *material availability date*, not at the requested delivery date.
- The scope of check is plant-specific and controlled in Customizing — not all stock movements are considered by default.
- Manual changes to the confirmed quantity or delivery date in the sales order are possible if Customizing allows it.

## Relationship with Other SAP SD Objects
- *Sales order*: the availability check runs during order creation; its result (confirmed schedule lines) determines whether and when a delivery can be created
- *Delivery and transportation scheduling*: calculates the *material availability date* that the ATP check uses as its reference date
- *Material master*: the *Availability check* field on *Sales: General/Plant Data* controls check behavior per material
- *Business partner master*: the *Shipping* tab in sales area data stores the complete delivery agreement
- *Customer-material info record*: higher-priority source for partial delivery agreement at item level, overriding the business partner master
- *Transfer of requirements → MRP*: confirmed order quantities flow to MRP, which plans procurement or production to cover demand
- *Backorder processing*: resolves situations where ATP cannot confirm; directly continues from the results of this check

## Cross-References
Prior step: order-management-sales-order-source-of-data-001
Next step: order-management-backorder-processing-001
See also: configuration-delivery-scheduling-001 (scheduling that calculates the material availability date)
See also: master-data-material-master-sd-001 (Availability check field in material master)
See also: master-data-material-master-sd-001 (CMiR priority for partial delivery agreement and plant determination)
