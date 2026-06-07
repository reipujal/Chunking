---
schema_version: 1
id: configuration-sales-copying-control-001
title: "Copying Control for Sales Documents"
area: configuration
process_tags: [order-to-cash, delivery-processing, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "75-80"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - copying control
  - control de copia
  - crear con referencia customizing
  - copying requirements data transfer routines
  - como configurar copia entre documentos de ventas
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Copying Control for Sales Documents

## Operational Summary
*Copying control* determines which document types can be copied into other document types and how the copy behaves at header, item, and schedule line level. The source covers sales-to-sales, billing-to-sales, sales-to-delivery, sales-to-billing, delivery-to-billing, and billing-to-billing relationships. It also explains that copying control contains data transfer routines, copying requirements, and switches that govern field transfer, eligibility checks, and transaction-specific behavior.

## Questions This Chunk Answers
- What does copying control determine in SAP SD?
- At which levels is copying control maintained for sales documents?
- What is the difference between a data transfer routine and a copying requirement?
- Which standard copying requirements are mentioned in the course?
- Why can an invalid target item or schedule line category cause determination issues?

## What This Configuration Controls
Copying control controls document creation with reference. It determines the permitted source and target document type relationships and the detailed logic used when data moves from one document to another.

**Important constraint:** A sales document can be created with reference to another existing sales document **only if copying control is set up** for that source-target relationship. Without the copying control entry, the reference is not allowed.

**Standard document flow examples from the source:**

| Source document type | Target document type | Example |
|---|---|---|
| Sales doc type (QT, quotation) | Sales doc type (OR, standard order) | Order from quotation |
| Billing doc type (F2, invoice) | Sales doc type (G2, credit memo request) | Credit memo request from invoice |
| Sales doc type (OR, standard order) | Delivery type (DL, delivery) | Delivery from standard order |
| Sales doc type (G2, credit memo request) | Billing doc type (G2, credit memo) | Credit memo from credit memo request |
| Delivery type (DF) | Billing doc type (F1, invoice) | Invoice from delivery |
| Billing doc type (F1, invoice) | Billing doc type (S1, invoice cancellation) | Cancellation from invoice |

**Document flow information.** The document flow contains information on what was copied from the source document to the target document. At item level, it shows the quantities and values that were transferred.

## SPRO Path or Direct T-code
The source describes copying control in Sales and Distribution Customizing and mentions that routines and requirements can be processed under the menu option *System Modifications*. It does not provide a direct transaction code in the extracted text.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Source document type* | Document type being copied from | Sales, delivery, or billing document type |
| *Target document type* | Document type being created | Sales, delivery, or billing document type |
| *Data transfer routine* | Controls field transfer from the preceding document | Standard or copied routine |
| *Copying requirement* | Checks business prerequisites before copying | Header, item, or schedule line requirement |
| *Switches* | Transaction-specific behavior toggles | Transfer item numbers or other controls |
| *Target item/schedule line category* | Optional explicit target category | Must exist in category assignment |

## Configuration Impact
Copying control mirrors the sales document structure. At header, item, and schedule line level, a consultant can configure routines for data transfer, copying requirements, and switches. If a target value is invalid or missing at item or schedule line level, SAP determines the target from the assignment of item or schedule line categories. Any value entered must exist in the relevant assignment as an alternative.

Copying requirements enforce process logic. The source names requirement 001 at header level, which checks whether sold-to party and sales area in source and target are the same. It names requirement 301 at item level, which checks whether the item used as a copy has a reason for rejection or completed status. It names requirement 501 at schedule line level, which ensures that only schedule lines with open quantity greater than zero are copied.

## Common Configuration Errors
**Document cannot be created with reference**
-> The source-target document type relationship may be missing in copying control, or a copying requirement fails.

**Rejected or completed items are copied**
-> Check item-level copying requirement, especially logic comparable to the standard requirement that checks rejection or completed status.

**Schedule lines with no open quantity are copied**
-> Check schedule-line-level copying requirement.

**Custom routine behaves unexpectedly**
-> Routines and requirements are ABAP code. The course recommends checking whether standard objects are suitable and copying them before adjusting.

## Cross-References
- Prior step: order-management-sales-document-data-flow-001
- See also: configuration-billing-copying-control-001
- Next step: special-processes-sales-special-business-transactions-001
