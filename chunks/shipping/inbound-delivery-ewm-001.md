---
schema_version: 1
id: shipping-inbound-delivery-ewm-001
title: "Inbound Delivery Creation in EWM — Goods Receipt Process"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "79-82"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - inbound delivery EWM
  - entrega de entrada EWM
  - goods receipt EWM
  - entrada de mercancías EWM
  - confirmation control key
  - clave de control de confirmación
  - vendor confirmation
  - confirmación de proveedor
  - advanced shipping notification
  - ASN
  - aviso de expedición avanzado
  - purchase order inbound delivery
  - entrega de entrada pedido de compra
  - putaway EWM
  - colocación en stock EWM
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Inbound Delivery Creation in EWM — Goods Receipt Process

## Operational Summary
For goods receipt in an EWM-managed warehouse, an inbound delivery document must be created referencing the purchase order or manufacturing order. There are three creation paths depending on the information available and the physical process. The inbound delivery drives both the physical putaway in EWM (warehouse tasks) and the goods receipt posting in inventory management. A **confirmation control key** in the purchase order is required to enable inbound delivery creation.

## Questions This Chunk Answers
- How is an inbound delivery created in an EWM warehouse?
- What are the three options for creating an inbound delivery?
- What is the confirmation control key and why is it needed?
- What documents are involved in the goods receipt process with EWM?
- Can the inbound delivery be created directly in EWM without going through LE?

## When It Applies and Context
This process covers goods receipt from external vendors or from other plants (STO). It applies when the receiving storage location is managed by an EWM warehouse number. The inbound delivery is the prerequisite for creating EWM warehouse tasks for putaway and for posting the goods receipt.

## Process Flow

### Source Documents
The purchasing process generates the following documents:
- **Purchase requisition** → request for externally procured material
- **Request for quotation / Quotation** → for new vendors or one-time transactions
- **Purchase order** → formal commitment; can reference a PR or quotation, or be created directly
- **Purchasing info record** → master data for regular vendor + material combinations (price, quantities, delivery times)

Vendor master data (business partner with address, accounting, and default PO values) is required for external vendors.

### Three Creation Paths for the Inbound Delivery

| Path | Trigger | Result |
|---|---|---|
| 1. Automatic from ASN | Vendor sends advance shipping notification (ASN) | LE inbound delivery created automatically; copy replicated to EWM |
| 2. Manual with PO reference | User creates LE inbound delivery manually with reference to the PO | Copy replicated to EWM |
| 3. Direct creation in EWM | User creates inbound delivery directly in SAP EWM | LE inbound delivery created automatically as a side effect |

**Path 3 (direct EWM creation)** is particularly useful when:
- The vendor does not send ASNs or electronic shipping notifications
- Goods arrive at the warehouse and need to be processed immediately without waiting for LE document creation
- A simplified interface (app) is preferred: create delivery + post GR + create warehouse task in one step

### Confirmation Control Key
To enable inbound delivery creation for a purchase order, a **confirmation control key** must be entered in the purchase order.

The confirmation control key defines:
- What types of vendor confirmations are expected (e.g., order acknowledgement, shipping notification, delivery note)
- Whether creating an inbound delivery is required or optional

A **vendor confirmation** is a notification from the vendor about the status of a purchase order. It provides increasingly precise delivery information during the period between PO issuance and the planned delivery date, enabling more accurate procurement planning.

### After Inbound Delivery Creation
The inbound delivery is the basis for:
1. **EWM warehouse tasks** for putaway (placing goods into the correct storage bins)
2. **Goods receipt posting** in inventory management (stock increased, accounting documents created)

## Conditions and Restrictions
- A confirmation control key must be present in the PO for the system to allow inbound delivery creation.
- Path 1 (automatic from ASN) requires the vendor to send a shipping notification message (EDI/IDoc).
- GR posting requires the picking (putaway confirmation) quantity to match the delivery quantity.

## Cross-References
- EWM organizational units (warehouse number, storage bins): enterprise-structure-warehouse-org-units-ewm-001
- EWM picking process for outbound deliveries: shipping-ewm-picking-process-001
- Inbound delivery concept: shipping-delivery-document-concept-001
- Delivery type for inbound (EL) Customizing: configuration-delivery-process-customizing-001
