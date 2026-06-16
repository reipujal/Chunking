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
  - client company code business area SD
  - cliente sociedad area de negocio ventas
  - cross-company sales ventas interempresarial
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Enterprise Structure for Sales and Distribution in SAP

## Operational Summary
SAP uses organizational units to map the company structure used by sales, logistics, controlling, and financial accounting. The structure supports flexibility in representing complex corporate structures, adapts to corporate changes, and allows processing data across company codes. In Sales and Distribution, the main commercial structure is the *sales area* (combination of sales organization, distribution channel, and division). Delivering plants connect the commercial side of SD with logistics execution and company-code accounting.

## Questions This Chunk Answers
- What organizational units form a sales area in SAP SD?
- How does a sales organization relate to a company code and plants?
- Why can master data and conditions differ by sales area?
- What is the difference between sales office, sales group, and salesperson?
- How does a delivering plant connect sales processing with logistics?
- What is a client in SAP and how does it relate to company codes?
- What is Cross-Company Sales?

## Definition
The SAP enterprise structure separates financial units from operational and sales units. The objectives of defining organizational structures in SAP are: achieving flexibility in representing complex corporate structures; adapting to changes in the corporate structure; distinguishing between views in logistics (sales and distribution, purchasing, production), cost accounting, and financial accounting; and processing data across company codes.

**Financial units:**
- *Client*: the top level of SAP; a self-contained technical unit with shared general data and tables. All organizational units within a client share one business control. A client is synonymous with a corporate group. General data and tables used across multiple organizational structures are stored at client level.
- *Company code*: an independent accounting unit representing a legally independent company. Multiple company codes can be created per client to carry out financial accounting for several independent companies simultaneously. Multiple company codes can share the same chart of accounts. At least one company code must exist in each client.
- *Business area*: an optional organizational unit for internal reporting that crosses company code boundaries. Business areas are not limited by company code — for this reason, business areas in all company codes must share the same description. In SD postings, the business area can be derived automatically. Use business areas when profit and loss statements must be calculated independently of company code.

**SD sales units:** sales organization, distribution channel, division, sales area, sales office, sales group.

## Purpose in the SD Process

**Sales organization** represents a selling unit as a legal entity responsible for product liability and customer rights of recourse. Markets can be subdivided into regions using sales organizations. Each business transaction is processed in exactly one sales organization. A sales organization is assigned to exactly one company code. One or more plants can be assigned to a sales organization. Each sales organization has its own customer and material master data and condition records.

**Distribution channel** structures how goods reach the market: wholesale, sales to industrial customers, direct sales from a plant. Distribution channels can be set up according to market strategy or internal organization. Customers can be served through one or more distribution channels within a sales organization. Sales-relevant master data, prices, surcharges, and discounts can vary per sales organization and distribution channel.

**Division** allows a broad product range to be organized into product groups. Division-specific sales structures and division-specific customer agreements are possible (partial deliveries, pricing). Within a division, statistical analyses can be carried out and separate marketing strategies devised. Note: a material can only be assigned to one division in the material master (division is a general field of the material master, not sales-area-specific).

## Structure and Variants

**Sales area** = sales organization + distribution channel + division. Sales documents, delivery documents, and billing documents are always assigned to a sales area. Every sales process occurs in a specific sales area. Master data maintained by sales area includes: sales-relevant customer data, sales-relevant material data (note: a material can be assigned to only one division since division is a general material master field), and conditions (prices, discounts, surcharges). Sales volume evaluations and other analyses can be run within a sales area. SAP recommends keeping the sales area structure as simple as possible because every sales process runs in a specific sales area and an overly complex structure multiplies master-data maintenance effort across all sales-area-specific objects.

**Sales office** defines geographical aspects such as an office, territory, or region. A sales office can be assigned to multiple sales areas. If a sales order is entered for a sales office within a particular sales area, the sales office must be permitted for that area.

**Sales group** represents employees of a sales office assigned per division or distribution channel. Sales groups are assigned to sales offices.

**Salesperson**: a sales group consists of salespersons. A salesperson is assigned to a sales office and sales group in the sales employee master record and can then be selected in the partner screen of a sales document. Sales analyses can be run at each of these internal organizational levels.

## Relationship with Other SAP SD Objects

**Plant** is the logistics location for production, MRP, or stock storage. Material stocks can be described at storage location level within a plant. Each plant is assigned to exactly one company code. A plant serves either as a production and MRP planning location or as a material stock location. For SD, a plant must be configured specifically as a delivering plant in Customizing. During the sales process, delivering plants are used first to verify stock availability, and later to supply the goods the customer ordered.

**Delivering plant** assignment: delivering plants are assigned to a distribution chain (sales organization + distribution channel). By making the plant dependent on the distribution channel, different plants can be permitted for different distribution channels within the same sales organization — for example, the distribution channel "direct sales" can be enabled for certain plants but not others. A single plant can be assigned to multiple distribution chains and multiple sales organizations. A delivering plant can belong to a different company code than the sales organization — this scenario is called *Cross-Company Sales*.

## Cross-References
- Prior step: order-management-sales-distribution-process-001
- Next step: order-management-sales-order-source-of-data-001
- See also: configuration-delivery-field-determination-001
- See also: master-data-sd-partner-functions-001
