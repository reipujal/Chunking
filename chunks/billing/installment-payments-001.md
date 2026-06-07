---
schema_version: 1
id: billing-installment-payments-001
title: "Installment Payments in SAP SD"
area: billing
process_tags: [order-to-cash, billing, billing-plans]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "89"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - installment payment
  - pago a plazos
  - cuotas de pago
  - installment billing
  - facturación en cuotas
  - payment terms installment
  - condiciones de pago a plazos
  - split receivable
  - fraccionamiento de deuda
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Installment Payments in SAP SD

## Operational Summary
An *installment plan* lets a customer pay for a single invoice in multiple periodic installments rather than one lump sum. Unlike a *milestone billing plan* (which creates multiple billing documents over time), an installment plan generates exactly **one** SD billing document. The installment schedule is reflected in Financial Accounting, where multiple receivable line items — one per installment — are automatically created within that single accounting document.

## Questions This Chunk Answers
- How many billing documents are created for an installment plan?
- What is the difference between an installment plan and a milestone billing plan?
- Where are installment payment terms defined in Customizing?
- How does the system generate multiple FI line items from a single billing document?
- Is the installment schedule visible on the printed invoice?

## Definition
An *installment payment plan* is a payment terms configuration that divides the total billing amount into a schedule of partial payments due on specific future dates. The configuration lives in the payment terms Customizing, not in the billing plan structure. From the SD perspective, billing generates one document; FI splits it into the defined installment line items automatically.

## Purpose in the SD Process
Installment plans enable deferred payment without the complexity of milestone billing. They are used when the goods or service is delivered in full upfront but the customer pays in portions. The printed invoice shows the total amount and the installment schedule, giving the customer clarity on payment obligations.

## Structure and Variants
- **One billing document** in SD (unlike milestone billing, which creates one per date).
- **Multiple FI line items** — one per installment, each with its own due date and partial amount.
- The installment percentages and due dates are defined in Customizing for **payment terms**.
- The printed invoice output shows the full total along with the schedule of installments and their individual amounts.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Payment Terms | Installment schedule defined in payment terms Customizing; assigned to the billing document |
| FI Accounting Document | One FI document with N line items (one per installment), each with its own due date |
| Billing Plan | Conceptually different: billing plan creates multiple SD billing documents; installment plan creates one SD document with multiple FI items |
| Customer Master | Default payment terms carried from customer master into the order/billing document |

## Cross-References
- Prior step: billing-billing-plans-concept-001
- See also: billing-down-payment-processing-001
