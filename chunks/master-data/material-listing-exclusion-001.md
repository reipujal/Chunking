---
schema_version: 1
id: master-data-material-listing-exclusion-001
title: "Material Listing and Exclusion in SAP SD"
area: master-data
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "137-142"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - material listing
  - lista de materiales permitidos
  - exclusion de materiales
  - customer material listing exclusion
  - como limitar materiales que puede comprar un cliente
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Material Listing and Exclusion in SAP SD

## Operational Summary
*Material listing* and *material exclusion* control which materials a customer may receive in a sales process. Listing is restrictive: the customer should receive only the materials included in the listing. Exclusion is prohibitive: the customer may receive other materials, but not the materials explicitly excluded. Both functions are controlled using condition technique and can be activated in the sales document type.

## Questions This Chunk Answers
- What is material listing in SAP SD?
- What is material exclusion in SAP SD?
- How do listing and exclusion differ functionally?
- Which technique controls material listing and exclusion?
- Where is the check activated for a sales document?

## What This Configuration Controls
Material listing controls permitted materials. The course example uses master records with a key for customer and material numbers and notes that this key is delivered in the standard system. The access sequence for the condition type searches for valid master records for both the sold-to party and the payer. If listing is in place, the business intent is that the customer receives only specific materials.

Material exclusion controls prohibited materials. It ensures that the customer does not receive specific materials. Like listing, exclusion is controlled with the condition technique.

## SPRO Path or Direct T-code
Not stated in source.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Sales document type check* | Determines whether listing or exclusion is checked | Active or inactive |
| *Condition type* | Controls listing or exclusion record lookup | Listing or exclusion condition type |
| *Access sequence* | Search strategy for master records | Sold-to/material, payer/material, or custom keys |
| *Condition table key* | Defines the fields used for lookup | Customer/material, customer group/material, customer/product hierarchy |
| *Master record validity* | Determines when the listing or exclusion applies | Date range |

## Configuration Impact
Material listing is a positive list: only listed materials may be ordered. If the requested material is not on the valid list, the order should be prevented.

Material exclusion works as a negative list. It prevents the customer from receiving certain materials, while other non-excluded materials remain possible. Exclusion does not create substitute sub-items — it simply blocks the listed materials. Use material determination/product selection for substitution.

Because both functions use condition technique, the search key is flexible. The source names customer group/material and customer/product hierarchy as examples of custom keys beyond the delivered customer/material key.

## Common Configuration Errors
**Customer can order a material that should be restricted**
-> Check whether material listing is activated in the sales document type and whether a valid listing master record exists for the correct key.

**Exclusion expected to substitute another material**
-> Material exclusion does not create substitute sub-items; use material determination/product selection for substitution.

**Listing checks only one partner**
-> The delivered access sequence in the example searches valid records for sold-to party and payer. Review access sequence design if partner-based behavior differs.

## Cross-References
- Prior step: master-data-material-determination-001
- Next step: pricing-free-goods-001
- See also: order-management-sales-order-source-of-data-001
