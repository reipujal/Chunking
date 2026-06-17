---
schema_version: 1
id: configuration-text-control-determination-001
title: "Text Determination Configuration in SAP SD"
area: configuration
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    pages: "36-48"
    source_type: A
    role: primary
transactions:
  - VOFM
tables: []
aliases:
  - text control SAP SD
  - text determination procedure
  - access sequence text
  - procedimiento de determinación de texto
  - secuencia de acceso texto
  - how to configure text control in SAP SD
  - text type Customizing
  - VOFM text routines
  - referenced text vs copied text SAP
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Text Determination Configuration in SAP SD

## Operational Summary
*Text control* is the mechanism by which SAP S/4HANA Sales automatically determines which texts appear in sales, delivery, and billing documents — and from which sources those texts originate. It is configured through a six-step process: defining *text types*, organizing them into *text determination procedures*, assigning *access sequences* that specify the search strategy, and binding the procedures to document types and item categories. Text control also governs whether an adopted text is a live reference to the source or a static copy.

## Questions This Chunk Answers
- What is the six-step process for configuring text control in SAP SD?
- What is a text type and how are custom text types created?
- What is an access sequence in text determination and how is it structured?
- How is a text determination procedure assigned to a document type or item category?
- What is the difference between referencing a text and copying a text?
- How are texts from preceding documents brought into billing documents?
- How do you create customer-specific data transfer routines for texts?

## What This Configuration Controls
Text determination configuration controls:
- Which text types are active for each document type and item category
- The order in which the system searches for a text (from which objects, in which sequence)
- Whether a found text is copied (static duplicate) or referenced (dynamic link)
- Whether a text is mandatory (included in the incompleteness log) or optional
- Whether the text determination analysis is available for troubleshooting

## Six-Step Configuration Process

Text control is set up in the following sequence:

1. **Create text types for a document text object.** A text type defines a category of text within a specific text object (e.g., a text type for "Shipping Instructions" within the sales order header object).
2. **Define text determination procedures.** A procedure groups all text types relevant to a specific text object (e.g., all text types that can appear on a sales order header).
3. **Assign text types to the procedures.** Each text type used in the document's text object is listed in the procedure, with its specific control attributes.
4. **Assign the text determination procedure to the relevant document type or item category.** This binding activates the procedure whenever a document of that type is created or changed.
5. **Define an access sequence for every text type in the procedure.** The access sequence defines the search path the system follows to locate a text — which text objects to search, in which order, and under what conditions.
6. **Define specific controls for each text type.** These controls include: whether the text is mandatory (incompleteness log), whether it is determined automatically, and whether it is shown in a popup window when transferred to the document.

## Text Type

A *text type* belongs to a specific *text object* (for example, the customer master, the sales order header, or the delivery item). SAP S/4HANA provides a large set of standard text types. Organizations can create additional custom text types for each text object to meet specific business needs. Custom text types are then incorporated into text determination procedures to become active in document processing.

## Access Sequence

An *access sequence* is the search strategy the system uses to locate a text automatically. It consists of individual *access steps*, each pointing to a specific text object and text type as the source. The system executes the access steps in sequence until it finds a text that satisfies the conditions.

Each access step can be restricted by conditions such as:
- A specific partner function (for example, only search in the sold-to party's customer master)
- A specific language
- Any other configurable condition

Access sequences are searched **from the most specific to the most general**. If a new access sequence is created or an existing one is modified, it must be generated (regenerated) to activate the changes.

## Permitted Text Objects

The text objects available in SD — and therefore usable in access sequence steps — are defined in the system's allowed values for text determination. These include customer master sub-objects, material master, customer-material info record, preceding SD documents, and general standard texts. The text object selected in each access step determines which entity the system reads to find the text.

## Text Determination Procedure

A *text determination procedure* collects all the text types to be used for a specific text object. For example, a procedure for the sales order header text object lists every text type the system can place in the order header. Procedures can be created or adapted per text object.

An important distinction exists between procedures for **customers** and procedures for **documents**:
- Procedures for **customer text objects** do not use access sequences — customer master data is essentially static, so texts are simply read directly from the relevant master record.
- Procedures for **document text objects** use access sequences to find texts dynamically.

For document procedures, each text type entry can also specify:
- Whether the text is **mandatory** (the incompleteness log checks for it)
- Whether the text should be **determined automatically**
- Whether a **popup window** displays the text when it is first transferred to the document

## Procedure Assignment

Each text determination procedure must be assigned to the relevant business object. The assignment key determines which procedure is used when:

- For **customer master records**: the procedure is assigned to the *account group*. When a customer is created under that account group, the system applies the corresponding procedure.
- For **sales document header texts**: the procedure is assigned to the *sales document type*.
- For **sales document item texts**: the procedure is assigned to the *item category*.

## Text Determination Analysis

SAP S/4HANA provides an analysis function accessible from the text maintenance screens of sales documents (both create and change modes). To access it: navigate to *Goto → Header (or Item) → Texts*, then choose the *Log* button. The analysis shows which text types were determined, which access steps were executed, and which source provided the text. The analysis screen also offers a direct link to Customizing, allowing configuration adjustments directly from the analysis result.

## References and Copies

For each text type in a text determination procedure, the configuration specifies whether the adopted text is **referenced** or **copied**:

**Referenced text** (reference to source):
- The text in the target document is a live pointer to the source text.
- If the source text changes (in document 1), the change is immediately visible via the reference (in document 2).
- If the referenced text is edited in the target document, a new independent copy is stored automatically; subsequent changes to the source no longer affect the target.

**Copied text** (static duplicate):
- The text is fully duplicated at copy time.
- Changes to the original text do not affect copies in other documents.
- Copying requires more storage than referencing. The CLAUDE.md guideline states: choose copying only when it is a functional necessity, not as a default.

## Billing Document Text Source Selection

For a billing document, the Customizing of the *billing type* allows selection of the preceding document for the text objects VBBK (billing header) and VBBP (billing item). This selection applies to all text types of that billing document:
- If the *Text Delivery* checkbox is selected, texts are taken from the **outbound delivery**.
- If not selected, texts are taken from the **sales order**.

This control point allows billing teams to decide whether the invoice reflects the delivery's texts or the order's texts — a relevant choice when delivery conditions differ from order conditions.

## SPRO Path

Not stated in source.

## Customer-Specific Data Transfer Routines

Standard text determination covers the most common use cases. For customer-specific text transfer logic, additional *data transfer routines* for texts can be created using transaction **VOFM**. The namespace for customer-specific routines uses two-digit keys between 50 and 99. Sample routines 1 and 2 (standard) document the available data structures.

## Cross-References
- Prior step: configuration-text-sources-sd-001
- See also: configuration-sales-document-type-control-001
- See also: configuration-delivery-item-category-001
