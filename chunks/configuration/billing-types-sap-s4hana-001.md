---
schema_version: 1
id: configuration-billing-types-sap-s4hana-001
title: "Standard Billing Types and Controls in SAP SD"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "29-30"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - billing type
  - clase de factura
  - tipo de factura
  - F2 billing type
  - G2 billing type
  - L2 billing type
  - define billing type
  - definir clase de factura
  - billing type controls
  - parámetros de clase de factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Standard Billing Types and Controls in SAP SD

## Operational Summary
The *billing type* is the central control element for billing document processing. It governs the document's number range, partner and output determination, account determination procedure, FI interface settings (posting block, document type), and special behaviors like negative posting, value dating, or cancellation type. SAP delivers a complete set of standard billing types covering all standard business transactions; these can be redefined or extended in Customizing.

## Questions This Chunk Answers
- What is a billing type and what does it control?
- What are the standard billing types available in SAP S/4HANA and what are they used for?
- How does the billing type determine the FI document type?
- Can new billing types be created or existing ones modified?
- Where is the billing type configured in Customizing?
- What is the relationship between billing type and the cancellation document?

## What This Configuration Controls
The billing type controls:
- **Number range**: the document number assignment range for billing documents of this type
- **Partner determination**: which partner functions are determined (payer, sold-to, ship-to)
- **Text determination**: which text types are copied or determined
- **Output determination**: procedure assigned for print/email/EDI output
- **Account determination procedure**: which procedure is used to find G/L accounts
- **FI interface settings**: posting block, document type, reference/allocation number rules
- **Special features**: negative posting indicator, value-dated credit memos, branch/head office logic, cancellation billing type

## SPRO Path or Direct T-code
Sales and Distribution → Billing → Billing Documents → Define Billing Types

## Key Parameters
Standard billing types in SAP S/4HANA:

| Billing Type | Description |
|---|---|
| F2 | Standard invoice (delivery-related) |
| F5 | Pro forma invoice (order-based) |
| F8 | Pro forma invoice (delivery-based) |
| CS | Cash sale invoice |
| G2 | Credit memo |
| L2 | Debit memo |
| RE | Returns |
| IV | Intercompany billing (invoice) |
| IG | Intercompany billing (credit memo) |
| S1 | Cancellation invoice |
| S2 | Cancellation credit memo |
| LR | Invoice list (invoices/debit memos) |
| LG | Credit memo list |
| FAZ | Down payment request |

Each billing type specifies its *cancellation billing type* — the document type used when that billing document is canceled.

## Configuration Impact
The billing type is the entry point for all billing-related configuration. Incorrect billing type assignment in copying control causes the wrong document type to be created (e.g., a returns being billed as a standard F2 invoice instead of RE). Missing account determination procedure on the billing type causes account determination failure at billing release.

## Common Configuration Errors

**Wrong FI document type used for billing**
→ The FI document type is configured per billing type. Verify the *Document type* field in the billing type settings (standard: DR for invoices, DG for credit memos, RV default when blank).

**Billing cancellation uses wrong cancellation type**
→ Each billing type has a *Cancellation billing type* field. If blank or incorrectly set, VF11 creates the wrong document type for the cancellation.

**Account determination fails at billing release**
→ The billing type has no account determination procedure assigned, or the procedure does not have the correct condition types for the billing type's business transaction.

## Cross-References
- See also: configuration-billing-relevance-item-category-001
- See also: configuration-billing-copying-control-001
- See also: configuration-flexible-billing-document-numbering-001
- See also: configuration-billing-fi-interface-controls-001
