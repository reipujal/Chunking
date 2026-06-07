---
schema_version: 1
id: pricing-free-goods-001
title: "Automatic Free Goods Determination in SAP SD"
area: pricing
process_tags: [order-to-cash, pricing, free-of-charge]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "143-152"
    source_type: A
    role: primary
transactions: [VOFM]
tables: []
aliases:
  - free goods
  - mercancias gratuitas
  - bonificacion de mercancias gratuitas
  - bonus quantity
  - inclusive exclusive free goods
  - como configurar determinacion automatica de free goods
  - TAN TANN item category free goods
  - regla calculo mercancias gratuitas prorrateado
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Automatic Free Goods Determination in SAP SD

## Operational Summary
Free goods provide discounts in the form of bonus quantities in the sales order. SAP distinguishes *inclusive bonus quantities* (part of the ordered quantity is free; material is the same as ordered; quantity units must match) from *exclusive bonus quantities* (extra goods delivered free of charge, excluded from invoice; can be the same material or a different article). SAP determines free goods using condition technique and creates a sub-item for the free goods material automatically. Re-running pricing does not affect free goods determination.

## Questions This Chunk Answers
- What is the difference between inclusive and exclusive free goods?
- How are free goods represented in a sales order?
- How does SAP determine free goods master records?
- What happens when the main item quantity or pricing date changes?
- How can free goods values be transferred to accounting?
- How are calculation rules applied to determine the free goods quantity?
- Can free goods determination be analyzed step by step?

## What This Configuration Controls
Free goods configuration controls when a bonus quantity is granted, whether it is inclusive or exclusive, how the free goods quantity is calculated, which sub-item is created, and how pricing and accounting treat the main item and sub-item. The standard item categories are TAN (main item) and TANN (free goods sub-item). Manual entry of a TANN sub-item is possible but does not use the free goods master record; automatic controls such as inclusive quantity reduction and some delivery controls are then unavailable.

## SPRO Path or Direct T-code
Free goods master records are maintained through the Sales master data menu, either via a separate menu entry or through Prices and Discounts/surcharges. Custom free goods calculation rules can be defined with transaction *VOFM* under the formulas menu entry.

## Key Parameters

| Field or setting | Description | Typical Values |
|---|---|---|
| *Free goods procedure* | Determined from sales area + document determination procedure + customer determination procedure | Procedure with free goods condition types |
| *Condition type* | Controls free goods record access | Customizing-defined condition type |
| *Access sequence* | Search strategy for master records | One or more accesses |
| *Condition table* | Search key for valid master record | Material, customer/material, hierarchy/material, price list/currency/material |
| *Minimum quantity* | Threshold quantity before free goods apply | Quantity from master record |
| *Calculation rule* | Determines free goods quantity from document and additional quantities | Prorated (rule 1), related to units (rule 2), whole units (rule 3), custom |
| *Item category usage* | Drives free goods sub-item category assignment | FREE |
| *Scales* | Can be defined in the master record | Threshold quantities |
| *Validity period* | Limits when the master record applies | Date range |

## Configuration Impact

**In the sales order**, the ordered material appears as a main item and the free goods material is generated automatically as a sub-item. The sub-item's item category controls later processing (delivery, pricing). For automatic free goods, SAP accesses condition records using the *pricing date*. If the main item quantity or pricing date changes, SAP re-reads the master record, deletes the existing sub-items, and recreates them — manual changes to the free goods quantity are lost.

**Calculation rules** (standard system provides three):
- Rule 1 — Prorated: free goods quantity = document quantity × (additional quantity ÷ free goods quantity), rounded down. Example: 162 units ordered, 20 free per 100 → 32 units free.
- Rule 2 — Related to units: free goods quantity = full units of the free goods quantity × (additional quantity ÷ free goods quantity). Example: 162 units → 20 units free (one full unit of 100).
- Rule 3 — Whole units: free goods only if document quantity is an exact multiple of the free goods quantity. Example: 162 units → 0 free (162 is not a multiple of 100).

Custom calculation rules can be defined using ABAP code via transaction VOFM under formulas.

Free goods master records can be maintained at different levels: material, customer/material, price list category/currency/material, or customer hierarchy/material. At a given level, multiple records with the same key can exist for inclusive and exclusive bonus quantities simultaneously — a single button switches between them. For exclusive bonus quantities, an extra entry line appears to specify a different free goods material.

**Analysis:** The free goods determination analysis can be activated in the sales document before items are entered. The analysis then displays detailed step-by-step information about how the free goods were determined.

**Accounting transfer.** Revenue, sales deductions, and costs of free goods can be transferred to accounting in different ways:
- *Scenario 1 (standard):* Main item unaffected; sub-item pricing deactivated; calculation price (VPRS) configured as cost.
- *Scenario 2:* Main item unaffected; sub-item has pricing active with item category TANN characteristic B, condition R100 (100% discount) activated by condition 55 at level 819; discount transfers as sales deduction, VPRS transfers as cost.
- *Scenario 3:* Calculation price cumulated from sub-item to main item in copying control (delivery → billing); main item transfers cumulated cost; sub-item pricing deactivated.

## Common Configuration Errors
**Manual TANN entry does not behave like automatic free goods**
-> Manual entry does not reference the master record; automatic inclusive quantity reduction and delivery controls are unavailable.

**Free goods quantity changes are lost**
-> SAP deletes and recreates sub-items whenever main item quantity or pricing date changes; manual quantity changes are overwritten.

**Free goods not found**
-> Check free goods procedure determination, condition type, access sequence, condition table, and master record validity period and minimum quantity.

**Analysis shows no detail**
-> Analysis must be activated in the sales document before entering items; it cannot be run retroactively after determination.

## Cross-References
- Prior step: master-data-material-listing-exclusion-001
- See also: special-processes-sales-special-business-transactions-001
- Next step: integration-sales-document-technical-tables-001
