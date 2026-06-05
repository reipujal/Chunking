---
schema_version: 1
id: shipping-delivery-special-functions-001
title: "Special Functions in Outbound Deliveries — Pricing, Interface, and Incompletion Control"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    relative_path: "S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf"
    pages: "84-87"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - pricing outbound delivery
  - precios entrega de salida
  - freight costs delivery
  - costes de flete entrega
  - delivery interface
  - interfaz de entrega
  - IDoc DELVRY07
  - EDI delivery
  - ALE delivery
  - incompletion control
  - control de compleción
  - log of incomplete items
  - log de posiciones incompletas
  - delivery conditions
  - condiciones de entrega
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Special Functions in Outbound Deliveries — Pricing, Interface, and Incompletion Control

## Operational Summary
Beyond the standard pick-pack-ship flow, outbound deliveries support three additional functional areas: (1) **pricing** for shipping-related charges (freight, handling); (2) a **delivery interface** for exchanging EDI and ALE messages with external partners and systems; and (3) **incompletion control** to detect missing mandatory data before follow-on activities are executed.

## Questions This Chunk Answers
- Can freight or shipping costs be calculated in the outbound delivery?
- Can pricing conditions be transferred from the sales order to the delivery?
- How does the delivery communicate with external systems or business partners?
- What is incompletion control and how does it work?
- Which fields can be configured as mandatory in a delivery?

## Definition
These functions extend the operational capabilities of the outbound delivery document beyond the core logistics flow, enabling cost capture, system integration, and data quality enforcement within the delivery process.

## Purpose in the SD Process

### 1 — Pricing in the Outbound Delivery
The outbound delivery can contain shipping-related conditions such as freight costs, postage, or handling charges.

Key points:
- Condition values can be entered **manually** or determined via the **SD pricing condition technique**.
- Conditions can be **printed on the delivery note** and **transferred to the billing document**.
- Conditions **cannot be transferred from preceding documents** (sales order or purchase order) to the outbound delivery — freight conditions must be maintained on the delivery directly.
- Configuration: use standard pricing Customizing (define condition types, maintain pricing procedure) and assign the pricing procedure to the delivery type.

### 2 — Delivery Interface (EDI / ALE)
When business partners are involved in shipping or when non-SAP systems perform certain functions, the delivery interface manages electronic message exchange.

| Communication Type | Protocol | Use Case |
|---|---|---|
| External communication | EDI (Electronic Data Interchange) | Vendor notifications, carrier messages, ASNs |
| Internal communication | ALE (Application Link Enabling) | Communication between SAP systems |

All EDI and ALE messages related to the delivery are based on **IDoc DELVRY07** — the data structure containing segments for delivery fields and shipping-related data (route, batch characteristics, etc.). Output control at the **delivery header level** triggers the filling of IDoc fields. The system provides standard message types for common communication scenarios.

### 3 — Incompletion Control
The incompletion log checks whether all required data in the outbound delivery is present. It can be triggered:
- From within delivery processing (manually called during document editing)
- Via a special report that generates a **worklist of incomplete deliveries** for collective review

The log operates at both **header level** and **item level**. If mandatory fields are missing, the log flags the document and can prevent follow-on activities (e.g., picking blocked if item volume is missing; packing blocked if weight is missing).

Configurable per **delivery type** and **delivery item category**:
- Which fields cause a delivery to be incomplete
- What effect missing fields have on subsequent activities (picking, packing, goods issue, billing)
- **Partner functions** can be set as "Required" — if a required partner is missing, the incompletion log flags it
- **Texts** can also be set as required

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Delivery Type | Pricing procedure assigned here; incompletion checks configured per delivery type |
| Delivery Item Category | Incompletion checks also configured at item category level |
| Billing Document | Delivery pricing conditions transferred to billing |
| IDoc DELVRY07 | Carrier and output message types for delivery EDI/ALE |
| Output Condition Record | Controls when, how, and to whom output is sent |

## Cross-References
- Delivery type configuration: configuration-delivery-type-001
- Delivery item category: configuration-delivery-item-category-001
- Output in shipping (condition technique): shipping-outbound-delivery-creation-process-001
- EWM picking (uses delivery data): shipping-ewm-picking-process-001
