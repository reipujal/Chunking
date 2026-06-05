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
    pages: "15-16"
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
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The configuration of organizational units for billing requires careful cross-module alignment. A *company code* represents an independent company in the legal sense. For billing to function, *sales organizations* and *plants* must be assigned to a company code. Furthermore, each company code is linked to exactly one *chart of accounts* in Financial Accounting.

## Questions This Chunk Answers
- How are plants, sales organizations, and company codes linked for billing purposes?
- How is the company code determined during sales order entry?

## Relationship with Other SAP SD Objects
A unique assignment is made between the sales organization and the company code. Due to this unique assignment, the system can automatically determine the underlying company code simply by entering the relevant sales organization in the sales order.

*Sales organizations* and *plants* are also assigned uniquely to one company code. However, you can assign a *plant* to multiple sales organizations. The system determines the allowed plants for a given sales organization on the basis of the *distribution channel*. This allows a single sales organization to sell goods supplied by multiple plants. Furthermore, a sales organization can sell products supplied by a plant assigned to a different company code (this is known as *intercompany sales processing*).

## Purpose in the SD Process
In Financial Accounting, business transactions are posted at the company code level. Each company code uses general ledger (G/L) accounts from exactly one *chart of accounts*. Ensuring the correct organizational assignment guarantees that SD billing documents generate automatic FI postings in the correct legal entity and general ledger accounts.
