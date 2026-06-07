---
schema_version: 1
id: master-data-material-determination-001
title: "Material Determination and Product Selection in SAP SD"
area: master-data
process_tags: [order-to-cash]
chunk_type: configuration
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "127-136"
    source_type: A
    role: primary
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "161-165"
    source_type: A
    role: secondary
transactions: []
tables: []
aliases:
  - material determination
  - determinacion de material
  - sustitucion de material
  - automatic product selection
  - como sustituir materiales automaticamente en pedidos
  - substitution reason EAN number product selection
  - razon sustitucion seleccion producto
  - partial confirmation product selection shortfall
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-08
---

# Material Determination and Product Selection in SAP SD

## Operational Summary
*Material determination* lets SAP automatically exchange or propose materials in a sales document using condition technique. During order entry, the material entered by the customer can be replaced by a configured substitute, and SAP then continues processing with the substitute (availability check, pricing, delivery, billing). No material master record is required for the original material number being replaced. The item overview always shows the originally entered material and the reason for substitution. Material determination can optionally be re-run at delivery creation.

## Questions This Chunk Answers
- What is material determination in SAP SD?
- How does manual product selection differ from automatic product selection?
- What substitution reason codes are standard and what do they control?
- How does the sequence of substitute materials influence automatic product selection?
- How does condition technique control material determination?
- What happens when the original material should also be considered in automatic selection?
- How does partial confirmation of product selection work?

## What This Configuration Controls
Material determination controls whether and how an entered material is replaced or proposed in the sales document. A master record links an entered material to one or more substitutes and assigns a substitution reason. The substitution reason defines the rule — manual selection, automatic replacement by EAN number, automatic replacement based on availability. Multiple substitutes can be defined in a single master record; their sequence determines priority.

**Standard substitution reasons:**
| Reason | Description |
|---|---|
| 0002 | Customized material (replaces with a predefined substitute) |
| 0003 | EAN number (replaces entered EAN with the correct material) |
| 0004 | Automatic product selection depending on availability in the order |
| 0005 | Manual product selection (displays a list for user choice) |
| 0006 | Automatic product selection depending on availability in order and delivery |

## SPRO Path or Direct T-code
Master records for material determination are maintained in the SD master data menu under *Products*. No direct transaction code is provided by the source.

## Key Parameters

| Field or setting | Description | Typical Values |
|---|---|---|
| *Material determination procedure* | Assigned to sales document type; contains all Customizing for determination | Procedure with one or more condition types |
| *Condition type* | One access strategy step; linked to one access sequence | Customizing-defined |
| *Access sequence* | Search strategy; one or more accesses, each with one condition table | Material, material/customer, or custom |
| *Condition table* | Search key for valid master record | Material, customer/material, or similar |
| *Substitution reason* | Defines behavior: manual or automatic | 0002, 0003, 0004, 0005, 0006 |
| *Substitute sequence* | Priority order for candidates in master record | Position in list defines priority |
| *Validity period* | When the master record applies | Date range |

## Configuration Impact

**Manual product selection (reason 0005):** SAP does not automatically replace the product. Instead, it displays a list of all substitution materials and master-record information so the user can choose. To assist selection, SAP shows the quantity confirmable on the requested delivery date. If full confirmation is not possible, it shows the date when full delivery can be made.

**Automatic product selection (reasons 0004 and 0006):** SAP automatically replaces the entered material if it is unavailable. The system tries to fill the order quantity with the first material in the master record. If insufficient stock exists, it moves to the next material in the sequence. Depending on Customizing, the original entered material and the substituted material may appear in the order as main item and sub-item.

**Original material in the substitution list:** if the original material should be included in automatic selection, it must be explicitly entered in the substitution list. Position matters:
- *Case A*: original material is first in the list — its available stock is consumed first, then the next materials.
- *Case B*: original material is not first — stock of earlier materials is consumed first; the original is only considered after earlier entries are depleted.

**Product attributes exclusion:** product attributes in material and customer master records can exclude a specific material from product selection, preventing it from being determined as a substitute.

**Partial confirmation:** when automatic product selection results in only partial confirmation (available quantity less than order quantity), the shortfall quantity can be passed to material planning. An additional sub-item is generated with a specifically defined material to handle the shortfall.

**Re-execution at delivery:** material determination can be configured to re-run when the delivery is created. This allows substitution results to change if availability has shifted between order entry and delivery creation.

**Analysis:** the material determination analysis can be activated in the sales document before entering items (menu path: Environment → Analysis → Material Determination On). It shows detailed information about how materials were determined at each step. Activate before entering the first item — the analysis runs during determination and cannot be triggered retroactively.

**Order confirmation content:** depending on Customizing, the order confirmation printed document can contain either the material originally entered by the customer or the substitution material that was actually determined. This choice is configured per substitution reason.

**Condition technique structure:** one material determination procedure is assigned per sales document type. The procedure contains one or more condition types. Each condition type has one access sequence. Each access in the sequence contains exactly one condition table — the search key used to find a valid master record.

## Common Configuration Errors
**Original material is not considered during automatic substitution**
-> Include the originally entered material in the substitution list. Its position in the list determines when its stock is considered.

**Manual selection expected but SAP replaces automatically**
-> Check the substitution reason in the master record. Reasons 0004 and 0006 trigger automatic replacement; reason 0005 triggers manual selection.

**Substitution result differs between order and delivery**
-> Re-execution at delivery creation may be active. The result can change because availability at delivery time may differ from order time.

**Analysis shows no detail**
-> Activate material determination analysis in the sales document before entering items; it cannot be run retroactively.

## Cross-References
- Prior step: order-management-value-contracts-001
- Next step: master-data-material-listing-exclusion-001
- See also: special-processes-sales-special-business-transactions-001
