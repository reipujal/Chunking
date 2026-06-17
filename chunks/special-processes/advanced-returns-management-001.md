---
schema_version: 1
id: special-processes-advanced-returns-management-001
title: "Advanced Returns Management (ARM): Customer Returns in SAP S/4HANA"
area: special-processes
process_tags: [order-to-cash, returns]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    relative_path: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    pages: "155-163, 173-176"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - advanced returns management
  - gestión avanzada de devoluciones
  - ARM SAP S/4HANA
  - customer returns process S/4HANA
  - devoluciones de cliente S4HANA
  - returns order RE2
  - pedido de devolución RE2
  - refund code SAP returns
  - Returns Overview SAP
  - accelerated customer returns BKP
  - devoluciones aceleradas cliente SAP
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Advanced Returns Management (ARM): Customer Returns in SAP S/4HANA

## Operational Summary

Advanced Returns Management (ARM) is the standard returns processing framework in SAP S/4HANA Sales. It replaces the ECC returns model (document type RE) with a more structured process that introduces *refund codes*, *follow-up activities*, and a consolidated monitoring tool called *Returns Overview*. ARM is always active in SAP S/4HANA — it is not a separately activated switch; the relevant business functions (OPS_ADVRETURNS and related functions) are delivered as always-on capabilities in S/4HANA. The controlling document is the *advanced returns order*, created with sales document type RE2. ARM manages the customer-side of returns; the supplier-side return (returning defective goods to the supplier) is handled by separate processes (MM or MM/SD integration) that are out of scope for this chunk.

## Questions This Chunk Answers

- What sales document type is used for customer returns in SAP S/4HANA Advanced Returns Management?
- What is a refund code and how does it control what happens after a customer return?
- What are the follow-up activities that ARM can trigger from a returns order?
- How does the Returns Overview support status management for open returns?
- What is the difference between the standard ARM process (RE2), Accelerated Customer Returns (BKP), and Customer Returns without ARM (BDD)?
- How does ARM in S/4HANA differ from the ECC approach with document type RE?

## When It Applies and Context

ARM applies whenever a customer sends goods back to the selling company or refuses a delivery. The customer return may occur because goods are defective, incorrectly ordered, damaged in transit, or surplus to requirements. The process requires a decision on what to do with the physical goods (return to stock, scrap, refurbish, forward to supplier) and how to refund the customer (credit memo, replacement delivery, or no refund). ARM provides a framework for tracking all these decisions and actions in a single advanced returns order.

In SAP S/4HANA, the OPS_ADVRETURNS business function suite is always delivered. This means the RE2 document type, refund codes, and Returns Overview are always available — unlike in SAP ERP ECC 6.0, where a specific business function activation was required. ARM coexists with simplified alternatives for specific use cases (BKP and BDD, described below).

The S4680 course covers the customer returns side of ARM. Supplier-side returns (returning goods to the original vendor) are MM processes outside the scope of this chunk.
<!-- L2 content removed: movement type 122 and supplier-return order mechanics are MM detail from S4680 U6 L2 (supplier returns, pages 164-172, deferred as MM-pure). The intercompany ARM extension note referenced pages outside the cited range (155-163, 173-176) — removed as uncited. -->

## Process Flow (Standard ARM with RE2)

1. **Advanced returns order creation (RE2):** The customer service representative creates an advanced returns order using sales document type RE2. The order captures the return reason, material, quantity, and the *refund code*. The refund code is a key control element: it determines which follow-up activities are automatically proposed or created by the system. Unlike ECC returns (document type RE), the RE2 order is not confirmed with a billing block that must be manually removed — the process follows the refund code configuration.

2. **Refund code determination:** The refund code is entered on the advanced returns order item. It controls:
   - Whether a credit memo is created (and if so, immediately or after inspection).
   - Whether a replacement delivery is triggered.
   - Whether the goods can be returned to unrestricted stock, moved to blocked stock, or scrapped.
   - The sequence and dependency of follow-up activities.

   Example: a refund code configured for *credit memo after inspection* will create a credit memo request but place it on a billing block; the block is removed only after the inspection result confirms the goods are defective. A refund code for *immediate credit* creates a credit memo request without requiring prior inspection.

3. **Returns delivery (inbound delivery):** When the customer ships the goods back, an inbound delivery is created with reference to the advanced returns order. This delivery records the physical arrival of goods at the company's warehouse. A goods receipt (GI reversal) is posted when the goods are received, which updates the stock and creates a financial accounting document. The destination storage location is determined by the returns delivery configuration and the refund code settings.

4. **Follow-up activities:** ARM can automatically create or trigger the following follow-up activities from the advanced returns order:
   - *Credit memo request*: generated from the returns order and converted to a customer credit memo through standard SD billing. The credit memo is posted to the customer's account.
   - *Replacement delivery*: a new sales order or delivery is created to replace the defective goods.
   - *Inspection*: a quality inspection task is created. The inspection result can unblock the credit memo or route the goods for scrapping.
   - *Supplier return*: if the returned goods must be sent back to the original supplier (e.g., they are defective and under warranty), a supplier return process can be triggered. For third-party scenarios, the scope item 1Z3 (*Third-Party Returns with Advanced Returns Management*) covers the return to supplier variant.

5. **Returns Overview:** The Returns Overview (accessible via the *Returns Overview* Fiori app) is the monitoring cockpit for open returns. It shows all advanced returns orders, their status, the status of each follow-up activity, and any blocking conditions. The customer service representative or returns manager uses the Returns Overview to identify which returns are awaiting inspection, which credit memos are blocked, and which replacement deliveries are pending. This consolidated view replaces the need to navigate multiple transactions to track a single return.

6. **Credit memo posting:** When all required conditions are met (inspection complete if required, goods received if required), the credit memo request is released from its billing block and a credit memo is created via standard SD billing. The credit memo posts a credit to the customer account in financial accounting. The customer's account is balanced, and the returns cycle is complete from the SD perspective.

## ARM Variants

### Accelerated Customer Returns (BKP)

BKP is a scope item optimized for high-volume returns where speed is the priority. It uses a simplified process with fewer steps and less inspection overhead. The goods are processed quickly without the full follow-up activity framework of RE2. BKP targets scenarios like retail returns where the volume is high and defects are returned without individual assessment. The BKP scope item is delivered as part of S/4HANA and shares the ARM infrastructure but is configured for accelerated throughput.

### Customer Returns without ARM (BDD)

BDD is the process for companies that do not use the advanced returns capabilities and instead process customer returns through a streamlined path without the full ARM framework. It can be used when the ECC returns approach (based on document type RE) is preferred or when ARM features are not required for a specific customer segment. In S/4HANA, BDD is a backward-compatible configuration option, not a rollback of the business function.

## Comparison: ARM vs ECC Returns

| Dimension | ECC Returns (RE) | ARM Returns (RE2) |
|---|---|---|
| Sales document type | RE | RE2 |
| Refund control | Manual billing block + credit memo | Refund code drives follow-up activities |
| Follow-up automation | Manual creation | System-proposed follow-ups from refund code |
| Status monitoring | No dedicated cockpit | Returns Overview app |
| Business function | Separate activation required | Always-on in S/4HANA |
| Inspection integration | Manual | Integrated via follow-up activity |

## Conditions and Restrictions

- The advanced returns order (RE2) is always available in SAP S/4HANA — no manual business function activation is required.
- Refund codes are configured in Customizing and drive the process. Without correctly configured refund codes, the follow-up activity automation does not function.
- ARM covers customer returns. Supplier-side returns (returning goods to the vendor) are MM processes and are not controlled by RE2.
- The scope item 1Z3 (Third-Party Returns with Advanced Returns Management) extends ARM to third-party scenarios where goods need to be returned to an external supplier.

## Cross-References

See also: special-processes-third-party-order-processing-001 (third-party order processing; 1Z3 scope item extends ARM to this scenario)
See also: billing-credit-debit-memo-process-001 (credit memo creation in SD billing; ARM creates credit memo requests that follow this path)
See also: billing-returns-process-001 (billing treatment of customer returns; complement to this process chunk)
See also: order-management-sales-order-special-features-001 (special SD order types including returns-related document types)
