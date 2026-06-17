---
schema_version: 1
id: enterprise-structure-shared-master-data-cross-division-001
title: "Shared Master Data and Cross-Division Sales in SAP SD"
area: enterprise-structure
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf"
    pages: "14-19"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - shared master data SAP SD
  - common distribution channel
  - common division sales
  - datos maestros compartidos
  - canal de distribución común
  - división común ventas
  - cross-division sales configuration
  - how to share customer master across distribution channels
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Shared Master Data and Cross-Division Sales in SAP SD

## Operational Summary
*Shared master data* allows multiple sales areas within the same sales organization to reuse customer and material master data rather than maintaining independent copies. In Customizing, a sales organization can designate one *common distribution channel* and one *common division* whose master data records serve as the shared source for all participating sales areas. This mechanism reduces master data maintenance effort significantly for organizations that operate across multiple channels or divisions.

## Questions This Chunk Answers
- What is shared master data in SAP SD and why is it used?
- How do you configure common distribution channels and common divisions in Customizing?
- Which sales areas can share master data with each other?
- What are the limits of shared master data — what cannot be shared?
- How does the division in a sales document get determined when shared master data is active?
- How does shared master data affect reporting in SAP BW or SAP BI?

## Definition

*Shared master data* is a Customizing-driven mechanism that allows one sales area's customer and material master records to be accessed by other sales areas within the same sales organization. Rather than creating separate master data entries for each combination of sales organization, distribution channel, and division, organizations designate a *reference* channel and division whose data is visible to all configured participating areas.

The configuration is made at two independent levels:
- **Distribution channel level**: in Customizing, you specify which distribution channel is used to access *condition records* and which is used to access *customer and material master data* for a given sales organization and channel combination.
- **Division level**: similarly, you define which division is used to access condition records and customer master data for a given sales organization and division combination.

These two levels are independent — it is possible, for example, to share customer and material master data across distribution channels while keeping condition records unshared (so each sales area follows its own pricing strategy).

## Shared Master Data Example

Consider a sales organization 1000 with channels 10 and 12, and divisions 01 and 02. By configuring the common distribution channel and division in Customizing, a single set of master data records created for sales area (1000, 10, 01) can be made accessible to four sales areas:

| Sales Org | Channel | Division |
|---|---|---|
| 1000 | 10 | 01 |
| 1000 | 10 | 02 |
| 1000 | 12 | 01 |
| 1000 | 12 | 02 |

In this example, condition records are not shared — each sales area maintains independent pricing. Only the customer and material master data is shared through the common channel/division setting.

## Limits of Shared Master Data

Shared master data operates **within** a single sales organization. It is **not possible to share master data across different sales organizations**. This is an architectural constraint of the SD organizational model: the sales organization is the highest-level SD organizational unit and has its own separate master data namespace.

Misusing the sales organization — for instance, mapping a distribution channel at the sales organization level instead of the appropriate level — has serious consequences: the shared master data functions cannot operate at that level, which leads to an increase in the number of SD master data views that must be maintained individually.

## Division in Sales Documents

When a sales document is created in a sales area where shared master data is active, the division in the sales document *header* is proposed from the sales area Customizing. If a different division should appear at the item level — reflecting the material's own division from the material master — the *Item Division* indicator must be activated in Customizing for the relevant sales document type. If this field is left blank, the header division applies uniformly to all items regardless of the individual material's division.

## Relationship with Cross-Division Sales

Cross-division sales refers to the scenario in which a single sales order contains items belonging to different divisions. This is made possible precisely through shared master data: when material master data is shared across divisions, items from multiple product divisions can be combined in one order without requiring separate sales areas. The shared master data configuration is thus the enabling mechanism for cross-division business processing.

## Reporting Impact

When sales, delivery, and billing documents are processed, the organizational data from those documents — including the sales area used at the time of the transaction — is transferred to SAP Business Information Warehouse (BW) and SAP Business Intelligence reporting tools. Using shared master data does not compromise the reporting granularity: detailed reporting remains available for all organizational structures because the actual transactional sales area is preserved in the document, while the amount of master data that needs to be created and maintained is minimized.

## Cross-References
- See also: enterprise-structure-sales-distribution-enterprise-structure-001
- See also: master-data-business-partner-master-data-001
- See also: master-data-material-master-sd-001
