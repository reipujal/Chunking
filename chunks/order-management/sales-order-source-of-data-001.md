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
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sources of Data During Sales Order Entry

## Operational Summary
During sales document entry, SAP supports the user by deriving values from several sources: master data, data already present in the document, Customizing, and hard-coded program controls. This reduces manual entry and prevents inconsistent orders. The course highlights customer and material master data, Business Partner integration, partner roles, business data, and automatic delivering plant proposal as central mechanisms behind sales order data determination.

## Questions This Chunk Answers
- Which sources does SAP use to propose data in a sales document?
- How does the Business Partner concept support customer master processing?
- Which partner master records provide delivery, payment, and invoice data?
- How does SAP determine the delivering plant in a sales order item?
- What happens if no valid delivering plant can be determined?

## When It Applies and Context
This applies during creation or change of a *sales document*, especially a sales order. The goal is to make order entry efficient by using default values and reference data rather than requiring the user to manually enter every field. It also applies when troubleshooting why a field in the order was proposed from an unexpected source.

## Process Flow
1. The user begins entering the sales document.
2. SAP reads *master data* for customers, materials, pricing conditions, customer-material information, item proposals, bills of material, output, texts, taxes, discounts, freight, and similar data.
3. SAP uses *existing document data* that has already been entered or determined. For example, the delivering plant contributes to later shipping point determination.
4. SAP applies *Customizing* defaults and strategies, such as default delivery dates, delivery or billing blocks, and multi-criteria determinations.
5. SAP applies hard-coded controls where the standard program prioritizes sources, such as plant proposal logic.
6. The user can change allowed values manually, but downstream determinations may depend on the final values.

## Conditions and Restrictions
The Business Partner model is the central entry point for maintaining business partners, customers, and vendors. A *business partner category* must be chosen when a partner is created and cannot be changed later. The category controls which name and identification fields appear for an organization, person, or group. A *business partner grouping* controls number assignment. BP-to-customer integration requires matched Customizing, aligned required fields, number ranges, account groups, and synchronization settings.

For sales orders, the sold-to party is mandatory and acts as the anchor point. The sold-to party determines mandatory partners: ship-to party, payer, and bill-to party. The course also notes that a user may enter a ship-to party instead of a sold-to party. If exactly one sold-to party can be derived, SAP determines it automatically; if multiple alternatives exist, a selection appears; if no sold-to party can be derived, an error appears.

## Common Errors
**No valid plant can be determined**
-> SAP first checks the customer-material info record, then the ship-to party customer master, then the material master. If none contains a plant, shipping point determination, availability check, and delivery creation cannot proceed automatically.

**Unexpected payment terms or invoice address**
-> Payment conditions come from the payer, while the invoice address comes from the bill-to party. Delivery address and control information come from the ship-to party.

**Business data differs between header and item**
-> Item category Customizing controls whether item-level business data, such as payment terms or Incoterms, may differ from the header.

## Cross-References
- Prior step: enterprise-structure-sales-distribution-enterprise-structure-001
- See also: master-data-sd-partner-functions-001
- Next step: order-management-sales-order-special-features-001
