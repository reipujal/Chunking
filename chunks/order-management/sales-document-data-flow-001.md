---
schema_version: 1
id: order-management-sales-document-data-flow-001
title: "Document Flow and Create with Reference in SAP SD"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "68-74"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - document flow
  - flujo de documentos
  - crear con referencia
  - create with reference item selection
  - como ver el flujo de documentos SD
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Document Flow and Create with Reference in SAP SD

## Operational Summary
SAP SD supports creating sales documents with reference to existing documents and tracking the resulting chain through *document flow*. A user can copy all items and quantities or select specific items and partial quantities. Copying control determines which reference relationships are allowed, while completion rules and document flow update settings determine whether the preceding document is marked completed, partially referred, or still open.

## Questions This Chunk Answers
- How does create with reference work for sales documents?
- Can only selected items or partial quantities be copied from a reference document?
- What controls whether a preceding document becomes completed or partially referred?
- What information does document flow show during an SD process?
- Why must copying control exist before one document can reference another?

## When It Applies and Context
This applies when a user creates a new SD document from a preceding document, such as creating an order from one or more quotations or another logically valid document relationship. It also applies when a consultant analyzes the process history using *document flow* to understand what has been copied, which quantities or values remain open, and which later documents already exist.

## Process Flow
1. The user chooses create with reference from the initial screen or during document processing.
2. SAP opens a uniform dialog with tab pages for Inquiry, Quotation, Order, Contract, Scheduling agreement, and Billing document.
3. The default tab is determined by the sales document category and the mandatory reference field.
4. The user identifies the required reference document.
5. If the user chooses Copy, SAP copies the full quantities of all eligible items.
6. If the user chooses item selection, selected items can be copied with adjusted quantities.
7. SAP updates reference statuses and document flow according to copying control and completion rules.

## Conditions and Restrictions
Create with reference is allowed only for logical business processes configured in copying control. The source gives a positive example of a free-of-charge subsequent delivery based on a sales order and a negative example of an order based on a free-of-charge subsequent delivery.

When Copy is used, full quantities of all items are copied except items already partially or fully completed. To update referred quantities or values, the *Document flow update* field must be checked at item level in copying control. If reference should be limited, for example only until the full quantity has been referenced, the appropriate *completion rule* must be set in the item category.

## Common Errors
**Reference document cannot be used**
-> Copying control for the source and target relationship may not exist, or the relationship may not be a logical business process.

**Preceding item remains open even after copying**
-> Check document flow update and the item category completion rule.

**Only part of a quotation was copied but the status is unexpected**
-> Completion rule A completes an inquiry item as soon as it has been referenced in a quotation, even for partial quantity. Completion rule B keeps a quotation item partially referred until the full quantity is copied.

## Cross-References
- Prior step: configuration-schedule-line-category-control-001
- Next step: configuration-sales-copying-control-001
- See also: configuration-billing-data-flow-001
