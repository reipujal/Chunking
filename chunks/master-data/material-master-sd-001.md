---
schema_version: 1
id: master-data-material-master-sd-001
title: "Material Master Data and Customer-Material Info Records in SAP SD"
area: master-data
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "64-68"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - material master SD
  - maestro de materiales SD
  - material master sales distribution views
  - vistas maestro materiales ventas
  - customer material info record
  - registro info cliente material
  - CMiR SAP SD
  - número de material del cliente
  - cross-division sales
  - ventas multidivisión
  - division-specific sales
  - ventas específicas de división
  - qué vistas del maestro de materiales son relevantes para SD
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Material Master Data and Customer-Material Info Records in SAP SD

## Operational Summary
The *material master record* is the central object that stores all material-related information used across SAP modules. In Sales and Distribution, specific views of the material master supply default values to sales orders, outbound deliveries, and pricing. A *customer-material info record* (CMiR) extends this with customer-specific material data — particularly the mapping between the customer's own material number and the company's internal material number — and has higher priority than both the customer master and the material master when the system determines defaults in a sales order.

## Questions This Chunk Answers
- Which views of the material master are relevant for SD processes?
- What is cross-division sales and how does it differ from division-specific sales?
- What is a customer-material info record and what information can it store?
- What priority does the CMiR have over other master data sources?
- How do you use a customer-specific material number when entering a sales order?

## Definition
The *material master record* is the central database object that stores all information about a material used across SAP S/4HANA. It is a prerequisite for most logistics and financial transactions: inventory management, procurement, sales order entry, and billing all depend on material master data being maintained for the relevant organizational units. The record is organized into *views*, each associated with a specific organizational level, so that different departments (Sales, Purchasing, Production, Accounting) maintain only the data fields relevant to their function while sharing a single consistent master record.

A *customer-material info record* (CMiR) complements the material master by storing customer-specific overrides and mappings — particularly the translation between the customer's own material number and the company's internal number — for a given customer-material combination.

## Material Master — Structure for SD
Material master records are organized into *views* assigned to different organizational units. Each view activates data fields relevant to a specific business area:

| View | Org Unit Level | SD Relevance |
|---|---|---|
| *Basic Data 1* and *Basic Data 2* | Client (all areas) | Description, base unit of measure, gross/net weight, volume, tax classification, material group |
| *Sales: Sales Org. Data 1* | Sales org + Distribution channel | Delivering plant (default), sales unit, item category group, material pricing group, account assignment group |
| *Sales: Sales Org. Data 2* | Sales org + Distribution channel | Item category group (overwrite), delivering plant alternatives |
| *Sales Text* | Sales org + Distribution channel | Customer-facing text used in sales documents and correspondence |
| *Sales: General/Plant Data* | Delivering plant | Availability check control, loading group, transportation group, profit center |

The *Sales: General/Plant Data* tab is particularly important for logistics operations: the *Availability check* field controls whether and how ATP runs for this material, the *loading group* contributes to shipping point determination, and the *transportation group* contributes to route determination.

Because many departments use the same material master, the organizational structure ensures that Sales, Purchasing, Production, Warehousing, and Finance each maintain only the data fields relevant to their function, while reading shared fields from common views.

## Division-Specific vs. Cross-Division Sales
SAP SD supports two models for how divisions relate to sales orders. This behavior is controlled via parameters in the Customizing for each *sales document type*:

**Division-specific sales** restricts a sales order to materials belonging to the division specified in the order header. The system can be configured to issue a warning or an error message if a user tries to add a material with a different division. This model suits organizations where each division has its own sales team and customers should not mix products from different divisions in a single order.

**Cross-division sales** (also called centralized sales) allows a single sales order to contain materials from multiple divisions, regardless of the division in the document header. The division on each item is copied from the material master record rather than forced from the header. This model suits organizations with a single sales department that sells the full product portfolio.

Both models can coexist in the same SAP system by assigning different Customizing parameters to different sales document types.

## Customer-Material Info Record (CMiR)
A *customer-material info record* stores customer-specific material data for a given combination of customer and material. It is maintained separately from both the customer master and the material master.

### What the CMiR Stores
- **Customer material number**: the material identifier the customer uses in their own systems, mapped to the company's internal material number
- **Customer-specific material description**: the customer's name for the product, which can be printed on order confirmations and delivery notes
- **Shipping information specific to this material and customer**:
  - Delivery tolerances (under-delivery and over-delivery percentages)
  - Partial delivery control (whether partial deliveries are allowed for this item)
  - Default delivering plant

### Priority in Sales Order Processing
When a sales document is created for a customer and material for which a CMiR exists, the system uses CMiR values as the highest-priority default, overriding the corresponding defaults from the customer master and material master:
1. **Customer-material info record** (highest priority)
2. Ship-to party customer master record
3. Material master record

This priority sequence applies to the delivering plant default, shipping instructions, and partial delivery agreement at item level.

### Order Entry with Customer Material Numbers
On the *Ordering party* tab page of a sales order, the user can enter the customer's own material number. The system uses the CMiR to determine the company's internal material number and copies it into the order item. This eliminates manual translation of customer material numbers by the sales employee and reduces entry errors in high-volume order environments.

## Relationship with Other SAP SD Objects
- The material master's *item category group* (Sales Org. Data 1) is one of the inputs for *item category determination* in sales documents
- The *loading group* (General/Plant Data) is one of the inputs for *shipping point determination*
- The *transportation group* (General/Plant Data) is one of the inputs for *route determination*
- The *availability check* field (General/Plant Data) controls whether the ATP check runs and which check rule applies

## Cross-References
See also: master-data-business-partner-master-data-001 (customer master data and partner functions)
See also: order-management-availability-check-atp-001 (how CMiR priority affects partial delivery agreement and plant determination for ATP)
See also: configuration-delivery-field-determination-001 (shipping point and route determination using loading group and transportation group)
See also: configuration-sales-item-category-control-001 (item category group usage in determination)
