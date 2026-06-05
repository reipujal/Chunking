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
    pages: "99"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - head office
  - central
  - branch
  - sucursal
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Companies frequently ship goods to a subsidiary branch while the financial receivables are directed exclusively to the central head office. SAP handles this discrepancy using partner functions or FI linkages to determine exactly who receives the financial liability.

## Questions This Chunk Answers
- How do you configure a scenario where the branch receives goods but the head office pays?

## What This Configuration Controls
When maintaining master data, you can represent the relationship between the head office and its branches in two primary ways:

1. **Via the Financial Accounting linkage**: You enter the head office entity directly into the accounting segment of the branch's customer master record.
2. **Via Sales and Distribution Partner Functions**: The branch serves strictly as the sold-to party/ship-to party, while the head office serves as the payer.

## The Branch/Head Office Field in the Billing Type
In highly specific setups where a branch acts as a pure SD customer, you might strategically omit maintaining its financial accounting segment completely. You configure the `Branch/Head office` field in the billing type settings to determine identically which entity is passed as the financial party responsible.
These field settings dictate forcefully whether the *sold-to party* or the *payer* assumes the `KUNNR` (customer number) designation in the billing header upon transmission to FI. If this field is blank, the system explicitly prioritizes any relationship stored directly in the `Head office` field of the FI master record.
