---
schema_version: 1
id: pricing-special-condition-types-001
title: "Special Condition Types in SAP SD Pricing"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "63-75"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - HM00 manual order value SAP
  - PN00 net price SAP
  - AMIW minimum order value SAP
  - PMIN minimum price material SAP
  - PR02 interval price scale SAP
  - customer hierarchy pricing SAP
  - jerarquía de cliente precio SAP
  - pallet discount KP00 SAP
  - descuento palet SAP
  - DIFF rounding condition SAP
  - tipos de condición especiales precio SAP
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Special Condition Types in SAP SD Pricing

## Operational Summary
SAP SD delivers a set of special-purpose condition types that handle pricing scenarios not covered by standard price/discount/surcharge conditions: manual order values (HM00), net price override (PN00), minimum order and material prices (AMIW, AMIZ, PMIN), interval scales (PR02), customer hierarchy discounts (HI01), pallet-based discounts and surcharges (KP00–KP03), and currency rounding (DIFF). Each condition type has a specific role in the pricing procedure and cannot be substituted by a generic condition.

## Questions This Chunk Answers
- How does HM00 allow entering a total order value manually?
- What is PN00 and how does it differ from a standard price override?
- How do AMIW and AMIZ enforce a minimum order value?
- How does PMIN protect a minimum price per material?
- What is interval scale pricing (PR02) and its limitation?
- How does customer hierarchy pricing work in SAP SD?
- What are pallet discounts (KP00, KP01, KP02, KP03) and which formulas control them?
- What does the DIFF condition type do?

## Definition

### HM00 — Manual Order Value
*HM00* is a header condition that allows the total order value to be entered manually. The system distributes the new order value proportionally among items based on each item's previous net value. Taxes are recalculated for each item after the distribution.

### PN00 — Net Price
*PN00* allows specifying the net price for an individual item manually. When PN00 is entered, the system deactivates all original conditions for that item. This differs from a standard manual price change, which works within existing condition limits.

### AMIW and AMIZ — Minimum Order Value
*AMIW* defines a minimum value for the entire order. If the net order value at header level is below this minimum during pricing, SAP substitutes the minimum value as the net order value automatically. AMIW is a *statistical* condition and a *group condition*, distributed among all items by value. *AMIZ* uses formula 13 in the pricing procedure to calculate the minimum value surcharge: minimum order value minus the net sales order value.

### PMIN — Minimum Price per Material
*PMIN* enforces a minimum price for a specific material. If the minimum price is not met during pricing, the system calculates the shortfall and posts it as a PMIN condition.

### PR02 — Interval Price
*PR02* supports condition records with interval scales (scale type D in Customizing). Interval scales define different rates for specific quantity or value ranges (not cumulative scales). **Restriction:** interval scales cannot be used for group conditions.

### Customer Hierarchy Pricing
Customer hierarchies model multi-level buying groups, cooperatives, or retail chains. The hierarchy consists of nodes; customers are assigned to the lowest relevant node. Steps to set up:
1. Create master records for each node.
2. Assign nodes to each other (define the hierarchy).
3. Assign customer master records to the relevant nodes.

Price or rebate agreements assigned to a high-level node apply automatically to all subordinate customers. SAP follows the access sequence through the hierarchy path during pricing and applies condition records at each relevant node level. Nodes can be moved; the system reassigns all related customers automatically. Customer hierarchies are valid for a specific period.

**HI01 (Hierarchy Discount):** a standard condition type for hierarchy-based discounts. The access sequence is configured so the discount is initiated at the lowest applicable hierarchy level. This means the most specific node in the path — the one closest to the customer — that has a condition record is applied first.

### Pallet Discounts and Surcharges

| Condition type | Purpose | Formula | Behavior |
|---|---|---|---|
| KP00 | Pallet discount | 22 | Discount for whole pallets only; ignores incomplete pallets |
| KP01 | Incomplete pallet surcharge | 24 | Surcharge on the fractional portion of a pallet |
| KP02 | Mixed pallet discount | Group condition, UoM = PAL | Accumulates quantities across items; discount for complete pallets only |
| KP03 | Surcharge for incomplete mixed pallets | Formula 23, group condition, UoM = PAL | Surcharge on the fractional total across all items |

All pallet conditions use formulas in the pricing procedure that test for complete vs. fractional pallet quantities. KP02 and KP03 are group conditions that accumulate across document items.

### DIFF — Rounding Condition
Rounding rules are maintained in table T001R per company code and currency. If the final order header amount differs from the rounding unit, SAP rounds it up or down as specified. *DIFF* calculates the difference amount. DIFF is a group condition distributed among all items by value.

## Classification Summary

Which of the above condition types are group conditions distributed among all items by value?
- **Yes:** AMIW (minimum order value) and HM00 (manual order value)
- **No:** PN00, PMIN — these are item-level conditions

Price or rebate agreements in customer hierarchies are assigned to a **high-level node**, not a low-level one — agreements at a high node apply automatically to all subordinate customers. Within the hierarchy, SAP initiates the discount at the **lowest applicable level** of the hierarchy path, meaning the most specific node that has a condition record is used first.

The behavior of pallet discounts (KP00 controlled by formula 22, KP01 by formula 24) is fully defined by a basic formula in the pricing procedure — no additional Customizing outside of the condition type and formula assignment is needed for the core calculation logic.

Interval scales (PR02, scale type D) define non-cumulative, band-based pricing. The restriction — no use with group conditions — means interval pricing must always be evaluated per-item independently.

## Relationship with Other SAP SD Objects
- *HM00* and *AMIW* are header conditions — they affect the entire order, not individual items
- *Customer hierarchy* nodes are separate master data objects; the hierarchy is assigned to a sales area and has its own validity period
- *KP00–KP03* require the material to have a unit-of-measure conversion to PAL (pallet) configured in the material master
- *DIFF* reads rounding rules from table T001R, which is maintained in Financial Accounting basic settings per company code and currency
- All special condition types are included in a pricing procedure alongside standard condition types; their placement (step, counter, requirements) in the procedure controls when they are evaluated

## Cross-References
- Prior step: pricing-special-pricing-functions-001
- Next step: pricing-statistical-condition-types-001
- See also: pricing-condition-technique-overview-001
