---
schema_version: 1
id: configuration-sales-incompletion-check-001
title: "Incompletion Check and Incompletion Procedure in Sales Documents"
area: configuration
process_tags: [order-to-cash, delivery-processing, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "88-95"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - incompletion log
  - log de incompletos
  - procedimiento de incompletos
  - incomplete sales document status group
  - como bloquear facturacion por datos incompletos
  - lista documentos incompletos
  - incomplete for delivery billing pricing
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Incompletion Check and Incompletion Procedure in Sales Documents

## Operational Summary
The *incompletion log* lists required sales document data that has not yet been entered. Customizing defines which fields are checked, at which document level, and what business consequence missing data has. The log can navigate the user directly to the views needed to enter missing data. Incompletion can prevent saving the document or, through status groups, allow saving while blocking selected follow-on steps such as delivery, billing, pricing, order confirmation, or creation of reference documents. Any field in any SD document level can be made mandatory — there is no fixed standard list.

## Questions This Chunk Answers
- What is the incompletion log in SAP SD?
- Can incomplete sales documents be saved?
- How does missing data block delivery, billing, or pricing?
- At which levels can incompletion procedures be assigned?
- Can partner functions, texts, and pricing condition types be mandatory?
- How does a user find and correct all incomplete documents they created?

## What This Configuration Controls
The incompletion configuration controls which data fields are mandatory for the company's process and what happens when they are missing. The system navigates directly from the incompleteness log to the view where the user can enter the missing data. The specific views accessible from the log can be configured in Customizing.

All employees can list all the incomplete sales documents they have entered. They can also display documents that have been blocked for a specific processing step — for example, a list of all documents blocked for shipping due to incompleteness. Incomplete documents can be opened and corrected from the list; after completing the required data, the system automatically returns to the list of incomplete documents.

## SPRO Path or Direct T-code
Not stated in source.

## Key Parameters

| Field or setting | Description | Typical Values |
|---|---|---|
| *Incompletion messages* | Controls whether incomplete sales documents can be saved | Active or inactive in sales document type |
| *Incompletion procedure* | Defines fields checked for completion | Header, item, or schedule line procedure |
| *Assignment object* | Determines where the procedure is valid | Sales document type, item category, schedule line category |
| *Status group* | Defines which process steps are blocked when data is missing | Delivery, billing, pricing/confirmation, or reference document creation |
| *Mandatory partner/text/condition* | Makes partner functions, texts, or pricing condition types required | Required or optional |

## Configuration Impact
The incompletion log differentiates between three levels: *sales document header*, *sales document item*, and *sales document schedule line*. Procedures are assigned by level:
- Header-level procedure assigned via sales document type
- Item-level procedure assigned via item category
- Schedule-line-level procedure assigned via schedule line category

If the *incompletion messages* field in the sales document type is active, it controls whether incomplete sales documents can be saved at all. If the switch is not set, the document can be saved, but subsequent processing is controlled by status groups in the incompleteness procedure.

**Status group consequences.** Each field in the incompleteness procedure can be assigned a status group. The status group defines which steps are prevented if that field is missing:

| Status group consequence | Effect |
|---|---|
| Incomplete for delivery | No delivery can be created |
| Incomplete for billing | No billing document can be created |
| Incomplete for pricing | No order confirmation and no billing are possible |

A single status group can contain any combination of these consequences. This allows different missing fields to block different steps independently — for example, missing payment terms might block billing but allow delivery, while a missing shipping point blocks delivery but not billing.

Beyond individual fields, partner functions, texts, and condition types in pricing can also be flagged as mandatory within the incompletion procedure. If these are missing, a note appears in the incompletion log.

The incompleteness procedure can be configured with any field from any of the relevant document levels. SAP does not impose a fixed mandatory field list.

## Common Configuration Errors
**Document saves but cannot be billed**
-> A missing field is assigned to a status group that allows delivery but blocks billing, such as missing payment terms.

**Users cannot save incomplete orders**
-> Review the incompletion messages setting in the sales document type; if active, the document cannot be saved while incomplete.

**Missing purchase order number appears but does not block processing**
-> The incompletion procedure flags the field but no status group is assigned, so no blocking consequence applies.

**A required partner is missing but no log entry appears**
-> Partner functions can be flagged as mandatory within the incompletion procedure. Check both the incompletion procedure and the partner determination settings.

**User cannot navigate to incomplete field from the log**
-> The target view or screen is not configured in Customizing for the incompletion procedure navigation.

## Cross-References
- Prior step: order-management-sales-order-special-features-001
- See also: shipping-delivery-special-functions-001
- Next step: master-data-sd-partner-functions-001
