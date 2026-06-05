---
schema_version: 1
id: billing-billing-document-cancellation-001
title: "Canceling Billing Documents in SAP SD"
area: billing
process_tags: [order-to-cash, billing, returns]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "21-22"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - cancellation
  - anulación
  - cancellation document
  - documento de anulación
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
To cancel a billing document, you create a cancellation document. The system then copies data from the reference document into the cancellation and offsets the entry in Financial Accounting automatically.

## Questions This Chunk Answers
- How is a billing document canceled in SAP?
- Does a cancellation require entries in copying control?
- Can individual items be canceled?

## When It Applies and Context
You create a cancellation document when a billing document has been generated in error or contains incorrect details (e.g., prices or quantities) and has already been saved. 

## Process Flow
1. **Initiate Cancellation**: Create the cancellation document with reference to the billing document containing errors. In the standard system, for example, billing document type S2 is used to cancel credit memos.
2. **Review Overview Screen**: You branch to an overview screen containing both the original billing document and the new cancellation billing document. This allows you to compare both documents to avoid discrepancies before saving.
3. **Save and Offset**: When updating, the system offsets the entry in Financial Accounting.
4. **Re-billing**: Once canceled, the reference document of the original billing document (e.g., the delivery) can be billed again.

## Conditions and Restrictions
- **No Copying Control Needed**: You do not need to make an entry in copying control for cancellations. The specific parameters to be changed (such as assignment number and reference number) are stored directly in the *Cancellation* area of the screen for each billing type.
- **Item-Level Cancellation**: You can also cancel individual items within a billing document rather than the entire document.
