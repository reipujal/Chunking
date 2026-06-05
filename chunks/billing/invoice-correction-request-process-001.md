---
schema_version: 1
id: billing-invoice-correction-request-process-001
title: "Invoice Correction Requests in SAP SD"
area: billing
process_tags: [order-to-cash, billing, invoice-correction, complaints]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "32-34"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - invoice correction request
  - solicitud de corrección de factura
  - corrección de factura
  - credit and debit combined
  - crédito y débito combinado
  - incorrect invoice correction
  - corregir factura incorrecta
  - price correction billing
  - quantity correction billing
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Invoice Correction Requests in SAP SD

## Operational Summary
An *invoice correction request* combines a credit memo item and a debit memo item in a single document to correct pricing or quantity errors on an existing invoice. The system automatically creates two paired items per line — one credit (reverses the original) and one debit (states the corrected value) — so the net difference is precisely the amount credited or charged to the customer. It must always be created with reference to the original billing document.

## Questions This Chunk Answers
- What is an invoice correction request and how does it differ from a plain credit memo?
- Why are two items created automatically for each corrected line?
- Can the credit memo item be changed? Can the debit item be changed?
- How does the system handle a quantity error versus a price error?
- Why must the invoice correction request reference a billing document, not an order?
- How are unchanged correction items cleaned up?

## When It Applies and Context
Use an invoice correction request when a customer disputes an incorrect invoice and the correction requires both a reversal of the wrong amount and re-billing of the correct amount in the same document. Unlike a plain credit memo, the invoice correction request provides a self-contained audit trail of what was wrong and what was corrected.

## Process Flow
1. **Create with reference to billing document**: The invoice correction request must reference the billing document that contains the error — references to orders or inquiries are not valid here.
2. **Automatic paired items**: For each item in the reference billing document, the system creates two items:
   - All **credit memo items** are listed first (the original values, reversed).
   - All **debit memo items** follow (where the correction is entered).
3. **Adjust the debit item**: The credit memo item cannot be changed — it represents the full reversal of the original. The debit memo item is where you enter the corrected values:
   - **Quantity difference**: Change the quantity on the debit item (e.g., reduce for damaged goods).
   - **Price difference**: Adjust the pricing elements on the debit item (e.g., correct the price).
4. **Net calculation**: The difference between the locked credit item and the adjusted debit item is the final amount credited or debited.
5. **Cleanup**: Use the *Delete unchanged item* function to remove paired lines where no correction was needed, keeping the document clean.

## Conditions and Restrictions
- Must always reference a billing document — not an order, inquiry, or delivery.
- The credit memo item is read-only; only the debit memo item can be changed.
- Billing block may be set automatically depending on Customizing, requiring release before billing.

## Common Errors

**Correction request shows no net value difference**
→ Both credit and debit items are copied identically from the reference. The debit item has not been adjusted yet — enter the corrected quantity or pricing elements on the debit side.

**Cannot create invoice correction request with reference to order**
→ Invoice correction requests require a billing document as reference. Use a credit memo request if the source is a sales order.

**Unwanted zero-value pairs remain in the document**
→ Use the *Delete unchanged item* function to remove paired items that required no correction before saving.

## Cross-References
- See also: billing-credit-debit-memo-process-001
- See also: billing-returns-process-001
- See also: configuration-billing-types-sap-s4hana-001
