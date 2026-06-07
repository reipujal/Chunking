---
schema_version: 1
id: shipping-delivery-document-structure-001
title: "Delivery Document Structure in SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "13-14"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - delivery document structure
  - estructura entrega
  - delivery header
  - cabecera entrega
  - delivery item
  - posición entrega
  - shipment document
  - documento de expedición
  - freight order
  - TM freight order
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Delivery Document Structure in SAP SD

## Operational Summary
The SAP SD delivery document has two levels: header and items. The header groups data common to the entire delivery; items contain the materials to be delivered. The screen is organized into tabstrips by logistics activity type. The delivery document differs from the *shipment document* and the *TM Freight Order* in scope and purpose.

## Questions This Chunk Answers
- How is a delivery document internally organized?
- What data does the header contain, and what data do the items contain?
- What is the difference between a delivery document and a shipment document?
- What is a *TM Freight Order* and when is it used instead of a delivery?

## Definition
The delivery document consists of a header and a variable number of items. The header contains data that applies to the entire delivery. Items contain information about the materials to be delivered.

## Purpose in the SD Process
The document structure supports the complete logistics flow: from determining the shipping point and route, through picking, packing, loading, and finally the *Goods Issue* or *Goods Receipt* posting. Each phase of the process has its own tabstrip in the document.

## Structure and Variants

### Header
Contains data that applies to the entire delivery:
- *Ship-to party* (recipient)
- *Shipping point*
- *Route*

The overview screen displays selected header and item data grouped by activity in tabstrips.

**Header tabstrips:** processing, picking, loading, shipment, foreign trade/customs, texts, partners, document output, package monitoring, conditions.

### Items
Contain information about the materials to be delivered. In the item detail screen, data is also organized into tabstrips similar to the header level.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order | Delivery created with reference; items and quantities inherited |
| *Transfer Order* (WM/EWM) | Created from delivery items to trigger warehouse picking |
| *Goods Issue* | Executed at header level via VL02N; closes the delivery logistically |
| Shipment Document (LE-TRA) | Groups multiple deliveries into one transport unit |
| Invoice | Created with reference to the delivery after GI is posted |

## Delivery vs. Shipment Document vs. TM Freight Order

| Document | Scope | When Used |
|---|---|---|
| Outbound Delivery | One shipping point → one ship-to party along a route | Standard goods issue process |
| *Shipment Document* (LE-TRA) | Groups multiple deliveries into one shipment | Multiple destinations or loading points on the same vehicle (legacy WM) |
| *TM Freight Order* | Groups multiple deliveries with configurable criteria (route, transport requirement) | Multiple shipping points, multiple ship-to parties on the same route (SAP TM) |

> As of SAP S/4HANA 1709, *Transportation Management* is integrated into the core system, progressively replacing the legacy *LE Transportation Management*.

## Cross-References
- Delivery types and general concept: shipping-delivery-document-concept-001
