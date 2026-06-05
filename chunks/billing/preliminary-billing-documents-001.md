---
schema_version: 1
id: billing-preliminary-billing-documents-001
title: "Preliminary Billing Documents (PBD) in SAP"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "60-62"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - PBD
  - preliminary billing
  - factura preliminar
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
A *Preliminary Billing Document (PBD)* serves as an optional intermediary draft document created solely to facilitate negotiations with customers before the actual, final binding invoice is finalized and posted to Financial Accounting.

## Questions This Chunk Answers
- What is a preliminary billing document used for?
- Does a preliminary billing document update financial accounting?
- What are the statuses of a PBD?

## Definition
Particularly in the professional services industry, invoicing logic entails continuous negotiation. A Preliminary Billing Document is structurally identical to a standard billing document, mirroring all header and item fields. However, while it is output-relevant (so it can be printed and sent to the customer), it does *not* trigger postings to Financial Accounting. It can be repeatedly changed (prices, terms, dates) based on customer feedback.

## Setup and Workings
A configuration expert must activate the business function `SD_BIL_PRELIMBILLINGDOC`. Once activated, generating a PBD from the billing due list securely marks the preceding document as "billed" so it cannot be inadvertently invoiced by another user.

## Overview of Statuses
The lifecycle of a PBD cycles through four statuses:
- **In progress**: The default status. The document is free to be modified, rejected, finalized, or directly converted explicitly to a final billing document.
- **Rejected**: The user manually rejected the PBD due to it being unsuitable. The preceding document reopens for billing.
- **Finalized**: Manually flagged to indicate no further negotiations are required for now. It restricts changes until it is converted, but the document can be sent back to "In progress" if needed.
- **Completed**: The PBD has been formally converted to an actual billing document. It can no longer be altered unless the successor billing document is canceled.
