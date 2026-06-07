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
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "29-30, 125"
    source_type: "A"
    role: "primary"
transactions: [VF11]
tables: []
aliases:
  - VF11
  - cancellation
  - anulación
  - cancel billing document
  - anular factura
  - cancellation document
  - documento de anulación
  - reverse invoice
  - reversar factura
  - S2
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Canceling Billing Documents in SAP SD

## Operational Summary
To cancel a billing document, you create a cancellation document using transaction *VF11*. The system copies data from the original billing document into the cancellation and automatically offsets the corresponding entry in Financial Accounting. The reference document (e.g., the delivery) becomes available for billing again after cancellation. Individual items within a billing document can also be canceled without canceling the entire document.

## Questions This Chunk Answers
- How is a billing document canceled in SAP?
- What transaction is used to cancel an invoice or credit memo?
- Does cancellation require entries in copying control?
- Can individual items be canceled without canceling the entire billing document?
- What happens to the original reference document after cancellation?
- What billing document type cancels a credit memo in the standard system?

## When It Applies and Context
Use cancellation when a billing document has been saved with incorrect data (wrong price, quantity, or payer) and must be reversed. The cancellation offsets the FI posting rather than overwriting it, preserving audit integrity.

## Process Flow
1. **Initiate Cancellation**: Run transaction *VF11* and enter the billing document number to be canceled. In the standard system, billing type S2 is used to cancel credit memos.
2. **Review Overview Screen**: The system displays an overview with both the original billing document and the new cancellation document side by side. Review to confirm there are no discrepancies before saving.
3. **Save and Offset**: Upon saving, the system offsets the original FI entry automatically. The cancellation document carries the reversed amounts.
4. **Re-billing**: The reference document of the original billing document (e.g., the outbound delivery) is now open for billing again.

## Conditions and Restrictions
- **No Copying Control entry needed**: Cancellation parameters (assignment number, reference number) are stored directly in the billing type's *Cancellation* area — no copying control entry is required.
- **Item-Level Cancellation**: Individual items within a billing document can be canceled independently.
- **Accounting period**: Cancellation may not be possible if the FI posting period of the original document is already closed.

## Common Errors

**Cancellation not possible — accounting period closed**
→ The FI posting period of the original billing document is closed. Resolve via FI period management or handle via credit memo process.

**Re-billing does not pick up the reference document**
→ After cancellation, confirm the reference document (e.g., the delivery) has returned to an open, billable status before re-running billing.

**Wrong cancellation billing type proposed**
→ Each billing type has its own cancellation type configured in billing type settings. Verify the *Cancellation billing type* field in Customizing.

## Cross-References
- Prior step: billing-billing-document-creation-methods-001
- See also: configuration-billing-negative-postings-001
- See also: configuration-billing-types-sap-s4hana-001
- See also: billing-credit-debit-memo-process-001
