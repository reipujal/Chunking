---
schema_version: 1
id: configuration-text-sources-sd-001
title: "Text Sources and Text Types in SAP SD"
area: configuration
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    pages: "32-35"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - text sources SAP SD
  - text types sales and distribution
  - fuentes de texto SAP ventas
  - tipos de texto SD
  - where do texts come from in sales orders
  - customer master text types
  - material master text SAP
  - notas de venta texto cliente
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Text Sources and Text Types in SAP SD

## Operational Summary
In SAP S/4HANA Sales and Distribution, texts are stored in multiple objects — customer master records, material master records, the customer-material info record, and SD documents themselves — and can flow automatically from one object into another during document processing. Understanding where texts originate and what categories exist is a prerequisite for configuring *text control*, which governs how texts are found and copied across the O2C document chain.

## Questions This Chunk Answers
- Where are texts stored in the SAP SD system?
- What text types are available in the customer master record?
- What text types exist in the material master for SD purposes?
- How do texts move between SD documents and master data records?
- Can texts be maintained in multiple languages in SAP SD?

## Definition

A *text* in SAP SD is a free-form or structured textual entry attached to a business object (master data record or transaction document). Texts are stored within *text objects* — each object type (customer master, material master, sales order, delivery, billing document) maintains its own set of texts. Each text object can hold multiple *text types*, which categorize texts by purpose (e.g., shipping specifications, sales notes). Understanding which text objects exist and which text types they support is the starting point for configuring *text control*.

## Text Objects in SAP SD

Texts reside in distinct *text objects*, each associated with a specific SAP entity. The main text objects used in SD are:

- **Customer master record**: contains texts organized into sub-categories: central texts (usable by any SAP module), accounting-specific texts, sales and distribution-specific texts, and texts for contact persons. Each sub-category supports multiple defined *text types*.
- **Material master record**: contains a *purchase order text* and a *sales text*. The sales text is the main SD-relevant text; it describes the material for sales-facing purposes.
- **Customer-material info record**: stores texts that reflect agreements or specifics for a particular customer-material combination.
- **SD documents**: every sales order, delivery, and billing document carries texts at both the *header level* (applying to the whole document) and the *item level* (applying to individual line items).

## Text Types in the Customer Master

The customer master's SD section supports several standard text types. Examples include:

| Text Type | Purpose |
|---|---|
| Sales notes | Internal notes about the customer for sales staff |
| Marketing notes | Notes for marketing and campaign tracking |
| Shipping specifications | Instructions or requirements for delivery |

Additional text types for contact persons and centrally visible texts exist outside the SD section. Organizations can also create custom text types to meet specific business needs.

## Text Types in the Material Master

The material master contains two SD-relevant texts:
- **Sales text**: describes the material from a sales perspective; this is the text most commonly copied into sales documents.
- **Purchase order text**: used in procurement-oriented contexts; available in SD when relevant to cross-functional processing.

## Texts in SD Documents

Documents maintain texts at header and item levels independently. During order entry, the system can automatically retrieve texts from master data objects and propose them in the document. Users can also edit these proposed texts or add new text entries manually. All text types support multilingual entry — texts can be entered and stored in different languages, and the system can select the appropriate language during document processing.

## Text Flow in Business Processes

In a standard O2C process, texts travel through the document chain as follows:

1. **From master data into documents**: texts stored in the customer master (sales notes, shipping specs) or material master (sales text) are copied into the sales order during order entry, according to the configured *access sequence*.
2. **From document to document**: when a delivery is created from a sales order, or a billing document is created from a delivery, texts can be copied or referenced from the preceding document to the successor.
3. **Standard texts**: a preconfigured standard text (for example, standard terms and conditions or a seasonal greeting) can be inserted into a sales document type automatically.
4. **Language-specific copying**: the system can copy texts in a specific language when multiple language versions of a text exist.

The mechanism that controls which texts are found, from which sources, and whether they are copied or referenced, is *text control* — configured separately via text determination procedures and access sequences.

## Relationship with Other SAP SD Objects

| Related Object | Relationship |
|---|---|
| Text control (text determination procedure) | Defines which text types are active, the access sequence used to find them, and whether texts are copied or referenced |
| Business partner / customer master | Primary source for customer-specific texts (sales notes, shipping specs) |
| Material master | Source for sales text and purchase order text |
| Sales document type / item category | Determines which text determination procedure applies (procedure assignment) |
| Output management | Some output types (e.g., invoices, delivery notes) include text fields populated from text control |

## Cross-References
- Next step: configuration-text-control-determination-001
- See also: master-data-business-partner-master-data-001
- See also: master-data-material-master-sd-001
