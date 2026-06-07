---
schema_version: 1
id: configuration-delivery-field-determination-001
title: "Automatic Field Determination for Outbound Deliveries — Plant, Shipping Conditions, Shipping Point, Route"
area: configuration
process_tags: [order-to-cash, delivery-processing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "43-47"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivering plant determination
  - determinación centro suministrador
  - shipping point determination
  - determinación punto de expedición
  - route determination
  - determinación ruta
  - shipping conditions
  - condiciones de expedición
  - loading group
  - grupo de carga
  - transportation group
  - grupo de transportes
  - departure zone
  - zona de salida
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Automatic Field Determination for Outbound Deliveries — Plant, Shipping Conditions, Shipping Point, Route

## Operational Summary
SAP S/4HANA automatically determines four critical fields for each sales order item during order entry: the delivering plant, the shipping conditions, the shipping point, and the route. These determinations cascade — each depends on the previous one. All four are determined at item level in the sales order and copied to the outbound delivery. Errors in master data setup for any of these fields will prevent correct delivery creation.

## Questions This Chunk Answers
- How does SAP determine the delivering plant for a sales order item?
- What are shipping conditions and how are they determined?
- How does the system determine the shipping point?
- What factors control route determination?
- What changed with shipping conditions in SAP S/4HANA 1909?

## What This Configuration Controls
These four automatic determinations govern which warehouse handles the shipment, how the delivery is scheduled, and which route and carrier are used. Incorrect setup leads to missing deliveries, wrong shipping points, or incorrect scheduling.

## SPRO Path or Direct T-code
- Delivering plant: customer-material info record, customer master, material master
- Shipping conditions: sales document type Customizing, customer master (sold-to or ship-to)
- Shipping point determination: LE → Shipping → Basic Shipping Functions → Shipping Point and GI Point Determination
- Route determination: LE → Shipping → Basic Shipping Functions → Routes → Route Determination

## Key Parameters

### 1 — Delivering Plant Determination
Determined per order item. Priority sequence (hard-coded):

| Priority | Source |
|---|---|
| 1 | Customer-material information record (if a delivering plant is maintained) |
| 2 | Ship-to party customer master record |
| 3 | Material master record |

> To change this logic, use user exit `USEREXIT_SOURCE_DETERMINATION`.

### 2 — Shipping Conditions
Describes the shipping requirements for how goods are delivered (e.g., express vs. standard, road vs. export container). Stored at **sales order header level**. Acts as a key input into shipping point and route determination.

Determination priority:
1. Sales document type (if a shipping condition is assigned)
2. Business partner (customer master)

**S/4HANA 1909 change**: the field *Shipping Conditions from Ship-to-party Master Record* in sales document type Customizing controls which partner supplies the shipping condition:

| Value | Behaviour |
|---|---|
| Blank | Shipping conditions from sold-to party (legacy behaviour) |
| A | Shipping conditions from ship-to party |
| B | Shipping conditions from ship-to party; falls back to sold-to if ship-to has none |

### 3 — Shipping Point Determination
Determined per order item. Automatic proposal; can be changed manually within limits. **Cannot be changed in the outbound delivery**.

Determination key:
- **Delivering plant** (from step 1)
- **Shipping conditions** (from step 2)
- **Loading group** (from material master)

Items with different shipping points cannot be combined in the same outbound delivery.

### 4 — Route Determination
Determined per order item. Can be manually overwritten in the order item. Can optionally be re-determined in the outbound delivery based on weight (weight group), if the delivery type is configured for it.

Determination key:
- Country and **departure zone** of the shipping point (from Customizing)
- **Shipping condition** (from sales document type or customer master)
- **Transportation group** (from material master)
- Country and **transportation zone** of the ship-to party (from customer master)

## Configuration Impact
These four determinations feed directly into delivery scheduling (pick/pack/load times come from shipping point; transit and transport lead times come from route) and into the delivery creation process. Any gap in master data — missing loading group, missing transportation zone on the ship-to party — prevents automatic determination and may block delivery creation.

## Common Configuration Errors
- No delivering plant in customer-material info or customer master → system falls back to material master; if also missing there, delivery creation fails.
- Shipping condition not defined on customer master or order type → route and shipping point cannot be determined.
- Shipping point assignment missing for plant + shipping condition + loading group combination → "Shipping point could not be determined" error in sales order.
- Transportation zone missing on ship-to customer master → route determination fails.

## Cross-References
- Shipping point and loading point concept: enterprise-structure-shipping-point-loading-point-001
- Delivery scheduling (uses these determinations): configuration-delivery-scheduling-001
- Delivery type configuration: configuration-delivery-type-001
