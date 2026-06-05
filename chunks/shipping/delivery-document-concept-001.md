---
schema_version: 1
id: shipping-delivery-document-concept-001
title: "Delivery Document in SAP SD — Concept and Types"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "9-12"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivery document
  - documento de entrega
  - outbound delivery
  - entrega de salida
  - inbound delivery
  - entrega de entrada
  - Logistics Execution
  - LE
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Delivery Document in SAP SD — Concept and Types

## Operational Summary
The *delivery document* is the central object of *Logistics Execution* (LE) in SAP S/4HANA. It represents the physical execution of a goods movement — outbound to customers, inbound from vendors, or transfers between plants. There are three main types depending on the business process they support.

## Questions This Chunk Answers
- What is *Logistics Execution* in SAP S/4HANA?
- What is a delivery document and what is it used for?
- What is the difference between an outbound delivery, an inbound delivery, and a transfer delivery?
- In which processes is a delivery document used?

## Definition
*Logistics Execution* (LE) provides the functions required to execute all logistics processes — goods receipts and goods issues — regardless of industry or sector. LE connects procurement and distribution processes, whether internal or involving third parties (vendors, customers, service providers).

The *delivery document* is the SAP document that manages these movements. It serves as the basis for warehouse activities (picking, packing, putaway, *warehouse order* creation) and for the accounting posting of the goods movement (*Goods Issue* or *Goods Receipt*).

> The *warehouse order* is the document used to execute all physical material movements in the EWM warehouse.

## Purpose in the SD Process
Delivery documents manage the outbound (goods issue) and inbound (goods receipt) movement of goods. Depending on the business process, the document takes a different type.

## Structure and Variants

### Outbound Delivery
Referenced to a sales order. Represents the outbound shipment of goods to a customer. Serves as the basis for picking, packing, document printing, and *Goods Issue* posting.

### Inbound Delivery
Referenced to one or more purchase orders (full or partial quantities). Represents the receipt of goods from a vendor. Serves as the basis for packing, putaway, *warehouse order* creation, and *Goods Receipt* posting.

### Transfer Delivery (Stock Transfer Order)
When a company transfers stock between two of its own plants, the receiving plant creates a purchase order against the supplying plant. The supplying plant creates a delivery document referencing that purchase order. The delivery serves as the basis for picking, packing, and *Goods Issue* posting.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order | Reference document for the outbound delivery |
| Purchase Order | Reference document for the inbound delivery or transfer |
| *Warehouse Order* (EWM) | Created from the delivery to execute physical movements in the warehouse |
| *Goods Issue* / *Goods Receipt* | Posted with reference to the delivery; decreases or increases stock |
| Invoice | Created with reference to the outbound delivery after *Goods Issue* |

## Note on EWM
As of SAP S/4HANA 1610, *SAP Extended Warehouse Management* (EWM) functions are available in the core system. Legacy *Warehouse Management* (WM) remains available, but all future development is focused exclusively on EWM.

## Cross-References
- Internal document structure: shipping-delivery-document-structure-001
