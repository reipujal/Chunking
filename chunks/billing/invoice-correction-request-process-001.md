---
schema_version: 1
id: billing-invoice-correction-request-process-001
title: "Invoice Correction Requests in SAP SD"
area: billing
process_tags: [order-to-cash, billing, invoice-correction, complaints]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "24-26"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - invoice correction request
  - solicitud de corrección de factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
An *invoice correction request* represents a combination of credit and debit memo requests. It is used to correct pricing or quantities for a complaint, automatically creating a paired credit and debit item where the net difference represents the final amount to be credited or debited.

## Questions This Chunk Answers
- How does an invoice correction request work?
- How does the system handle quantity or price differences using this process?

## When It Applies and Context
You create an invoice correction request whenever a customer complains about an incorrect invoice due to a quantity discrepancy (e.g., damaged goods) or a pricing error. It must always be created with reference to the corresponding **billing document** (no reference to orders or inquiries).

## Process Flow
1. **Creation**: When you create the invoice correction request, the system automatically duplicates the items. For every item in the reference billing document, it creates two items with opposite (+ and -) signs. First, all credit memo items are listed, followed by all debit memo items.
2. **Adjustment**: 
   - **Credit Item**: Grants full credit for the incorrect billing item. *You cannot change the credit memo item.*
   - **Debit Item**: You update the debit memo item with the new, correct characteristics (e.g., the correct price or the accepted correct quantity).
3. **Calculation**: The difference between the credit item and the adjusted debit item represents the final full amount to be credited to the customer.
4. **Cleanup**: You can delete the credit and debit memos in paired steps using the "Delete unchanged item" function for any lines that required no correction.

## Variants: Quantity vs. Price Differences
- **Quantity Difference**: Used when correcting the quantity (e.g., a certain amount of goods were damaged or substandard). You alter the quantity on the debit memo item.
- **Price Difference**: Used when processing a complaint for incorrect pricing. The correction of the pricing elements is carried out strictly in the debit memo item.
