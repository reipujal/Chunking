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
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "68-70"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - PBD
  - preliminary billing
  - preliminary billing document
  - documento de factura preliminar
  - factura preliminar
  - draft invoice
  - borrador de factura
  - SD_BIL_PRELIMBILLINGDOC
  - invoice negotiation
  - negociación de factura
  - invoice draft professional services
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Preliminary Billing Documents (PBD) in SAP

## Operational Summary
A *Preliminary Billing Document (PBD)* is an optional draft invoice that facilitates customer negotiation before the final, binding invoice is posted to Financial Accounting. It is structurally identical to a standard billing document — same header and item fields — and can be printed and sent to the customer, but it **does not trigger FI postings**. The PBD can be revised repeatedly based on customer feedback, then converted to a final billing document when agreed. Business function `SD_BIL_PRELIMBILLINGDOC` must be activated to use this feature.

## Questions This Chunk Answers
- What is a Preliminary Billing Document and when is it used?
- Does a preliminary billing document post to Financial Accounting?
- How many times can a PBD be changed before finalizing?
- What are the four statuses of a PBD lifecycle?
- What happens to the reference document while a PBD is open?
- What business function must be activated to use PBDs?

## Definition
A *Preliminary Billing Document* is a draft version of a billing document used as a negotiation tool. It has the same data structure as a final billing document, is output-relevant (can be printed or sent), but explicitly does not generate accounting postings. It exists in a separate lifecycle with its own statuses that control when it can be changed, finalized, or converted.

## Purpose in the SD Process
In professional services and project billing, the invoice amount is often subject to negotiation after service completion. The PBD enables iterative agreement on price, terms, or scope before the financial commitment is made. Once the PBD is agreed, it is converted to a binding billing document that triggers the FI posting. This eliminates the need for cancellation if the initial invoice was incorrect.

## Structure and Variants
PBD statuses control the document lifecycle:

| Status | Description |
|---|---|
| In progress | Default initial status. The PBD can be modified, rejected, finalized, or directly converted to a final billing document. |
| Rejected | User manually rejected the PBD (e.g., customer dispute not resolved). The preceding document reopens for billing. |
| Finalized | Manually flagged to indicate negotiation is complete. Restricts further changes until conversion. Can be moved back to *In progress* if needed. |
| Completed | The PBD has been converted to a final billing document. Cannot be altered unless the successor billing document is first canceled. |

When a PBD is created from the billing due list, the reference document (order or delivery) is marked as *billed* — it cannot be inadvertently invoiced by another user while the PBD is open.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Billing Due List | PBD created from the due list; reference document locked while PBD is open |
| FI Accounting Document | NOT created at PBD time — only created when PBD is converted to final billing document |
| Final Billing Document | Created from PBD upon conversion; triggers FI posting |
| Business Function | SD_BIL_PRELIMBILLINGDOC must be activated in system configuration |

## Cross-References
- See also: billing-billing-document-creation-methods-001
- See also: billing-pro-forma-invoice-001
