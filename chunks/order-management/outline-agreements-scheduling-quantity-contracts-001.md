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
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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

**Standard document types.** The simplest and most common scheduling agreement uses document type DS. Document types BL and DEL are special cases used in the automotive component supplier industry. Contracts can cover both goods and services; rental and maintenance contracts are frequently used in the service industry.

**Scheduling agreement warnings.** When the sum of schedule line quantities exceeds the target quantity, SAP issues a warning message. The system always shows the comparison between entered quantities, target quantity, and quantity already shipped.

**Release order creation.** Copying control determines which sales document types can be used as release orders from a contract. Four ways to create release orders exist:
1. Choose *Create with reference* on the initial screen
2. Via the Sales document menu: *Sales document → Create with reference → To contract*
3. Assign an order item retrospectively to a contract
4. Automatic search for open outline agreements when creating an order

**Open outline agreement search options.** Sales document type Customizing controls whether and how SAP searches for open contracts when a release order is created:

| Setting | Behavior |
|---|---|
| Blank | No check |
| A/B | Check at header/item level; display dialog box if agreements found; user selects |
| C/D | Check at header/item level; if exactly one agreement found, copy automatically and show info message |
| E/F | Check at header/item level; branch immediately to selection list; if only one agreement, behave as C/D |

**Return orders and contract quantities.** When a return order is placed with reference to a release order, the ordered quantity in the contract is automatically corrected and reduced. Subsequent changes in any release order always cause a correction of the ordered quantity in the contract.

## Common Errors
**Quantity contract expected to contain delivery dates**
-> Contracts do not contain schedule lines, delivery quantities, or delivery dates. Those are created in the release order.

**No message appears about open contracts**
-> Review the sales document type setting (A/B/C/D/E/F) for searching open outline agreements.

**Release order was created without reference to contract**
-> Assign the order item retrospectively to the contract. All subsequent changes in that release order will then correct the contract quantity.

**Schedule line quantities exceed target quantity**
-> SAP issues a warning message. This is informational; the system does not block further schedule lines unless additional restrictions are configured.

## Cross-References
- Prior step: master-data-sd-partner-functions-001
- Next step: order-management-value-contracts-001
- See also: order-management-sales-document-data-flow-001
