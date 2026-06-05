---
schema_version: 1
id: billing-billing-plans-concept-001
title: "Periodic and Milestone Billing Plans"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "68-74"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing plan
  - plan de facturación
  - periodic billing
  - facturación periódica
  - milestone billing
  - facturación por hitos
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
*Billing plans* allow an item's total value to be invoiced across multiple dates rather than via a single billing document. The SAP system provides two distinct variants: *periodic billing* (used primarily for repeating rental/service fees) and *milestone billing* (used primarily for project-based construction).

## Questions This Chunk Answers
- What is the difference between periodic and milestone billing?
- How are billing plans configured and executed?

## Variants of Billing Plans

### 1. Periodic Billing
Periodic billing is used to systematically bill a customer for the full predetermined amount of an agreement at regular intervals (e.g., monthly lease payments for a rental contract). 
- It relies on a defined start date, end date, and horizon (specifying how far in advance dates are plotted). 
- To continually compute future dates once the horizon is reached without manual intervention, you can schedule the report `RVFPLA01` to run at regular intervals.

### 2. Milestone Billing
Milestone billing is used primarily for plant engineering and construction to equitably spread the billing of a large total amount over several distinct completion dates within the lifespan of a project.
- Dates are linked to project milestones. A milestone acts as a billing block until the actual milestone is confirmed as completed in the underlying project network. 
- You can distribute the invoice value assigning percentages or fixed values per milestone. Any subsequent manual adjustments automatically redistribute remaining values.

## Configuration and Rules
The system automatically proposes the correct billing plan type if the item category dictates it via its relevance for billing. 

Key Customizing rules include:
- **Date description**: Describes the date (e.g., "0005 for assembly").
- **Date category**: A control parameter specifying the actual billing rule to settle the date, whether the date is fixed, or whether a temporary billing block should be set.
- **Date rules**: Formal rules defining a basis date to which a specific period offset is added.
