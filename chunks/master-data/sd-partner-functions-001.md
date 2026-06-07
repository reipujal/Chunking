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
  - account group partner determination procedure
  - grupo de cuentas funciones interlocutor
  - interlocutor obligatorio ventas
level: functional
status: draft
quality: medium
created: 2026-06-07
last_updated: 2026-06-07
---

# Partner Functions and Partner Determination in SAP SD

## Operational Summary
Partner processing separates who a business partner is from the role they play in a transaction. SAP defines *partner types* (the technical category: customer, vendor, personnel, contact person) and *partner functions* (the business role in the transaction: sold-to party, ship-to party, payer, bill-to party, forwarding agent, responsible employee). Partner determination procedures define which functions may or must appear in master data and SD documents, and how partners are automatically proposed or determined.

## Questions This Chunk Answers
- What is the difference between a partner type and a partner function?
- Which partner functions are central to a sales transaction?
- How are partner relationships proposed into sales documents?
- What does a partner determination procedure control?
- How can indirect partner functions be determined from another partner's master record?
- What controls which fields appear in a customer master record?
- Can the sold-to party be changed after it has been entered in a sales document?

## Definition
A *partner type* is the technical category of business partner. In Sales and Distribution, four partner types are defined:

| Partner type | Meaning |
|---|---|
| AP | Contact person |
| KU | Customer |
| LI | Vendor |
| PE | Personnel |

A *partner function* is the business role the partner plays in the transaction. One business partner can hold several partner functions simultaneously. In the simplest case, a single customer is the sold-to party, ship-to party, payer, and bill-to party. In more realistic scenarios these can be different business partners.

Business relationship examples from the source: a vendor acts as forwarding agent for a customer; a contact person is employed at the customer company; a contact person acts as the customer's external consultant; sold-to party and ship-to party are different customers; a customer manager employee is linked to a customer as a partner.

## Purpose in the SD Process
Partner functions assign commercial, delivery, payment, logistics, and internal responsibility roles within SD documents. They make it possible for the customer placing the order, the recipient of goods, and the invoice payer to each be a different business partner, without requiring a different transaction model for each combination.

Contact persons can be entered directly in the customer master record and assigned automatically to that customer. A contact person can also be assigned to a different customer in a consultant role. The forwarding agent, as a vendor partner, is an example of a cross-type assignment. Employees at your own company — sales representatives or clerks — are managed in employee master records and can assume partner functions of type PE such as partner function ER (responsible employee).

## Structure and Variants

**Partner determination procedures** can be defined for several document levels and assigned through different keys:

| Partner object | Assignment key |
|---|---|
| Customer master | Account group |
| Sales document header | Sales document type |
| Sales document item | Item category in sales |
| Free-of-charge delivery | Delivery type |
| Shipment | Shipment type |
| Billing header | Billing type |
| Billing item | Billing type |

**Account group** controls customer master record behavior: which fields are displayed, whether entry is mandatory, optional, or suppressed, the number range for the customer number, and other controls such as partners and texts. Account groups are delivered in the standard system:

| Account group | Standard purpose |
|---|---|
| 0001 | Sold-to party |
| 0002 | Ship-to party |
| 0003 | Payer |

A customer master created with account group 0002 (ship-to party) displays shipping-relevant fields and hides billing fields that are not needed for a ship-to-only partner.

**Partner determination in customer master.** If Customizing permits it, multiple partners can be assigned to the same partner function in the customer master. When a sales order is created, a selection list appears so the user can choose among them. In sales documents, only one partner per function is allowed — with the exception of outline agreements, where partner functions AA and AW allow multiple authorized releasers.

**Partners at item level.** Partners can also be defined at item level in sales documents. A partner defined only at header level cannot be changed or supplemented at item level. Customizing can prevent users from changing a partner once it has been entered — for example, preventing changes to the sold-to party in a saved document. Address changes to a partner such as the ship-to party can be made manually in the document without affecting the master record.

## Relationship with Other SAP SD Objects

Partner relationships are usually maintained in the customer master and proposed automatically into the sales document header when the document is created. SAP accesses the customer master of the sold-to party.

**Partner determination procedure** — what it controls: In a partner determination procedure, you define which partner functions may or must appear (mandatory functions), whether multiple partners can be assigned to the same function, and the sequence and sources for automatic determination. Customizing can prevent users from changing a partner once it has been entered. Address changes made to a partner in the document (such as the ship-to party delivery address) do not affect the underlying master record.

**Indirect partner determination.** SAP can determine a partner function from a different customer master record by specifying a source partner function and a determination sequence. Example: the forwarding agent in the sales document is determined by first accessing the sold-to party master, then the ship-to party master to find the forwarding agent stored there.

Other tables and sources used for automatic partner determination include the customer hierarchy table (KNVH), contact persons table (KNVK), and credit representatives table (T024P). An analysis function is available to trace automatic partner determination step by step in detail.

**Which partner functions are mandatory** is a Customizing decision per partner determination procedure — SAP does not impose a fixed standard set of mandatory functions. Partner procedures can include any combination of mandatory and optional functions. Functions can be mandatory in the customer master (controlled by account group) while optional in the sales document, or vice versa.

## Cross-References
- Prior step: configuration-sales-incompletion-check-001
- See also: order-management-sales-order-source-of-data-001
- Next step: order-management-outline-agreements-scheduling-quantity-contracts-001
