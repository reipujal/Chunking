---
schema_version: 1
id: order-management-presales-additional-processes-001
title: "Presales Documents, Make-to-Order, and Service Products in SAP SD"
area: order-management
process_tags: [order-to-cash, make-to-order]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "127-134"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - presales documents SAP SD
  - documentos preventa SAP
  - inquiry SAP SD
  - consulta preventa SAP
  - quotation SAP SD
  - oferta SAP SD
  - make-to-order SAP
  - fabricación contra pedido SAP
  - MTO SAP SD
  - service products SAP SD
  - productos de servicio SAP
  - DIEN material type
  - tipo de material DIEN
  - reason for rejection quotation
  - motivo rechazo oferta SAP
  - cómo funciona la preventa en SAP SD
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Presales Documents, Make-to-Order, and Service Products in SAP SD

## Operational Summary
SAP S/4HANA SD supports a range of additional sales scenarios beyond the standard order-delivery-invoice cycle. *Presales documents* (inquiries and quotations) capture pre-order customer interactions and feed into the sales document flow without being mandatory steps. *Make-to-order* (MTO) production links a specific sales order item directly to a production order, ensuring manufactured goods are assigned to the customer who ordered them. *Service products* use a dedicated material type (DIEN) that bypasses logistics and bills directly from the sales order, skipping the delivery step entirely.

## Questions This Chunk Answers
- What are inquiries and quotations in SAP SD, and when are they used?
- Is it mandatory to create a quotation before a sales order?
- How are rejected quotation items handled and why is the reason for rejection important?
- How does make-to-order production work and how does it differ from standard stock-based order processing?
- What makes a service product different in SAP SD, and which material type and item category group are used?

## When It Applies and Context
These three process variants apply to sales scenarios outside the standard order-to-cash cycle. Presales processing applies when a company engages customers before placing a binding order. Make-to-order applies when materials are not kept in general stock but produced exclusively for a specific customer demand. Service products apply when the sale involves non-physical deliverables (consulting, maintenance, support) that require no warehouse or shipping steps.

## Process Flow

### Presales Documents

#### Purpose
During the presales phase, companies may conduct marketing campaigns, attend trade fairs, and have sales representatives visit customers before any binding order is placed. SAP SD supports these activities through two document types:
- *Inquiry*: a non-binding request from a customer for information about pricing, delivery dates, or availability
- *Quotation*: a formal offer from the company to the customer, created with or without reference to an inquiry

**Important**: the use of inquiries and quotations is not mandatory for the sales process. A standard order can be created directly without any presales document. Companies that sell through high-volume, repetitive channels typically skip presales documents.

#### Document Flow in the Presales Phase
When an inquiry is received, the sales team can create a quotation with reference to the inquiry. The inquiry is then completed by the first such reference (standard Customizing behavior). When the customer subsequently places an order, it is created with reference to the quotation, pulling prices and quantities from the quoted document.

This creates a traceable document flow: inquiry → quotation → sales order, which SAP records in the *document flow* of each document.

#### Status Management and Reason for Rejection
Not all inquiries lead to quotations, and not all quotations lead to orders. Reasons for failure include:
- Requested delivery date cannot be met
- Customer disagrees with the offered price and purchases from a competitor

Open presales documents remain in the system and can be closed using a *reason for rejection*. The available reasons (for example, "Too expensive," "Delivery date too late," "Unreasonable request") are defined in Customizing.

Items with a reason for rejection are **not copied to billing documents** (they cannot trigger invoicing) but remain in the system for statistical and analytical purposes. This stored information feeds into win/loss analysis and helps shape future sales strategies.

When reviewing a credit/debit memo request, unjustified complaints are also handled by assigning a reason for rejection, which prevents the item from being forwarded to billing.

### Make-to-Order Production (MTO)

#### Concept
*Make-to-order* production is characterized by manufacturing goods exclusively to satisfy a specific customer order, rather than producing for stock. The key distinction from standard (make-to-stock) processing is that the manufactured quantity is linked to the sales order and cannot be redirected to another customer's order.

#### MTO Process Steps
1. A standard sales order is created; the relevant item is flagged for MTO.
2. An *individual customer requirement* is generated from the sales order item and transferred to *material requirements planning* (MRP).
3. MRP generates a *planned order* for the material automatically, also determining *dependent requirements* using the relevant bill of material (BoM) for sub-components.
4. Planned orders for components are also created based on the dependent requirements.
5. When production is ready to begin, the planned order for the final product is converted to a *production order*.
6. After conversion, the system transfers the confirmed quantity and the new *material availability date* from the production order back to the sales order *schedule line*.
7. When the delivery due date arrives, the goods are picked from *sales order stock* (a separate stock category exclusive to this order), and the goods issue is posted, reducing the MTO stock.

#### Key Characteristics of MTO
- Net requirements are calculated **individually per sales order**: stock cannot be transferred between sales orders to satisfy a different customer's requirement
- Planned and production orders maintain a direct reference to the originating sales order throughout the production process
- Goods are posted to *sales order stock* upon goods receipt, keeping them reserved for the specific customer

### Service Products

#### Definition
Service products represent non-physical goods such as consulting services, maintenance, support contracts, or installation work. Because no physical goods are stored or shipped, the logistics execution steps (delivery creation, picking, goods issue) are not needed.

#### Material Master Configuration for Service Products
Service products are configured using:
- **Material type DIEN**: designed specifically for services; the system suppresses logistics-relevant data fields (warehouse management views, storage conditions) that are irrelevant for services. Only sales-relevant data is required.
- **Item category group LEIS**: maintained in the Sales: Sales Org. Data 1 view of the DIEN material master. This item category group drives the determination of the correct item category for service items in sales documents.

The item category determined for DIEN/LEIS combinations is configured in Customizing to set the item as *not delivery-relevant* and *order-related billing relevant*, enabling direct billing from the sales order.

#### Billing Flow for Service Products
Because no delivery is required, the service item in the sales order can be billed directly: the billing document is created with reference to the sales order, not to an outbound delivery. This shortens the process cycle and eliminates the need for warehouse or logistics involvement.

## Cross-References
Prior step: order-management-sales-order-source-of-data-001
See also: configuration-sales-item-category-control-001 (item category determination for DIEN/LEIS)
See also: configuration-sales-document-type-control-001 (sales document types for inquiries and quotations)
See also: configuration-billing-relevance-item-category-001 (order-related billing relevance for service items)
See also: order-management-sales-distribution-process-001 (standard order-to-cash flow that MTO extends)
