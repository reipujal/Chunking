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
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "31-34"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - item category billing relevance
  - relevancia de facturación tipo de posición
  - billing relevance
  - relevancia para factura
  - delivery-related billing
  - facturación basada en entrega
  - order-related billing
  - facturación basada en pedido
  - TAN item category
  - tipo de posición TAN
  - service billing
  - facturación de servicios
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Billing Relevance and Item Category in SAP SD

## Operational Summary
The *billing relevance* setting in the item category determines whether an item is billed from an outbound delivery or directly from the sales order, and what quantity is used as the billing basis. Delivery-related billing is standard for physical goods; order-related billing is typical for services where no delivery is created. The proposed billing type for a sales order comes from the sales document type configuration.

## Questions This Chunk Answers
- Does the system bill based on the outbound delivery or the sales order?
- Where is billing relevance configured — in the item category or somewhere else?
- What is the difference between order-related and delivery-related billing?
- When is order-related billing used instead of delivery-related billing?
- Can the billing type proposed by the system be changed by the user?
- What item category is used for standard delivery-related billing?

## What This Configuration Controls
The *billing relevance* field in the item category Customizing determines:
- **The reference document for billing**: delivery or order
- **The billing quantity**: which quantity field drives the invoice amount
- **Whether billing is even possible**: items with no billing relevance configured cannot be billed

## SPRO Path or Direct T-code
Sales and Distribution → Sales → Sales Documents → Sales Document Item → Define Item Categories
(Field: *Billing Relevance* in the item category settings)

The proposed billing type for the overall sales document comes from:
Sales and Distribution → Sales → Sales Documents → Sales Document Types
(Field: *Billing type* in the sales document type)

## Key Parameters

| Billing Paradigm | Reference Document | Typical Use Case |
|---|---|---|
| Delivery-related billing | Outbound delivery | Physical goods; billing quantity = delivered quantity minus already billed |
| Order-related billing | Sales order | Services (consulting, carpet laying); no outbound delivery created; billing quantity = order quantity |

Standard item category for delivery-related billing: **TAN** (standard sales order item).

The system proposes the billing type from the sales document type (e.g., standard order OR → billing type F2). Users can override the proposed billing type when creating billing documents by entering a different type in the default data.

## Configuration Impact
Setting the wrong billing relevance leads to billing failures: items configured for delivery-related billing cannot be billed without a posted delivery; items for order-related billing may be billed before goods are shipped (which may not be the business intent). For service scenarios, order-related billing eliminates the need for a delivery, simplifying the process but requiring that goods issue is not a prerequisite for revenue recognition.

## Common Configuration Errors

**Item does not appear in the billing due list**
→ Billing relevance is blank or set to "not relevant" in the item category. Set the correct relevance value.

**Billing attempted but "goods issue not posted" error**
→ Item is set to delivery-related billing, which requires GI. Either post goods issue or change to order-related billing if appropriate for the business process.

**Order-related service item billed too early**
→ Order-related billing does not wait for delivery/GI. Add a copying requirement (via VOFM) to enforce a prerequisite before billing if business rules require it.

## Cross-References
- See also: configuration-billing-types-sap-s4hana-001
- See also: configuration-billing-copying-control-001
- See also: configuration-delivery-item-category-001
