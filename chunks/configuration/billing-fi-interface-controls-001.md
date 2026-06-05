---
schema_version: 1
id: configuration-billing-fi-interface-controls-001
title: "Interface Controls Between SD Billing and Financial Accounting"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "95-98, 102"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - FI interface
  - interfaz FI
  - posting block
  - bloqueo de contabilización
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Configuring the interface between Sales and Distribution (SD) and Financial Accounting (FI) securely dictates how structural data, like reference numbers and transaction document types, pass over during billing release, and whether they pass automatically or are blocked.

## Questions This Chunk Answers
- How can you block billing documents from posting to accounting automatically?
- What parameters dictate the reference and allocation numbers on the FI document?
- Which document type represents a billing document in FI?

## Posting Block
Normally, SD transfers accounting-related data to FI automatically upon saving the billing document. However, you can configure a *posting block* directly at the billing type level.
This allows you to generate SD documents, audit them, and print them out before manually releasing them to Financial Accounting. The system handles postings in an all-or-nothing approach; if the posting block is active or errors prevent account determination, zero accounting documents are generated.

## Reference Numbers and Allocation Numbers
You can automatically propagate the Reference and Assignment fields in the FI accounting document utilizing numbers from the precursor SD documents. 
- The **reference number** (residing in the FI header) is used extensively for clearing.
- The **assignment number** (residing in the customer line item) is used for sorting line numbers.
You configure this mapping in the SD copying control. For example, `A` = Purchase order number, `C` = Delivery number, `E` = Billing document number, etc. Note: if these billing documents are bundled into an *invoice list*, the reference number natively from the invoice list overwrites the initial reference numbers.

## Transaction-Related Document Types
You can differentiate billing outputs mapped into Financial Accounting by specifying a distinct FI Document Type for each billing type in Customizing.
For instance:
- `F2` maps to Doc Type `DR`
- `G2` maps to Doc Type `DG`
- `L2` maps to Doc Type `NN`
If left blank, the system defaults unconditionally to transferring all SD documents natively as FI Document type `RV`.
