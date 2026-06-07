---
schema_version: 1
id: special-processes-sales-special-business-transactions-001
title: "Rush Orders, Cash Sales, Consignment, and Free-of-Charge Deliveries"
area: special-processes
process_tags: [order-to-cash, consignment, free-of-charge]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "81-87"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - rush order
  - venta al contado
  - consignacion
  - entrega gratuita
  - diferencia entre cash sales y rush order
  - orden tipo KB KE KA KR consignacion
  - delivery free of charge SDF FD SD
  - entrega gratuita siguiente entrega gratuita
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Rush Orders, Cash Sales, Consignment, and Free-of-Charge Deliveries

## Operational Summary
SAP SD includes special business transactions for immediate pickup, immediate payment, customer consignment stock, and free deliveries. *Rush orders* and *cash sales* both create a delivery automatically when saved, but differ in billing, financial posting, and whether an immediate invoice is printed. Consignment processing uses four document types (KB, KE, KA, KR) to manage goods at a customer location that remain company property until consumed. Free-of-charge deliveries use document type FD or SDF, require a delivery block until reviewed, and are controlled at item level by item category KLN.

## Questions This Chunk Answers
- What is the difference between a rush order and a cash sale?
- When does SAP automatically create a delivery for immediate sales processes?
- Which document types are used in consignment processing?
- Which consignment processes are billing-relevant?
- What delivery types are configured for rush orders and cash sales?
- How does the financial posting differ between cash sales and standard orders?
- Why should free-of-charge deliveries often be blocked for review?

## When It Applies and Context
Use these scenarios when a standard sales order does not fit the business process. Rush orders and cash sales apply when the customer picks up goods immediately from the plant or warehouse. Consignment processing applies when goods are physically placed at the customer but remain company property until consumed. Free-of-charge delivery applies to samples or complaint-related replacement deliveries.

## Process Flow

### Rush Order
1. The user creates a rush order. The sales document type has the *immediate delivery* switch and delivery type **DF** configured.
2. When the rush order is saved, the system automatically creates a delivery of type **LF**.
3. Once goods are withdrawn from the warehouse, picking and posting goods issue begin.
4. Billing documents are created later, for example through collective processing, and invoices are sent to the customer. **No document is printed at order creation** — the customer receives the invoice only at billing time.

### Cash Sale
1. The user creates a cash sale. The sales document type has the immediate delivery switch and delivery type **BV** configured.
2. When saved, SAP automatically creates a delivery of type **BV** and prints a cash invoice document that can be handed immediately to the customer.
3. An order-related billing index is generated automatically, which updates the billing due list.
4. Once goods are withdrawn, picking and goods issue are posted. **SAP recommends posting goods issue in the background using a program.**
5. Billing type **BV** is created while processing the billing due list. The system does not print an invoice during billing — the receipt was already printed at order creation.
6. The financial posting goes directly to a cash account — **no open customer receivable** arises, unlike rush or standard orders. The sales order number is used as the reference for the accounting document in Financial Accounting.

### Consignment

Four document types manage the consignment lifecycle:

| Process | Order type | Effect | Billing |
|---|---|---|---|
| Fill-up | **KB** | Delivers goods to customer consignment stock; goods remain in delivering plant's valuated stocks | Not billing-relevant |
| Issue | **KE** | Reduces customer special stock AND delivering plant stock | Billing-relevant |
| Pick-up | **KA** | Customer returns consignment goods; credits special customer stock at goods issue | Not billing-relevant |
| Return | **KR** | Reverses a consignment issue; goods receipt re-establishes special stock at customer | Credit memo generated |

### Free-of-Charge Delivery and Subsequent Delivery Free-of-Charge
- *Delivery free-of-charge* (FD): used to send a sample or other item at no charge.
- *Subsequent delivery free-of-charge* (SDF): used when material must be delivered due to a complaint. Requires a preceding document (configurable in Customizing for SDF). Copying controls must exist for all allowed preceding documents, e.g., SDF from RE (returns order).

A *delivery block* is activated in the sales document type to ensure these transactions are reviewed before release. If the reviewer decides against delivery, a reason for rejection is entered. At item level, item category **KLN** marks items in FD and SD document types as free-of-charge; pricing and billing behavior is controlled in the item category Customizing.

### Employee Sales
Employees purchase goods at reduced prices from a dedicated internal shop. Because employees can only buy goods that are in the shop, availability check and transfer of requirements are not necessary.

1. Orders are created using a **collective one-time customer master record** — no individual customer master per employee is maintained.
2. Orders must always have a net value to prevent documents without items or free items from being created.
3. Employees generally receive a **15% discount** off the material price; some materials may carry higher discounts.
4. When the order is saved, **SAP creates the delivery automatically**. Picking is not required because employees take only goods available in the shop.
5. Goods issue can be posted manually for a single delivery, or automatically in the background at day end.
6. Because goods are delivered as soon as the order is saved, order quantity always equals goods issue quantity → **order-related billing**.
7. Billing documents are created automatically in a collective run (e.g., billing list during night processing).
8. The financial posting goes to a **special cash sales account** — no open customer receivable is created.

Configuration objects required for employee sales: dedicated sales document type, new item category, incompleteness procedure controlling essential fields, one-time customer master, pricing extension for employee discounts.

## Common Errors
**Rush order expected to print an immediate invoice receipt**
-> Rush orders do NOT print a document for the customer at creation. Only the cash sales process prints an immediate cash invoice. The learning assessment in the source confirms this distinction explicitly.

**Cash sale expected to create receivables**
-> The invoice amount posts directly to a cash account; no open customer receivable arises.

**Consignment fill-up is billed**
-> Fill-up (KB) is not billing-relevant because the consignment stock remains company property.

**Free-of-charge delivery released without review**
-> Activate the delivery block in the sales document type to ensure the relevant employee checks the transaction before it is released.

**Preceding document not found for SDF**
-> Customizing for SDF requires a preceding document; copying controls must exist for all allowed document types that may serve as the reference.

## Cross-References
- Prior step: configuration-sales-copying-control-001
- See also: special-processes-cash-sales-process-001
- See also: pricing-free-goods-001
- See also: billing-returns-process-001
