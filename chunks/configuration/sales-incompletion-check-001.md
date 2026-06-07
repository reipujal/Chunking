---
schema_version: 1
id: configuration-sales-incompletion-check-001
title: "Incompletion Check and Incompletion Procedure in Sales Documents"
area: configuration
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
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
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Incompletion Check and Incompletion Procedure in Sales Documents

## Operational Summary
The *incompletion log* lists required sales document data that has not yet been entered. Customizing defines which fields are checked, at which document level, and what business consequence missing data has. Incompletion can prevent saving the document or, through status groups, allow saving while blocking selected follow-on steps such as delivery, billing, pricing, order confirmation, or creation of reference documents.

## Questions This Chunk Answers
- What is the incompletion log in SAP SD?
- Can incomplete sales documents be saved?
- How does missing data block delivery, billing, or pricing?
- At which levels can incompletion procedures be assigned?
- Can partner functions, texts, and pricing condition types be mandatory?

## What This Configuration Controls
The incompletion configuration controls which data fields are mandatory for the company's process and what happens if they are missing. The log can navigate users directly to the relevant views where they maintain missing data. Users can also list incomplete orders they created and filter documents blocked for a specific step, such as shipping due to incompleteness.

## SPRO Path or Direct T-code
The course describes Customizing for incompletion procedures and sales document types but does not provide a direct transaction code. No T-code is listed in the frontmatter.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Incompletion messages* | Controls whether incomplete sales documents can be saved | Active or inactive in sales document type |
| *Incompletion procedure* | Defines fields checked for completion | Header, item, or schedule line procedure |
| *Assignment object* | Determines where the procedure is valid | Sales document type, item category, schedule line category |
| *Status group* | Defines process consequences of missing data | Delivery block, billing block, pricing/confirmation impact |
| *Mandatory partner/text/condition* | Makes partner functions, texts, or pricing condition types required | Required or optional |

## Configuration Impact
The source distinguishes three levels for the incompletion log: *sales document header*, *sales document item*, and *sales document schedule line*. Procedures are assigned by level. Header procedures can be assigned through the sales document type, item procedures through item category, and schedule line procedures through schedule line category.

If the *incompletion messages* field in the sales document type is active, it controls whether incomplete sales documents can be saved. If the switch is not set, the subsequent business process is controlled by status groups in the incompleteness procedure. This means the document may be saved but prevented from delivery, billing, pricing, confirmation, or reference creation depending on the missing field.

## Common Configuration Errors
**Document saves but cannot be billed**
-> A missing field may be assigned to a status group that allows delivery but blocks billing, such as missing payment terms in the course example.

**Users cannot save incomplete orders**
-> Review the incompletion messages setting in the sales document type.

**Missing purchase order number appears but does not block processing**
-> That is possible if the incompletion procedure flags it without assigning a status group that prevents follow-on steps.

**A required partner is missing but no log appears**
-> Partner functions can be flagged as mandatory; check the relevant incompletion and partner determination settings.

## Cross-References
- Prior step: order-management-sales-order-special-features-001
- See also: shipping-delivery-special-functions-001
- Next step: master-data-sd-partner-functions-001
