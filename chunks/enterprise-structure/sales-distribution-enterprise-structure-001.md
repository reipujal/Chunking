---
schema_version: 1
id: enterprise-structure-sales-distribution-enterprise-structure-001
title: "Enterprise Structure for Sales and Distribution in SAP"
area: enterprise-structure
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "16-28"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - sales area
  - estructura organizativa de ventas
  - organizacion de ventas canal sector
  - delivering plant sales area
  - como se modela la estructura comercial en SAP
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Enterprise Structure for Sales and Distribution in SAP

## Operational Summary
SAP uses organizational units to map the company structure used by sales, logistics, controlling, and financial accounting. In Sales and Distribution, the main commercial structure is the *sales area*, which combines *sales organization*, *distribution channel*, and *division*. Sales documents, delivery documents, and billing documents are assigned to a sales area, while delivering plants connect the commercial side of SD with logistics execution and company-code accounting.

## Questions This Chunk Answers
- What organizational units form a sales area in SAP SD?
- How does a sales organization relate to a company code and plants?
- Why can master data and conditions differ by sales area?
- What is the difference between sales office, sales group, and salesperson?
- How does a delivering plant connect sales processing with logistics?

## Definition
The SAP enterprise structure is the set of organizational units used to represent a company and process business data. The course distinguishes financial units, such as *client*, *company code*, and *business area*, from SD sales units such as *sales organization*, *distribution channel*, *division*, *sales area*, *sales office*, and *sales group*. These units allow SAP to process transactions in a way that reflects legal responsibility, market channels, product responsibilities, and internal sales accountability.

## Purpose in the SD Process
The *sales organization* represents a selling unit and legal responsibility for sales activities. Each business transaction is processed in one sales organization, and each sales organization is assigned to exactly one company code. A sales organization may be assigned to one or more plants and has its own master data, including customer data, material data, and condition records.

The *distribution channel* structures how goods reach the market, such as wholesale, industrial customers, or direct sales. Customers can be served through one or more channels within a sales organization, and sales-relevant master data, prices, surcharges, and discounts can vary by sales organization and distribution channel. The *division* represents a product-oriented sales structure and supports division-specific agreements such as partial deliveries or pricing.

## Structure and Variants
The course presents the *sales area* as the combination of:

| Element | Role |
|---|---|
| *Sales organization* | Selling unit and legal sales responsibility |
| *Distribution channel* | Route to market or distribution strategy |
| *Division* | Product grouping or product-specific sales responsibility |

Sales-relevant customer master data, sales-relevant material master data, and conditions are usually maintained by sales area. SAP recommends keeping the sales-area design as simple as possible, because all sales processes occur in a specific sales area and complexity multiplies master-data maintenance.

Sales offices and sales groups support internal analysis and assignment. A *sales office* can represent an office, territory, or region and may be assigned to multiple sales areas. *Sales groups* represent employees assigned within sales offices, and salespersons are assigned in the sales employee master record.

## Relationship with Other SAP SD Objects
The *plant* is the logistics location used for production, MRP, or stock storage. For SD, a plant must be configured as a delivering plant. Delivering plants are assigned to sales organization and distribution channel combinations. This assignment enables stock checks and later delivery of ordered goods. A delivering plant can serve multiple distribution chains and even belong to a different company code than the sales organization, which the source identifies as *Cross-Company Sales*.

## Cross-References
- Prior step: order-management-sales-distribution-process-001
- Next step: order-management-sales-order-source-of-data-001
- See also: configuration-delivery-field-determination-001
- See also: master-data-sd-partner-functions-001
