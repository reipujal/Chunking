---
schema_version: 1
id: enterprise-structure-billing-organizational-assignment-001
title: "Organizational Unit Assignments for Billing in SAP SD"
area: enterprise-structure
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "23-24"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - company code
  - sociedad
  - sales organization
  - organización de ventas
  - chart of accounts
  - plan de cuentas
  - intercompany sales
  - ventas entre sociedades
  - plant assignment billing
  - asignación de centro a sociedad
  - company code determination billing
  - determinación de sociedad en factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Organizational Unit Assignments for Billing in SAP SD

## Operational Summary
For billing to post correctly to Financial Accounting, the key organizational units — *company code*, *sales organization*, and *plant* — must be correctly assigned to each other. The company code is the legal entity in FI. The sales organization is uniquely assigned to one company code, which allows SAP to determine the company code automatically during order entry. Each company code is linked to exactly one *chart of accounts*, ensuring G/L accounts are correctly resolved when billing generates FI postings.

## Questions This Chunk Answers
- How does SAP determine the company code for a billing document?
- Can a plant be assigned to more than one sales organization?
- Can a sales organization sell goods supplied by a plant in a different company code?
- What is the relationship between the sales organization and the company code?
- Why must the chart of accounts be correctly assigned for billing to work?
- What is intercompany sales processing and when does it apply?

## Definition
*Organizational unit assignment* in the context of billing refers to the configuration linkages between SD organizational structures (sales organizations, plants) and FI organizational structures (company codes, chart of accounts). These assignments ensure that SD billing events generate FI postings in the correct legal entity.

## Purpose in the SD Process
In Financial Accounting, every posting belongs to a company code. Because the company code is not entered directly in the sales order, SAP derives it automatically from the sales organization. Without the correct sales organization → company code assignment, billing cannot determine where to post revenue. The chart of accounts assignment ensures that the G/L accounts used in account determination exist in the correct accounting framework.

## Structure and Variants
The organizational assignments for billing follow these rules:

| Assignment | Rule |
|---|---|
| Sales organization → Company code | **Unique**: one sales organization belongs to exactly one company code |
| Plant → Company code | **Unique**: one plant belongs to exactly one company code |
| Plant → Sales organization | **Multiple allowed**: a plant can serve multiple sales organizations (within the same company code) |
| Plant in different company code | Allowed — enables *intercompany sales processing* (cross-company billing) |
| Company code → Chart of accounts | Exactly one chart of accounts per company code |

**Intercompany sales**: a sales organization can sell goods supplied by a plant assigned to a different company code. This triggers intercompany billing (billing type IV) between the two company codes.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Organization | Primary SD org unit; drives company code determination at order entry |
| Company Code | FI legal entity; all revenue postings are made here |
| Plant | Supplies goods; must be assigned to the selling company code (or triggers intercompany billing) |
| Chart of Accounts | Defines G/L account numbers available for revenue posting in that company code |
| Account Determination | Uses company code + sales organization + account assignment groups to find G/L accounts |

## Cross-References
- See also: enterprise-structure-head-office-branch-billing-001
- See also: configuration-billing-account-determination-001
- See also: configuration-billing-types-sap-s4hana-001
