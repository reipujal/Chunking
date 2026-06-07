---
schema_version: 1
id: master-data-sd-partner-functions-001
title: "Partner Functions and Partner Determination in SAP SD"
area: master-data
process_tags: [order-to-cash]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "96-107"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - partner functions
  - funciones de interlocutor
  - determinacion de interlocutores
  - sold-to ship-to payer bill-to
  - como se determinan partners en SD
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Partner Functions and Partner Determination in SAP SD

## Operational Summary
Partner processing separates who a business partner is from which role that partner plays in a transaction. The course distinguishes *partner types*, such as customer, vendor, personnel, and contact person, from *partner functions*, such as sold-to party, ship-to party, payer, bill-to party, forwarding agent, or responsible employee. Partner determination procedures define which functions may or must appear in master data and SD documents and how partners are copied or determined.

## Questions This Chunk Answers
- What is the difference between a partner type and a partner function?
- Which partner functions are central to a sales transaction?
- How are partner relationships proposed into sales documents?
- What does a partner determination procedure control?
- How can indirect partner functions be determined from another partner's master record?

## Definition
A *partner type* represents the technical category of business partner used in the process. The source lists partner types AP for contact person, KU for customer, LI for vendor, and PE for personnel in Sales and Distribution. A *partner function* represents the role the partner plays in the business transaction. One business partner may hold several functions.

## Purpose in the SD Process
Partner functions determine commercial, delivery, payment, logistics, and internal responsibility roles in SD documents. In the simplest case, one customer is simultaneously sold-to party, ship-to party, payer, and bill-to party. In more realistic scenarios, the customer placing the order may differ from the customer receiving goods or paying the invoice. Partner functions let SAP represent those differences without creating a different transaction model for each relationship.

Partner relationships are usually maintained in the customer master and proposed automatically into the sales document header. If Customizing allows it, the user can change or supplement them in the partner screen. Partners can also be defined at item level, but a partner defined only at header level cannot necessarily be changed at item level.

## Structure and Variants
Partner determination procedures can be defined for several levels and assigned through different keys:

| Partner object | Assignment key from the source |
|---|---|
| Customer master | Account group |
| Sales document header | Sales document type |
| Sales document item | Item category in sales |
| Free-of-charge | Delivery type |
| Shipment | Shipment type |
| Billing header | Billing type |
| Billing item | Billing type |

The account group controls customer master data, including field display, mandatory entry, number range, and controls such as partners and texts. Partner functions define the business role a partner assumes within the sales process.

## Relationship with Other SAP SD Objects
Partner determination for sales documents accesses the sold-to party customer master and can copy stored partner relationships. SAP can also determine a partner function from other customer master records by using a source partner function and a determination sequence. The course example is determining the forwarding agent from the ship-to party. Other sources named in the course include customer hierarchy, contact persons, and credit representatives. An analysis function helps trace automatic partner determination in detail.

## Cross-References
- Prior step: configuration-sales-incompletion-check-001
- See also: order-management-sales-order-source-of-data-001
- Next step: order-management-outline-agreements-scheduling-quantity-contracts-001
