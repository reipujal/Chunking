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
  - installment plan billing
  - facturación en plazos
  - billing plan dates
  - fechas del plan de facturación
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Periodic and Milestone Billing Plans

## Operational Summary
*Billing plans* allow a sales order item's total value to be invoiced across multiple dates rather than as a single billing document. SAP provides two variants: *periodic billing* (equal recurring amounts, used for rental and service agreements) and *milestone billing* (amounts tied to project completion milestones, used in construction and capital goods). The billing plan is maintained at item level in the sales order and drives automatic date generation for billing.

## Questions This Chunk Answers
- What is a billing plan and what are its two main variants?
- When is periodic billing used versus milestone billing?
- How are billing dates generated in a periodic billing plan?
- What is a milestone in the context of milestone billing and how does it trigger invoicing?
- How do you automate the generation of future billing dates in a periodic plan?
- What parameters are defined in billing plan Customizing?

## Definition
A *billing plan* is a schedule of billing dates and amounts attached to a sales order item. Instead of billing the full item value when the order ships, the system distributes billing across predefined dates according to a plan. Each date represents a billing event that creates a separate billing document.

## Purpose in the SD Process
Billing plans enable complex invoicing arrangements for long-duration contracts and project business. They decouple the billing trigger from the goods movement, allowing revenue recognition aligned with contractual milestones or calendar periods rather than physical delivery events.

## Structure and Variants

### 1. Periodic Billing
Used for repeating, equal-amount billing over a fixed period — common for rental contracts, maintenance agreements, and subscription services.
- Defined by a start date, end date, and *horizon* (how far in advance dates are pre-generated).
- Each date generates a billing document for the full predetermined amount.
- To automatically generate future dates once the horizon is reached, schedule report *RVFPLA01* to run at regular intervals.

### 2. Milestone Billing
Used in plant engineering and construction to spread the billing of a large total amount across project completion events.
- Each billing plan date is linked to a *milestone* in a project network (PS module).
- The milestone date acts as a **billing block** until the milestone is confirmed as completed in the project.
- Value distribution: assign percentages or fixed amounts per milestone. Manual adjustments automatically redistribute remaining values across open milestones.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order Item | Billing plan maintained at item level; item category must support billing plans |
| Project Network (PS) | Milestone billing: each billing date linked to a PS milestone; completion confirms the date |
| Billing Document | Each due billing plan date generates a separate billing document |
| Billing Plan Customizing | Date descriptions, date categories, and date rules configured in Customizing |
| Down Payment | Milestone billing combined with billing type FAZ enables down payment requests |

## Cross-References
- Next step: billing-down-payment-processing-001
- See also: billing-installment-payments-001
- See also: configuration-billing-relevance-item-category-001
