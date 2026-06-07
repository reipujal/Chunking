---
schema_version: 1
id: configuration-sales-document-type-control-001
title: "Sales Document Type Control in SAP SD"
area: configuration
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "47-53"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - sales document type
  - clase de documento de ventas
  - tipo de pedido de ventas
  - order types permitted for sales area
  - que controla la clase de documento de ventas
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sales Document Type Control in SAP SD

## Operational Summary
The *sales document type* is the header-level control object for sales processes. Together with item categories and schedule line categories, it determines how a sales document behaves and how data is passed to later documents. The source highlights that sales processes are controlled through Customizing at header, item, and schedule line level, and that the sales document type influences categories, default values, blocks, follow-on document types, checks, and permitted sales areas.

## Questions This Chunk Answers
- What does the sales document type control in SAP SD?
- Which basic functions must be assigned or configured for sales documents?
- Why should a new sales document type usually be copied from an existing one?
- How can sales document types be restricted to a sales area?
- What checks can be activated in sales document type Customizing?

## What This Configuration Controls
The *sales document type* controls the overall business process represented by the sales document. It works with the *item category* and *schedule line category* to control the document structure. At header level, it can influence the sales document category, delivery and billing blocks, document types for subsequent deliveries and billing documents, number assignment, default values, and activation of checks.

The source also names basic functions that must be configured for sales documents: *partner determination*, *pricing*, *message determination*, *text determination*, *material determination*, *credit management*, *incompleteness*, and *delivery scheduling*. These functions can be fine tuned at the different levels of the sales document.

## SPRO Path or Direct T-code
The source describes Customizing for sales documents but does not provide a transaction code. Use the IMG sales document type configuration area in the project system; no T-code is listed in the extraction field because the course page does not literally name one.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Sales document category* | Classifies the broad behavior of the document | Inquiry, quotation, order, contract-like categories |
| *Delivery block* | Proposed block that can prevent or delay delivery processing | Blank or configured block reason |
| *Billing block* | Proposed block that can prevent billing | Blank or configured block reason |
| *Default delivery type* | Follow-on delivery document type proposed for the process | Course examples include delivery types in later units |
| *Default billing type* | Follow-on billing type proposed for the process | Depends on business process |
| *Requested delivery date default* | Proposed date when creating the document | Customizing-defined default |
| *Checks* | Optional messages and validations | Open quotation, outline agreement, customer-material info record, credit limit |
| *Sales area assignment* | Defines where the document type is valid | Sales organization, distribution channel, division |

## Configuration Impact
The sales document type is not complete by itself. The course emphasizes that a sales document is not fully configured until all required basic functions have also been processed. For example, pricing requires configuration of both the sales document type and pricing procedure, followed by assignment of the procedure to the sales document type. Output works similarly through assignment of an output determination procedure.

Adding a new sales document type has broad impact because many Customizing entries depend on it. SAP recommends copying an existing, tested document type with similar functions, then adapting it. Copying transfers fields and dependent entries and generates a log that can be saved for documentation.

## Common Configuration Errors
**Document type works in one sales area but not another**
-> Check whether the sales document type is permitted for the relevant sales organization, distribution channel, and division.

**Follow-on delivery or billing proposal is wrong**
-> Review the default subsequent document types and related copying control settings.

**Performance degrades after activating many checks**
-> The source warns that activating checks such as open quotations, outline agreements, customer-material info records, or credit limit checks can affect system performance.

## Cross-References
- Prior step: order-management-sales-order-special-features-001
- Next step: configuration-sales-item-category-control-001
- See also: configuration-sales-copying-control-001
