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
transactions: []
tables: []
aliases:
  - material determination
  - determinacion de material
  - sustitucion de material
  - automatic product selection
  - como sustituir materiales automaticamente en pedidos
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Material Determination and Product Selection in SAP SD

## Operational Summary
*Material determination* lets SAP automatically exchange or propose materials in a sales document. The course explains manual product selection, automatic product selection, substitution reasons, master records, and condition technique. During order entry, the material entered by the customer can be replaced by a substitute, and SAP continues processing with the substitute for availability check, pricing, delivery, and billing.

## Questions This Chunk Answers
- What is material determination in SAP SD?
- How does manual product selection differ from automatic product selection?
- What role does the substitution reason play?
- How does the sequence of substitute materials influence automatic product selection?
- How does condition technique control material determination?

## What This Configuration Controls
Material determination controls whether and how an entered material is replaced or selected in the sales document. A master record defines the substitute materials and the substitution reason. The substitution reason defines the substitution rule. The course names examples such as customized material, EAN number, manual product selection, and automatic product selection depending on availability in order and delivery.

## SPRO Path or Direct T-code
The source states that master records for material determination are maintained in the Sales and Distribution master data menu under *Products*. It does not provide a direct transaction code, so `transactions` remains empty.

## Key Parameters
| Field or setting | Description | Typical Values |
|---|---|---|
| *Material determination procedure* | Assigned to a sales document type and contains determination Customizing | Procedure with one or more condition types |
| *Condition type* | Represents a material determination access strategy step | Customizing-defined condition type |
| *Access sequence* | Search strategy assigned to a condition type | One or more accesses |
| *Condition table* | Search key used to find valid master records | Material, material/customer, or custom keys |
| *Substitution reason* | Defines how the material is determined | Manual or automatic substitution behavior |
| *Substitute sequence* | Priority order for candidate materials | First entry has priority unless unavailable |
| *Validity period* | Limits when the master record applies | Date range |

## Configuration Impact
Manual product selection does not automatically replace the product. Instead, SAP displays a list of substitution materials and master-record information so the user can choose. The system can show quantities that can be confirmed on the requested delivery date and, if full confirmation is not possible, the date on which full delivery is possible.

Automatic product selection replaces the entered material automatically if it is unavailable. SAP tries to fill the order quantity with the first material in the material determination master record and then continues with the next material if there is not enough stock. If the original entered material should be included in substitution, it must appear in the substitution list. Product attributes in material and customer master records can exclude particular materials from product selection.

The source also notes that material determination can be re-run when delivery is created. This matters because availability may have changed between order entry and delivery creation.

## Common Configuration Errors
**Original material is not considered during substitution**
-> Include the originally entered material in the substitution list if its available stock should be consumed.

**Manual selection expected but SAP replaces automatically**
-> Review the substitution reason assigned in the material determination master record.

**Substitution changes between order and delivery**
-> Re-execution at delivery creation may be active, allowing the result to change based on the newer availability situation.

**No visibility into how the substitute was found**
-> Activate material determination analysis in the sales document before entering items.

## Cross-References
- Prior step: order-management-value-contracts-001
- Next step: master-data-material-listing-exclusion-001
- See also: special-processes-sales-workshop-scenarios-001
