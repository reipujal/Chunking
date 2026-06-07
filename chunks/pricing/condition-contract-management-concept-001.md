---
schema_version: 1
id: pricing-condition-contract-management-concept-001
title: "Condition Contract Management (CCM) — Concept and Configuration Overview"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "92-99"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - condition contract management SAP S/4HANA
  - gestión de contratos de condición SAP
  - CCM SAP rebate
  - CCM descuento retroactivo SAP
  - SAP S4HANA rebate settlement
  - liquidación de rappel SAP S4HANA
  - condition contract types 0S01 0S02
  - tipos contrato condición SAP
  - RES1 REA1 rebate condition type
  - condición rappel SAP
  - rebate accruals SAP SD
  - acumulaciones rappel SAP
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Condition Contract Management (CCM) — Concept and Configuration Overview

## Operational Summary
*Condition Contract Management (CCM)* is the S/4HANA mechanism for managing rebate agreements and subsequent settlements. It replaces the traditional rebate settlement with a HANA-optimized approach: real-time business volume data, accruals posted to FI, and a minimal set of condition types. A *condition contract* combines the eligible partners, discount conditions, and settlement calendar in a single object. Settlement can be partial, final, or delta-based. CCM is configured in three sequential steps: pricing conditions, condition contract types, and settlement parameters.

## Questions This Chunk Answers
- What is Condition Contract Management and how does it differ from traditional rebate settlement?
- What is a condition contract and what does it contain?
- Which use cases does CCM support?
- What are the three CCM configuration steps?
- What condition contract types are delivered in the SAP standard?
- What are the condition types RES1, REA1, and RED1 and what is each used for?
- Which pricing procedures does SAP deliver for CCM?

## Definition

### Condition Contract
A *condition contract* stores all information relevant to a subsequent settlement agreement:
- Condition granter or contract owner
- List of eligible partners (customers or groups)
- Special conditions: discounts, prices, rebate amounts, accrual conditions
- Settlement dates and settlement types
- Business volume determination data and validity scope

Condition contract conditions are stored in Customizing as condition tables. The *condition contract number* is included in the access sequence and condition table to ensure conditions are applied only to eligible partners.

### Supported CCM Scenarios
**Customer-based:** sales-related rebates, scan-back rebates, customer funds (fixed amounts).
**Supplier-based:** purchase-related rebates, shipping-based rebates, supplier funds.
**Trade Promotion Management (TPM):** special retail industry scenarios; dedicated condition contract types 0ST1–0ST4.

## Purpose in the SD Process
CCM is the S/4HANA replacement for the ECC rebate agreement. Key improvements over the traditional approach:
- Real-time business volume aggregation (leverages SAP HANA database for aggregate calculations)
- Minimal condition types in settlement pricing procedures
- Accruals calculated and posted to FI without impacting the billing process
- Retroactive contract entry: contracts can be entered with past validity dates; business volume from already-posted documents is included

## Structure and Variants

### CCM Configuration — Three Steps
1. **Configure pricing including condition contract conditions:** define pricing procedures and condition types for settlement calculation; configure specific condition contract condition settings.
   - IMG: Logistics - General → Settlement Management → Condition Contract Management
2. **Configure condition contract maintenance:** define condition contract type parameters and the types themselves.
   - IMG: Logistics - General → Settlement Management → Condition Contract Management → Condition Contract Maintenance → Define Condition Contract Types
3. **Configure condition contract settlement:** define settlement parameters; enhance condition contract types with settlement settings.

### Condition Contract Types — Standard Delivery

| Type | Scenario | Taxation |
|---|---|---|
| 0S01 | Sales Rebate — basic, one customer | As service |
| 0S02 | Sales Rebate — multiple customers | As service |
| 0S03, 0S04 | Variations | As service |
| 0SG1–0SG4 | Same scenarios as 0S01–0S04 | Goods-related |
| 0ST1–0ST4 | TPM integration (mirrors 0S01–0S02) | As service |

Taxation as service: rebate treated as a service → VAT for services applies.
Goods-related taxation: rebate treated as revenue reduction → tax valid for the material's sales applies.

### Condition Types for CCM

| Condition type | Role | Key settings |
|---|---|---|
| RES1 | Rebate condition | Access sequence RE01; set as discount but Plus/Minus = positive (creates credit memo); account key 0S1; subtotal 1; base formula 214 for fixed amount rebates |
| REA1 | Rebate Accruals | Accruals indicator active; access sequence REA1; determines accruals amount during settlement run |
| RED1 | Delta accruals helper | Not an accruals condition itself (Accruals indicator NOT set); uses REA1 as reference; required because accruals conditions are excluded from net amount determination |

RES1 and REA1 are the conditions maintained in the condition contract. RED1 is used in the delta accruals pricing procedure (A10006) only.

### Delivered Pricing Procedures for CCM
| Procedure | Purpose |
|---|---|
| A10005 | Rebate Germany (standard partial and final settlement) |
| A10006 | Rebate Delta Accrual Germany |
| A10007 | Rebate Goods-Related Germany |
| A10008 | Rebates Manual Germany |

Configuration path for SD pricing: Sales and Distribution → Basic Functions → Pricing → Pricing Control → Define And Assign Pricing Procedures.
Also reachable via: Logistics - General → Settlement Management → Basic Settings (SD) → Define Pricing Procedures.

### Calculation Optimization
CCM leverages SAP HANA for aggregate calculations: simple aggregations and calculations are delegated to the database, minimizing the number of condition types required. At condition record level, the calculation rule and scale base indicator can be selected directly in the contract, independently of Customizing defaults.

## Relationship with Other SAP SD Objects
- The *condition contract* is the CCM equivalent of the ECC rebate agreement; it replaces the BO (rebate agreement) object
- *Settlement documents* created by the settlement run are linked to the source SD billing documents via the business volume determination
- *Pricing procedures* A10005–A10008 are standard SD pricing procedures, configurable via the same IMG path as regular SD pricing procedures
- *Condition types* RES1, REA1, RED1 are standard SD condition types; RES1 and REA1 are maintained in the condition contract's Conditions screen area, not in VK11
- The condition contract's eligible partner list integrates with the SD partner determination: only partners listed in the contract receive the condition
- FI is updated via the settlement documents (credit memos or other types); the posting uses account key 0S1 from condition type RES1

## Cross-References
- Prior step: pricing-pricing-agreements-001
- Next step: pricing-condition-contract-maintenance-001
- See also: pricing-condition-technique-overview-001
- See also: configuration-pricing-procedure-configuration-001
