---
schema_version: 1
id: special-processes-third-party-order-processing-001
title: "Third-Party Order Processing"
area: special-processes
process_tags: [order-to-cash, third-party]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    relative_path: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    pages: "8-21, 33-38"
    source_type: A
    role: primary
transactions: [VA01, ME21N, MIGO, MIRO, VF01, VF04]
tables: []
aliases:
  - third-party order processing
  - procesamiento de pedido a terceros
  - TAS item category
  - categoría de posición terceros
  - schedule line category CS
  - proveedor entrega directamente al cliente
  - how to configure direct ship-from-supplier
  - pedido a terceros configuración SAP
  - item category group BANS
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Third-Party Order Processing

## Operational Summary

In third-party order processing, a company sells goods to a customer without physically stocking or shipping those goods. The company forwards a purchase order to an external supplier, who delivers the material directly to the customer and invoices the company. The company then bills the customer. No warehouse movement occurs in the company's own plant. The process bridges SAP S/4HANA Sales and SAP S/4HANA Procurement: a sales order automatically generates a purchase requisition, the requisition is converted to a purchase order, and the posted supplier invoice determines when and for what quantity the customer is billed.

## Questions This Chunk Answers

- What item category controls third-party processing in the standard SAP S/4HANA sales order?
- How does the system automatically create a purchase requisition from a third-party sales order?
- What is the difference between *Billing Relevance* B and F for item category TAS?
- How is the billing quantity for the customer determined — from the goods receipt or the supplier invoice?
- What must be set up in Customizing for a goods receipt to be possible for a third-party item?
- How does automatic purchase order creation (item category ALES) differ from TAS?
- What happens to stock and accounting when a goods receipt is posted for a third-party item?

## When It Applies and Context

Third-party order processing applies when a company acts as an intermediary between a customer and an external supplier, without ever warehousing the sold material. Common scenarios: goods that are bulky, hazardous, or uneconomical to stock; specialized items procured on demand; and drop-ship arrangements agreed with specific suppliers.

The process can apply to individual items within a sales order that also contains standard items. Two activation modes exist:

- *Automatic third-party order processing*: item category TAS is determined from the material master record (item category group BANS in the *Sales Org. 2* view). The process is triggered on every order for that material.
- *Manual third-party order processing*: a standard item category is changed to TAS manually in the order. Used when the same material is usually shipped from stock but occasionally drop-shipped.

The process requires aligned master data: material master with the correct item category group, a purchasing info record for source determination, and a business partner master record for the ship-to party (whose address is forwarded to the supplier).

## Process Flow

1. **Sales order creation (VA01):** The user creates a standard sales order (document type OR). If item category group BANS is maintained in the material master *Sales Org. 2* view, item category *TAS* is determined automatically. The system then assigns schedule line category *CS* (*Third-Party Busin.*) to the item. Schedule line category CS is configured without a movement type and without delivery relevance — no outbound delivery is ever created for this item. The item appears in the sales order as a third-party item; the customer sees a normal order line from the sales perspective.

2. **Automatic purchase requisition creation:** When the sales order is saved, one purchase requisition item is created per schedule line with a confirmed quantity greater than zero. Schedule line category CS determines the document type, purchasing item category, and account assignment category for the requisition. Account assignment category X (*All auxiliary account assignments*) is the standard. The delivery address in the requisition is taken from the ship-to party business partner master record. Quantities, dates, and delivery addresses remain synchronized: changes to the sales order schedule line are automatically transferred to the requisition as long as the requisition status permits it. If purchase order texts are entered in the sales order item, they are copied into the requisition item and from there into the purchase order.

3. **Source determination:** Source determination is executed automatically when the requisition is generated. The system analyzes purchasing info records, source lists, and quota arrangements to identify and assign a unique source of supply. A source list has the second-highest priority after a quota arrangement. If more than one valid source exists and no quota arrangement uniquely identifies one, the system does not assign a source automatically; the buyer must do so manually. The planned delivery time from the purchasing info record (or contract if that is the fixed source) is used for purchase order scheduling — applying backward scheduling first, then forward scheduling if the requested delivery date is too early.

4. **Purchase order creation (ME21N):** The buyer converts the purchase requisition into a purchase order with purchasing item category *S* (*Third-party*). The PO can be created via ME21N or the *Manage Purchase Requisitions* Fiori app. The delivery address on the PO item shows the customer ship-to address and cannot be changed in the PO itself (only in the sales order). The purchase order number appears in the document flow of the sales order. An automated variant uses item category *ALES*: when the *Create PO Automatic.* indicator is set in the item category, saving the sales order triggers both the requisition and its immediate conversion to a PO, provided a unique source exists and ALE data is configured in the sales organization.

5. **Goods receipt (MIGO — optional):** Since the supplier delivers directly to the customer, no physical goods movement occurs in the company's warehouse. A pseudo goods receipt can be posted in MIGO when the supplier reports that delivery has taken place. This GR does not change inventory stock; the quantity is posted directly as consumption, with accounting entries to a consumption account (sales order item as the cost object) and a GR/IR clearing account. The *Goods receipt* checkbox in the purchase order item must be set to enable this step. The *GR-Bsd IV* (goods-receipt-based invoice verification) flag, when set in the PO item, blocks payment of the supplier invoice until the GR is posted.

6. **Supplier invoice posting (MIRO):** The incoming supplier invoice is entered via MIRO or the *Create Supplier Invoice* Fiori app. The system proposes a quantity based on what is configured: if a GR was posted, the GR quantity is proposed; if no GR is expected, the ordered quantity is proposed. Automatic payment blocks arise from: quantity variance (GR expected but not yet posted) or price variance (invoice price deviates significantly from the PO price). Price variances affect the profit margin visible on the sales order item via the VPRS condition type. When the invoice is posted, the GR/IR clearing account is released, the purchase order history is updated, and an open item is posted to the supplier account in accounts payable.

7. **Customer billing document (VF04 / VF01):** The customer is billed with reference to the sales order, not a delivery (no delivery exists). The billing timing and quantity are controlled by the *Billing Relevance* field in item category TAS and the *Billing Quantity* field in copying control:

   - **Billing Relevance F** (default for TAS): the sales order enters the billing due list only after the incoming supplier invoice is posted. For each supplier invoice received, one customer billing document is created. *Billing Quantity* = F (*Invoice receipt quantity minus invoiced quantity*) in copying control from sales documents to billing documents.
   - **Billing Relevance B**: the sales order enters the billing due list immediately after saving, without waiting for GR or invoice receipt.
   - **Billing Quantity E** (alternative when using Relevance F): the GR quantity is used as the billing reference instead of the invoice quantity. Configured in SPRO copying control for billing type F2 + sales document type OR, item TAS.

## SD Configuration

**Item category TAS:** Key settings — no delivery relevance, no movement type, *Billing Relevance* = F (default). SPRO path: *Sales and Distribution → Sales → Sales Documents → Sales Document Item → Define Item Categories*.

**Item category group BANS:** Maintained in the material master *Sales Org. 2* view. Drives automatic determination of TAS in the order. Materials without BANS use TAS only via manual override.

**Schedule line category CS:** Assigned to item category TAS. Contains the document type for the purchase requisition, purchasing item category S, and account assignment category X. No movement type; no delivery relevance. SPRO: *Sales and Distribution → Sales → Sales Documents → Schedule Lines → Define Schedule Line Categories*.

**Automatic PO creation (ALES):** The *Create PO Automatic.* indicator must be set in the item category. A unique source of supply must exist. ALE data (purchase order document type and related settings) must be maintained in the sales organization configuration (*Enterprise Structure → Definition → Sales and Distribution → Define Sales Organization*, ALE data section).

**Copying control for billing quantity:** In copying control from sales documents to billing documents (billing type F2, sales document type OR, item TAS), the *Billing Quantity* field must be F or E. SPRO: *Sales and Distribution → Billing → Billing Documents → Maintain Copying Control For Billing Documents*.

## Conditions and Restrictions

- No outbound delivery is created for third-party items. The delivery-related fields (picking, goods issue) are irrelevant.
- The ship-to address in the PO is derived from the sales order and cannot be changed independently once the PO output messages have been issued.
- Account assignment (sales order item) in the requisition and PO cannot be changed manually.
- Multiple supplier invoices for the same PO item each generate a separate customer billing document (Billing Relevance F).
- Only external suppliers can be sources of supply for third-party items. Internal plants (cross-company stock transfer) are not valid sources.
- If no unique source of supply is found, the system does not assign one automatically; the buyer must intervene before the PO can be created.

## Common Errors

| Symptom | Cause | Solution |
|---|---|---|
| No purchase requisition created on save | Schedule line category CS misconfigured or unique source not assignable | Check CS config (item category, purchasing doc type); verify source list or info record |
| Invoice blocked for payment — Quantity Variance | GR required per PO item but not yet posted | Post the GR via MIGO, or deactivate the GR flag in the PO item if GR is not needed |
| Sales order not appearing in billing due list | Billing Relevance = F and supplier invoice not posted | Post incoming invoice via MIRO; the order appears automatically afterward |
| Billing quantity differs from expected | Wrong Billing Quantity field (E vs F) in copying control | Correct the Billing Quantity setting in SPRO copying control for billing type F2 / OR / TAS |
| Ship-to address change not reflected in PO | Change made after output messages issued | Change the address only in the sales order before output is issued; afterwards it cannot be updated |

## Integration with Other SAP Processes

**Third-party and intercompany combined:** When the supplying vendor is not an external company but an internal plant belonging to a different company code, the third-party process combines with the cross-company code sales process. The purchase order is directed at the internal supplier; the intercompany billing type IV is then used to settle between the two company codes in addition to the standard customer invoice. This is a more complex scenario covered by dedicated integration configuration.

**Third-party returns (scope item 1Z3):** When a customer returns goods from a third-party order, the standard return process requires coordination between the returns delivery (from customer back to company or directly to supplier) and the supplier credit. SAP S/4HANA scope item 1Z3 (*Third-Party Returns with Advanced Returns Management*) provides a framework for this. The refund code in the Advanced Returns Order (RE2) controls whether a supplier return is triggered in addition to the customer credit memo.

**Consignment stock interaction:** Third-party order processing is not applicable to consignment stock scenarios, where goods are already at the customer's location and billing is triggered by goods issue from consignment stock. Third-party processing requires the goods to flow from supplier directly to customer — not via previously consigned stock.

## Cross-References

Prior step: order-management-sales-distribution-process-001 (standard O2C overview; third-party is a variant)
See also: configuration-sales-document-type-control-001 (sales document type OR + item category determination)
See also: configuration-sales-item-category-control-001 (general item category configuration rules)
See also: configuration-billing-copying-control-001 (billing quantity field for TAS)
See also: special-processes-intercompany-sales-process-001 (when the delivering plant belongs to a different company code)
See also: special-processes-advanced-returns-management-001 (ARM scope item 1Z3 for third-party returns)
