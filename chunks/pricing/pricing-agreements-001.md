---
schema_version: 1
id: pricing-pricing-agreements-001
title: "Pricing Agreements: Promotions and Sales Deals in SAP SD"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "85-91"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - promotion SAP SD pricing
  - promoción precio SAP ventas
  - sales deal SAP pricing
  - acuerdo comercial SAP precio
  - release status sales deal SAP
  - estado de liberación acuerdo comercial
  - condition records linked to promotion SAP
  - registros condición vinculados promoción SAP
  - pricing agreements SAP SD
  - acuerdos de precio SAP SD
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Pricing Agreements: Promotions and Sales Deals in SAP SD

## Operational Summary
SAP SD organizes promotional pricing through two linked objects: a *promotion* representing the high-level marketing plan, and one or more *sales deals* providing product-line-level focus within it. Condition records for discounts are linked to the sales deal (and carry the promotion number). The *release status* of a sales deal controls where those condition records are active — from CO-PA planning only, to pricing simulation, to live document pricing. Sales deal and promotion numbers are visible in billing document item detail.

## Questions This Chunk Answers
- What is a promotion in SAP SD and how does it relate to sales deals?
- How are condition records linked to a sales deal or promotion?
- Where are the sales deal and promotion numbers visible in the document flow?
- What does the release status of a sales deal control?
- Can the same condition record be analyzed by promotion?

## When It Applies and Context
Use promotions and sales deals when discounts or special prices apply for a limited marketing period and need to be tracked separately from standard pricing agreements. This structure supports post-campaign analysis by linking all condition records back to a specific promotion or deal.

## Process Flow

### Creating Promotions and Sales Deals
1. Create a promotion defining the high-level marketing plan, product scope, and time period.
2. Within the promotion, create one or more sales deals — each covering a specific product line or discount type.
3. Create or assign condition records to the sales deal. Customer-specific discounts and material-based discounts can coexist within the same sales deal.
4. When a condition record is linked to a sales deal that is itself linked to a promotion, the condition record carries the promotion number automatically.

### Release Status for Sales Deals
The release status determines where the condition records of a sales deal are active:

| Status | Effect |
|---|---|
| B | Records included in pricing simulation (net price list) but **not** used in current sales documents |
| C | Records considered in CO-PA planning (Profitability Analysis), not in live documents |

Without an explicit release status, records linked to an active sales deal are applied in live document pricing.

### Visibility in Documents
The billing item detail screen displays both the sales deal number and the promotion number. This makes it possible to trace any billed discount back to its originating promotion or deal.

### Analysis
All condition records linked to a specific promotion number can be listed and analyzed together. This enables post-campaign evaluation of which discounts were applied under a promotion.

## Common Errors
**Promotional discount not applied in sales order**
-> Check the release status of the sales deal. Status B means the records appear only in pricing simulations, not in live orders.

**Cannot find which orders used a specific promotion**
-> Use condition record analysis filtered by the promotion number. The promotion number is stored on the condition record and flows to the billing document.

**Sales deal condition records not appearing in pricing simulation**
-> Check the release status. Status B makes records visible in pricing simulation (net price list) but not in live documents. Status C restricts records to CO-PA planning only.

## Cross-References
- Prior step: pricing-statistical-condition-types-001
- Next step: pricing-condition-contract-management-concept-001
- See also: pricing-condition-records-001
- See also: order-management-outline-agreements-scheduling-quantity-contracts-001
