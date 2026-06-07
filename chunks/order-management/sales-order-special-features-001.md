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
SAP sales order processing includes special functions for changing document data, blocking follow-on steps, rejecting items, and handling cases where the sold-to party is entered late or changed. Key functions covered: fast changes, mass changes, delivery and billing blocks, reasons for rejection, and the controlled replacement of a default sold-to party. These functions allow users to manage order exceptions without deleting business evidence from the document.

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
A delivery block can be customized with detailed effects in shipping processing. Options include: preventing delivery creation entirely, allowing delivery and picking but blocking goods issue, and other granular combinations. A billing block can be set at the document header and in individual items. The *Fast change* function can be used to set blocks on several or all items simultaneously, and a separate button allows rejecting all items in a document at once.

Reasons for rejection conclude a business transaction without deleting the item — the item receives *Completed* status, preserving the business evidence. Reasons for rejection also serve as a marketing tool: they allow the company to analyze what customers think of its products during a period, providing planning input for future sales strategies. Order reasons and reasons for rejection can be limited per sales document type and/or sales organization in Customizing so users select only from relevant values.

**Incoterms** are derived from the *sold-to party*, not the ship-to party. This is a common misconception.

**Sold-to party changes have restrictions.** Once subsequent documents (deliveries, billing documents) already exist for a sales order, the sold-to party **cannot be changed**. Changes are only possible while no subsequent documents exist.

For phone-sales-like processing, a default sold-to party can be used if supported by user-specific parameters or a transaction variant for the sales document type. The default must be flagged as such in the customer master (*Default SP* customer type active). The incompletion log ensures the responsible user replaces the default with the real sold-to party before the document is complete.

When the sold-to party changes, SAP runs the same checks as initial entry and redetermines data such as texts, prices, and delivering plant. Changing the ship-to party later on the overview screen does not trigger redetermination of the sold-to party.

## Common Errors
**Rejected item still appears in a subsequent document**
-> Copying control must include a requirement to prevent copying of rejected items.

**Default customer remains in the order**
-> The incompletion log must check that the default sold-to party has been replaced with the real customer.

**Sold-to party field cannot be changed**
-> If subsequent documents already exist, the sold-to party cannot be changed. Cancel or reverse dependent documents first if a change is truly required.

**Incoterms show unexpected values**
-> Incoterms come from the sold-to party master record, not the ship-to party.

**User enters order reason to reject an item**
-> Order reasons and reasons for rejection are distinct. To close an item without deleting it, a reason for rejection must be used, not an order reason.

## Cross-References
- Prior step: order-management-sales-order-source-of-data-001
- See also: configuration-sales-incompletion-check-001
- Next step: configuration-sales-document-type-control-001
