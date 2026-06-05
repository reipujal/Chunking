---
schema_version: 1
id: billing-down-payment-processing-001
title: "Down Payment Processing in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "75-80"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - down payment
  - pago a cuenta
  - anticipo
  - FAZ
  - AZWR
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Arranging down payments is standard practice in plant engineering or capital goods sales. SAP handles down payments seamlessly by intertwining SD milestone billing plans with specialized conditions and utilizing special G/L indicators in Financial Accounting.

## Questions This Chunk Answers
- How is a down payment request generated in SAP SD?
- How are down payments cleared during partial or final invoicing?
- Which specific condition types control down payment pricing calculations?

## Process Flow

### 1. Generating the Request
Down payment obligations are recorded as specific dates immediately within the sales order's milestone billing plan. The transaction utilizes specific billing rules (Rule 4 for percentage-based, Rule 5 for value-related). 
At the due date, you automatically or explicitly create a down payment request to send to the customer using billing type `FAZ`. This maps to a statistical (noted) FI item under a special G/L indicator `F`. 

### 2. Condition Type `AZWR`
Standard items use typical pricing conditions like `PR00`. However, down payment items explicitly utilize the special condition type `AZWR`. When `AZWR` is determined (categorized with rule B for fixed amounts), all other standard condition types are set to inactive.

### 3. Incoming Payment
The customer pays the down payment. The amount is assigned to the request in FI, registering as a down payment clearing under special G/L indicator `A`. The status of the down payment request in the SD document flow securely shifts to *Cleared*.

### 4. Down Payment Clearing
When a partial invoice (proportional settlement) or final invoice is processed, the system automatically detects the down payments already made by the customer. The calculated down payment value is appended to the billing document as an item to be explicitly cleared and deducted from the gross receivables, reflecting the accurate outstanding balance owed by the customer.
