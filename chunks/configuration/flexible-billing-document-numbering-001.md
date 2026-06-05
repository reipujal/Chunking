---
schema_version: 1
id: configuration-flexible-billing-document-numbering-001
title: "Flexible Billing Document Numbering and Prefixes"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "121-122"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - flexible numbering
  - numeración flexible
  - prefixes
  - prefijos
level: technical
status: draft
quality: high
created: 2026-06-05
last_updated: 2026-06-05
---

## Operational Summary
Historically constrained strictly by standard number ranges per billing document type, SAP S/4HANA enables dynamic *Flexible Billing Document Numbering* utilizing a designated Business Add-In (BAdI). This logic allocates alphanumeric prefixes and interval rules conditionally based on any header field attribute.

## Questions This Chunk Answers
- How do you implement alphanumeric invoice numbering in SAP S/4HANA?
- How can multinational companies configure different invoice number intervals per country branch dynamically?

## The BAdI: `SD_BIL_FLEX_NUMBERING`
You utilize the filter-enabled Business Add-In (BAdI) `SD_BIL_FLEX_NUMBERING` to execute custom logic overriding standard assignment procedures. The BAdI intercepts the document creation, rapidly evaluating the header attributes (e.g., Company Code, Sales Organization). Based on the evaluation result, it outputs a customized number range interval and optionally prepends alphanumeric prefixes to the outcome.

## Use Case Example
A corporation contains operational branches in both Germany and France. 
- When an `F2` invoice is created by the German branch, the custom logic identifies the branch and selectively diverts the assignment interval to range `G1`. 
- Conversely, for France, the interval diverts to `F1`. 
This fulfills country-specific legal invoicing numbering sequences securely inside the same unified billing type.

## Number Range Prefixes
In circumstances where raw numeric integers limit business requirements, you can merge numeric sequences with alphanumeric prefixes (spanning up to five characters long). 
By creating a prefix like `ABC`, you natively open a completely new subspace for numbering iteration. A prefix coupled securely with interval ranging from `0000001` to `9999999` seamlessly produces legal output numbers formatted natively as `ABC1234567`.
