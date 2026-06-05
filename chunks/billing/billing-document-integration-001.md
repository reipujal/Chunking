---
schema_version: 1
id: billing-billing-document-integration-001
title: "Integration of Billing Documents in the SAP SD Process"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "10"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing document
  - factura
  - integration
  - integración
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The *billing document* represents the final function in the Sales and Distribution (SD) process chain. It integrates seamlessly with Financial Accounting (FI), allowing for the automatic creation of documents in Financial Accounting and Controlling.

## Questions This Chunk Answers
- How does the billing document integrate with the broader Sales and Distribution process?
- What are the downstream effects of creating a billing document?

## Definition
The billing document is the final step in the order-to-cash process. It serves as the interface between the SD module and Financial Accounting.

## Relationship with Other SAP SD Objects
Creating a billing document has multiple effects on various areas of the system, including:
- Billing orders and deliveries
- Updating the document flow
- Creating documents automatically in Financial Accounting
- Updating the billing status
- Updating the Sales Information System (SIS)
- Updating the customer credit account
- Forwarding data to Profitability Analysis (CO-PA)
