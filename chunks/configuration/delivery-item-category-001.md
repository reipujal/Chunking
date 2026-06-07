---
schema_version: 1
id: configuration-delivery-item-category-001
title: "Delivery Item Category — Determination and Configuration"
area: configuration
process_tags: [order-to-cash, delivery-processing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "30-32"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivery item category
  - categoría de posición de entrega
  - item category determination delivery
  - determinación categoría posición entrega
  - PACK usage
  - CHSP usage
  - batch split delivery
  - DLN
  - ELN
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Delivery Item Category — Determination and Configuration

## Operational Summary
The *delivery item category* controls how each item in a delivery is handled and processed during shipping or goods receipt. Determination follows two paths depending on whether the delivery references a sales order. For order-referenced deliveries, the item category is copied from the order. For order-independent items and inbound deliveries, the system determines it using the delivery type and item category group from the material master.

## Questions This Chunk Answers
- What does the delivery item category control?
- How does the system determine the delivery item category when a delivery is copied from an order?
- How is the item category determined for items not coming from a sales order?
- What are the internal usages (PACK, CHSP, PSEL, V) and when are they set?

## What This Configuration Controls
The delivery item category provides a high degree of automatic determination and checking. It controls picking relevance, goods movement, billing relevance, and other item-level processing behaviours in the delivery document.

## SPRO Path or Direct T-code
Logistics Execution → Shipping → Deliveries → Define Item Categories for Deliveries

## Key Parameters

### Case 1 — Item Category Copied from Sales Order
When an outbound delivery is created with reference to a sales order, the system copies the item category from the order item to the delivery item. The delivery item category must have **the same key** as the order item category. The order item or its schedule line must be marked as delivery-relevant.

### Case 2 — Independent Item Category Determination
For items that do not originate from a sales order — packing material, deliveries without order reference (type LO), or inbound deliveries (type EL) — the system determines the item category using:

| Factor | Description |
|---|---|
| Delivery type | Header-level control object |
| Item category group | From material master (general or sales-org specific) |
| Internal usage | Set automatically by the system for specific scenarios |

In Customizing, for each valid combination of delivery type + item category group (+ usage), a default item category and optional manual alternatives are defined.

### Item Category Determination Factors in Sales Documents
The order item category (source for Case 1) is determined by four factors:
1. **Sales document type** — controls which item categories are eligible
2. **Item category group** — defined per material/sales org/distribution channel in the material master
3. **Item category usage** — identifies specific scenarios (text item, free-of-charge item, substituted material); assigned by internal programming logic; can also be set in the customer-material information record
4. **Item category of the higher-level item** — applies when the item is a sub-item

### Internal Usages (Set Automatically by the System)

| Usage | Trigger |
|---|---|
| PACK | Generating packing items |
| CHSP | Batch split |
| PSEL | Product selection |
| V | Inbound deliveries for purchase orders; deliveries in stock transport processes |

> Usage determination is hard-coded. It can only be changed via code modification (not Customizing). Exception: a usage can be specified in the customer-material information record — but this applies to the order, not the delivery item category determination.

### Material Master: Two Item Category Group Fields
- **General item category group**: not tied to sales org or distribution channel; used for inbound deliveries
- **Item category group**: tied to sales org and distribution channel; used for outbound deliveries referencing a sales document

## Configuration Impact
- Delivery item categories of type **SD document category 7** (inbound delivery / shipping notification, e.g., ELN) have the movement type maintained **directly in the delivery item category**. For all other categories, the movement type comes from the schedule line category.
- All delivery item categories must be defined as sales item categories in SD, even those never used in sales documents (e.g., DLN, ELN).
- For delivery item categories without SD document category 7, a schedule line category must be determined in SD to supply the movement type.

## Common Configuration Errors
- Delivery item category key does not match the order item category key → item not copied to delivery.
- No item category maintained for a delivery type + item cat group combination → item category not determined for order-independent items.
- Movement type missing for delivery item category of type 7 → goods receipt cannot be posted.

## Cross-References
- Delivery type concept: configuration-delivery-type-001
- Copying control and process Customizing: configuration-delivery-process-customizing-001
