---
schema_version: 1
id: enterprise-structure-head-office-branch-billing-001
title: "Billing with Head Office and Branches in SAP"
area: enterprise-structure
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "107"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - head office
  - central
  - branch
  - sucursal
  - head office payer
  - pagador central facturación
  - branch ship-to
  - sucursal destinatario facturación
  - KUNNR billing header
  - purchasing association
  - asociación de compras
  - FI head office field
  - campo central FI
  - cómo facturar a la central en SAP
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Billing with Head Office and Branches in SAP

## Operational Summary
In many purchasing association scenarios, goods are shipped to a branch while the financial receivable is directed to the head office. SAP handles this by defining the relationship between head office and branches either through the FI accounting segment of the customer master (the *Head office* field) or through SD partner functions (where the branch is the ship-to and the head office is the payer). A third option, the *Branch/Head office* field in the billing type, controls which customer number is passed to FI when the branch has no FI master data at all.

## Questions This Chunk Answers
- How do you configure a scenario where the branch receives goods but the head office pays?
- What are the two ways to represent the head office/branch relationship in SAP?
- What is the Branch/Head office field in billing type settings?
- Which customer number is used as the FI payer when the sold-to is a pure SD customer with no FI segment?
- How does the head office field in the FI customer master interact with SD partner functions?

## Definition
In SAP, the *head office* is the entity that settles payments on behalf of its branches (subsidiaries). The *branch* is the receiving location. Both are represented as separate customer master records. The relationship between them can be configured at the FI master data level, at the SD partner function level, or via billing type settings.

## Purpose in the SD Process
Without correctly configured head office/branch relationships, billing documents might send the receivable to the branch (which has no payment authority) instead of the head office. Proper configuration ensures the FI open item is created under the head office's account, enabling correct payment clearing when the head office pays for all its branches.

## Structure and Variants

### Option 1: Via Financial Accounting (FI) Master Data
Enter the head office customer number directly in the *Head office* field of the branch's customer master (accounting segment). When billing is released to FI, the receivable is automatically posted to the head office's account.

### Option 2: Via SD Partner Functions
The branch is the sold-to party and ship-to party. The head office is defined as the *payer* partner function in the SD document. The FI posting uses the payer partner.

### Option 3: Branch/Head Office Field in Billing Type
For branches that are purely SD customers (no FI accounting segment configured), the `Branch/Head office` field in billing type settings determines which entity is passed as the financial party (`KUNNR`) in the FI document:
- If the field is blank: the system uses the *Head office* field from the FI master record (Option 1 logic).
- If configured: forces either the sold-to party or the payer as the financial entity.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Customer Master (Branch) | Head office field in FI segment defines the paying entity |
| SD Partner Functions | Payer partner function provides the paying entity in SD documents |
| Billing Type | Branch/Head office field controls KUNNR in FI for branches without FI segments |
| Invoice List | Invoice lists often used in head office/branch scenarios to consolidate branch invoices |

## Cross-References
- See also: billing-invoice-list-001
- See also: enterprise-structure-billing-organizational-assignment-001
- See also: configuration-billing-types-sap-s4hana-001
