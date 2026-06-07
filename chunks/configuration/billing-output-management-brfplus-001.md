---
schema_version: 1
id: configuration-billing-output-management-brfplus-001
title: "Output Management for Billing Using BRFplus"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "113-114"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - BRFplus output management
  - gestión de mensajes BRFplus
  - NAST replacement
  - sustitución NAST
  - output management S/4HANA billing
  - gestión de salidas facturación S/4HANA
  - decision table output
  - tabla de decisión salida
  - billing output determination
  - determinación de salida facturación
  - Adobe XFA billing
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Output Management for Billing Using BRFplus

## Operational Summary
In SAP S/4HANA, the legacy NAST-based output determination (condition technique + NAST table) for billing is replaced by the *SAP S/4HANA Output Management* framework, powered by *Business Rule Framework Plus (BRFplus)*. Output parameters (type, recipient, print queue, form template) are determined using *Decision Tables* in BRFplus rather than condition records in NAST. Adobe XFA is the default form technology, though legacy formats (SAPscript, SmartForms, Adobe Forms) remain technically supported. NAST can still be enabled via a specific Customizing parameter during transition periods.

## Questions This Chunk Answers
- What replaced NAST for output management in SAP S/4HANA billing?
- How are output parameters determined in the BRFplus output framework?
- Can NAST still be used in S/4HANA?
- What output channels does S/4HANA Output Management support natively?
- What are Decision Tables and how do they work?
- What form technology is used by default in S/4HANA output management?

## What This Configuration Controls
The BRFplus output management framework controls:
- **When** output is triggered (billing document creation, save, release to accounting)
- **How** output is delivered (print, e-mail, XML, IDoc)
- **To whom** output is sent (partner functions, e-mail addresses)
- **What form** is used (Adobe XFA template, SmartForms, etc.)
- **Print queue** assignment

## SPRO Path or Direct T-code
Sales and Distribution → Billing → Billing Documents → Output Determination for Billing Documents
(S/4HANA Output Management framework — BRFplus configuration accessed via the Fiori *Output Management* app or transaction BF_WORKBENCH)

Note: the legacy NAST Customizing path remains available if NAST is explicitly re-enabled via SAP Note 2267376.

## Key Parameters

### Supported Output Channels (Native)
| Channel | Description |
|---|---|
| Print | Standard printer output |
| E-mail | HTML e-mail with multiple recipients; superior to NAST e-mail |
| XML | Structured data output |
| IDoc | For on-premise system integrations |

### Decision Table Logic
- Replaces NAST condition records.
- Each row specifies condition columns (evaluated left to right) and result columns (output type, receiver, print queue, form template).
- The first matching row determines the output parameters.
- CDS views are used for extensibility.

### Benefits of BRFplus vs. NAST
- Unified framework across SD, MM, FIN.
- Full Fiori integration.
- Superior e-mail capabilities (HTML templates, multiple recipients).
- Extensible via CDS views.

## Configuration Impact
If BRFplus output management is active but Decision Tables are not configured for a billing type, no output (invoice PDF, e-mail) is generated at billing creation. This is a silent failure — the billing document is created and posted, but no customer-facing document is produced. Migration from NAST to BRFplus requires maintaining equivalent Decision Table rows for each NAST condition record.

## Common Configuration Errors

**No output generated after billing document creation**
→ No matching row in the BRFplus Decision Table for the billing document's attributes. Verify that the Decision Table covers the relevant billing type, sales organization, and output channel combination.

**Legacy NAST condition records exist but have no effect**
→ The system is running in BRFplus mode. NAST condition records are ignored unless NAST is re-enabled via Customizing. Migrate to Decision Tables.

**E-mail output sent but attachments missing**
→ The form template referenced in the Decision Table is not configured for PDF attachment. Verify the output parameter for the e-mail channel in BRFplus.

## Cross-References
- See also: billing-billing-document-creation-methods-001
- See also: configuration-billing-types-sap-s4hana-001
