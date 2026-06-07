---
schema_version: 1
id: order-management-sales-order-source-of-data-001
title: "Sources of Data During Sales Order Entry"
area: order-management
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "29-39"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - source of data
  - fuentes de datos pedido de ventas
  - propuesta automatica de datos
  - business partner customer master plant determination
  - de donde salen los datos del pedido de ventas
  - BP category organization person group
  - categoria interlocutor de negocio
  - proposing plant automatically sales order
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sources of Data During Sales Order Entry

## Operational Summary
During sales document entry, SAP supports the user by deriving values from four sources: master data, existing document data, Customizing defaults, and hard-coded program controls. The aim is to make order creation faster and avoid errors by using default values rather than requiring manual entry of every field. The Business Partner model is the central entry point for customer and vendor master data. The delivering plant is determined from a three-step priority search across customer-material info record, ship-to party master, and material master.

## Questions This Chunk Answers
- Which sources does SAP use to propose data in a sales document?
- How does the Business Partner concept support customer master processing?
- Which partner master records provide delivery, payment, and invoice data?
- How does SAP determine the delivering plant in a sales order item?
- What happens if no valid delivering plant can be determined?
- What is a BP category and can it be changed after creation?
- Can a ship-to party be entered instead of a sold-to party when creating an order?

## When It Applies and Context
This applies during creation or change of a sales document, especially a sales order. It also applies when troubleshooting why a field was proposed from an unexpected source, or when configuring BP-to-customer master synchronization.

## Process Flow
1. The user begins entering the sales document.
2. SAP reads **master data**: customer records, material records, pricing conditions, customer-material information, item proposals, bills of material, output, texts, taxes, discounts and surcharges, freight, and other relevant data. It is advisable to store as much as possible in master records to reduce entry time and avoid errors.
3. SAP uses **existing document data** already entered or automatically determined. The delivering plant, once determined at item level, contributes to shipping point determination.
4. SAP applies **Customizing** defaults: default delivery dates, delivery or billing blocks defined in the sales document type, and multi-criteria determination strategies (example: shipping point determined from delivering plant + loading group + shipping condition).
5. SAP applies **hard-coded controls** that prioritize and weight information sources, such as the automatic plant proposal logic.
6. The user can change allowed values manually, but downstream determinations depend on the final values chosen.

## Business Partner Concept
The Business Partner (BP) model is the single entry point for creating, editing, and displaying master data for business partners, customers, and vendors. A business partner can be created in one or more BP roles. Central data such as name, address, and bank details only needs to be entered once.

**BP category** classifies the partner as a natural person, an organization (legal entity or department), or a group (combination of persons such as a married couple). The category must be selected at creation and **cannot be changed later**. It controls which name and address fields are displayed:
- Organization: legal form, name, industry, legal entity
- Person: form of address, first and last name, gender, title
- Group: form of address, two names, partner group type

Standard BP categories are natural person, organization, and group. No additional categories can be created — they are hard-coded by SAP.

**BP grouping** controls number assignment: internal (system assigns number) or external (user enters number). The grouping is linked to a number range. Assigning account groups to business partner groupings ensures the customer master is updated simultaneously with the business partner.

**BP-to-customer integration** requires: matching Customizing between BP and customer account fields, aligned mandatory entry fields, number range mapping between BP grouping and customer account group, and Master Data Synchronization setup via IMG.

## Partner Data Sources in the Sales Document
Business data in the sales document is taken from the master data of the business partners involved:

| Business data | Source master record |
|---|---|
| Delivery address and control information | Ship-to party |
| Payment conditions | Payer |
| Invoice address | Bill-to party |

The sold-to party is mandatory in a sales order and is the anchor point that determines the other three mandatory partners (ship-to party, payer, bill-to party). A user may also enter the ship-to party instead of the sold-to party in the sold-to party field. SAP then determines the sold-to party:
- If exactly one sold-to party exists for that ship-to party: determined automatically
- If several sold-to parties exist: a selection screen appears
- If none can be determined: an error appears in the status bar
- If the ship-to party was entered in the sold-to party field inadvertently: a message appears and SAP processes the entry as if it were entered in the ship-to party field

Business data (payment conditions, Incoterms) can be maintained at document header level or at individual item level. Whether item-level business data may differ from the header is controlled per item category in Customizing.

## Delivering Plant Determination
The plant is an integral part of logistics and assumes the role of delivering plant in sales. When an item is entered, SAP attempts to determine the delivering plant automatically through a three-step priority search:

1. **Customer-material info record**: the system checks for a delivering plant entry there first.
2. **Ship-to party customer master**: if the info record contains no plant, SAP checks the ship-to party master record.
3. **Material master**: if that is also unsuccessful, SAP checks the material master record.

If all three are empty, no valid delivering plant can be determined. Without a plant, shipping point determination fails, no availability check is possible, and no delivery can be created automatically. A USEREXIT can be used to enhance the standard plant proposal logic if needed.

## Common Errors
**No valid plant can be determined**
-> Check customer-material info record, ship-to party customer master, and material master in that order. If all are empty, shipping and availability fail.

**Unexpected payment terms or invoice address**
-> Payment conditions come from the payer; invoice address from the bill-to party; delivery address and control from the ship-to party.

**Business data differs between header and item unexpectedly**
-> Item category Customizing controls whether item-level business data may differ from the header. Review the item category setting.

**BP-to-customer synchronization is incomplete**
-> Verify number range mapping between BP grouping and customer account group, and that Master Data Synchronization is set up in IMG.

## Cross-References
- Prior step: enterprise-structure-sales-distribution-enterprise-structure-001
- Next step: order-management-sales-order-special-features-001
- See also: master-data-sd-partner-functions-001
- See also: master-data-material-determination-001
