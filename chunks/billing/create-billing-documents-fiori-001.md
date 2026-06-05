---
schema_version: 1
id: billing-create-billing-documents-fiori-001
title: "Create and Manage Billing Documents using SAP Fiori"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "57-58"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - fiori apps billing
  - aplicaciones fiori facturación
  - Create Billing Documents app
  - Manage Billing Documents app
  - Billing Due List Items app
  - temporary billing document
  - documento de factura temporal
  - factura preliminar fiori
  - automatic posting billing
  - contabilización automática factura
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

# Create and Manage Billing Documents using SAP Fiori

## Operational Summary
In SAP S/4HANA, billing documents can be created and managed through two dedicated Fiori apps: the *Create Billing Documents – Billing Due List Items* app (for creating invoices from a worklist with advanced settings) and the *Manage Billing Documents* app (for reviewing, changing, canceling, and manually posting documents). A key Fiori-specific feature is the *Temporary Billing Document*, which allows a draft preview before finalizing the invoice.

## Questions This Chunk Answers
- What Fiori apps are available for creating and managing billing documents in S/4HANA?
- What is a Temporary Billing Document and how is it different from a final invoice?
- How is automatic posting to accounting configured in the Fiori billing app?
- Can the Fiori billing app create one invoice per item regardless of combination rules?
- What operations does the Manage Billing Documents app support?
- What happens if you discard a Temporary Billing Document?

## When It Applies and Context
Use the Fiori billing apps in S/4HANA environments where users prefer a browser-based, responsive interface. The apps complement (and for many users replace) the classic SAP GUI transactions VF04/VF06. They are particularly useful for billing clerks who need to preview invoices before posting.

## Process Flow

### Create Billing Documents — Billing Due List Items App
This app displays a filtered worklist of all documents due for billing. Before running the billing job, configure *Billing Settings*:
- **Enter billing date and type**: Prompts the user to confirm the billing date and billing type before creating.
- **Create separate billing document per item**: Overrides combination logic — each selected item generates its own individual invoice.
- **Automatically post billing documents**: When active, the system posts to accounting and triggers output (e.g., email) automatically upon creation. When inactive, posting must be triggered manually from the *Manage Billing Documents* app.
- **Display billing documents after creation**: Generates a *Temporary Billing Document* — a draft preview displayed before finalizing. The user can save it (converts to final document) or discard it (returns documents to the due list, no cancellation needed).

### Manage Billing Documents App
Used to review, change, display, cancel, and manually release billing documents to Financial Accounting. Features:
- Seamless navigation between selected documents for inline updates.
- Detailed object-page view with summary and line-item breakdowns.
- PDF-based print preview generation.

## Conditions and Restrictions
- Automatic posting requires that account determination is fully configured; otherwise, the document remains in the due list with an error.
- A discarded Temporary Billing Document does not require VF11 cancellation — the reference document is released automatically.
- Item-level billing override (one document per item) affects combination rules globally for that billing run.

## Common Errors

**Billing Due List app shows no items**
→ Selection criteria exclude the documents, or items are not yet due. Widen the date range or verify the billing date and sold-to party filter.

**Documents created but not posted to accounting**
→ *Automatically post billing documents* was not active. Go to the Manage Billing Documents app and manually release documents to accounting.

**Temporary billing document cannot be saved**
→ Missing or incorrect data (account determination error, incomplete master data). Review the error log in the document and resolve before saving.

## Cross-References
- See also: billing-billing-document-creation-methods-001
- See also: billing-invoice-list-001
- See also: configuration-billing-output-management-brfplus-001
