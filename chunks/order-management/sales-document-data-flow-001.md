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
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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
  - completion rule quotation order status
  - regla de finalizacion referencia parcial
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Document Flow and Create with Reference in SAP SD

## Operational Summary
SAP SD supports creating sales documents with reference to existing documents and tracking the resulting chain through *document flow*. A user can copy all items and quantities or use item selection to copy specific items and partial quantities. Copying control determines which reference relationships are allowed. Completion rules in the item category and the *Document flow update* setting in copying control determine how preceding document statuses update after copying.

## Questions This Chunk Answers
- How does create with reference work for sales documents?
- Can only selected items or partial quantities be copied from a reference document?
- What controls whether a preceding document becomes completed or partially referred?
- What information does document flow show during an SD process?
- Why must copying control exist before one document can reference another?
- What is the difference between completion rule A and completion rule B?

## When It Applies and Context
This applies when a user creates a new SD document from a preceding document, such as creating an order from one or more quotations, or when a consultant analyzes the process history using *document flow* to understand what has been copied, which quantities remain open, and which later documents exist.

## Process Flow
1. The user initiates create with reference from the initial screen or during document processing.
2. SAP opens a uniform dialog with six tab pages: Inquiry, Quotation, Order, Contract, Scheduling agreement, and Billing document.
3. The default tab appearing first is determined by the sales document category and the *Mandatory reference* field in Customizing.
4. The user identifies the required reference document.
5. If the user chooses *Copy*, SAP copies the full quantities of all eligible items. Items in the reference document that have been partially or fully completed are excluded.
6. If the user chooses *Item selection*, a list appears where the user selects specific items and adjusts quantities before copying. This allows partial quantities, all items, or a subset to be transferred.
7. When using item selection, the user can also specify a different requested delivery date for the new document at header level, which applies to all referenced items.
8. The user can create with reference from both the initial screen and during document entry, making it possible to group several quotations for a customer into a single order by referencing multiple preceding documents in sequence.
9. SAP updates reference statuses and document flow according to copying control and completion rules.

Create with reference is supported for inquiries, quotations, sales orders, contracts, scheduling agreements, and billing documents.

## Conditions and Restrictions
Create with reference is allowed only for logical business processes configured in copying control. Positive example: free-of-charge subsequent delivery based on a sales order. Negative example (not allowed): order based on a free-of-charge subsequent delivery.

To track referred quantities or values in the preceding document, the *Document flow update* field must be active at item level in copying control. If reference should be limited — for example, only until the full quantity has been referenced — the appropriate *completion rule* must be set in the item category. Each item's status in the preceding document is updated independently.

**Completion rule A:** An inquiry item receives *Completed* status as soon as it has been referenced in any quotation, even if only a partial quantity is referenced.

**Completion rule B:** A quotation item does not receive *Completed* status until the full quantity has been copied to subsequent orders. If only part of the quantity is copied, the item receives *Partially referred* status, allowing further orders from that item until the total quantity is consumed.

Additional completion rules exist for contract items. Entering a reason for rejection on an item also sets that item to *Completed* status.

## Document Flow
A sales process is captured in the *document flow* as a sequence of individual process steps, each recorded as a document. Document flows are maintained at both the overall document level and at individual item level. A user can view all documents in the flow in a list and branch directly to any individual document for display, then return to the list.

For each document in the flow, a status overview is available showing detailed processing status at every stage. A typical status chain for a standard order runs: order → delivery status → outbound delivery with picking status → billing status → billing document → posting status.

## Common Errors
**Reference document cannot be used**
-> Copying control for the source-target document type combination may not exist, or the relationship is not a logical business process.

**Preceding item remains open even after copying all quantities**
-> The *Document flow update* field in copying control at item level may be inactive. Also check the item category completion rule.

**Only part of a quotation was copied but the quotation item shows unexpected status**
-> Check which completion rule is assigned to the item category. Rule A gives *Completed* on first partial reference; rule B requires full quantity before *Completed* status.

**Manual quantity changes on referenced items are not tracked back in the preceding document**
-> Quantity updates are only reflected when *Document flow update* is active in copying control at item level.

## Cross-References
- Prior step: configuration-schedule-line-category-control-001
- Next step: configuration-sales-copying-control-001
- See also: configuration-billing-data-flow-001
