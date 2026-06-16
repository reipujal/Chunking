---
schema_version: 1
id: order-management-sales-distribution-process-001
title: "Sales and Distribution Process Documents in SAP S/4HANA"
area: order-management
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "11-15"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - sales document
  - documento de ventas
  - proceso de ventas y distribucion
  - sales document header item schedule line
  - como se estructura un documento de ventas
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Sales and Distribution Process Documents in SAP S/4HANA

## Operational Summary
In SAP S/4HANA Sales, every sales activity is represented by a *sales document*. The process chain uses purpose-built document types in Sales, Shipping, and Billing: inquiries, quotations, and standard orders on the sales side; outbound and returns deliveries on the logistics side; and invoices, credit memos, and debit memos in billing. Each document has its own number, search support through matchcodes, and an overall status that summarizes the detailed processing statuses of the business activity.

## Questions This Chunk Answers
- What kind of document records a sales activity in SAP S/4HANA Sales?
- How are Sales, Shipping, and Billing represented in the SD process?
- What are the structural levels of a sales document?
- Why does a sales document item need schedule lines when it has delivery requirements?
- What does the overall status of an SD document represent?

## Definition
A *sales document* is the SAP record used to model a sales activity. It is not a single flat record. It has three levels: *header*, *item*, and *schedule line*. The header carries data and default values that apply to the whole document. Items describe the goods or services requested by the customer, including material number, description, price information, and delivery or payment terms. Schedule lines carry shipping and procurement data, especially delivery dates and quantities.

## Purpose in the SD Process
The purpose of the document structure is to let SAP model an order-to-cash process with enough detail to control later steps. A customer order can contain multiple items, and each item can have more than one schedule line. That is important because delivery commitments are not always fulfilled in one date or quantity. If an item has delivery requirements, at least one schedule line must exist because the delivery deadline and order quantity are held there.

The document status summarizes where the business process stands. A sales order, delivery, or billing document receives an overall status, and that status is built from more specific statuses for individual steps. This allows a consultant or user to understand whether a document is open, partially processed, completed, blocked, or awaiting a later SD activity without reading every field manually.

## Structure and Variants
SAP SD uses three document families:

| Family | Examples from the course | Business meaning |
|---|---|---|
| *Sales document types* | inquiries, quotations, standard orders | Commercial request, offer, or order entry |
| *Delivery types* | outbound delivery, returns delivery | Physical movement or return of goods |
| *Billing document types* | invoices, credit memos, debit memos | Financial settlement of the SD process |

The sales document itself is structured as:

| Level | Main role |
|---|---|
| *Header* | General data and defaults valid for the whole document |
| *Item* | Ordered goods or services and commercial terms |
| *Schedule line* | Delivery dates, quantities, shipping, and procurement data |

## Relationship with Other SAP SD Objects
The *sales document* initiates or records the commercial step, while later *delivery documents* and *billing documents* represent logistics and financial follow-on activities. Because the same SD process can pass through several document types, document numbers, statuses, and document structure are central to tracing a customer transaction from the initial sales activity through delivery and billing.

## Cross-References
- Next step: enterprise-structure-sales-distribution-enterprise-structure-001
- See also: order-management-sales-document-data-flow-001
- See also: integration-sales-document-technical-tables-001
- See also: order-management-presales-additional-processes-001 (presales documents, make-to-order, service products)
