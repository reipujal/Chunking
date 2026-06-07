---
schema_version: 1
id: configuration-schedule-line-category-control-001
title: "Schedule Line Category Control in SAP SD"
area: configuration
process_tags: [order-to-cash, delivery-processing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "61-67"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - schedule line category
  - categoria de reparto
  - lineas de reparto ventas
  - delivery relevance movement type MRP type
  - que controla la categoria de reparto
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Schedule Line Category Control in SAP SD

## Operational Summary
The *schedule line category* controls delivery dates, delivery quantities, requirements transfer, availability behavior, inventory management, movement type, and delivery relevance at schedule line level. Schedule lines are prerequisites for delivering materials. The source explains that item categories allow or prevent schedule lines, schedule line categories are assigned to item categories, and automatic determination uses item category plus MRP type, then item category without MRP type if no more specific assignment exists.

## Questions This Chunk Answers
- What does a schedule line category control in SAP SD?
- When is a schedule line relevant for delivery?
- How does SAP determine the schedule line category automatically?
- Which settings connect schedule lines to inventory management and goods movements?
- Can schedule line categories exist for items that are not delivered?

## What This Configuration Controls
The *schedule line category* determines how an item's delivery dates and quantities behave. It also controls whether requirements are transferred, whether availability checks are active, which movement type posts inventory changes, and whether a delivery block is set automatically at schedule line level. The course notes that schedule line categories are required by item categories: a schedule line category always needs an item category.

## SPRO Path or Direct T-code
The source describes schedule line category Customizing but does not provide a direct transaction code. No transaction is listed in the extraction field.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Relevant for delivery* | Determines whether schedule lines generate delivery items | Active for deliverable sales order items |
| *Requirements transfer* | Controls whether demand is passed to requirements planning | Active or inactive |
| *Availability check* | Can be deactivated at schedule line level | Active or inactive |
| *Movement type* | Controls quantity and value postings in inventory accounting | Course examples include 601 and 651 |
| *Purchase requisition controls* | Supports automatic purchase requisition generation | Purchase order type, item category, account assignment category |
| *Delivery block* | Can be set automatically on the schedule line | Configured block |

## Configuration Impact
Different schedule line categories model different processes. The source describes quotation schedule lines as not relevant for delivery, with inactive requirements transfer and no need for goods movement. Sales order schedule lines from category CP generate delivery items, have delivery relevance active, transfer requirements, and use movement type 601 so goods issue removes stock from unrestricted use. Return orders need a schedule line category that is relevant for delivery but does not require requirements transfer; movement type 651 posts the return goods receipt to blocked returns stock instead of a normal goods issue.

Automatic determination uses two steps. First, the system searches for a schedule line category with the combination of item category and MRP type from the material master. If it finds no match, it searches by item category with no MRP type. This means MRP type can refine the logistics behavior without changing the item category.

## Common Configuration Errors
**Order item cannot be delivered**
-> Check whether schedule lines are allowed for the item category and whether the determined schedule line category is relevant for delivery.

**Requirements are not visible in planning**
-> Requirements transfer may be inactive in the schedule line category or incomplete in requirements-transfer Customizing.

**Wrong inventory posting at goods issue or returns**
-> Review the movement type assigned in the schedule line category.

**Unexpected delivery block appears**
-> A delivery block may be activated directly in the schedule line category.

## Cross-References
- Prior step: configuration-sales-item-category-control-001
- Next step: order-management-sales-document-data-flow-001
- See also: configuration-delivery-type-001
