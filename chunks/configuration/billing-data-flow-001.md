---
schema_version: 1
id: configuration-billing-data-flow-001
title: "Data Flow and Reference Documents in Billing"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "41-43, 45"
    source_type: "A"
    role: "primary"
transactions: [VOFM]
tables: []
aliases:
  - data flow billing
  - flujo de datos facturación
  - reference document billing
  - documento de referencia facturación
  - VOFM
  - data transfer routine
  - rutina de transferencia de datos
  - billing reference
  - referencia de factura
  - copying requirements
  - requisitos de copia
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Data Flow and Reference Documents in Billing

## Operational Summary
Every billing document (except external transactions) requires a reference document from which it copies data. The rules governing what data is copied, at what level (header or item), and under what conditions are defined in *copying control*. Data transfer can be further customized using *data transfer routines* created or modified with transaction *VOFM*.

## Questions This Chunk Answers
- What types of documents can be used as references for billing?
- How does the system determine what data to copy from the reference into the billing document?
- What is the difference between copying requirements and data transfer routines?
- Can the terms of payment in the billing document differ from the sales order?
- Where is pricing behavior during copy (pricing type) configured?
- What transaction is used to create custom data transfer routines?

## Definition
*Billing data flow* describes the mechanism by which an SD billing document inherits its content from a preceding SD document. The reference document provides the commercial and logistics data; copying control rules and data transfer routines control exactly which fields are populated, which are recalculated, and which are excluded.

## Purpose in the SD Process
Without a structured data flow mechanism, each billing document would require manual data entry — replicating partner data, pricing, and quantities from upstream documents. Copying control ensures that billing faithfully reflects the agreed commercial terms while allowing controlled exceptions (e.g., re-pricing, date recalculation, payment term override).

## Structure and Variants

### Reference Document Types
| Reference Document | Billing Use Case |
|---|---|
| Sales document or delivery | Standard invoices (F2), pro forma invoices |
| Credit/debit memo request | Credit memos (G2), debit memos (L2) |
| Returns document | Returns credit memos |
| Invoice correction request | Credit memos for invoice corrections |
| Billing document | Cancellation documents, invoice lists |
| External transaction | External billing (general billing interface) |
| Delivery | Intercompany billing |
| Rebate request | Rebate credit memos |

### Data Controls at Header Level
- **Reference document**: which documents can be used as billing references.
- **Determination**: foreign trade data, allocation numbers, reference numbers, item number assignment.

### Data Controls at Item Level
- **Billing quantity**: order quantity minus billed, delivery quantity minus billed, or others (see `configuration-billing-copying-control-001`).
- **Pricing behavior**: copy unchanged, re-determine, or selectively update (pricing type A/B/C/D/G/H).
- **Price source**: can copy shipment costs from a shipment cost document.

### Custom Routines (VOFM)
Data transfer routines can be customized using transaction *VOFM* to handle individual requirements. For example, a routine can copy terms of payment from the customer master instead of adopting them from the preceding sales document.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Copying Control | The primary configuration object that references these data control settings |
| Billing Document | Destination of the copied data |
| Reference Document | Source of data (order, delivery, previous billing document) |
| VOFM | Transaction for creating/modifying data transfer and copying requirement routines |

## Cross-References
- See also: configuration-billing-copying-control-001
- See also: billing-billing-document-creation-methods-001
- See also: billing-pro-forma-invoice-001
