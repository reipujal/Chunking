---
schema_version: 1
id: configuration-output-determination-sd-001
title: "Output Determination for SD Documents (Condition Technique)"
area: configuration
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    pages: "49-64"
    source_type: A
    role: primary
transactions:
  - SFP
  - SFW5
tables: []
aliases:
  - output determination SAP SD
  - output types sales distribution
  - NAST output condition records
  - determinación de salida SAP ventas
  - tipos de salida SD
  - output timing dispatch time
  - communication strategy output
  - how to configure output in SAP SD
  - BA00 order confirmation output
  - PDF form output SAP
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Output Determination for SD Documents (Condition Technique)

## Operational Summary
In SAP S/4HANA, *output determination* controls which messages are generated from sales, delivery, and billing documents — and to whom, via which medium, and at what time. Output can be used for customer communication (order confirmations, invoices, delivery notes) and internal notifications. The system uses the *condition technique* to determine output: *output condition records* store the relevant properties, and an *access sequence* searches for the applicable record. Output can be issued via print, EDI, internet, or other transmission media.

## Questions This Chunk Answers
- What are output types and how are they used in SAP SD?
- How does the condition technique determine output in SD documents?
- What transmission media are available for output?
- What timing options control when output is dispatched?
- What is a communication strategy and when is it used?
- How does the output determination analysis function work?
- How are PDF-based forms used for SD output?
- How do you modify an existing output type (Case 1 and Case 2)?
- How do you integrate a new customer-specific output type?

## What This Configuration Controls

Output determination configuration governs:
- Which output types are proposed in which SD documents (sales, delivery, billing)
- The recipient (determined via partner function in the condition record)
- The transmission medium (print, EDI, email, internet, etc.)
- The dispatch timing (automatic on save, batch program, user-scheduled)
- The form layout (PDF-based form or legacy SAPscript)
- The communication strategy for external output routing

## Output Types

An *output type* defines a category of output message. Examples in SD: order confirmation (BA00), delivery note, invoice. Output types can operate at header level (covering the entire document) or at item level (covering individual line items). Each output type is assigned a *processing program* and one or more form definitions per transmission medium.

The output type, once determined for a document, is placed in the document's output list with its properties: transmission medium, dispatch time, and recipient partner function. Multiple output types can be active for the same document simultaneously.

Output can target different document types within SD: quotations, sales orders, outbound deliveries, and billing documents each have their own output types. Header output covers data from the entire document; item output covers information specific to individual items. Each output type is associated with a specific document type in the output determination procedure for that document category.

## Condition Technique for Output Determination

Output determination reuses the same *condition technique* used by pricing and text determination:

- An **output condition record** stores the properties of an output type for a specific context (for example: for sales organization 1000, send output type BA00 to the sold-to party via EDI at time of posting).
- The condition record contains: transmission medium, dispatch time, language, and partner function.
- An **access sequence** defines the search path used to find the applicable condition record.
- If a condition record is found whose requirements are met, the system proposes that output type with those properties in the document.

Output is sent to the partner matching the partner function specified in the condition record. It is also possible to create output that is not dependent on a partner (for example, warehouse labels).

## Transmission Media

The *transmission medium* determines how output reaches its destination. Available media in SD include:

| Medium | Example Use Case |
|---|---|
| Print | Physical invoice or delivery note on paper |
| EDI | Electronic Data Interchange with customer systems |
| Internet/email | Online order confirmation or notification |
| Internal | Workflow, internal routing within the company |

Each medium requires a corresponding processing program assigned to the output type in Customizing. The program controls how data is extracted and transferred to the medium.

## Communication Strategy

A *communication strategy* is a prioritized sequence of communication types used for external output. When external output is to be sent, the system works through the strategy's sequence until it finds valid communication data (an address) in *Central Address Management*. The communication strategy is specified in the additional data of the output condition record. It enables fallback routing — for example, try EDI first, then email if no EDI address is found.

## Timing of Output

Output can be dispatched at four different points in time:

1. **Timing 1 (next batch run)**: a standard batch program (`RSNAST00`) processes output at regular intervals. Output with timing 1 is selected the next time the batch runs.
2. **Timing 2 (user-specified time)**: similar to timing 1, but the user specifies a particular time for dispatch. The batch program processes it at that time.
3. **Timing 3 (special selection program, online or batch)**: dedicated selection programs per document type (deliveries, billing documents) process output online or in batch. Scheduling a regular batch achieves the same effect as timing 1.
4. **Timing 4 (automatic, immediate)**: output is issued automatically as soon as the document is posted. No batch program is needed.

## Access Sequences for Output Determination

An *access sequence* in output determination is a search strategy through a sequence of condition tables. Each access step contains the name of a condition table with the key fields used to search for output condition records.

The search always proceeds **from the most specific to the most general**: a narrower combination of key fields (e.g., sales organization + distribution channel + document type) is checked before a broader one (e.g., sales organization alone).

To create a new access sequence, copy an existing similar one and adjust the copies. Customer-specific access sequences must begin with **Y or Z** (the namespaces reserved in the standard system for customer developments).

## Output Determination Analysis

The output determination analysis function is available on the output screen of SD documents in create and change mode. To use it: choose *Extras → Output → Header (or Item) → Edit*, then *Goto → Determination analysis*. The analysis shows which output types were evaluated, which access steps were executed, which condition records were found, and why a particular output was proposed or rejected. This is the primary troubleshooting tool for output issues.

## PDF-Based Forms

SAP introduced PDF-based forms in the Form Builder to replace legacy SAPscript forms for SD output. Technical prerequisites:
- SAP ERP 6.0 Enhancement Package 2 installed
- Business function SD_01 active (transaction **SFW5**)

Standard PDF forms available:
- `SD_SDOC_FORM01` — order confirmation (processing program: `SD_SDOC_PRINT01`)
- `SD_INVOICE_FORM01` — invoice / billing document
- `SD_BIL_LIST_FORM01` — invoice list
- `SD_CAS_FORM01` — customer contact
- `SD_CFS_FORM01` — sales summary
- `SD_CAS_MAIL_FORM01` — mailing example for customer contact

The Form Builder is accessed via transaction **SFP** (SAP Easy Access → Tools → Form Printout → Interactive Forms). Customers can create their own forms; forms are assigned to the output type in Customizing, exactly as with SAPscript.

## Adjusting Output Types

### Case 1: Simple Form Modification

Simple changes — adding a field, a logo, or a barcode to an existing form without needing new preparation logic or new fields in the communication structure — can be made directly in the PDF or SAPscript form. Prerequisites for a simple modification:
- The field already exists in the communication structure.
- The field is not yet included in the form.
- The field can be integrated into the form within an existing format element.

### Case 2: New Fields Requiring Communication Structure Extension

When a new field does not exist in the communication structure, additional logic is needed. The field can be populated using a standard BAdI. New fields for printing are added to INCLUDE structures that are integrated into the communication structures:

| Document Type | Header INCLUDE | Item INCLUDE |
|---|---|---|
| Sales (order) | VBDKAZ (in VBDKA) | VBDPAZ (in VBDPA) |
| Delivery | VBDKLZ (in VBDKL) | VBDPLZ (in VBDPL) |
| Billing | VBDKRZ (in VBDKR) | VBDPRZ (in VBDPR) |

After the INCLUDE is extended, the new field can be placed in the form as in Case 1. Occasionally, direct access to the output processing program is also needed (for example, to read additional data not covered by the communication structure).

### Integrating a New Output Type

New customer-specific output types are normally based on an existing document type. Steps:
1. Copy most of the document data from an existing communication structure.
2. Write a new processing program (named in the customer namespace, starting with Z) that extracts the required data and controls form output. The program must be based on the specified communication structures.
3. Define the layout in a PDF or SAPscript form.
4. Assign the processing program and form to the new output type in Customizing.
5. Add the new output type to the relevant output determination procedure so the system includes it during determination.

**Example**: a special delivery note ZLD0 uses processing program `ZRELE_DELNOTE` and the delivery communication structures VBDKL (document header) and VBDPL (document item).

## SPRO Path

Not stated in source.
Navigate via IMG: Sales and Distribution → Basic Functions → Output Control → Output Determination.

## Common Configuration Errors

| Symptom | Likely Cause |
|---|---|
| Output not proposed in document | Condition record missing or access sequence finds no match; use analysis function to diagnose |
| Wrong recipient for output | Partner function in condition record does not match partner in document |
| Output generated with empty form | Processing program assigned, but form not assigned to the output type/medium combination |
| Custom output type never triggered | Output type not added to the output determination procedure for that document type |

## Cross-References
- See also: configuration-output-management-s4hana-001
- See also: configuration-billing-output-management-brfplus-001
- See also: configuration-billing-types-sap-s4hana-001
