---
schema_version: 1
id: pricing-condition-technique-overview-001
title: "Condition Technique and Pricing Overview in SAP SD"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "8-24"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - condition technique
  - técnica de condición SAP
  - cómo determina SAP el precio automáticamente
  - pricing procedure determination
  - determinación de esquema de precios
  - access sequence pricing
  - secuencia de acceso precios SAP
  - condition record pricing SAP
  - registro de condición precio
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Condition Technique and Pricing Overview in SAP SD

## Operational Summary
Pricing in SAP SD is driven by the *condition technique*: a search mechanism that locates valid *condition records* using a defined *access sequence*, applies them through a *pricing procedure*, and writes the results to the sales document. The pricing procedure is determined at order creation from three inputs — sales area, customer pricing procedure, and document pricing procedure. The process repeats for every *condition type* in the procedure until pricing is complete. Manual changes, header conditions, and pricing types provide additional flexibility for both order creation and billing re-pricing.

## Questions This Chunk Answers
- What is the condition technique in SAP SD pricing?
- How does SAP determine the price automatically when a sales order is created?
- What is a pricing procedure and how is it determined?
- What is an access sequence and how does it find a condition record?
- What is a condition type and what does it control?
- What is a condition table and how does it define a key combination?
- How do header conditions work and how are they distributed across items?
- What are pricing types and when are they used?

## Definition

### Condition Records
*Condition records* store the master data for pricing — prices, surcharges, and discounts. Pricing is most commonly performed at predefined levels in the SAP standard system, but conditions can be defined at any key level. A standard field catalog of commonly used pricing fields is provided in Customizing; additional fields can be added to the catalog.

Each record is defined for a specific *key combination* assigned to a *condition type*. A single condition type (such as PR00 for Price) can have multiple possible key combinations. Key characteristics of condition records:
- A *validity period* restricts the agreement to a specific time window — condition records can be created today for a validity date in the future.
- Values can be structured as *scales* with unlimited levels.
- Each record can carry an upper and lower limit that restricts manual changes (e.g., a discount changeable only between 1% and 3%).

A new *condition maintenance interface* provides mass maintenance based on characteristics such as customers: all condition types and condition tables can be updated simultaneously. For example, material prices, discounts, and surcharges for a specific customer can be displayed and maintained in a single step. The previous transaction-based maintenance (Select Using Condition Type) remains available alongside the new interface.

### Condition Types
The *condition type* determines the category of a condition and controls how it is used. For each condition type, the *scale base type* and *calculation type* are defined in Customizing:

The source lists these as two **independent** sets of options — not one-to-one pairings:

**Possible scale base types:** Value, Quantity, Weight, Volume, Period

**Possible calculation types:** Percentage of an initial value, Fixed amount, Amount by unit of measure, Amount per unit of weight, Amount per unit of volume, Quantity per unit of time

Any scale base type can be combined with any calculation type in Customizing for the condition type.

### Condition Table
A *condition table* is a combination of fields that forms the key for a condition record. Condition tables 501-999 are reserved for customer-defined tables. Key fields must appear at the top of the table. A field can be placed in the header or item part of the condition record's fast entry screen.

### Access Sequence
An *access sequence* is a search strategy that determines the sequence in which SAP reads condition tables to find a valid condition record. Accesses are arranged from specific to general. An access can be made dependent on a requirement, allowing accesses to be skipped when they are unnecessary.

### Pricing Procedure
The *pricing procedure* contains all condition types permitted for a transaction in a defined sequence. Its key Customizing attributes per condition type position:
- **Level (STEP):** sequence of processing and placement in the document.
- **Subtotals:** leave the Condition Type field blank and provide a description to define a subtotal line.
- **Condition formula (AltCBV):** defines an alternative base for calculating the condition value or consolidating subtotals. The default base is the running value after previous conditions.
- **Requirements:** control when and how the condition type is applied.
- **Flags:** mark a condition type as mandatory, manual-only (access sequence ignored), or statistical.

## Purpose in the SD Process

### Pricing Process Flow
When a sales order is created, SAP runs the following sequence for each condition type in the pricing procedure:
1. SAP determines the relevant pricing procedure based on sales area, customer pricing procedure (customer master), and document pricing procedure (sales document type).
2. For each condition type in the procedure, SAP reads its assigned access sequence.
3. SAP reads the access sequence and evaluates each condition table in order (specific to general).
4. SAP searches for a valid condition record using the key defined by the condition table.
5. If the first access fails, SAP moves to the next access in the sequence.
6. When a valid record is found, SAP reads the condition record and copies the value that matches the scale into the document.
7. The process repeats until all condition types in the procedure have been evaluated.

## Structure and Variants

### Manual Price Changes
Prices, surcharges, and discounts determined automatically can be changed manually; the system marks them accordingly. Condition records define the limits within which manual changes are allowed (e.g., a discount changeable only between 1% and 3%). Manual entries are also possible directly on the conditions screen. A condition type can be locked against manual changes in Customizing.

### Header Conditions
Header conditions are valid for all items and entered at document header level. SAP distributes them automatically across items based on net value. The distribution basis can be changed in the pricing procedure's *Alternative Condition Base Value* (AltCBV) field using routines such as:
- 12 = gross weight
- 13 = net weight
- 01 = volume

Two distribution modes: amount copied identically into each item, or amount distributed proportionally by each item's share of the total net value.

### Pricing Types
Pricing types control what happens when *New Pricing* is triggered on a sales or billing document. Pricing type B (carry out new pricing) is the system default. A pricing type can be assigned to the pricing procedure in Customizing to control the behavior of the Edit → New Pricing Document function. Pricing types are supported in both sales orders and billing documents.

### Pricing in the Billing Document
Copying control handles re-pricing of billing documents based on different scenarios. The pricing type in copying control determines how pricing is recalculated when a billing document is created from a sales or delivery document. Every implementation must decide which pricing types to use and when, as this directly affects invoice accuracy and process design.

### Key Facts from Source
- Header conditions are distributed **automatically** among items based on net value — the system does not require manual distribution.
- The condition type controls the calculation type, not the period or amount directly.
- A condition table is a combination of fields that forms the key for a condition record — this is the foundational definition the system uses to search for pricing.
- Pricing agreements can always be limited to a specific validity period defined in the condition record.


**Pricing fields.** The fields available for defining condition table keys are maintained in a standard field catalog in Customizing. Fields not in the standard catalog can be added using a release-neutral procedure. This catalog determines which data from the sales document can be used as search criteria when looking up condition records.

## Relationship with Other SAP SD Objects
- *Condition table* → defines the key → used by *access sequence* → assigned to *condition type* → included in *pricing procedure*
- *Pricing procedure determination* uses: sales area + customer pricing procedure + document pricing procedure
- *Condition records* are the master data that the access sequence searches for
- *PRCD_COND* is the S/4HANA table that stores pricing condition data (replaces KONV from ECC)

## Cross-References
- Next step: configuration-pricing-procedure-configuration-001
- See also: pricing-condition-records-001
- See also: pricing-special-pricing-functions-001
- See also: billing-document-table-structure-001
