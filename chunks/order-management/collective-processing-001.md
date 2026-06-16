---
schema_version: 1
id: order-management-collective-processing-001
title: "Collective Processing of Deliveries, Picking, and Billing in SAP SD"
area: order-management
process_tags: [order-to-cash, delivery-processing, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    relative_path: "S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf"
    pages: "117-124"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - collective processing
  - procesamiento colectivo
  - delivery due list
  - lista de entregas vencidas
  - billing due list
  - lista de facturación vencida
  - worklist SAP SD
  - creación masiva entregas
  - facturación masiva SAP
  - procesamiento masivo pedidos entregas facturas
  - invoice split collective invoice
  - división de facturas factura colectiva
level: functional
status: draft
quality: high
created: 2026-06-16
last_updated: 2026-06-16
---

# Collective Processing of Deliveries, Picking, and Billing in SAP SD

## Operational Summary
*Collective processing* allows logistics and billing users to create follow-up documents for multiple preceding documents in a single step, rather than processing each sales order individually. The same approach applies to outbound delivery creation (delivery due list), picking (warehouse task creation), and billing document creation (billing due list). Collective processing can run online (interactive selection and creation) or in background mode (scheduled batch job during off-peak hours). The system automatically consolidates or splits documents depending on *split criteria* defined in Customizing and master data settings.

## Questions This Chunk Answers
- How does collective processing work for creating outbound deliveries?
- What criteria prevent multiple sales orders from being combined into a single delivery?
- What conditions must be met to combine multiple orders into one billing document?
- What are the possible results of collective billing (invoice split, separate documents, collective invoice)?
- Can collective processing be executed automatically in the background?
- How does collective picking work in SAP EWM?

## When It Applies and Context
Collective processing is used by shipping departments and billing clerks when volumes are too large for individual document processing. It is a standard operation in the order-to-cash cycle:
1. Sales orders created (individually or via EDI)
2. **Collective delivery creation** groups eligible order items into outbound deliveries
3. **Collective picking** creates warehouse tasks in EWM for all selected deliveries
4. After goods issue, **collective billing** groups eligible deliveries into billing documents

## Process Flow

### Step 1 — Collective Delivery Creation (Delivery Due List)
The user opens the *Create Outbound Deliveries* app (or equivalent transaction) and selects sales order items eligible for delivery. Selection criteria include:
- *Shipping point* (mandatory grouping criterion)
- *Delivery creation date* (upper limit on the requested delivery date)
- Optional: route, ship-to party, sales organization

The system generates a list of orders meeting the selection criteria. The user can refine the list with sorting and filtering. Upon confirmation, the system creates one or more outbound deliveries, automatically grouping or splitting items based on split criteria.

**Background processing**: the same logic can be scheduled as a batch job during off-peak hours, with the same selection criteria, eliminating the need for manual intervention.

### Step 2 — Collective Picking
After outbound deliveries are created, picking must be executed. In SAP S/4HANA with *SAP Extended Warehouse Management* (EWM), the picking step creates *warehouse tasks* with reference to outbound delivery orders. Warehouse tasks specify the materials, quantities, and storage bin locations to pick.

The pick list for warehouse staff is generated from the warehouse task data and can be printed automatically. Confirmation of the warehouse task (and therefore of the picking activity) can be:
- **Automatic**: the system confirms upon creation of the warehouse task
- **Manual**: a separate step in which the warehouse clerk confirms the picked quantities

After warehouse tasks are confirmed, the corresponding *goods issue* can be posted, which reduces the stock and triggers the FI posting.

### Step 3 — Collective Billing (Billing Due List)
The user opens the billing due list and selects outbound deliveries (or sales orders for order-related billing) that are ready for invoicing. The list shows all items due for billing within a selected date range and billing organization.

The system creates billing documents by grouping or splitting items based on *billing split criteria*. The main split criteria are:
- Payer
- Billing date
- Terms of payment

Additional criteria are maintained in Customizing. Items that differ in any of these characteristics cannot be combined into a single billing document.

## Split Criteria — Key Table

| Criterion | Scope | Consequence if different |
|---|---|---|
| Ship-to party | Delivery | No combination into one outbound delivery |
| Shipping point | Delivery | No combination into one outbound delivery |
| Route | Delivery | No combination into one outbound delivery |
| Incoterms | Delivery | No combination into one outbound delivery |
| Payer | Billing | No combination into one billing document |
| Payment terms | Billing | No combination into one billing document |
| Billing date | Billing | No combination into one billing document |

## Billing Results — Three Scenarios

**Invoice split**: one sales order has one outbound delivery, but some items have different billing-relevant characteristics (for example, different payment terms). The system creates multiple billing documents from the single delivery.

**Separate billing document per delivery**: one sales order with two outbound deliveries (for example, partial deliveries to the same customer). The system creates two billing documents, one per delivery.

**Collective invoice**: two or more sales orders with multiple outbound deliveries where all billing-relevant characteristics are identical. The system creates a single billing document referencing all eligible deliveries.

## Customer Master Data Influence on Collective Delivery Creation

Three delivery agreement scenarios affect how collective processing handles a customer's orders:

1. **Complete delivery required**: all quantities in the entire sales order must be delivered in a single outbound delivery; no splitting across deliveries.
2. **No complete delivery required (partial deliveries allowed)**: each item can be delivered independently; the system can create partial deliveries and can combine items from multiple orders into one delivery if other criteria match.
3. **Orders can be combined**: the customer explicitly allows items from multiple sales orders to be merged into a single outbound delivery, provided they share the same shipping point, delivery date, ship-to party, route, and Incoterms.

## Common Errors
**Expected combination of orders does not happen**: verify that ship-to parties, shipping points, routes, and Incoterms are identical across the orders. Differences in any one of these criteria prevent combination.

**Invoice split created unexpectedly**: check that payment terms, payer, and billing dates are consistent across delivery items. Differences in any billing split criterion trigger a split.

**Background billing job creates fewer documents than expected**: some items may have open status-relevant issues (billing blocks, incompletion log errors) that prevent them from appearing on the billing due list.

## Cross-References
Prior step: order-management-availability-check-atp-001
See also: shipping-outbound-delivery-creation-process-001
See also: billing-billing-document-creation-methods-001
See also: billing-invoice-combination-and-split-001
See also: shipping-ewm-picking-process-001
