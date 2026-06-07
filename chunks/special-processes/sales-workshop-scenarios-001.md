---
schema_version: 1
id: special-processes-sales-workshop-scenarios-001
title: "Sales Workshop Scenarios: Employee Sales, BOM, and Material Determination"
area: special-processes
process_tags: [order-to-cash]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "153-165"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - sales workshop
  - taller de ventas
  - ventas a empleados
  - bill of material sales scenario
  - escenarios practicos S4605 ventas
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sales Workshop Scenarios: Employee Sales, BOM, and Material Determination

## Operational Summary
The S4605 workshop unit applies earlier configuration concepts to three scenarios: sales to employees, bill of material sales, and customer-specific material determination. The scenarios combine sales document types, item categories, schedule line categories, pricing, incompletion, one-time customer processing, automatic delivery, purchase requisition generation, and condition technique. They are practical design patterns rather than isolated configuration objects.

## Questions This Chunk Answers
- How is a sales-to-employee process modeled in SAP SD?
- Why can availability check and transfer of requirements be unnecessary for employee sales?
- How does a bill of material explode in a sales order?
- Which configuration objects are needed for a BOM sales scenario?
- How is material determination configured for customer-specific substitution requirements?

## When It Applies and Context
Use these scenarios when designing non-standard sales processes. Employee sales model internal shop purchases with reduced prices and immediate receipt. BOM sales model configurable or component-based products where the main item and components must appear in sales, delivery, and invoice processing. Material determination scenarios model replacement of old products by new products for selected customers or when old stock is depleted.

## Process Flow
### Sales-to-Employee
1. Employees select goods from a special shop and pay at checkout.
2. Orders are created only with a net value to avoid documents without items or free items.
3. Individual employee customer masters are not maintained; a collective one-time customer account is used.
4. Employee discounts are applied, with the course example stating a general 15% discount and possible higher discounts for some materials.
5. The delivery is created automatically when the sales document is saved.
6. Picking is unnecessary because employees can only buy available goods in the shop.
7. Goods issue can be posted manually per delivery or automatically at day end.
8. Billing is order-related and can be created automatically in a collective run; the financial posting goes to a special cash sales account with no customer receivable.

### Bill of Material Scenario
1. The customer orders a material that has a BOM master record.
2. SAP determines the item category of the main item.
3. The main item category controls whether and how the BOM explodes.
4. If explosion is required, SAP creates sub-items for the components.
5. SAP determines item categories for the sub-items and then schedule line categories based on those item categories.
6. Requirements can be transferred to purchasing at component level, allowing one order to generate several purchase orders.

### Material Determination Scenario
1. Define the business requirement: special customers receive the newest model even if they order the old one, while other customers receive it only if they order it specifically.
2. Configure material determination using condition technique in the reverse sequence of the system search.
3. Create condition table, access sequence, condition type, procedure, substitution reason, and master records.
4. Activate analysis before entering items if step-by-step determination tracing is needed.
5. Test the effect in order, delivery, and order confirmation.

## Conditions and Restrictions
For employee sales, availability check and transfer of requirements are unnecessary because goods are only purchased from the shop stock. For the BOM scenario, the delivery note must contain the bike and all components, and the invoice must contain the whole package with delivered quantity while also listing components. For material determination, substitution can be re-executed at delivery creation if availability changes between order and delivery.

## Common Errors
**Employee sales creates customer receivables**
-> The scenario expects posting to a special cash sales account with no receivable for the customer.

**BOM components do not appear as sub-items**
-> Check the main item category explosion settings and sub-item category determination.

**Material determination analysis shows no detail**
-> The source warns that analysis must be activated before entering items because it runs during determination.

## Cross-References
- Prior step: pricing-free-goods-001
- See also: configuration-sales-item-category-control-001
- See also: master-data-material-determination-001
- Next step: integration-sales-document-technical-tables-001
