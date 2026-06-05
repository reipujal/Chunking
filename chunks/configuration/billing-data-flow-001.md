---
schema_version: 1
id: configuration-billing-data-flow-001
title: "Data Flow and Reference Documents in Billing"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "33-35"
    source_type: "A"
    role: "primary"
transactions: [VOFM]
tables: []
aliases:
  - data flow
  - flujo de datos
  - reference document
  - documento de referencia
level: functional
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Except for external transactions, every billing document requires a reference document. The system uses copying control rules and data transfer routines (VOFM) to determine how data flows from the underlying reference document (e.g., an order or a delivery) into the newly created billing document.

## Questions This Chunk Answers
- What types of reference documents can be used to generate a billing document?
- How is the flow of data controlled during invoice creation?

## Reference Documents
When billing explicitly, you must enter the number of a reference document as the transaction to be billed. Examples of reference document types include:
- Sales document or delivery (for standard invoices and pro forma invoices)
- Credit/Debit memo request or a previous billing document (for credit/debit memos)
- Returns document (for returns credit memos)
- Invoice correction request (for credit memos)
- Billing document (for cancellation invoices / invoice lists)
- External transaction (for billing document external transactions)
- Delivery (for intercompany billing)
- Rebate request (for rebate credit memos)

## Data Control Options
You can heavily influence the data flow from the reference documents to the billing documents using Customizing (billing types and copying control). Controls can be applied at two levels:

- **At Header Level**: Control over foreign trade data, allocation number, reference number, and item number assignment.
- **At Item Level**: Control over the quantity to be billed and the pricing rules.

Additionally, data transfer routines can be customized using transaction `VOFM` to meet individual requirements. For example, a routine can be designed to copy terms of payment directly from the customer master instead of adopting the terms from the preceding sales document.
