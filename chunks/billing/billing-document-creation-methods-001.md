---
schema_version: 1
id: billing-billing-document-creation-methods-001
title: "Methods for Creating Billing Documents in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "44-48, 51"
    source_type: "A"
    role: "primary"
transactions: [VF01, VF04]
tables: []
aliases:
  - due list
  - pool de facturación
  - background processing
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
SAP offers several methods for processing billing documents, ranging from manual, on-request billing for single documents, up to fully automated background collective runs based on specific dates and schedules.

## Questions This Chunk Answers
- How can users generate individual or collective billing documents?
- How is background billing set up?
- Can collective billing runs be canceled?

## Process Flow and Options
There are multiple modes via which invoices can be created:

### 1. Billing on Request (Manual)
By manually entering the document numbers (e.g., using transaction `VF01`), you explicitly specify the transaction to be billed (order-related or delivery-related). You can select individual items or partial quantities (using the Item Selection function) as long as the item category is relevant for it.

### 2. Processing Billing Due Lists
Most transactions are not billed individually. Using the billing due list (transaction `VF04`), you can periodically carry out collective billing runs.
- **Filters**: You use selection criteria like sold-to party, billing date, and destination country to narrow down the worklist.
- **Individual Option**: Creates a separate invoice per checked document without combination.
- **Collective Option**: System processes all marked documents in the background and attempts to combine them into collective invoices as much as possible.

### 3. Billing on Specific Dates
To process invoices periodically on predefined dates, you maintain a factory calendar using special rules and enter it in the customer master record of the payer (Billing schedule). The system combines deliveries due on that specific date into a collective invoice.

### 4. Background Processing
To improve performance and efficiency, billing runs can be scheduled as background jobs running periodically (e.g., every Monday at 2 a.m.) or at a specific time. The system can divide the list into multiple simultaneous jobs to leverage multi-processing hardware.

### 5. Cancellation of Collective Runs
If an error affects an entire collective processing run, it can be canceled. This cancels all billing documents within the collective run type S, leaving the preceding documents open for billing again.
