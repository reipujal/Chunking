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
    pages: "129-130"
    source_type: "A"
    role: "primary"
transactions: []
tables: []
aliases:
  - flexible numbering
  - numeración flexible
  - alphanumeric invoice number
  - número de factura alfanumérico
  - SD_BIL_FLEX_NUMBERING
  - BAdI billing numbering
  - invoice number prefix
  - prefijo número de factura
  - country-specific invoice number
  - numeración de factura por país
  - number range billing
  - rango de números factura
level: technical
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-05
---

# Flexible Billing Document Numbering and Prefixes

## Operational Summary
Standard SAP billing assigns document numbers from fixed number ranges defined per billing type. *Flexible Billing Document Numbering* extends this by allowing a BAdI (`SD_BIL_FLEX_NUMBERING`) to dynamically assign number ranges and alphanumeric prefixes based on any header field attribute (e.g., company code, sales organization, country). This enables legal number series compliance in multinational deployments — for example, different invoice number sequences for German and French branches within the same billing type.

## Questions This Chunk Answers
- How do you implement alphanumeric invoice numbering in SAP S/4HANA?
- How can different invoice number sequences be configured per country or branch?
- What is the BAdI SD_BIL_FLEX_NUMBERING and how does it work?
- How are number range prefixes constructed and how long can they be?
- Is flexible numbering a standard feature or does it require custom development?
- What is an example use case for flexible billing numbering?

## What This Configuration Controls
This configuration controls the document number format and assignment logic for billing documents beyond standard number ranges:
- **Dynamic number range selection**: the BAdI evaluates header attributes at document creation and routes the number assignment to the matching range
- **Alphanumeric prefixes**: up to 5 characters can be prepended to the numeric sequence, creating legal invoice series like `ABC1234567`
- **Country-specific sequences**: separate number series for different legal entities or countries within one billing type

## SPRO Path or Direct T-code
BAdI implementation: Sales and Distribution → Billing → Billing Documents → BAdI: Flexible Billing Document Numbering (`SD_BIL_FLEX_NUMBERING`)

Standard number ranges (prerequisite): Sales and Distribution → Billing → Billing Documents → Define Number Ranges for Billing Documents

## Key Parameters

| Parameter | Description |
|---|---|
| BAdI: SD_BIL_FLEX_NUMBERING | Filter-enabled BAdI; activated per billing type; evaluates header fields to select number range |
| Number range interval | Standard SAP number range key (e.g., G1 for German branch, F1 for French branch) |
| Prefix (max 5 chars) | Alphanumeric prefix prepended to the numeric interval, creating legal series identifiers |
| Header attribute evaluated | Any billing document header field (company code, sales organization, country) |

**Example**: Corporation with German and French branches using billing type F2:
- German branch → BAdI routes to range `G1` → produces numbers like `G10000001`
- French branch → BAdI routes to range `F1` → produces numbers like `F10000001`

## Configuration Impact
Flexible numbering is essential for legal compliance in countries with strict invoice numbering requirements (sequential, gapless, prefixed by branch or year). Without it, SAP's standard single number range per billing type cannot produce the country-specific formats required by tax authorities. Incorrect BAdI implementation can produce duplicate document numbers if range overlaps are not avoided.

## Common Configuration Errors

**BAdI implemented but all documents still use the default number range**
→ The BAdI filter condition does not match the billing type or header attributes being processed. Verify the filter settings in the BAdI implementation match the relevant billing types.

**Alphanumeric prefix causes number range exhaustion faster than expected**
→ The prefix opens a new subspace, but the numeric interval within that subspace is finite. Plan the interval range size to accommodate expected document volume.

## Cross-References
- See also: configuration-billing-types-sap-s4hana-001
