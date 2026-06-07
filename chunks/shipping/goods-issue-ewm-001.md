---
schema_version: 1
id: shipping-goods-issue-ewm-001
title: "Goods Issue Posting in EWM — Process and Delivery Split"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "77"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - goods issue EWM
  - salida de mercancías EWM
  - EWM outbound delivery
  - entrega de salida EWM
  - delivery split
  - división de entrega
  - partial goods issue
  - salida de mercancías parcial
  - staging area
  - zona de preparación
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Goods Issue Posting in EWM — Process and Delivery Split

## Operational Summary
Once picking is complete and goods are at the goods issue zone, the *Goods Issue* (GI) is posted. In an EWM-managed warehouse, GI posting creates an **EWM outbound delivery** document that sends the GI information back to the LE outbound delivery, which in turn generates the inventory management and financial accounting documents. A key constraint is that GI against an LE outbound delivery must be for the **full quantity** — partial GI is not possible directly. For partial scenarios, the EWM outbound delivery triggers a **delivery split**.

## Questions This Chunk Answers
- How is Goods Issue triggered in an EWM warehouse?
- What documents does GI posting create?
- Why does EWM create an additional outbound delivery document?
- What happens when only part of a delivery can be shipped (partial GI)?

## When It Applies and Context
GI posting is the step that legally transfers ownership of goods to the customer and reduces warehouse stock. It is the prerequisite for invoice creation. This process applies when picking and warehouse activities are managed through embedded EWM.

## Process Flow

### 1 — Trigger Goods Issue
GI posting can be triggered in three ways:
1. **Manually** from the outbound delivery order in EWM
2. **Automatically** when materials reach the staging area
3. **Automatically** when the truck carrying the materials leaves the warehouse

### 2 — EWM Outbound Delivery Created
For GI in an EWM-managed warehouse, an **EWM outbound delivery** document is created. This document serves as the interface between EWM and Logistics Execution:
- Sends GI confirmation information back to the LE outbound delivery
- Is the document against which the actual GI posting is made

### 3 — Downstream Documents
The GI posting via the LE outbound delivery generates:
- **Inventory management document** (stock reduced)
- **Financial accounting documents** (COGS posting, balance sheet update)

### 4 — Partial GI and Delivery Split
Posting GI against an LE outbound delivery requires the **full quantity** of all items — partial GI is not possible. Partial scenarios arise when:
- Physical stock in the warehouse is less than the system shows
- Transport capacity is insufficient for the full quantity

In these cases, a **delivery split** is triggered through the EWM outbound delivery. The original LE outbound delivery is split into two: one for the quantity that can be shipped now, and one for the remainder.

## Conditions and Restrictions
- GI must be for the full quantity of the LE outbound delivery — no direct partial posting.
- The EWM outbound delivery is always created at GI time in an EWM-managed warehouse.
- Automatic GI trigger (staging area / truck departure) requires additional EWM configuration.

## Cross-References
- EWM picking process (precedes GI): shipping-ewm-picking-process-001
- Cancellation of Goods Issue via VL09: chunk not yet created — pending SD-Shipment.pdf processing
- Inbound delivery and GR in EWM: shipping-inbound-delivery-ewm-001
- See also: shipping-cash-sales-process-001
