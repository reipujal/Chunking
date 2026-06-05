---
schema_version: 1
id: billing-omnichannel-convergent-billing-001
title: "Omnichannel Convergent Billing and EBDRs"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "66-68"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - External Billing Document Requests
  - EBDRs
  - EBDR
  - convergent billing
  - facturación convergente
  - omnichannel billing
  - facturación omnicanal
  - external billing interface
  - interfaz de facturación externa
  - solution-centric invoice
  - factura solución integral
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Omnichannel Convergent Billing and EBDRs

## Operational Summary
*Convergent billing* combines different types of SD documents into a single customer invoice. *Omnichannel convergent billing* extends this further by allowing the convergence of internal SAP billing data (standard deliveries, service orders) with *External Billing Document Requests (EBDRs)* from non-SAP or external SAP systems into one unified invoice. EBDRs are uploaded via a predefined Excel template and appear in the standard billing due list alongside traditional SD documents.

## Questions This Chunk Answers
- What are External Billing Document Requests (EBDRs) and how are they created?
- How does omnichannel convergent billing differ from standard billing?
- Can external subscription or usage-based data be billed together with a physical delivery on one invoice?
- How are EBDRs uploaded into the SAP system?
- What controls whether external and internal items are combined into one invoice?

## Definition
*Omnichannel convergent billing* is the capability to invoice a customer for a mix of products and services — some originating from SAP (physical deliveries, services) and some from external systems (subscriptions, usage data, API fees) — in a single, unified billing document. EBDRs are the request objects that transform externally sourced billing data into SAP billing items.

## Purpose in the SD Process
Modern solution-centric businesses sell bundles: hardware, software licenses, consulting, and digital usage-based components. Billing these separately creates complexity for the customer (multiple invoices) and the seller (reconciliation overhead). Convergent billing produces a single, coherent invoice regardless of the source of each component.

## Structure and Variants

### Standard Convergent Billing
Combines different *internal* SD document types (e.g., delivery-related and order-related items from different sales documents) into one invoice, as long as header convergence criteria (payer, billing date) match.

### Omnichannel Convergent Billing with EBDRs
Extends standard convergent billing to include external data:
1. External billing data is prepared and uploaded using a predefined **Microsoft Excel (.XLSX)** template.
2. The upload creates *External Billing Document Requests (EBDRs)* inside SAP S/4HANA.
3. EBDRs appear directly in the standard billing due list alongside traditional SD documents (in the *Create Billing Documents* app).
4. During the billing run, the system aggregates EBDR items with internal SD items and creates a combined invoice — provided the header convergence criteria match.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Billing Due List | EBDRs appear in the same due list as standard deliveries and orders |
| External System | Source of EBDR data (non-SAP systems, external SAP instances) |
| Billing Document | Final output: single invoice combining internal and external billing items |
| Header Convergence Criteria | Control whether EBDRs and SD items can be combined (same payer, date, etc.) |

## Cross-References
- See also: integration-general-billing-interface-001
- See also: billing-billing-document-creation-methods-001
- See also: billing-invoice-combination-and-split-001
