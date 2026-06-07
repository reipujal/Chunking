---
schema_version: 1
id: pricing-condition-contract-settlement-001
title: "Condition Contract Settlement: Settlement Run and Document Flow"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "107-114"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - condition contract settlement run SAP
  - liquidación contrato condición SAP ejecución
  - settlement report SAP CCM
  - informe de liquidación CCM SAP
  - rebate settlement document flow SAP
  - flujo de documentos rappel SAP
  - eligible partner distribution rebate SAP
  - distribución socios autorizados rappel SAP
  - delta accruals settlement run SAP
  - ejecución acumulaciones delta rappel SAP
  - settlement calculation rebate accruals reversal
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Condition Contract Settlement: Settlement Run and Document Flow

## Operational Summary
The *settlement run* in CCM processes accumulated business volume data and generates settlement documents — credit memos or other document types — based on the condition contract settings. The settlement report is periodic, multi-partner, and multi-contract. Rebate amounts and tax are calculated in settlement document pricing. Delta accruals are separated from billing processing to avoid performance impact. Eligible partners receive their share of the rebate based on their proportional contribution to the business volume. The complete settlement process (delta accruals → partial → final) is visible in the document flow.

## Questions This Chunk Answers
- How does the settlement run generate settlement documents?
- What is the prototypic settlement sequence (delta accruals → partial → final)?
- How are rebate amounts distributed among eligible partners?
- How does the settlement calculation account for previously paid amounts?
- What is the document flow of a condition contract settlement?
- How does delta accruals separation protect billing performance?

## When It Applies and Context
The settlement run executes after the condition contract has been maintained and business volume has accumulated. It is typically scheduled periodically (daily, monthly) and can cover multiple business partners and condition contracts in a single run. Settlement documents flow to FI for posting.

## Process Flow

### Settlement Report — Execution
1. The settlement report processes formatted, accumulated business volume data from the business volume table.
2. Settlement documents are generated according to the settings in the condition contract type.
3. Rebate values and tax are calculated in settlement document pricing using the business volume values and the subsequent conditions from the condition contract.
4. Settlement documents can be integrated with pooled payment processes via Customizing in Settlement Management.

The settlement run is efficient because no aggregates need to be re-determined at runtime: the business volume is always current and determined at the level of the initiating documents (billing documents, deliveries, etc.).

### Prototypic Settlement Sequence

**Step 1 — Delta Accruals Settlement:**
- Determines accruals for business volume from the contract valid-from date.
- Deducts any accruals already posted by a previous delta accruals settlement within the same time interval.
- Posts the net accruals amount to FI.

**Step 2 — Partial Settlement:**
- Determines business volume from the contract valid-from date.
- Reverses accruals from previous delta accruals settlement runs.
- Calculates the rebate based on accumulated business volume.
- Deducts amounts already paid in prior partial settlements (cumulative mode).

**Step 3 — Final Settlement:**
- Like a partial settlement, but permanently closes the time period.
- All values from the period previously settled partially are settled in full.
- After a final settlement, the period cannot be re-opened in later partial or final runs.
- Corrections (e.g., due to late postings) are handled via a subsequent delta settlement.

### Settlement Calculation — Rebate Amount and Accruals Reversal
The settlement uses a strict separation between:
- Business volume base determination (cumulative key figures from transactional data)
- Rebate condition definition (condition types in the settlement pricing procedure)

This separation minimizes the number of condition types in the settlement pricing procedure, which directly improves runtime performance.

### Eligible Partner Distribution
When multiple eligible partners (plants, customers) are listed in the condition contract, the rebate amount is distributed proportionally by each partner's contribution to the business volume base:
- Granularity follows the business volume table: if volume is stored at plant, cost center, or material level, distribution can reach that level of detail.
- FI postings are made automatically at the account assignment object level, reflecting each partner's share at the time the service was provided.

### Document Flow
The settlement document flow provides a complete overview of the entire lifecycle:
- Delta accruals settlements → partial settlement documents → final settlement document
- After the final settlement, the process ends. The document flow shows each step, allowing full audit traceability.

## Common Errors
**Settlement document does not include all expected business volume**
-> Check the business volume table and the relevant transactional document types configured for inclusion. Documents posted before the contract entry date should be included if the contract is retroactive and the configuration covers those document types.

**Accruals not cleared after final settlement**
-> Verify that the settlement run included the accruals reversal step. In a partial or final settlement, accruals from prior delta accruals settlements are reversed automatically.

**Rebate not distributed correctly among multiple customers**
-> Check the eligible partner list in the condition contract and the business volume table granularity. If business volume is stored at an aggregate level, plant- or customer-level distribution may not be possible.

## Cross-References
- Prior step: pricing-condition-contract-maintenance-001
- See also: pricing-condition-contract-management-concept-001
- See also: billing-billing-document-creation-methods-001
- See also: integration-general-billing-interface-001
