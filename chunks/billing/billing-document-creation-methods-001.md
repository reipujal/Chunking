---
schema_version: 1
id: billing-billing-document-creation-methods-001
title: "Methods for Creating Billing Documents in SAP SD"
area: billing
process_tags: [order-to-cash, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "52-56, 59, 125"
    source_type: "A"
    role: "primary"
transactions: [VF01, VF04, VF06]
tables: []
aliases:
  - VF01
  - VF04
  - VF06
  - due list
  - billing due list
  - pool de facturación
  - lista de facturación pendiente
  - background processing
  - procesamiento en background
  - collective billing
  - facturación colectiva
  - billing on request
  - facturación individual
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Methods for Creating Billing Documents in SAP SD

## Operational Summary
SAP provides several methods for creating billing documents, from manual single-document creation to fully automated background collective runs. The *billing due list* (transaction *VF04*) is the standard operational mode — it processes all billable documents collectively, supports combination logic, and can run online or in the background. Individual billing (*VF01*) is used for exceptions. Background scheduling (*VF06*) automates the periodic run.

## Questions This Chunk Answers
- How are individual billing documents created manually?
- How does the billing due list work and what are its selection options?
- How is billing scheduled to run automatically in the background?
- What is the difference between Individual and Collective processing in VF04?
- Can collective billing runs be canceled if an error occurs?
- How does the factory calendar control billing dates for a customer?

## When It Applies and Context
Billing follows goods issue (for delivery-related billing) or order confirmation (for order-related billing). The billing due list is the primary tool for daily billing operations; manual VF01 is used for one-off corrections or exceptions.

## Process Flow and Options

### 1. Billing on Request — Manual (VF01)
Enter the specific document number (order or delivery) to be billed. You can select individual items or partial quantities using the *Item Selection* function, provided the item category is relevant for billing. Use for exceptions; not suitable for volume operations.

### 2. Processing the Billing Due List (VF04)
The standard collective billing tool. Criteria such as sold-to party, billing date, and destination country narrow the worklist.
- **Individual option**: Creates one separate invoice per selected document — no combination.
- **Collective option**: System attempts to combine compatible documents into collective invoices based on combination rules (same payer, same billing date, etc.).

The same list can be scheduled for background execution using transaction *VF06*.

### 3. Billing on Specific Dates
Maintain a factory calendar in the payer's customer master record (field: *Billing schedule*). On the configured dates, the system automatically selects and combines all due deliveries into one collective invoice for that payer.

### 4. Background Processing (VF06)
Schedule billing as recurring background jobs (e.g., every Monday at 2 a.m.). The system can split the worklist into multiple parallel jobs to leverage multiprocessor hardware, improving performance for high-volume operations.

### 5. Cancellation of Collective Runs
If an error affects an entire collective run, the entire run can be canceled. This removes all billing documents within the run and reopens the preceding reference documents for billing.

## Conditions and Restrictions
- Item-level selection in VF01 requires the item category to have billing relevance configured.
- Combination into collective invoices depends on header-level fields (payer, billing date, terms of payment) being identical across items.
- Background jobs require proper authorization and job scheduling configuration.

## Common Errors

**Transaction not in the billing due list (VF04)**
→ The reference document is not yet due for billing, or the billing date falls outside the selection range. Adjust the *Billing date* selection in VF04.

**Items not combined as expected**
→ Header fields (payer, terms of payment, destination country) differ across the documents. Check combination rules in copying control.

**VF06 job runs but creates no documents**
→ No documents are due on that date, or the selection criteria exclude all available items. Verify the billing date range and sold-to/payer filters.

## Cross-References
- Prior step: shipping-goods-issue-ewm-001
- Next step: billing-billing-document-cancellation-001
- See also: configuration-billing-copying-control-001
- See also: configuration-billing-types-sap-s4hana-001
- See also: billing-invoice-list-001
- See also: billing-invoice-combination-and-split-001
- See also: billing-create-billing-documents-fiori-001
