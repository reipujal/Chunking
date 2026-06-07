---
schema_version: 1
id: billing-billing-plans-concept-001
title: "Periodic and Milestone Billing Plans"
area: billing
process_tags: [order-to-cash, billing, billing-plans]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "76-82"
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
  - RVFPLA01
  - rental billing
  - facturación de alquiler
  - billing plan dates customizing
  - fechas del plan de facturación
  - date category date rule billing
  - billing rule fixed amount percentage
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-07
---

# Periodic and Milestone Billing Plans

## Operational Summary
*Billing plans* allow a sales order item's total value to be invoiced across multiple dates rather than as a single billing document. SAP provides two variants: *periodic billing* (equal recurring amounts, used for rental and service agreements) and *milestone billing* (amounts tied to project completion milestones, used in construction and capital goods). A billing plan can be maintained at item level or at header level (header billing plans are assigned to sales document types). Each billing plan date creates a separate billing document.

## Questions This Chunk Answers
- What is a billing plan and what are its two main variants?
- When is periodic billing used versus milestone billing?
- How are billing dates generated in a periodic billing plan?
- What is a milestone in the context of milestone billing and how does it trigger invoicing?
- How do you automate the generation of future billing dates in a periodic plan?
- What parameters are defined in billing plan Customizing?
- How is the billing value for each milestone date determined?
- What happens to already-billed milestone dates if amounts change?

## Definition
A *billing plan* is a schedule of billing dates and amounts attached to a sales document item. Instead of billing the full value at goods issue or order completion, the system distributes billing across predefined dates. Each date represents a billing event that triggers a separate billing document. The billing plan type is determined in Customizing from the item category and billing relevance (billing relevance `I` = relevant for billing plan with order-related billing).

A billing plan can be assigned at header level — header billing plans are directly assigned to sales document types and apply to all items.

## Purpose in the SD Process
Billing plans decouple the billing trigger from goods movement, enabling revenue recognition aligned with contractual milestones or calendar periods. They are used in long-duration contracts such as rental, maintenance, construction projects, and capital goods.

## Structure and Variants

### 1. Periodic Billing
Used for repeating billing over a fixed period — common for rental contracts and service agreements.
- Start date and end date define the billing duration. If duration is unlimited, no end date must be set.
- A *horizon* defines how far in advance future billing dates are generated in the billing plan.
- New dates can be created directly in the billing plan or by running report *RVFPLA01*. **RVFPLA01 must be scheduled at regular intervals** because future dates are not generated automatically when individual settlement periods are billed.
- Billing dates determine the day of billing — for example, the first or last day of every month.

### 2. Milestone Billing
Used in plant engineering and construction to spread billing of a large total amount across project completion events.
- Each billing plan date is linked to a *milestone* in a network (PS module) with planned and actual project data.
- The milestone date acts as a billing block until the milestone is confirmed as completed in the project.
- **Control options per billing date:**
  - Whether the billing date is a fixed date
  - Whether the billing date updates to the actual milestone completion date
  - Whether the date updates with the actual date only if production is completed before the planned billing date

**Billing rule** per date: determines how the value to be billed is calculated. Options include a fixed amount, a percentage of the total amount, or whether the amount constitutes a final invoice that also includes previously unbilled dates.

**Changes after billing:** amounts changed after milestone billing documents have been created are distributed among the remaining open billing plan dates. The retro-billed amount for already-created billing documents is included in the final invoice. Once a date has been billed, it cannot be changed in the billing plan.

**Billing index:** the system creates a billing index entry for each billing plan date, meaning milestone billing is processed as order-related billing. When a billing document is created, the status of the billing plan date is updated.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order Item | Billing plan at item level; item category must support billing plans (billing relevance I) |
| Header Billing Plan | Assigned to sales document type; applies to all items unless item-level plan overrides |
| Project Network (PS) | Milestone billing: each date linked to a PS milestone; milestone confirmation unblocks the date |
| Billing Document | Each due billing plan date generates a separate billing document via document flow |
| Down Payment | Milestone billing with billing type FAZ enables down payment requests; delivery block can be assigned in date proposal of billing plan type for milestone down-payments |

## Billing Plan Customizing

| Customizing element | Purpose |
|---|---|
| *Billing plan type* | Determined from item category + billing relevance I; controls periodic vs. milestone behavior |
| *Date description* | Text for billing dates (e.g., 0003 = contract completion, 0005 = assembly); informational only |
| *Date category* | Controls billing rule, fixed date flag, and billing block at date level |
| *Date rule* | Defines the basis date and period calculation for start, end, and billing dates (e.g., 2 days before end of month) |
| *Date proposal* | Used for milestone billing only; defines a sequence of dates used as reference during order processing |

## Cross-References
- Next step: billing-down-payment-processing-001
- See also: billing-installment-payments-001
- See also: configuration-billing-relevance-item-category-001
- See also: order-management-value-contracts-001
