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
    pages: "103-106, 110"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - FI interface billing
  - interfaz FI facturación
  - posting block
  - bloqueo de contabilización
  - billing to FI
  - facturación a contabilidad financiera
  - reference number FI billing
  - número de referencia FI factura
  - allocation number billing
  - número de asignación factura
  - FI document type billing
  - tipo de documento FI factura
  - RV document type
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Interface Controls Between SD Billing and Financial Accounting

## Operational Summary
The FI interface for billing controls three key behaviors: (1) whether billing documents are released to accounting automatically or held in a *posting block* for manual review; (2) what numbers from the SD document are copied into the FI document's *Reference* and *Allocation* fields for payment reconciliation; and (3) which FI document type is used to classify the billing document in the general ledger. All three are configured in the billing type settings.

## Questions This Chunk Answers
- How can you block billing documents from posting to accounting automatically?
- What is the purpose of the Reference and Allocation fields in the FI accounting document?
- How are Reference and Allocation numbers sourced from the SD documents?
- Which FI document type represents a billing document when the billing type field is blank?
- Can different billing types produce different FI document types?
- What happens if a posting block is active or account determination fails?

## What This Configuration Controls
The FI interface settings in the billing type control:
- **Posting block**: whether automatic accounting posting is suppressed on save
- **Reference number (FI header)**: SD document number copied as clearing reference in FI
- **Allocation number (FI line item)**: SD document number used for line item sorting in FI
- **FI document type**: the accounting document category assigned to this billing type's FI postings

## SPRO Path or Direct T-code
Sales and Distribution → Billing → Billing Documents → Define Billing Types
(Fields: *Posting Block*, *Reference number*, *Assignment number*, *Document type*)

For invoice list reference number override:
Sales and Distribution → Billing → Invoice Lists → Define Invoice List Types

## Key Parameters

### Posting Block
When active: billing documents are generated but **not** transferred to FI automatically. Documents remain in SD until manually released. Allows printing and auditing before FI impact. Posting is all-or-nothing: if the block is active or account determination fails, **zero** accounting documents are generated.

### Reference Number and Allocation Number
Define which SD document number populates the FI clearing and sorting fields:

| Code | Source |
|---|---|
| A | Purchase order number |
| C | Delivery number |
| E | Billing document number |
| (others) | Other SD document numbers |

Note: when billing documents are collected into an *invoice list*, the invoice list's own reference number overwrites the individual billing documents' reference numbers in FI.

### FI Document Type
| Billing Type | Standard FI Document Type |
|---|---|
| F2 | DR (Customer Invoice) |
| G2 | DG (Customer Credit Memo) |
| L2 | NN (Debit Memo) |
| (blank) | RV (default for all unspecified) |

## Configuration Impact
Incorrect FI document type mapping causes reconciliation issues in FI reports (e.g., credit memos classified as invoices). A missing posting block may allow unreviewed invoices to post to FI. Incorrect reference/allocation number setup prevents automated payment clearing programs from matching open items.

## Common Configuration Errors

**Billing document saved but no FI document created**
→ Posting block is active in the billing type. Manually release the document to accounting, or deactivate the posting block if automatic release is intended.

**Payment run cannot clear the invoice because the reference number is wrong**
→ The reference number field in billing type settings maps to the wrong SD document number (e.g., order number instead of delivery number). Verify the reference number configuration and align with FI clearing logic.

**All billing documents use document type RV regardless of billing type**
→ The *Document type* field in the billing type settings is blank. Assign the correct FI document type per billing type.

## Cross-References
- See also: billing-billing-document-integration-001
- See also: configuration-billing-account-determination-001
- See also: configuration-billing-negative-postings-001
