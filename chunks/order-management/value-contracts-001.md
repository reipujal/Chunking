---
schema_version: 1
id: order-management-value-contracts-001
title: "Value Contracts in SAP SD"
area: order-management
process_tags: [order-to-cash, billing-plans]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "114-126"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - value contract
  - contrato por valor
  - contrato WK1 WK2
  - partners authorized to release contract
  - como funciona un contrato por valor
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Value Contracts in SAP SD

## Operational Summary
A *value contract* is an outline agreement where the customer commits to purchasing a fixed target value of goods and services during a defined period. The course describes material restrictions, release orders, direct contract billing, partner authorization, contract data, and date determination. Standard value contract types include general value contract WK1 and material-related value contract WK2, with different item category behavior and release handling.

## Questions This Chunk Answers
- What is a value contract in SAP SD?
- How can valid materials be restricted in a value contract?
- Can a value contract be billed directly?
- Which partners are authorized to release from a contract?
- How are contract dates proposed and controlled?

## When It Applies and Context
Use a value contract when the commercial agreement is based on a target amount rather than fixed schedule lines or fixed quantities. The contract can contain special price agreements, customer restrictions, and material restrictions that are checked when release orders are created. If configured, SAP can notify users during release order entry that valid contracts exist.

## Process Flow
1. Create the value contract for a customer and target value.
2. Restrict allowed products if needed using an assortment module or product hierarchy, as described by the course.
3. Define whether the contract is general or material-related.
4. Maintain partners authorized to release against the contract.
5. Create release orders against the contract when the customer consumes value.
6. Bill either the release orders or, in the appropriate process, the value contract itself.
7. Use contract data and date determination rules to control validity, start/end dates, duration, and follow-up activities.

## Conditions and Restrictions
The source names two standard value contract types. WK1 is a general value contract that can refer to different materials and services. WK2 is material-related and is used when the contract contains exactly one material, such as a configurable material. In Customizing, WK1 and WK2 differ in screen sequence group for document header and item. The value contract material can be maintained in the item category and acts as a technical vehicle for account assignment, taxes, and statistical updates.

Billing has two options. A release order can be billed, using the standard order OR for release orders with either order-related or delivery-related billing. A value contract can also be billed using the source's described standard release order type and a billing plan. The system adjusts open billing dates if the target value changes later. The source states that SAP does not allow automatic billing of value contracts that have not been completely released.

## Common Errors
**Release exceeds target value and response is wrong**
-> Customizing can define no response, warning messages, or an error if a release exceeds the target value in a contract item.

**Wrong partner releases from contract**
-> Check partner authorization. It can be based on a customer list or customer hierarchy, and the partner determination procedure assigns partners authorized to release.

**Contract dates are not proposed**
-> Date determination rules and contract profile assignment to the sales document type control proposed start/end dates, duration category, subsequent activities, and cancellation procedure.

## Cross-References
- Prior step: order-management-outline-agreements-scheduling-quantity-contracts-001
- See also: billing-billing-plans-concept-001
- Next step: master-data-material-determination-001
