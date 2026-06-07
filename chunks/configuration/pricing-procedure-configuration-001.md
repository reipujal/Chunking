---
schema_version: 1
id: configuration-pricing-procedure-configuration-001
title: "Pricing Procedure Configuration in SAP SD"
area: configuration
process_tags: [order-to-cash, pricing]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "25-39"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - pricing procedure Customizing
  - configuración esquema de precios
  - cómo configurar un esquema de precios SAP
  - condition table Customizing
  - tabla de condición configuración
  - access sequence configuration
  - configuración secuencia de acceso
  - pricing procedure determination Customizing
  - requirement routines pricing
  - rutinas de requisito precios SAP
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Pricing Procedure Configuration in SAP SD

## Operational Summary
Configuring pricing in SAP SD follows a reverse-logic sequence: the final goal is to find a condition record with the right key, so configuration starts at the most granular level (condition table) and works upward to the pricing procedure and its determination. The five main objects to configure are condition tables, access sequences, condition types, pricing procedures, and procedure determination. Additional elements — new fields, requirement routines, and formulas — handle complex scenarios beyond standard Customizing.

## Questions This Chunk Answers
- In what order are pricing configuration objects created?
- What does a condition table define and how is it structured?
- What is an access sequence and how does it control condition table searches?
- What does a condition type control in Customizing?
- How does SAP determine which pricing procedure to use for a sales document?
- What is the counter field in a pricing procedure and when is it needed?
- How are requirement routines and formulas used to extend standard pricing logic?

## What This Configuration Controls
The condition technique in SD pricing requires five interrelated configuration objects, created in this order:

1. **Condition table** → defines the key fields for condition records
2. **Access sequence** → defines the search hierarchy across condition tables
3. **Condition type** → defines pricing properties; assigned to an access sequence
4. **Pricing procedure** → assembles condition types in the required processing sequence
5. **Procedure determination** → selects the correct procedure per sales context

## SPRO Path or Direct T-code
Not stated in source. Navigate via IMG: Sales and Distribution → Basic Functions → Pricing → Pricing Control.

## Key Parameters

### Condition Table Configuration
| Parameter | Description |
|---|---|
| Key fields | Must appear at the top of the table; define the unique key for condition records |
| Customer name-space | Tables 501–999 are reserved for customer-defined tables |
| Field placement | Each field is placed in the header or item part of the fast entry screen |

### Access Sequence Configuration
| Parameter | Description |
|---|---|
| Accesses | One or more condition tables; arranged from specific to general |
| Source field override | Within each access, specify an alternative document field (e.g., pricing material instead of material; ship-to party instead of sold-to party; local currency instead of document currency) |
| Restriction-dependent access | An access is only evaluated when a defined requirement is met (e.g., PR00's third access applies only when the document currency differs from local currency — restriction 3) |

### Condition Type Configuration
After creating the access sequence, assign it to a condition type. Condition type characteristics include whether the condition represents a surcharge or discount and whether it depends on values or quantities.

### Pricing Procedure Determination
The pricing procedure is determined from three factors:
1. Sales area (sales organization, distribution channel, division)
2. Customer pricing procedure — set in the customer master
3. Document pricing procedure — assigned to the sales document type

### Counter Field
If manual conditions must retain their input sequence, they must appear at the same level in the pricing procedure. The *Counter* subkey allows multiple conditions at the same level without overwriting each other.

## Configuration Impact

**New fields for pricing.** If a required field is not in the standard field catalog, it can be added via the release-neutral procedure in Customizing: Sales and Distribution → System Modifications → Create New Fields Using Condition Technique.

**Requirement routines and formulas.** Requirement routines define dependencies and improve performance (skip irrelevant accesses). Formulas expand standard configuration for unique requirements. Both are written in ABAP and accessible in Customizing under System Modifications. SAP recommends copying a standard object before modifying it.

**Pricing elements summary.** Each element has a distinct role:
- Condition table → key fields of condition records
- Access sequence → search hierarchy for condition record lookup
- Condition type → properties and behavior of pricing conditions
- Pricing procedure → sequence and processing rules for all condition types
- Procedure determination → selects the correct procedure per context

These elements must be designed with the final objective in mind from the start: which key combination(s) do condition records need to use, and in what order should the system search for them.

## Common Configuration Errors
**System cannot find a condition record even though it exists**
-> Check the access sequence: the condition table used as the access key may not match the fields populated in the document. Also verify source field overrides in the access.

**Wrong pricing procedure used for a sales document**
-> Check all three inputs to procedure determination: sales area assignment, customer pricing procedure in the customer master, and document pricing procedure in the sales document type Customizing.

**Manual conditions overwrite each other at the same level**
-> Use the Counter subkey to distinguish manual conditions entered at the same pricing procedure level.

**Standard pricing logic insufficient for a specific business case**
-> Implement requirement routines or formulas. Always copy an existing standard routine before modifying.

## Cross-References
- Prior step: pricing-condition-technique-overview-001
- Next step: pricing-condition-records-001
- See also: configuration-sales-document-type-control-001
