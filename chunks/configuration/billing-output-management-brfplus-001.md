---
schema_version: 1
id: configuration-billing-output-management-brfplus-001
title: "Output Management for Billing Using BRFplus"
area: configuration
process_tags: [order-to-cash, billing, output-management]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "105-106"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - BRFplus
  - output management
  - gestión de mensajes
  - NAST
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
In SAP S/4HANA, the legacy NAST-based output determination framework is supplanted by the modern SAP S/4HANA Output Management framework powered natively by Business Rule Framework Plus (BRFplus). 

## Questions This Chunk Answers
- What replaces the NAST table for output management in S/4HANA?
- How are output parameters determined dynamically?

## S/4HANA Output Management vs Legacy NAST
Historically traversing the condition technique mapped to the `NAST` table, output management has shifted firmly to BRFplus. (Note: NAST can hypothetically still be enabled via a specific Customizing parameter if needed during transitions).

The primary architecture natively supports print, e-mail, XML, and IDoc (for on-premise deployments) channels only. Adobe XFA operates as the default technology for form templates, although legacy formatting systems (SAPscript, SmartForms, Adobe Forms) are still technically supported.

### Benefits of BRFplus Output Management
- **Extensibility**: Broad adoption and usage of CDS views.
- **Unified solution**: A singular solution enveloping SD, MM, FIN, etc.
- **Fiori Integration**: Full graphical integration into SAP Fiori apps.
- **State-of-the-art e-mail support**: Superior configuration encompassing multiple recipients and HTML e-mail templates.

## Decision Tables
Within BRFplus, dedicated *Decision Tables* replace the old condition records. The system utilizes these tables securely to determine fundamental output parameters corresponding to rules: output type, receiver, print queue, and form template.
Every row is processed intelligently in sequence. The system evaluates the condition columns from left to right; if the conditional logic is met, the values strictly defined in the subsequent result columns are returned definitively to orchestrate the output.
