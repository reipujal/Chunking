---
schema_version: 1
id: configuration-output-management-s4hana-001
title: "SAP S/4HANA New Output Management Framework"
area: configuration
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    pages: "65-73"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - SAP S/4HANA Output Management
  - new output management framework
  - BRFplus output determination
  - gestión de salida S/4HANA
  - nuevo framework de gestión de mensajes SAP
  - NAST vs new output management
  - tabla de decisión BRFplus salidas
  - output management BRFplus decision table
  - how does new output management work in S/4HANA
  - KPro output archive SAP
  - Adobe XFA output forms
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# SAP S/4HANA New Output Management Framework

## Operational Summary
SAP S/4HANA introduces a strategic output management framework that replaces the legacy *NAST*-based condition technique approach. The new framework uses *Business Rule Framework Plus (BRFplus)* decision tables — instead of condition records — to determine output parameters. Adobe XFA is the default form technology, though legacy forms (SAPscript, SmartForms, Adobe Forms) remain supported. Migration is optional: the NAST approach can still be enabled via a Customizing parameter. Future SAP development will be focused exclusively on the new framework.

## Questions This Chunk Answers
- What is the SAP S/4HANA New Output Management and how does it differ from NAST?
- Is migration to the new Output Management mandatory?
- What are the main benefits of the new Output Management framework?
- What output channels are supported in the new framework?
- How does BRFplus determine output parameters?
- How does the system generate and store output PDFs in the new framework?
- What is the role of the KPro archive in output management?

## Definition

The *SAP S/4HANA Output Management* is the strategic output framework for SD, MM, FIN, and other application areas in SAP S/4HANA. It replaces the *NAST*-based approach (condition technique + NAST table) as the standard going forward. New SAP developments — new output types, enhancements, and improvements — will only be made in this framework.

The legacy NAST approach remains technically available. Organizations already using NAST can continue to do so by enabling it via a specific Customizing parameter (SAP Note 2228611). There are no mandatory migration actions for existing customers.

## Purpose in the SD Process

In the SD process, output management serves as the communication layer between the system and external parties (customers, logistics partners) and internal recipients. The new framework maintains this role while providing a more flexible and unified infrastructure:
- *Extensibility* via CDS (Core Data Services) views replaces rigid communication structures.
- *BRFplus* replaces condition records for output parameter determination — more flexible, table-driven, testable.
- *Unified solution* across SAP applications: SD, MM, FIN, and others share the same output framework.
- *SAP Fiori* integration: full integration with Fiori apps for output preview, monitoring, and reprocessing.
- *State-of-the-art email support*: flexible configuration for multiple recipients, email templates, and dynamic content.

## Supported Output Channels

The new Output Management supports the following channels:
- **Print** — rendered PDF sent to a printer queue
- **Email** — PDF attached or inline, with flexible recipient and template configuration
- **XML** — structured data output for system-to-system exchange
- **IDoc** — for on-premise system integration

Other channels (such as EDI) are not available by default in the new framework. Organizations requiring additional channels must evaluate whether to use the NAST approach or to implement custom extensions.

## Structure and Variants

### Form Template

An output document is produced by combining two components:
1. **OData Service**: retrieves the data for the SD document from the database. This replaces the ABAP communication structures (VBDKA, VBDPA, etc.) used in legacy output.
2. **Adobe Livecycle Design Document**: contains the layout. Adobe XFA is the default technology, though the framework also supports SAPscript, SmartForms, and Adobe Forms (non-XFA).

### PDF Generation and KPro Storage

When Output Management signals that output is ready for printing or emailing (status: *Pending* or *Successful*), the rendered PDF is stored in the *Knowledge Provider (KPro)* archive. KPro is a cross-application document management infrastructure. After a PDF is archived:
- Subsequent previews of that issued output are retrieved from KPro — ensuring historical accuracy even if the underlying document data changes.
- Output still *in preparation* (status: *In Preparation*) continues to reflect live document data until it is finalized.

## BRFplus Decision Tables

Output parameters are determined by *BRFplus (Business Rule Framework Plus)* decision tables rather than condition records. A BRFplus decision table:

- Contains **condition columns** (input: document attributes) and **result columns** (output: determined parameters).
- Is processed **row by row** in sequence.
- Within each row, **condition columns are evaluated left to right**.
- If all conditions in a row are satisfied, the result column values are returned: output type, recipient, channel, printer settings, form template.
- Rows can be **reordered** so that the most specific conditions are evaluated first (analogous to the specific-to-general principle in NAST access sequences).
- Decision tables can be **exported to and imported from Microsoft Excel**, facilitating mass editing and governance outside the SAP system.

This approach allows business users and functional consultants to maintain output determination rules in a structured table format without requiring ABAP development.

## Key Distinctions from NAST-Based Output

| Dimension | NAST Approach | New Output Management |
|---|---|---|
| Determination engine | Condition records + access sequence | BRFplus decision tables |
| Data extraction | ABAP communication structures | OData Services |
| Form technology | SAPscript / SmartForms / Adobe Forms | Adobe XFA (default); legacy still supported |
| Channels | Print, EDI, email, fax, and more | Print, email, XML, IDoc only |
| Fiori integration | Limited | Full |
| Future SAP development | Maintenance only | Active development |

The new framework does NOT use the NAST table. Condition records created for NAST-based output have no effect in the new framework. When an organization migrates to the new Output Management, it must recreate its output determination logic as BRFplus decision tables.

## Relationship with Other SAP SD Objects

| Object | Role |
|---|---|
| BRFplus decision table | Replaces NAST condition records for output parameter determination |
| OData Service | Replaces ABAP communication structure for data extraction |
| Adobe XFA form | Default form technology; replaces SAPscript / Adobe Forms |
| KPro archive | Stores rendered output PDFs for historical retrieval |
| SAP Fiori apps | Used for output monitoring, preview, reprocessing |
| configuration-output-determination-sd-001 | Covers the legacy NAST condition technique approach |
| configuration-billing-output-management-brfplus-001 | Covers BRFplus output determination specifically for billing documents |

## Cross-References
- See also: configuration-output-determination-sd-001
- See also: configuration-billing-output-management-brfplus-001
- See also: configuration-billing-types-sap-s4hana-001
