---
schema_version: 1
id: order-management-sales-order-special-features-001
title: "Special Features When Processing Sales Orders"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "40-46"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - sales order blocks
  - bloqueos pedido de ventas
  - motivo de rechazo
  - change sold-to party in order
  - como bloquear o rechazar posiciones de pedido
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Special Features When Processing Sales Orders

## Operational Summary
SAP sales order processing includes special functions for changing document data, blocking follow-on steps, rejecting items, and handling cases where the sold-to party is entered late or changed. The source emphasizes fast changes, mass changes, delivery and billing blocks, reasons for rejection, and the controlled replacement of a default sold-to party. These functions allow users to manage order exceptions without deleting business evidence from the document.

## Questions This Chunk Answers
- How can several sales order items be changed at the same time?
- What is the difference between a delivery block, billing block, and reason for rejection?
- How does a reason for rejection close an item without deleting it?
- Can users start entering items before the real sold-to party is known?
- What data is redetermined when the sold-to party changes?

## When It Applies and Context
This applies after a *sales document* has been created or while it is being entered. It is relevant for customer service and internal sales teams who need to change multiple items, prevent delivery or billing, reject customer-requested items, or handle fast phone-sales scenarios where the actual sold-to party is confirmed after item entry starts.

## Process Flow
1. The user enters or opens the sales document.
2. If multiple items need the same change, the user can use *Fast change* to change selected or all items together.
3. If several documents need changes, the document list can be used for mass changes such as plant, currency, materials, and pricing.
4. If the order should not proceed to a later step, the user sets a delivery block, billing block, or both according to the business issue.
5. If an item should be closed because the customer does not want it, the user enters a *reason for rejection*.
6. Copying control can prevent rejected items from being copied into subsequent documents.
7. If order entry began with a default sold-to party, the responsible user replaces it with the actual sold-to party before completion.

## Conditions and Restrictions
A delivery block can be customized with detailed effects in shipping processing. The source describes options such as preventing delivery creation generally, allowing delivery and picking, or blocking goods issue. A billing block can be set in the header and in individual items.

Reasons for rejection should be used to conclude a business transaction without deleting the item. The item receives completed status. The source also notes that order reasons and reasons for rejection can be limited by assigning them to sales document types and/or sales organizations in Customizing, so users only choose from relevant values.

For phone-sales-like processing, a default sold-to party can be used only if it is supported by user-specific parameters or by a transaction variant depending on the sales document type. The default sold-to party must be flagged as a default in the customer master. The incompletion log is then responsible for ensuring the default is replaced by the real sold-to party.

## Common Errors
**Rejected item still appears in a subsequent document**
-> The reason for rejection closes the item, but copying control must include a suitable requirement to stop copying rejected items.

**Default customer remains in the order**
-> The incompletion log must check that the default sold-to party has been replaced with the real customer.

**Unexpected redetermination after changing sold-to party**
-> When the sold-to party changes, SAP runs the same checks as initial entry and redetermines data such as texts, prices, and delivering plant. Changing the ship-to party later on the overview screen does not redetermine the sold-to party.

## Cross-References
- Prior step: order-management-sales-order-source-of-data-001
- See also: configuration-sales-incompletion-check-001
- Next step: configuration-sales-document-type-control-001
