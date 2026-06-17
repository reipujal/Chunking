---
schema_version: 1
id: integration-stock-transfer-order-intra-company-001
title: "Stock Transport Order: Intra-Company Code Stock Transfer with SD Delivery"
area: integration
process_tags: [stock-transfer, delivery-processing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    relative_path: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    pages: "76-92"
    source_type: A
    role: primary
transactions: [ME21N, VL10G, MMBE]
tables: []
aliases:
  - intra-company stock transfer
  - stock transport order same company code
  - traslado de stock misma sociedad
  - STO con entrega SD
  - delivery type NL
  - tipo de entrega NL
  - replenishment delivery SAP
  - entrega de reaprovisionamiento SAP
  - intra-company code STO SD integration
  - how to configure SD delivery for plant-to-plant transfer
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Stock Transport Order: Intra-Company Code Stock Transfer with SD Delivery

## Operational Summary

An intra-company code stock transfer moves materials between two plants assigned to the same company code. When the standard stock transport order (STO) approach with an outbound delivery is used, SAP S/4HANA creates an SD outbound delivery (delivery type NL) to manage shipping activities in the supplying plant. No customer billing document is created — the two plants belong to the same company code and no intercompany financial settlement is required. The SD delivery provides logistics capabilities (picking, packing, goods issue) and status tracking through the purchase order history. Understanding the SD delivery integration is relevant for SD consultants who configure shipping data for plants involved in STO processes.

## Questions This Chunk Answers

- What delivery type does the standard SAP S/4HANA system use for intra-company code stock transport orders?
- How does the system determine the ship-to party (goods recipient) for an intra-company replenishment delivery?
- What Customizing settings link the SD delivery type to the stock transport order document type?
- What is the difference between a one-step and a two-step procedure for intra-company goods movements?
- Why does a goods receipt posting for an intra-company STO not create an accounting document?
- What advantages does a stock transport order provide over a direct IM transfer posting?
- What role does the sales area assignment to the supplying plant play in STO configuration?

## When It Applies and Context

An intra-company code stock transfer moves materials between plants within the same legal entity. The receiving plant issues a stock transport order to procure goods from the supplying plant, often triggered by a material requirements planning run. This approach is used when the company wants purchase order-based control of internal replenishments, MRP integration, planned delivery costs, and full visibility of process status through purchase order history.

The STO with outbound delivery variant is preferred when the two plants require formal shipping activities — picking, packing, and a documented goods issue. The SD outbound delivery document handles these logistics steps and provides integration with SAP EWM or Stock Room Management for picking. The process is distinct from a simple IM transfer posting (MIGO), which provides no purchase order tracking or MRP integration.

## Process Flow

1. **Stock transport order creation (ME21N):** The purchasing department of the receiving plant creates a stock transport order using document type *UB* (*Stock Transp. Order*). Unlike a cross-company code stock transport order, document type UB specifies the supplying plant directly in the purchase order — no supplier business partner master record is required. The receiving plant is always specified in each purchase order item. MRP in both the supplying and receiving plant can take this STO into account for planning. Purchase requisitions created by MRP can be converted into STOs with document type UB.

2. **Outbound delivery creation (VL10G):** When the stock transport order is due for shipping, an outbound delivery (*replenishment delivery*) is created in the supplying plant. Collective processing transaction VL10G creates deliveries for multiple open STOs simultaneously, using the stock transport order number as a selection criterion. Alternatively, the SAP Fiori app *My Purchase Orders Due for Delivery* can be used.

   The delivery type used for this replenishment delivery is *NL* (*IntPlant Stock Dely*). This delivery type is assigned in Customizing to the combination of the stock transport order document type (UB) and the supplying plant. It is one of the key SD configuration settings for the intra-company STO process.

3. **Determination of delivery parameters:** Because the replenishment delivery is created with reference to a stock transport order (not a sales order), some delivery parameters are determined differently. The shipping point is determined from the shipping point assignments of the supplying plant. The delivery type is assigned to the UB document type + supplying plant combination (not derived from a sales order type). The sold-to and ship-to party for the delivery are derived from the *goods recipient*: a business partner master record assigned to the receiving plant in Customizing.

4. **Goods recipient (ship-to party):** A business partner master record must exist to act as the ship-to party for the replenishment delivery. This business partner — representing the receiving plant — is created using the sales area assigned to the supplying plant. That sales area assignment is maintained in Customizing (*Materials Management → Purchasing → Purchase Order → Set Up Stock Transport Order → Define Shipping Data for Plants*). The business partner master record provides address data, transportation zone, and shipping conditions needed to execute the delivery. The same sales area assignment is reused for cross-company code STO processes and for cross-company code sales intercompany billing.

5. **Shipping activities:** The replenishment delivery drives standard shipping activities in the supplying plant: picking (optionally via SAP EWM or Stock Room Management), packing, and goods issue. The goods issue posting is the final shipping step.

6. **One-step vs two-step procedure:**

   - *Two-step procedure*: when the goods issue is posted, the quantity moves to *stock in transit* in the receiving plant. This stock is financially valuated as belonging to the receiving plant (for accounting purposes) but is not yet available as unrestricted-use stock. A separate goods receipt must be posted in the receiving plant when the materials arrive. The goods receipt is *not valuated* (no accounting document is created) because the financial movement already occurred at goods issue within the same company code.
   - *One-step procedure*: the goods receipt is posted automatically at the moment the goods issue is posted, without a separate receiving step. This makes sense when the two plants are physically adjacent. The decision between one-step and two-step is configured per combination of issuing and receiving plant in Customizing.

7. **Stock in transit visibility (MMBE):** During the two-step procedure, the transferred quantity can be monitored via MMBE (*Stock Overview*) or the *Stock Single Material* Fiori app. The in-transit quantity is visible for the receiving plant as *stock in transit*, which can optionally be included in availability checks (controlled by the *With Stock in Transfer* flag in the availability check scope of the receiving plant).

8. **No billing document:** An intra-company code STO does not produce a billing document. Both plants belong to the same company code; no intercompany financial settlement is required. Planned delivery costs can be specified in the stock transport order and settled via a goods receipt posting, but no SD billing type is involved. This distinguishes the process from a cross-company code STO, where billing type IV (intercompany) is used.

## SD Customizing Configuration Points

**Delivery type NL assignment:** In Customizing, delivery type NL must be assigned to the combination of stock transport order document type (UB) and supplying plant. SPRO path: *Logistics Execution → Shipping → Deliveries → Define Delivery Types* (for NL review); assignment is in *Materials Management → Purchasing → Purchase Order → Set Up Stock Transport Order → Assign Delivery Type and Checking Rule*.

**Sales area assignment to supplying plant:** Each plant involved in STO processes must have a sales area assigned. This sales area is used to create the goods recipient BP master record and is shared across intra-company STO, cross-company STO, and cross-company sales intercompany billing. SPRO: *Materials Management → Purchasing → Purchase Order → Set Up Stock Transport Order → Define Shipping Data for Plants*.

**Goods recipient BP assignment:** Each receiving plant must have a business partner (ship-to party) assigned to it in Customizing. This BP is created in the sales area of the supplying plant. Without this assignment, a replenishment delivery cannot be created.

**One-step / two-step selection:** Configured per issuing plant / receiving plant combination. Determines whether a goods receipt posting in the receiving plant is required (two-step) or happens automatically at goods issue (one-step).

## MRP Integration

Both the supplying and the receiving plant can integrate the stock transport order into MRP planning. For the receiving plant, the STO is treated as a supply element: the confirmed delivery date of the STO reduces the net requirements that MRP would otherwise fulfill with production orders or external purchase orders. For the supplying plant, the STO generates a demand element (dependent requirement) that MRP includes when scheduling production or procurement. This bilateral MRP visibility is one of the main advantages of the STO approach over a direct IM transfer posting, which has no planning integration.

When MRP generates a planned order or a purchase requisition for plant-to-plant replenishment and the receiving plant is configured to source from an internal plant, the requisition can be converted automatically into a stock transport order of document type UB. The *Source of Supply* configuration in the material master and the purchasing info record (plant-to-plant) govern this conversion.

## Planned Delivery Costs

Although no billing document is created for intra-company STOs, planned delivery costs (freight, insurance, customs duties) can be entered in the stock transport order. These costs are assigned to the receiving plant at the time of the goods receipt and are included in the valuation of the received stock. The costs are not invoiced by the supplying company code — they are posted directly from the purchase order to the receiving plant cost center or stock account. This distinguishes planned delivery cost handling in UB STOs from the full intercompany billing that applies to cross-company STOs (NB document type).

## Conditions and Restrictions

- Document type UB is specific to intra-company STOs. For cross-company STOs with billing, document type NB (standard purchase order) must be used.
- No billing document, no intercompany invoice, no SD sales order — the STO is a procurement document from the receiving plant's perspective.
- Delivery costs can be planned in the UB STO and settled at GR, but no accounts payable open item is created for the material value itself.
- The *stock in transit* stock type (two-step procedure) is visible in inventory but cannot be consumed from unrestricted stock until the goods receipt is posted.

## Cross-References

See also: integration-stock-transfer-order-cross-company-001 (cross-company STO with intercompany billing type IV; shares delivery configuration concepts including the IV sales area)
See also: special-processes-intercompany-sales-process-001 (same sales area for intercompany billing; closely related organizational setup)
See also: shipping-outbound-delivery-creation-process-001 (standard outbound delivery process that NL replenishment deliveries extend)
See also: configuration-delivery-process-customizing-001 (delivery type configuration that includes NL)
