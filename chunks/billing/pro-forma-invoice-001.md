---
schema_version: 1
id: billing-pro-forma-invoice-001
title: "Pro Forma Invoices in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "26-27"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - pro forma
  - proforma
  - factura proforma
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
A *pro forma invoice* is a draft or preliminary invoice typically used for export transactions or customs documentation. It does not update the billing status of the reference document and is never transferred to Financial Accounting (FI).

## Questions This Chunk Answers
- What is a pro forma invoice used for?
- Does a pro forma invoice generate accounting postings?
- Can multiple pro forma invoices be created for the same document?

## Characteristics of Pro Forma Invoices
- **References**: You can create pro forma invoices with reference to either an order or an outbound delivery.
- **Goods Issue**: You do *not* need to post the goods issue before creating a delivery-related pro forma invoice.
- **Repeatability**: You can create as many pro forma invoices as required. This is because creating a pro forma invoice does not update the billing status in the reference document.
- **Accounting**: Data from pro forma invoices is never transferred to Financial Accounting.
- **Standard Types**: The standard system provides billing type `F5` (based on order quantity) and `F8` (based on delivery quantity).

## Restrictions in Copying Control
In copying control, the `Pos./neg. quantity` field is intentionally made unavailable for entry for pro forma invoices. This avoids the possibility of a pro forma invoice updating the quantity that has already been billed in the reference document.
