---
schema_version: 1
id: order-management-outline-agreements-scheduling-quantity-contracts-001
title: "Scheduling Agreements and Quantity Contracts in SAP SD"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "108-113"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - outline agreement
  - acuerdo marco
  - contrato por cantidad
  - scheduling agreement release order
  - diferencia entre scheduling agreement y quantity contract
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Scheduling Agreements and Quantity Contracts in SAP SD

## Operational Summary
Outline agreements formalize agreed goods or services, conditions, and validity periods between business partners. The course identifies two main outline agreement types: *scheduling agreements* and *contracts*. Scheduling agreements contain fixed delivery dates and quantities directly in schedule lines. Quantity contracts do not contain schedule lines, delivery quantities, or delivery dates; they are fulfilled by release orders that reference the contract and update released quantities or values.

## Questions This Chunk Answers
- What is an outline agreement in SAP SD?
- How does a scheduling agreement differ from a quantity contract?
- How are release orders created from a contract?
- How does SAP search for open outline agreements during order entry?
- How are released quantities in a contract updated?

## When It Applies and Context
Use outline agreements when a customer and seller agree on goods or services over a period instead of handling each demand as an isolated order. Scheduling agreements are appropriate where delivery dates and quantities are already known and maintained in the agreement. Quantity contracts are appropriate where the customer commits to a target quantity or value over time but releases individual orders as needed.

## Process Flow
### Scheduling Agreement
1. Create an outline agreement valid for a period with a sold-to party.
2. Enter schedule lines with fixed delivery dates and quantities.
3. SAP sums entered quantities and compares them with the target quantity and already shipped quantity.
4. When schedule lines are due, create delivery normally or via the delivery due list.
5. If periodic billing is required, combine due deliveries in a collective invoice.

### Quantity Contract
1. Create a contract valid for a defined period.
2. Maintain contract conditions such as special prices or delivery times.
3. Create release orders with reference to the contract.
4. SAP creates schedule lines in the release order, not in the contract.
5. Process the release order like a standard order.
6. SAP updates released quantities and values in the contract through document flow.

## Conditions and Restrictions
Copying control determines which sales document types can be used as release orders from a contract. Release orders can be created from the initial screen with create with reference, from the sales document menu, by assigning an order item to a contract retrospectively, or by using automatic search for open outline agreements during order creation.

Sales document type Customizing can activate messages about open outline agreements. The source lists options ranging from no check, to header or item checks with a selection dialog, to automatic copy if exactly one open agreement exists, to immediate branching to the selection list.

## Common Errors
**Quantity contract expected to contain delivery dates**
-> The source states that contracts do not contain schedule lines, delivery quantities, or delivery dates. Those are created in the release order.

**No message appears about open contracts**
-> Review the sales document type setting for searching open outline agreements.

**Release order was created without reference**
-> The course notes that an order item can be assigned retrospectively to the contract; later changes in release orders correct the ordered quantity in the contract.

## Cross-References
- Prior step: master-data-sd-partner-functions-001
- Next step: order-management-value-contracts-001
- See also: order-management-sales-document-data-flow-001
