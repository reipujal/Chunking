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
    pages: "49-50"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - fiori apps
  - aplicaciones fiori
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
In SAP S/4HANA, the traditional transactional processing for creating billing documents is augmented by specific SAP Fiori apps like the *Create Billing Documents – Billing Due List Items* app and the *Manage Billing Documents* app, which offer enhanced filtering, automatic posting options, and temporary preview documents.

## Questions This Chunk Answers
- What are the main SAP Fiori apps for creating and managing SD billing documents?
- What are Temporary Billing Documents?

## Create Billing Documents – Billing Due List Items App
This app provides broad filtering and selection options. Via the Billing Settings, you can configure automatic behaviors:
- **Enter billing date and type**: Prompts for required billing date and type before billing.
- **Create separate billing document per item**: Overrides combination rules to invoice item-by-item.
- **Automatically post billing documents**: Triggers automatic posting to accounting and outputs (e.g., e-mail). If disabled, posting must be triggered manually via the *Manage Billing Documents* app.
- **Display billing documents after creation**: Generates a **Temporary Billing Document**. This allows the user to view the draft document visually. Saving it converts it to a final billing document, whereas discarding it safely returns the documents to the due list without needing to process a formal cancellation. Custom fields can also be used to filter or sort the items securely.

## Manage Billing Documents App
The *Manage Billing Documents* app is used to review, change, display, cancel, and manually post standard invoices, cancellations, and credit memos. It provides seamless navigation between selected documents for updates, detailed summary displays (object page), and allows generating PDF-based print previews.
