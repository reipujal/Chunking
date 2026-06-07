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
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Automatic Free Goods Determination in SAP SD

## Operational Summary
Free goods provide discounts as bonus quantities in the sales order. The course distinguishes *inclusive bonus quantities*, where part of the ordered quantity is free and the ordered and free goods are the same material, from *exclusive bonus quantities*, where extra goods are delivered free of charge and excluded from the invoice. SAP determines free goods using condition technique and creates a sub-item for the free goods material.

## Questions This Chunk Answers
- What is the difference between inclusive and exclusive free goods?
- How are free goods represented in a sales order?
- How does SAP determine free goods master records?
- What happens when the main item quantity or pricing date changes?
- How can free goods values be transferred to accounting?

## What This Configuration Controls
Free goods configuration controls when a bonus quantity is granted, whether it is inclusive or exclusive, how the free goods quantity is calculated, which sub-item is created, and how pricing and accounting treat the main item and sub-item. The standard item categories named in the source are TAN and TANN. The item category controls later processing such as delivery and pricing.

## SPRO Path or Direct T-code
The course states that custom free goods calculation rules can be defined with transaction *VOFM* under formulas. It also says free goods master records are maintained through Sales master records, either with a different menu entry or through Prices and Discounts/surcharges.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Free goods procedure* | Determined from sales area, document determination procedure, and customer determination procedure | Procedure with free goods condition types |
| *Condition type* | Controls free goods record access | Customizing-defined condition type |
| *Access sequence* | Search strategy for master records | One or more accesses |
| *Condition table* | Search key for valid master record | Material, customer/material, hierarchy/material, price list/currency/material |
| *Minimum quantity* | Threshold before free goods apply | Quantity from master record |
| *Calculation rule* | Determines free goods quantity | Prorated, related to units, whole units, or custom |
| *Item category usage* | Drives free goods sub-item category assignment | FREE |

## Configuration Impact
In the sales order, the ordered material is entered as a main item and the free goods material is generated as a sub-item. For automatic free goods, SAP reads the relevant condition records using the pricing date. If the main item quantity or pricing date changes, SAP re-reads the free goods master record, deletes the sub-items, and recreates them. Manual changes to the free goods quantity are lost. Re-running pricing does not affect free goods determination.

The course gives three calculation rule examples for a customer ordering 162 units when the offer is 20 free units for a free goods quantity of 100: prorated produces 32 units, related to units produces 20 units, and whole units produces 0 units because 162 is not a complete unit of 100.

Accounting treatment can differ. In the standard scenario, the main item is not influenced by free goods and pricing is deactivated for the sub-item while calculation price is configured as cost. Other scenarios activate pricing and a 100% discount for the sub-item or cumulate the calculation price from lower-level item to main item.

## Common Configuration Errors
**Manual TANN entry does not behave like automatic free goods**
-> Manual free goods does not reference the free goods master record, so controls such as automatic inclusive quantity reduction and some delivery controls are unavailable.

**Free goods quantity changes are lost**
-> SAP deletes and recreates sub-items when the main item quantity or pricing date changes.

**Free goods not found**
-> Check free goods procedure determination, condition type, access sequence, condition table, and master record validity.

## Cross-References
- Prior step: master-data-material-listing-exclusion-001
- See also: special-processes-sales-special-business-transactions-001
- Next step: special-processes-sales-workshop-scenarios-001
