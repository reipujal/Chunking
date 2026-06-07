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
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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
  - CP schedule line category movement type 601
  - tipo de movimiento categoria reparto
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Schedule Line Category Control in SAP SD

## Operational Summary
The *schedule line category* controls delivery dates, delivery quantities, requirements transfer, availability check, inventory management, movement type, and delivery relevance at schedule line level. Schedule lines are prerequisites for delivering materials. Item categories allow or prevent schedule lines, and schedule line categories are then assigned to item categories. Automatic determination uses item category plus MRP type; if no match is found, item category alone is used. A schedule line category can exist even for items that are not physically delivered, such as service items.

## Questions This Chunk Answers
- What does a schedule line category control in SAP SD?
- When is a schedule line relevant for delivery?
- How does SAP determine the schedule line category automatically?
- Which settings connect schedule lines to inventory management and goods movements?
- Can schedule line categories exist for items that are not delivered?
- What do the two characters in the schedule line category key mean?

## What This Configuration Controls
The schedule line category is defined with a two-character key with a specific naming convention:

**First character — sales process:**
| Code | Process |
|---|---|
| A | Inquiry |
| B | Quotation |
| C | Order |
| D | Returns |

**Second character — logistics behavior:**
| Code | Meaning |
|---|---|
| D | No inventory management |
| N | No MRP |
| V | Consumption-based planning |
| X | No inventory management with goods issue |
| P | Material requirements planning |

These standard keys can be kept or replaced with custom abbreviations that reference your specific sales document types.

## SPRO Path or Direct T-code
The source describes schedule line category Customizing but does not provide a direct transaction code.

## Key Parameters

| Field or setting | Description | Typical Values |
|---|---|---|
| *Relevant for delivery* | Determines whether schedule lines generate delivery items | Active for deliverable items |
| *Requirements transfer* | Controls whether demand is passed to requirements planning | Active or inactive |
| *Availability check* | Can be deactivated at schedule line level | Active or inactive |
| *Movement type* | Controls quantity and value postings in inventory accounting | 601 (standard GI), 651 (returns to blocked stock), 601-699 range for sales |
| *Purchase requisition controls* | Supports automatic PR generation from sales document | PO type, item category, account assignment category |
| *Delivery block* | Set automatically on schedule line when configured | Configured block type |

## Configuration Impact

**Standard examples from the source:**

*Quotation schedule lines* are not relevant for delivery. Requirements transfer is inactive; no movement type is needed since no physical goods movement is required.

*Sales order schedule lines — category CP* generate delivery items. The relevant-for-delivery indicator is active. Requirements transfer is active. Movement type **601** posts goods issue from unrestricted-use stock when the delivery is confirmed.

*Return order schedule lines* must be relevant for delivery (a returns delivery follows). Requirements transfer is not necessary. Movement type **651** posts the returned goods receipt to blocked returns stock instead of the normal unrestricted stock.

**Delivery block.** If a delivery block is configured in the schedule line category, the block is automatically set at schedule line level in the sales document whenever that category is determined.

**Automatic purchase requisition.** A purchase requisition can be generated automatically from the sales document (for third-party or individual purchase order scenarios). To enable this, configure the purchase order type, item category, and account assignment categories in the purchase order Customizing.

**Movement type range.** Many movement types relevant to sales are in the range 601-699. Inventory management is responsible for maintaining movement types; SAP delivers them pre-configured for all standard processes.

**Two-step determination.** The system determines the schedule line category automatically:
1. First: combination of item category + MRP type from the material master
2. If no match: item category + no MRP type

MRP type allows differentiation of logistics behavior for the same item category, depending on how the material is planned.

**Schedule line category is always tied to an item category.** A schedule line category always needs an item category. However, a schedule line category can exist for items that are not physically delivered — for example, service items where no inventory movement occurs.

## Common Configuration Errors
**Order item cannot be delivered**
-> Check whether the item category allows schedule lines and whether the determined schedule line category has the relevant-for-delivery indicator active.

**Requirements are not visible in planning**
-> Requirements transfer may be inactive in the schedule line category, or requirements-transfer Customizing (requirements class assignment) may be incomplete.

**Wrong inventory posting at goods issue or returns**
-> Review the movement type assigned in the schedule line category (601 for standard GI, 651 for returns to blocked stock).

**Unexpected delivery block on schedule line**
-> A delivery block may be configured directly in the schedule line category and set automatically.

**No automatic purchase requisition generated**
-> Verify purchase order type, item category, and account assignment category are configured in the purchase order settings for the schedule line category.

## Cross-References
- Prior step: configuration-sales-item-category-control-001
- Next step: order-management-sales-document-data-flow-001
- See also: configuration-delivery-type-001
