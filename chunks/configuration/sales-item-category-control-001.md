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
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "157-160"
    source_type: A
    role: secondary
transactions: []
tables: []
aliases:
  - item category
  - categoria de posicion
  - determinacion categoria de posicion
  - sales item category group usage
  - que controla la categoria de posicion
  - sub-items BOM explosion sales order
  - sub-posicion explosion lista de materiales
  - alternative items quotation inquiry
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-08
---

# Sales Item Category Control in SAP SD

## Operational Summary
The *item category* controls how each sales document item behaves during the current document and all follow-on processing. It determines whether business data (Incoterms, payment terms) can differ from the header, whether pricing applies, how the item is billed, whether it references a material or is a text item, which incompleteness procedure is used, and how sub-items such as free goods or BOM components are handled. Item category determination uses four inputs: sales document type, item category group, item usage, and the item category of the higher-level item.

## Questions This Chunk Answers
- What does the item category control in a sales document?
- How is the item category proposed automatically?
- When can item-level business data (Incoterms, payment terms) differ from header data?
- How are sub-items, free goods, and BOM components represented in sales orders?
- Why should new item categories always be copied from tested standard categories?
- What are alternative items in quotations and how do they differ from sub-items?
- What does the item category key structure indicate?

## What This Configuration Controls
An *item category* is defined with a four-digit key. The key follows a naming convention: the first two characters indicate the sales document type the category was originally designed for; the last two indicate the usage:

| Example key | Original doc type | Usage |
|---|---|---|
| AFTX | IN (Inquiry) | TEXT |
| TAD | OR (Standard Order) | LEIS (service) |
| KMN | AG (Quotation) | NORM |

Standard item categories can be modified. New ones should always be created by **copying an existing, tested item category**, then changing it to meet requirements — this avoids missing configuration dependencies.

The essential characteristics of an item category:
- Whether business data (e.g., Incoterms, payment terms) at item level can differ from the document header
- Whether pricing is carried out
- Whether and how the item is billed (order-related, delivery-related, or not relevant)
- Whether the item refers to a material or is a text item
- Which incompleteness procedure checks the item data
- *Delivery relevance* (for items without schedule lines, e.g., letting a text item be copied from the order into the delivery)

## SPRO Path or Direct T-code
Not stated in source.

## Key Parameters

| Field or setting | Description | Typical Values |
|---|---|---|
| *Business data at item level* | Controls whether item terms can differ from header | Same as header or separately maintainable |
| *Pricing relevance* | Determines whether pricing is carried out | Active or inactive |
| *Billing relevance* | Determines whether and how the item is billed | Order-related, delivery-related, not relevant |
| *Material relevance* | Material item or text item | Material or text |
| *Incompletion procedure* | Controls which item fields are checked | Assigned procedure |
| *Delivery relevance (no schedule lines)* | Lets items without schedule lines be copied to delivery | Example: text item delivery relevance |
| *Higher-level item support* | Enables sub-items | Free goods, BOM, service structures |

## Configuration Impact

**Item category determination.** The system proposes an item category using four elements:
1. Sales document type
2. Item category group (from the material master — groups materials with similar SD behavior; custom groups can be defined)
3. Item usage (set internally by the program in certain cases: `TEXT` when description is entered without a material number; `FREE` for free goods items)
4. Item category of the higher-level item (for sub-items)

The assignment to sales document types also defines *alternative item categories* that the user can manually override.

**Sub-items.** An item can be assigned to a higher-level item to create a sub-item structure. Example: for ordering 100 units of material M1 at 1000 Euro, the customer receives 10 units of M2 free of charge — M2's item (item 20) is assigned to M1's item (item 10) via the higher-level item field. Other sub-item use cases include BOM explosion and service items.

**Alternative items** can be recorded in quotations and inquiries (in addition to sub-items). Alternative items are treated differently: they are **not included in the net value of the document**, whereas sub-items contribute to value as configured.

**Bill of material (BOM) explosion.** When the item category is configured to allow it, entering the main BOM material in the order triggers automatic generation of sub-items for all BOM components. The BOM must be flagged as sales-relevant. Using BOM usage 5 (sales and distribution) flags all BOM items as sales-relevant automatically. Item categories control:
- Whether the BOM is exploded
- The extent of the structure (how deep)
- Which items are relevant for pricing
- Requirements transfer behavior

**BOM explosion sequence (step by step):** (1) enter the main BOM material in the order; (2) the system determines the item category for the main item; (3) the main item category controls whether and how deeply the BOM is exploded; (4) if explosion is configured, the system automatically lists all components as sub-items under the main item; (5) the system determines an item category for each sub-item; (6) schedule line categories are determined dependent on the sub-item's item category. All of these steps and their results can be customized.

**BOM in sales — business context.** BOM explosion fits scenarios where a company sells configured goods assembled from components sourced externally rather than stocked. Typical properties:
- No availability check in the order — components are procured from the distributor after the sales order is placed, eliminating warehouse stock and reducing capital tie-up.
- Requirements are transferred to purchasing at component level: one sales order can generate multiple purchase orders (one per component vendor).
- The outbound delivery lists both the main item and all its components.
- The invoice covers the full package with the delivered quantity; all components are itemized.
- Customers can also order individual replacement parts from the same BOM structure.

## Common Configuration Errors
**Wrong item category proposed**
-> Check the sales document type assignment, material item category group, item usage, and higher-level item category.

**Item-level Incoterms or payment terms cannot differ from header**
-> The item category must be configured to permit separate business data at item level.

**Text or free goods item behaves like a normal priced item**
-> Review pricing relevance and usage-based determination in the item category.

**BOM does not explode in the sales order**
-> Confirm the BOM is sales-relevant (BOM usage 5) and the main item category is configured to control BOM explosion.

**Alternative items appear in the net value**
-> Alternative items must not be included in net value; check the item category's billing/value relevance settings.

## Cross-References
- Prior step: configuration-sales-document-type-control-001
- Next step: configuration-schedule-line-category-control-001
- See also: pricing-free-goods-001
- See also: special-processes-sales-special-business-transactions-001
