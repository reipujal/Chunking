---
schema_version: 1
id: shipping-outbound-delivery-creation-process-001
title: "Creating Outbound Deliveries — Collective Processing, Delivery Due List, and Picking Location"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "55-60"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivery due list
  - lista de entregas pendientes
  - collective processing delivery
  - procesamiento colectivo de entregas
  - delivery scenario
  - escenario de entrega
  - picking location determination
  - determinación de ubicación de picking
  - MALA rule
  - regla MALA
  - order combination
  - combinación de pedidos
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Creating Outbound Deliveries — Collective Processing, Delivery Due List, and Picking Location

<!-- inferred transaction, pending validation: VL10E (the source names the "Delivery Due List" / "Create Outbound Delivery" by function but does not print the T-code) -->

## Operational Summary
Outbound deliveries can be created manually (one at a time) or via collective processing using the *Delivery Due List*. Collective processing is the standard operational mode — it handles all types of shipping documents, supports order combination, and can run online or in the background. The system also determines the picking storage location automatically when creating the delivery, using a configurable rule defined per delivery type.

## Questions This Chunk Answers
- What are the options for creating outbound deliveries?
- What is the Delivery Due List and how does it work?
- What are delivery scenarios and user roles in delivery processing?
- How does the system determine the picking storage location?
- Can items be added to an existing delivery? What can and cannot be changed?
- How is output (delivery note, packing list) controlled in shipping?

## When It Applies and Context
Outbound delivery creation follows sales order confirmation and is the first step in the physical execution of shipping. The delivery is the basis for picking, packing, loading, goods issue, and ultimately invoicing.

## Process Flow

### Option 1 — Manual Creation
Create a single outbound delivery with or without reference to a specific order. Limitation: cannot deliver purchase orders or other non-sales-order request documents in this mode.

### Option 2 — Collective Processing (Delivery Due List)
The standard operational approach. Creates multiple deliveries for all types of shipping documents in one run. Can execute **online** (user controls creation interactively) or **in the background** (batch, e.g., overnight).

**Delivery Due List** is a worklist of all operations requiring delivery. Selection criteria are organized on tabstrips — the number and type of criteria vary by delivery scenario and user role. After selection, the system displays all documents due for delivery matching the criteria. From the list, deliveries can be created online or in the background.

**Delivery scenarios**: pre-defined in S/4HANA, each modelling a specific business process for delivering goods (e.g., item-by-item delivery of sales orders). A default user role is assigned to each scenario.

**User roles (list profiles)**: control the scope of selection, the display of the Delivery Due List, and the delivery type. Users can configure personal default scenarios via parameters:

| Parameter ID | Value |
|---|---|
| LE_VL10_SZENARIO | VL10 |
| LE_VL10_PROFIL | Key for list profile |
| LE_VL10_USER_VARIANT | Variant name |

**Order combination**: if shipping criteria match (shipping point, route, ship-to party), the system can combine items from multiple orders into one delivery. Orders can also be split into several deliveries if criteria differ.

### Picking Location Determination
When the delivery is created, if no storage location is specified in the order item, the system determines the **picking storage location** using a rule defined in the delivery type.

Standard rules:
- **MALA**: determined from shipping point + delivering plant + material storage condition (from material master). Most common rule.
- **RETA / MARA**: used primarily in trade scenarios.

Custom logic can be implemented via SAP enhancement **V02V0002**. The picking location search is activated per delivery item category.

### Changing Existing Deliveries
After saving, a delivery can still be modified:
- **Add items with order reference**: additional orders can be added (same split criteria apply as during collective processing).
- **Add items without order reference**: item category is determined using standard rules.
- **Cannot change after creation**: ship-to party, shipping point.

### Output in Shipping
Output is a communication tool for exchanging information with partners. It can be sent from individual deliveries, groups of deliveries, or handling units.

Examples:
- Delivery note, packing list → from individual outbound delivery
- Freight list → from a group of outbound deliveries
- Handling unit labels → from handling units

Output is controlled via the **condition technique**: determines how (print, fax, EDI), when (send time), to whom (partner), and to which printer. Header output covers the entire document; item output is generated per delivery item.

## Conditions and Restrictions
- Manual creation cannot deliver purchase orders or transfer orders.
- Ship-to party and shipping point cannot be changed once the delivery is saved.
- Picking location determination is only active if the delivery item category is configured for it.
- Order combination requires identical delivery split criteria (shipping point, route, ship-to party).

## Common Errors
**Items not combined from multiple orders**
→ Verify that order combination is activated in copying control and that split criteria are identical across orders.

**Picking location not determined**
→ Check that the MALA assignment table is maintained for the shipping point + plant + storage condition combination, and that the delivery item category has the picking location search activated.

**Delivery not created in background run**
→ Check log for split conflicts or missing mandatory delivery data (incomplete log).

## Cross-References
- Prior step (delivering plant determination): order-management-sales-order-source-of-data-001
- Next step: shipping-goods-issue-ewm-001
- Delivery due list configuration (delivery scenarios): configuration-delivery-process-customizing-001
- Scheduling (dates for the delivery): configuration-delivery-scheduling-001
- Outbound delivery monitor: shipping-outbound-delivery-monitor-001
- Delivery document structure: shipping-delivery-document-structure-001
