---
schema_version: 1
id: pricing-special-pricing-functions-001
title: "Special Pricing Functions: Group Conditions, Exclusion, and Condition Supplements"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "54-61"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - group condition SAP pricing
  - condición de grupo precio SAP
  - condition exclusion group SAP
  - grupo de exclusión de condición
  - best price determination SAP
  - mejor precio automático SAP
  - condition supplement SAP pricing
  - suplemento de condición SAP
  - cumulative condition value pricing
  - valor acumulado condición precio
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Special Pricing Functions: Group Conditions, Exclusion, and Condition Supplements

## Operational Summary
Beyond standard item-level pricing, SAP SD provides three advanced pricing functions: *group conditions* that accumulate quantities or values across items to reach scale thresholds; *condition exclusion groups* that compare multiple conditions and apply only the best (or worst) price; and *condition updates* that track cumulative values against maximum limits. *Condition supplements* attach subordinate conditions to a main condition record without their own access sequence.

## Questions This Chunk Answers
- What is a group condition and when does it aggregate across document items?
- What are the group condition formulas (1, 2, 3) and how do they differ?
- How does condition exclusion determine the best price automatically?
- What comparison methods are available in condition exclusion groups?
- What are condition supplements and how are they maintained?
- What is condition update and what limits can it track?

## Definition

### Group Conditions
A *group condition* accumulates item quantities or values across the sales document to determine a scale threshold, rather than evaluating each item independently. Set a condition type as a group condition in Customizing and specify the unit of measure for accumulation.

**Group condition formulas:**

| Formula | Accumulation scope |
|---|---|
| 1 (complete document) | Quantities or values of all items with the same condition type as the current group condition |
| 2 (all condition types) | Quantities or values of all items, regardless of condition type |
| 3 (material pricing group) | Quantities or values of all items sharing the same material pricing group (KONDM field) |

**Group conditions with varying keys:** quantities are accumulated to determine the scale value, but the rate applied to each item is still calculated from its own individual condition record. This allows different prices per item while using the aggregate quantity for scale determination.

### Condition Exclusion
Conditions can be linked to requirements in the pricing procedure. A requirement can evaluate the *condition exclusion indicator* — set in either the condition type or the condition record — and suppress (deactivate) the condition when the indicator is present.

**Exclusion groups and comparison methods.** Condition types are placed in one or two exclusion groups. During pricing, SAP evaluates the group and selects the condition that gives the best or worst price depending on the comparison method:

| Method | Behavior |
|---|---|
| A | Compare all records in group 1; select the best price; deactivate others |
| B | Compare all records of one condition type; select the best; deactivate others — usable with PR00 |
| C | Compare total price of group 1 vs. group 2; select the group with best overall price; deactivate the other group |
| D | If any record in group 1 is found, deactivate all records in group 2 |
| E | Like A, but select the worst (highest charge or lowest discount) price |
| F | Like C, but select the group with the worst overall price |
| L | Like A, but select the worst price |

Custom exclusion indicators can be defined and tested in requirement routines.

### Condition Update
Values can be accumulated in condition records and tested against maximum limits. Configurable limits include:
- Maximum condition value
- Maximum condition base value
- Maximum number of orders

Cumulative values are visible in the condition record and track usage against the configured ceiling.

### Condition Supplements
*Condition supplements* have no access sequence of their own. They are found and maintained alongside the underlying condition record of a main condition type (e.g., PR00). The set of allowed supplements for a condition type is defined in Customizing by assigning a separate pricing procedure (e.g., PR0000) to the condition type. Multiple conditions can be grouped in a condition supplement procedure.

## Configuration Impact
Group conditions require the group condition flag and the accumulation unit of measure to be set in Customizing for the condition type. The correct formula (1, 2, or 3) determines the scope of the accumulation. Exclusion groups must be defined with the comparison method before the condition types are assigned to the groups. Condition update requires specific condition type settings to enable the accumulation fields in the condition record.

## Common Errors
**Scale not triggered even though total quantity across items reaches the threshold**
-> The condition type is not set as a group condition. Without the group flag, each item is priced independently and the scale is evaluated per-item.

**Multiple price agreements exist but the system is not selecting the best one**
-> Exclusion groups with comparison method A, B, or C are needed to force automatic best-price selection. Without an exclusion group, multiple condition records may all activate and stack.

**Condition supplements are not appearing in the document**
-> The main condition type must be assigned a supplement pricing procedure in Customizing. The supplement procedure lists the allowed supplement condition types.

## Relationship with Other SAP SD Objects
- *Group conditions* interact with the *condition type* (group flag + accumulation formula) and the *condition record* (individual rate per item even when quantities are aggregated)
- *Condition exclusion groups* are configured in pricing procedure Customizing alongside the condition types they compare
- *Condition supplements* are attached to a main condition record (e.g., PR00) and maintained in the same condition maintenance transaction
- *Condition update* writes cumulative values to the condition record and can trigger pricing analysis messages when limits are exceeded

## Cross-References
- Prior step: pricing-condition-records-001
- Next step: pricing-special-condition-types-001
- See also: pricing-condition-technique-overview-001
- See also: pricing-free-goods-001
