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
    pages: "58-60"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - External Billing Document Requests
  - EBDRs
  - convergent billing
  - omnichannel
  - facturación convergente
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
*Convergent billing* is the process of billing different types of SD documents together into a single invoice. *Omnichannel convergent billing* further extends this by permitting the convergence of internal SAP billing data (like standard deliveries) with External Billing Document Requests (EBDRs) originating from external systems into one unified customer invoice.

## Questions This Chunk Answers
- What are External Billing Document Requests (EBDRs)?
- How does omnichannel convergent billing facilitate solution-centric invoicing?

## Definition and Purpose
A traditional invoice typically bills for a product or a service individually. Today, companies frequently market solution-centric offerings that combine hardware, software licenses, consulting services, and digital usage-based subscriptions (e.g., pay-per-use data via an API). 

To invoice the customer concisely, the system uses *External Billing Document Requests (EBDRs)*. EBDRs act as request objects that successfully transform and persist billing data received from an external source (either external SAP systems or non-SAP systems). The data is frequently uploaded via a predefined Microsoft Excel spreadsheet template (`*.XLSX`). 

## Process Overview
1. Upload external billable data into the SAP S/4HANA system to generate EBDRs.
2. The newly created EBDRs appear directly in the standard SAP billing due list within the *Create Billing Documents* app, seamlessly alongside traditional SD documents like outbound deliveries or sales orders.
3. During the billing process, the system aggregates these disparate internal and external billable units.
4. As long as header convergence criteria match, the system creates a combined, single invoice reflecting all offering components, greatly reducing administrative overhead.
