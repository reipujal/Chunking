---
schema_version: 1
id: configuration-billing-relevance-item-category-001
title: "Billing Relevance and Item Category in SAP SD"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "23-26"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - item category
  - tipo de posición
  - billing relevance
  - relevancia para factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
The relevance for billing dictates whether a transaction should be invoiced based on the delivery or directly from the sales order. This behavior is determined in Customizing at the *item category* level.

## Questions This Chunk Answers
- Does the system bill based on the outbound delivery or the sales order?
- Where is the relevance for billing configured?

## What This Configuration Controls
In Customizing for the *item category* (for example, item category TAN), you configure the billing relevance to determine how an item is billed. 

There are two primary paradigms:
1. **Delivery-Related Invoices**: You create the invoice with reference to an outbound delivery. This ensures that goods have already been physically shipped before the customer is invoiced (e.g., delivering a physical product).
2. **Order-Related Invoices**: You create the invoice with reference directly to the sales order. This is typically used for services rendered (e.g., consulting or laying a carpet), where an outbound delivery is not usually created.

The system proposes the relevant billing type from the underlying sales document type. For example, in typical delivery-related billing, a standard order (order type OR) uses billing type F2. You are allowed to change the proposed billing type when physically creating the billing documents by entering it in the default data.
