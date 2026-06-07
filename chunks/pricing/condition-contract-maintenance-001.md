---
schema_version: 1
id: pricing-condition-contract-maintenance-001
title: "Condition Contract Maintenance: Creating and Managing Condition Contracts"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "100-106"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - create condition contract SAP
  - crear contrato de condición SAP
  - condition contract settlement calendar SAP
  - calendario de liquidación contrato condición
  - partial settlement condition contract SAP
  - liquidación parcial contrato condición SAP
  - final settlement condition contract SAP
  - liquidación final contrato condición SAP
  - delta settlement condition contract SAP
  - delta accruals condition contract SAP
  - acumulaciones delta rappel SAP
  - business volume base condition contract SAP
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Condition Contract Maintenance: Creating and Managing Condition Contracts

## Operational Summary
A *condition contract* is the operational record in CCM that combines all terms of a subsequent settlement agreement: eligible partners, discount conditions, accrual rules, and a settlement calendar. Contracts support both invoiced conditions (prices, quantity/value) and subsequent settlement conditions (settled later). Accruals are posted either with the source SD billing documents or via a periodic delta accruals run. Settlement can be partial, final, or delta-correcting. Retroactive contracts — with validity dates in the past — are fully supported.

## Questions This Chunk Answers
- What does a condition contract contain?
- What is the difference between partial, final, and delta settlement?
- What is a delta accruals settlement and when is it used?
- How is the business volume base determined for a condition contract?
- What settlement types are available in the settlement calendar?
- How is a cumulative partial settlement different from a normal partial settlement?
- Can condition contracts be entered retroactively?

## When It Applies and Context
Use condition contracts for any subsequent settlement scenario: customer rebates based on billing volumes, scan-back rebates, or agreed fixed budgets. Contracts can be entered after the business documents have already been posted — SAP includes historical business volume in the settlement calculation.

## Process Flow

### Creating a Condition Contract
1. Define the condition granter (owner) and the list of eligible partners.
2. Enter the condition data: discount rates, scale thresholds, accrual conditions (RES1, REA1).
3. Specify the validity interval for the contract.
4. Define the settlement calendar with settlement dates and settlement types.
5. Enter business volume determination data (what document type and key figures are used as the volume base).
6. Release the contract via the configured release scenario.

**Retroactive contracts:** a condition contract can be created with a validity date in the past. Business volume from documents already posted before the contract entry date is included in the settlement calculation — no re-posting of historical documents is required.

**Example (from source):** contract valid October–December, scale conditions, monthly interim settlement, USD 5,000 minimum:
- October: business volume USD 3,000 — below minimum, no settlement amount calculated
- End of November: cumulative USD 7,000 — 2% rebate → settlement USD 140; accruals updated
- End of December (final settlement): total USD 27,000 — second scale level → 4% → total rebate USD 1,080
- Final payment: USD 1,080 − USD 140 (already paid) = USD 940

### Settlement Calendar — Settlement Types

| Settlement type | Description |
|---|---|
| Partial settlement | Provisionally settles the contract for a specific time period within the overall contract duration |
| Cumulative partial settlement | "Rolls up" sales and revenues from previous periods already settled; allows earlier access to higher scale-level rates |
| Final settlement | Permanently settles a specific time period; start = validity start date or last final settlement date; end = current final settlement date or validity end; not re-settled in later runs; correctable via delta settlement |
| Delta settlement | Corrects a final settlement after subsequent changes or late postings altered the business volume base; repeatable; previous delta settlements are considered |
| Delta accruals settlement | Creates or corrects accruals in accumulated form when accruals are not created with source documents; periodic run; clears existing accruals automatically |

### Business Volume Base
The settlement is based on cumulative key figures, not individual document items. Sources for business volume determination include:
- Purchase orders
- Deliveries
- SD billing documents
- Point-of-sale data
- Agreed fixed budgets

Available key figures: quantity, monetary sales, weight, volume, points.

### Accruals Management
Accruals are legally required for customer settlement processes. Two creation methods:
- **With source documents:** accruals are posted when SD billing documents are created.
- **Delta accruals settlement:** accumulated accruals are posted in a periodic run. The system determines pending accruals and posts them to FI, deducting any already-created accruals. This ensures accruals always represent the current expected payment obligation without re-evaluating historical billing documents.

Corrections to accruals required by condition changes are handled through the delta accruals settlement: the run identifies and posts the correction amounts automatically.

## Common Errors
**Settlement amount does not match expected rebate**
-> Check the scale levels and the cumulative vs. non-cumulative logic. In a cumulative partial settlement, the system "rolls up" prior periods; in a standard partial, it does not.

**Accruals are overstated after a condition change**
-> Run a delta accruals settlement. The run clears the old accruals and posts the corrected amounts based on the updated conditions.

**Business volume not included from historical documents**
-> Check the business volume determination settings. Historical documents with posting dates within the contract validity period should be included automatically if the business volume determination rules cover the relevant document type.

## Cross-References
- Prior step: pricing-condition-contract-management-concept-001
- Next step: pricing-condition-contract-settlement-001
- See also: billing-billing-document-creation-methods-001
