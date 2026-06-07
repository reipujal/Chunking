---
schema_version: 1
id: billing-pro-forma-invoice-001
title: "Pro Forma Invoices in SAP SD"
area: billing
process_tags: [order-to-cash, billing, pro-forma]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "34-35"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - pro forma
  - proforma
  - factura proforma
  - F5 billing type
  - F8 billing type
  - customs invoice
  - factura de aduana
  - export documentation billing
  - documentación de exportación factura
  - no FI posting invoice
  - factura sin contabilización
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Pro Forma Invoices in SAP SD

## Operational Summary
A *pro forma invoice* is a non-binding draft invoice used primarily for export and customs documentation. It looks like a real invoice but has two critical distinctions: (1) it does **not** update the billing status of the reference document, so it can be created multiple times for the same order or delivery; and (2) it is **never transferred to Financial Accounting** — no FI posting is created. Standard types are *F5* (based on order quantity) and *F8* (based on delivery quantity).

## Questions This Chunk Answers
- What is a pro forma invoice used for?
- Can a pro forma invoice be created before goods issue is posted?
- Does creating a pro forma invoice prevent subsequent billing of the same document?
- Can multiple pro forma invoices be created for the same order?
- What is the difference between billing type F5 and F8?
- Does a pro forma invoice generate an accounting document?

## Definition
A *pro forma invoice* is a formal-looking billing document issued to a customer or customs authority as a preliminary price statement. It contains all the data of a standard invoice (pricing, quantities, materials) but carries no financial consequences — it is purely informational and is used to comply with documentation requirements for export, customs clearance, or internal approvals.

## Purpose in the SD Process
Pro forma invoices serve documentation needs that arise before or alongside the actual commercial invoice:
- **Export**: Customs authorities require a price declaration before clearing goods.
- **Internal approval**: Customers may need to approve the price before formal invoicing.
- **Interim documentation**: Provide a document to accompany the shipment without triggering the revenue posting.

Because they do not update the billing status, pro forma invoices can coexist with subsequent standard billing without double-billing risk.

## Structure and Variants

| Billing Type | Reference | Billing Quantity |
|---|---|---|
| F5 | Order | Order quantity |
| F8 | Outbound delivery | Delivery quantity |

**Key characteristics:**
- Goods issue does **not** need to be posted before creating a delivery-related (F8) pro forma invoice.
- The `Pos./neg. quantity` field is intentionally unavailable in copying control for pro forma invoices, preventing any billing status update on the reference document.
- Multiple pro forma invoices can be created for the same order or delivery without restriction.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order | F5 pro forma created with reference; no billing status change on the order |
| Outbound Delivery | F8 pro forma created with reference; no billing status change on the delivery; no GI prerequisite |
| FI Accounting Document | Never created — no financial posting |
| Standard Invoice (F2) | Can be created independently after the pro forma; both can reference the same order/delivery |
| Copying Control | pos./neg. quantity field intentionally locked for pro forma billing types |

## Cross-References
- See also: billing-billing-document-creation-methods-001
- See also: billing-preliminary-billing-documents-001
- See also: configuration-billing-types-sap-s4hana-001
