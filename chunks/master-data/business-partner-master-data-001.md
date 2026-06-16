---
schema_version: 1
id: master-data-business-partner-master-data-001
title: "Business Partner Master Data in SAP S/4HANA SD"
area: master-data
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "58-63"
    source_type: A
    role: primary
transactions: [BP]
tables: []
aliases:
  - business partner master data
  - maestro de interlocutores de negocio
  - customer master data S4HANA
  - maestro de clientes S4HANA
  - business partner roles
  - roles de interlocutor de negocio
  - sold-to ship-to payer bill-to
  - interlocutores obligatorios SD
  - estructura maestro cliente S4HANA
  - cómo se mantiene el maestro de clientes en S4HANA
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Business Partner Master Data in SAP S/4HANA SD

## Operational Summary
In SAP S/4HANA, customer and vendor master data is managed through the unified *Business Partner* (BP) concept. This replaces the separate customer and vendor master records used in SAP ECC. A business partner is created once and then assigned to one or more business contexts — called *roles* — that activate the corresponding data fields. For SD processes, the relevant roles are *Customer* and *FI Customer*. Business partner master data is the primary source of default values that flow into sales documents at header and item level.

## Questions This Chunk Answers
- What is the business partner approach in SAP S/4HANA and how does it differ from SAP ECC?
- How is customer master data structured in S/4HANA?
- What are the four mandatory partner functions required for SD sales order processing?
- What is the role concept in the business partner and how does it activate SD-relevant data?
- What sales area data is maintained in the customer master and what does it control?

## Definition
A *business partner* is a central master data object that represents companies, persons, or groups engaged in business relationships. The BP approach centralizes master data maintenance: a single business partner record can represent both a customer and a vendor, avoiding data redundancy and improving data integrity across Sales, Purchasing, Finance, and other modules.

In SAP ECC, customer and vendor master records were maintained separately. In SAP S/4HANA, both are managed under a single business partner, with the relevant data activated by assigning the appropriate role.

## Business Partner Categories
When a business partner is created (transaction **BP** or the corresponding Fiori app), the *Business Partner Category* must be selected:
- **Person**: an individual
- **Group**: a household, married couple, or executive board
- **Organization**: a company, department, or association (most common for SD customers)

## Role Concept
A *business partner role* corresponds to a business context in which the business partner participates. Assigning a role activates the data fields relevant for that context:

| Role | Context | Activates |
|---|---|---|
| Customer | SD sales processes | Sales area data, ordering, shipping, billing, partner functions |
| FI Customer | Financial Accounting | Company code data: reconciliation account, payment terms, dunning |
| Vendor | Purchasing | Purchasing org data, bank details |

A business partner can hold multiple roles simultaneously. For example, a company can be both a *Customer* (for sales) and a *Vendor* (for procurement) under the same BP record.

## Structure of Customer Master Data
Customer master data (business partner in the Customer and FI Customer roles) is organized into three data categories:

### General Data
Valid for all organizational units within the client. Contains information relevant to all company codes and sales areas: name, address, communication data, tax information. Changes here affect the customer globally.

### Sales Area Data
Valid for a specific combination of sales organization, distribution channel, and division. This is the most business-critical section for SD. It is organized into tab pages:
- **Orders**: ordering unit, currency, pricing procedure assignment, order probability
- **Shipping**: partial delivery agreement, delivery priority, shipping conditions (used for shipping point and route determination), relevant for delivery documents
- **Billing**: billing date, payment terms, Incoterms, invoice consolidation
- **Partner Functions**: default values for mandatory and optional partner functions

A customer must have sales area data maintained for each sales area in which it participates. Without it, the system cannot create SD documents for that sales area.

### Company Code Data
Valid for a specific company code. Contains accounting-relevant information: reconciliation account, payment terms, dunning procedure, bank details. Typically maintained by the accounting department.

## Mandatory Partner Functions in Sales Documents
For SD sales order processing, four *partner functions* are mandatory. They represent distinct roles in the commercial transaction:

| Partner Function | Description |
|---|---|
| *Sold-to party* | The customer who places the order |
| *Ship-to party* | The customer who physically receives the goods |
| *Bill-to party* | The customer who receives the invoice |
| *Payer* | The customer who pays the invoice |

In many transactions, all four partner functions refer to the same business partner (one company places, receives, invoices, and pays for its own orders). However, in more complex scenarios — such as centralized purchasing for multiple sites, or third-party billing — the four roles may reference different business partners.

Default values for these four mandatory partner functions are maintained in the *Partner Functions* tab of the customer's sales area data. When a sales order is created for a sold-to party, the system copies these defaults into the document automatically.

Optional partner functions (such as contact person, forwarding agent, or sales representative) can also be maintained in the business partner master and copied into documents where relevant.

## Relationship with Other SAP SD Objects
The business partner master record supplies default values to:
- **Sales orders**: sold-to party, ship-to party, bill-to party, payer, pricing conditions, payment terms, shipping conditions
- **Outbound deliveries**: ship-to party address, partial delivery agreement, shipping conditions for shipping point determination
- **Billing documents**: payer, payment terms, Incoterms, bank data for FI posting

## Cross-References
See also: master-data-sd-partner-functions-001 (partner determination procedures and account groups)
See also: master-data-material-master-sd-001 (material master data for SD)
See also: order-management-sales-order-source-of-data-001 (how master data feeds into sales documents)
See also: enterprise-structure-sales-distribution-enterprise-structure-001 (sales area definition)
