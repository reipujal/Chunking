---
schema_version: 1
id: configuration-billing-copying-control-001
title: "Copying Control in SAP SD Billing"
area: configuration
process_tags: [order-to-cash, billing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf"
    pages: "44-47"
    source_type: "A"
    role: "primary"
transactions: [VOFM]
tables: []
aliases:
  - copying control
  - control de copia
  - control de copia factura
  - billing quantity
  - cantidad a facturar
  - pricing type billing
  - tipo de precio facturación
  - VOFM routines
  - rutinas VOFM
  - data transfer routine
  - rutina de transferencia de datos
  - copying requirements
  - requisitos de copia
level: functional
status: draft
quality: medium
created: 2026-06-05
last_updated: 2026-06-17
---

# Copying Control in SAP SD Billing

## Operational Summary
Copying control defines how data flows from a reference document (sales order, delivery, or prior billing document) into the newly created billing document. It is configured at header level (source document type → billing type) and item level (source document type + item category → billing type). At item level, it controls the billing quantity, the pricing behavior, and whether goods issue must be posted before billing is allowed. Custom requirements and data transfer logic can be built using transaction *VOFM*.

## Questions This Chunk Answers
- How is the data transfer from an order or delivery to a billing document configured?
- What controls the billing quantity — order quantity, delivery quantity, or another?
- What are the pricing types and what does each one do when copying?
- Can goods issue be made mandatory before billing is allowed?
- Where are the header-level and item-level controls maintained?
- How do you customize data transfer logic using VOFM?

## What This Configuration Controls
Copying control specifies a **source document type** to **target billing type** mapping. It is configured at two levels:

### Header Level Controls
- **Reference document**: which document types can serve as billing references.
- **Determination**: rules for foreign trade data, allocation numbers, reference numbers, and item number assignment.

### Item Level Controls
- **Target matching**: target billing type mapped against source sales document type + item category.
- **Billing quantity**: determines which quantity is invoiced (see Key Parameters table).
- **Pricing and exchange rate**: determines whether pricing is re-determined or copied from the reference.
- **Copying requirements**: conditions that must be met before billing is allowed (e.g., goods issue must be posted).

## SPRO Path or Direct T-code
Sales and Distribution → Billing → Billing Documents → Maintain Copying Control for Billing Documents
- Sub-node: *Copying Control: Sales Document to Billing Document*
- Sub-node: *Copying Control: Delivery to Billing Document*

## Key Parameters

### Billing Quantity Options
| Billing Document | Billing Quantity |
|---|---|
| Order-based (e.g., standard order) | Order quantity minus quantity already billed |
| Delivery-based (e.g., billing types F1, F2) | Quantity delivered minus quantity already billed |
| Credit memo request | Order quantity minus quantity already billed |
| Pro forma invoice F5 | Order quantity |
| Pro forma invoice F8 | Delivery quantity |

### Pricing Types
| Pricing Type | Behavior |
|---|---|
| A | Copy from reference and update according to scale |
| B | Re-determine pricing entirely |
| C | Copy manual elements; re-determine the rest |
| D | Copy all elements unchanged |
| G | Copy unchanged; re-determine tax conditions |
| H | Copy unchanged; re-determine freight conditions |

## Configuration Impact
Incorrect copying control is the most common root cause of billing errors: wrong quantities billed, prices not updated after order changes, or goods-issue-not-posted errors. The copying requirement controls whether the system enforces business rules (e.g., GI must be complete) before billing proceeds.

## Common Configuration Errors

**Billing document created with wrong quantity**
→ The billing quantity setting in copying control does not match the business intention. Verify which quantity rule is assigned at item level for the relevant source document type and item category.

**Price on invoice does not reflect changes made after order creation**
→ Pricing type D copies prices unchanged — the invoice reflects the original order price even if conditions were updated. Change to pricing type B or G if repricing is needed.

**"Goods issue has not been posted" error when creating billing**
→ A copying requirement mandating GI (routine 101 or equivalent) is configured for this source-to-target combination. Post GI before billing or adjust the requirement.

## Cross-References
- See also: configuration-sales-copying-control-001 (sales facet of copy control)
- See also: configuration-delivery-process-customizing-001 (delivery facet of copy control)
- Supplementary: S4650 Unit 2 (phys 20-31) — unified cross-chain view of copy control across all three facets; S4650 is supplementary to these three authoritative chunks (density guardrail: not added as secondary source)
- See also: configuration-billing-data-flow-001
- See also: configuration-billing-types-sap-s4hana-001
- See also: billing-invoice-combination-and-split-001
