---
schema_version: 1
id: configuration-sales-item-category-control-001
title: "Sales Item Category Control in SAP SD"
area: configuration
process_tags: [order-to-cash, delivery-processing, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "54-60"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - item category
  - categoria de posicion
  - determinacion categoria de posicion
  - sales item category group usage
  - que controla la categoria de posicion
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sales Item Category Control in SAP SD

## Operational Summary
The *item category* controls how each sales document item behaves during the current document and follow-on processing. It determines whether business data can differ from the header, whether pricing applies, whether and how the item is billed, whether the item refers to a material or is only text, which incompleteness procedure checks the item, and how sub-items such as free goods or BOM components are handled. Item category determination depends on sales document type, item category group, usage, and higher-level item category.

## Questions This Chunk Answers
- What does the item category control in a sales document?
- How is the item category proposed automatically?
- When can item-level business data differ from header data?
- How are sub-items, free goods, and BOM components represented in sales orders?
- Why should new item categories usually be copied from tested standard categories?

## What This Configuration Controls
An *item category* controls the behavior of an item in the sales document and subsequent processing. The source lists its essential characteristics: separate item business data, pricing relevance, billing behavior, material versus text item behavior, and incompleteness procedure. It also mentions delivery relevance for items without schedule lines, such as copying a text item from the order into the delivery.

## SPRO Path or Direct T-code
The course describes Customizing for item categories but does not provide a direct transaction code. No transaction is listed in the frontmatter because the source does not literally name one.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Business data allowed at item level* | Controls whether item terms can differ from header business data | Same as header or separately maintainable |
| *Pricing relevance* | Determines whether pricing is carried out for the item | Pricing active or inactive |
| *Billing relevance* | Determines whether and how the item is billed | Order-related, delivery-related, not relevant, depending on setup |
| *Material relevance* | Determines whether the item refers to a material or is a text item | Material item or text item |
| *Incompletion procedure* | Controls which item fields are checked | Assigned procedure |
| *Delivery relevance for items without schedule lines* | Lets non-schedule-line items be copied into delivery | Example: text item |
| *Higher-level item support* | Enables sub-items below a main item | Free goods, BOM, service structures |

## Configuration Impact
Item categories are assigned to sales document types to propose a category when an order is created and to define alternatives the user may choose. The determination is influenced by the item category group from the material master, item usage, and the item category of the higher-level item for sub-items. The course gives examples of usage values set internally by the program, such as `TEXT` when a description is entered without a material number and `FREE` for free goods control.

For *bill of material* scenarios, item categories decide whether the BOM is exploded, which main and sub-items are generated, and which items are relevant for pricing and requirements transfer. The main material is entered in the order, and the system can generate sub-items for BOM components if the item category settings allow it.

## Common Configuration Errors
**Wrong item category proposed**
-> Check sales document type assignment, material item category group, item usage, and higher-level item category.

**Text or free goods item behaves like a normal priced item**
-> Review item category pricing relevance and usage-based determination.

**BOM does not explode in the sales order**
-> Confirm the BOM is sales-relevant and that the main item category is configured to control BOM explosion.

**Item-level Incoterms or payment terms cannot differ**
-> The item category must permit separate business data at item level.

## Cross-References
- Prior step: configuration-sales-document-type-control-001
- Next step: configuration-schedule-line-category-control-001
- See also: pricing-free-goods-001
- See also: special-processes-sales-workshop-scenarios-001
