---
schema_version: 1
id: pricing-condition-records-001
title: "Condition Records: Creation, Maintenance, and Reporting in SAP SD"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "40-53"
    source_type: A
    role: primary

transactions: [VK11, VK12, VK13, SE43]
tables: []
aliases:
  - VK11 crear registro de condición
  - VK12 modificar registro de condición
  - VK13 visualizar registro de condición
  - condition record maintenance SAP pricing
  - mantenimiento registros de condición precio
  - Manage Prices Sales app
  - lista de precios SAP
  - price list SAP SD
  - cómo crear precios en SAP SD
  - release procedure condition records
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Condition Records: Creation, Maintenance, and Reporting in SAP SD

## Operational Summary
*Condition records* are the master data that SAP pricing reads when determining prices, surcharges, and discounts. They can be created individually (VK11), changed (VK12), or displayed (VK13); or maintained in mass via the *Manage Prices - Sales* Fiori app. Creation with reference, copy rules, and release procedures provide structured lifecycle management. Price lists and pricing reports allow analysis and audit of existing condition records.

## Questions This Chunk Answers
- How are condition records created in SAP SD?
- What are the options for mass maintenance of condition records?
- How does the copy function work for condition records?
- What is the release procedure for condition records and when is it used?
- What is the Manage Prices - Sales app and what can it do?
- How are price lists generated from condition records?
- What is the difference between condition-type-based and characteristic-based condition maintenance?

## When It Applies and Context
Condition records are the operational layer of the pricing configuration. They are created during master data maintenance and apply whenever an order, quotation, or contract is processed and pricing is determined. Changes to condition records take effect based on the validity dates defined in each record.

## Process Flow

### Creating Condition Records Individually (VK11)
1. Enter the condition type to create.
2. Select the key combination (condition table) for the record.
3. Enter the key field values (e.g., customer, material), the validity period, and the rate.
4. Apply scale levels if applicable. Define upper and lower limits for manual changes.
5. Optionally select a calculation type that differs from the Customizing default for the condition type.
6. Save.

**Creating with reference:** New condition records can be created with reference to existing ones. Rate, validity period, and additional sales data can be changed during the copy. This is efficient for updating multiple records simultaneously.

### Copying Condition Records
Multiple records can be created by copying an existing record using *copying rules* defined in Customizing. Available copying options include:
- Create target conditions over a range of customer numbers.
- Create target conditions over a range of material numbers.
Custom copying rules can be defined.

### Mass Maintenance (Price Change Function)
The price change function allows multiple condition records to be maintained simultaneously. *Change documents* are generated automatically, enabling review and monitoring of all modifications.

### Manage Prices - Sales App (Fiori)
The Manage Prices - Sales app is the primary mass maintenance interface in S/4HANA:
- **Dynamic filters:** specifying a condition type determines the relevant key fields, which are added as filters automatically. Multiple condition types can be combined in one filter.
- **Create:** specify condition type and key combination first; key fields appear as columns dynamically.
- **Copy:** create new records by copying existing ones.
- **Edit:** change validity period and condition amount for multiple records simultaneously.
- **Spreadsheet import:** download a template (prefilled with key combinations per condition type), update values, and import. Existing records can be exported to spreadsheet, modified, and imported back.
- **Import tracking:** track the status of large imports running in background; correct import errors by downloading to spreadsheet.
- **Validity overlap:** when imported records overlap with existing validity periods, the system updates or replaces (deletes) the existing records.

### Release Procedure for Condition Records
When a condition table is created with the *With Release Status* checkbox selected, two fields are added:
- **KFRST:** Release status (last key field in the table)
- **KBSTAT:** Processing status (variable data field)

Release statuses available in the standard system:
| Status | Meaning |
|---|---|
| Released | Active for pricing |
| Blocked | Not used in pricing |
| Released for pricing simulation | Used in net price list but not current documents |
| Released for planning and pricing simulation | Used in CO-PA planning and pricing simulation |

The release status is set indirectly by defining a processing status in Customizing and assigning a release status to it. Business Transaction Event 00503303 allows custom processing logic for the processing status.

## Condition Maintenance Interfaces — Two Modes

| Interface | Scope | Access |
|---|---|---|
| Condition-type-based (VK11/VK12/VK13) | Only records of the selected condition type | Select Using Condition Type node |
| Characteristic-based (Manage Prices - Sales) | All condition types and condition tables simultaneously | Fiori app or area menu COND_AV |

The area menu COND_AV controls the condition maintenance navigation. Custom area menus can be created via SE43 by copying COND_AV and modifying the menu structure.

## Price Lists and Pricing Reports

### Price Lists
Enter: sales area (org/channel/division), customer number(s), material/product hierarchy/material pricing group, pricing date, sales document type (required to determine pricing procedure). Output options:
- Display directly in system using a configured layout
- Upload to FTP server
- Email as Excel spreadsheet or CSV (including ZIP format)

### Pricing Reports
Used to generate analysis lists of existing condition records. Example queries: customer-specific price agreements in a period, Incoterms condition records, scale-based price lists. The report structure is defined in Customizing by selecting fields from condition tables.

Report layout sections: Page header (break on value change), Group header (new heading per table analyzed), Items (detailed record data). The program for a pricing report is generated when a new set of condition table views is selected — the system creates the executable report from the field selection.

## Key Facts from Source (Learning Assessment)
- A release procedure can be used with a condition record — this is a supported standard feature.
- Condition records can be copied from one customer to another using the copy function with a range of customer numbers.
- A price list for condition record maintenance can be created using a user-defined price list structure in Customizing.
- Condition records can be maintained via the Manage Prices - Sales app in addition to VK11/12/13.
- The Manage Prices - Sales app supports both export to spreadsheet and import of changes back into the system.

## Common Errors
**Condition record exists but pricing finds no price**
-> Check the key fields of the condition record against the access sequence: the access may use different source fields than the document populates. Also check validity dates.

**Mass price change not reflected in open orders**
-> Validity period of new records may not cover existing order dates, or pricing re-determination has not been triggered in those orders.

**Spreadsheet import fails**
-> Download the template first with the filter specifying the required condition types so that the correct key combinations are pre-populated. Check import history for error detail.

## Cross-References
- Prior step: configuration-pricing-procedure-configuration-001
- Next step: pricing-special-pricing-functions-001
- See also: pricing-condition-technique-overview-001
