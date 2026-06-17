---
schema_version: 1
id: integration-stock-transfer-order-cross-company-001
title: "Stock Transport Order: Cross-Company Code Stock Transfer with Intercompany Billing"
area: integration
process_tags: [stock-transfer, intercompany, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    relative_path: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    pages: "100-117"
    source_type: A
    role: primary
transactions: [ME21N, VF04, VF01, MMBE]
tables: []
aliases:
  - cross-company stock transfer
  - STO intercompañía
  - traslado de stock entre sociedades
  - stock transport order different company codes
  - delivery type NLCC
  - tipo de entrega NLCC
  - intercompany billing STO
  - factura interna traslado entre sociedades
  - IV01 condition type stock transfer
  - cross-company code replenishment delivery
level: functional
status: draft
quality: high
created: 2026-06-17
last_updated: 2026-06-17
---

# Stock Transport Order: Cross-Company Code Stock Transfer with Intercompany Billing

## Operational Summary

A cross-company code stock transfer moves materials between plants belonging to different company codes using a standard purchase order (document type NB), an SD outbound delivery, and an intercompany billing document. Because two company codes are involved, a financial settlement between them is mandatory: the supplying company code issues an internal invoice to the receiving company code using the SD billing type IV. The process integrates SAP S/4HANA Procurement (purchase order, goods receipt, invoice receipt) with SAP S/4HANA Sales (SD outbound delivery with delivery type NLCC, intercompany billing). No customer-facing sales order is created; the STO serves as the controlling document.

## Questions This Chunk Answers

- What purchase order document type is used for a cross-company code stock transport order?
- What is delivery type NLCC and how is it assigned in Customizing?
- How is the internal invoice created for the cross-company code stock transfer, and what condition type represents the price?
- How does the system determine the sales area for intercompany billing in the STO context?
- What happens to the incoming invoice in the receiving company code if it is posted before the goods receipt?
- What is the difference between document types UB and NB for stock transport orders?
- How are the goods issue and goods receipt valued across two company codes?

## When It Applies and Context

A cross-company code stock transfer is required when a receiving plant in one company code needs to procure materials from a supplying plant in a different company code within the same enterprise. Unlike an intra-company STO (document type UB), which settles internally without billing, a cross-company STO requires financial settlement between the two company codes via an intercompany billing document (billing type IV). This process shares key Customizing with cross-company code sales (Unit 2 of S4680): the same IV sales area assigned to the supplying plant, the same payer business partner master record, and the same pricing procedure determination logic.

The SD consultant's role in this process covers delivery type NLCC configuration, the sales area assignment to the supplying plant, and intercompany billing creation and output.

## Process Flow

1. **Stock transport order creation (ME21N):** The purchasing department of the receiving plant creates a standard purchase order with document type *NB* (*Standard PO*) — not document type UB. This is the critical distinction: UB is used for intra-company STOs; NB is used for cross-company STOs where intercompany billing is required. Document type NB requires a supplier (vendor) to be specified. The supplying plant is assigned to this supplier in the supplier's business partner master record; when the supplier is entered in the STO, the system automatically copies the supplying plant from the BP master into the purchase order. MRP in both plants considers this STO for planning and scheduling.

   The internal transfer price is managed via pricing master data (purchasing info records) configured for the supplier-material-plant combination. The goods are issued at their valuation price from the supplying plant; the receiving plant values the GR using the purchase order price.

2. **Outbound delivery creation (replenishment delivery):** When the STO is due for shipping, a replenishment delivery is created using collective processing. The delivery type for a cross-company code STO is *NLCC* (*Replen.Cross-Company*). This delivery type is assigned in Customizing to the combination of purchase order document type NB and the supplying plant. The ship-to party (goods recipient) for the delivery is determined from the business partner master record assigned to the receiving plant — the same concept as in the intra-company STO (the sales area assigned to the supplying plant drives this configuration).

3. **Shipping activities (supplying plant):** All standard shipping activities are executed using the NLCC replenishment delivery: picking (optionally via SAP EWM or Stock Room Management), packing, and goods issue. The goods issue decreases the unrestricted-use stock in the supplying plant and creates accounting entries in the supplying company code. After the goods issue, the quantity in the supplying plant reflects the issued stock; the receiving plant shows a *cross-company code stock in transit* quantity (two-step procedure) until the goods receipt is posted.

4. **Intercompany billing (supplying company code):** After the goods issue, the replenishment delivery enters the billing due list of the sales organization responsible for intercompany billing in the supplying company code (the IV sales organization assigned to the supplying plant). An internal invoice is created using billing type *IV*. In VF04, the *Intercompany Billing* flag must be set to include these deliveries in the billing run.

   The internal invoice uses the IV sales area (assigned to the supplying plant in Customizing) and the pricing procedure determined from: the document pricing procedure stored in billing type IV, the IV sales area, and the customer pricing procedure from the payer's business partner master record. Condition type *IV01* (*Inter-company Price*) represents the internal transfer price. The billing type for the internal invoice is proposed from the default sales document type *DL* (*Order Type Sched.Ag.*), which is assigned to delivery type NLCC in Customizing — DL is the pseudo sales document type used for intercompany billing when no real sales order exists.

   Optionally, the creation of the intercompany billing document automatically triggers posting of the incoming invoice in the receiving company code via EDI/IDOC (based on message control using BRF+ or traditional Output Determination, same configuration as for cross-company code sales).

5. **Goods receipt in the receiving plant:** When the materials arrive at the receiving plant, the goods receipt is posted with reference to the stock transport order (NB) or the replenishment delivery. Movement type 101 is used. The GR is valuated using the purchase order price (the internal transfer price). If the goods receipt is posted with reference to the delivery, the delivery document flow is updated. If posted with reference to the STO (purchase order), a system message (M7 352) may appear; its severity (warning or error) is configurable in IM Customizing.

   If the incoming invoice was already posted before the GR (e.g., via automatic EDI posting), a payment block is applied to the invoice. The block is removed automatically once the goods receipt is posted.

6. **Invoice receipt in the receiving company code:** The internal invoice from the supplying company code is entered as an incoming invoice in the receiving company code. It can be posted manually or automatically triggered via EDI when the intercompany billing document is created in the supplying company code (same approach as for cross-company code sales in Unit 2). The incoming invoice creates an accounts payable open item in the receiving company code, which is released for payment after the goods receipt.

## Key Differences: UB vs NB Stock Transport Orders

| Dimension | UB (Intra-company STO) | NB (Cross-company STO) |
|---|---|---|
| Companies involved | Same company code | Two different company codes |
| Supplier in PO | Not required (plant entered directly) | Required (supplying plant via BP master) |
| Delivery type | NL | NLCC |
| Billing document | None | IV (intercompany billing) |
| Pricing in PO | Delivery costs only | Transfer price via purchasing info record |
| Accounting at GR | Not valuated (same CC) | Valuated (PO price used) |

## Account Postings

**Supplying company code — Goods issue:** Stock account credited (at material valuation price); offsetting posting to a transit/clearing account.

**Supplying company code — Intercompany billing (IV):** Customer (payer = receiving CC) debited; revenue account credited with the IV01 internal price.

**Receiving company code — Goods receipt:** Stock account debited (at PO price); GR/IR clearing account credited.

**Receiving company code — Invoice receipt:** GR/IR clearing account debited; supplier (supplying CC) account credited. Payment block removed after GR.

## Customizing Configuration Points

**Delivery type NLCC assignment:** Assign NLCC to the combination of NB document type and supplying plant. SPRO: *Logistics Execution → Shipping → Deliveries → Define Delivery Types* (for NLCC details); assignment in *Materials Management → Purchasing → Purchase Order → Set Up Stock Transport Order → Assign Delivery Type and Checking Rule*.

**Sales area assignment to supplying plant:** Same Customizing as for intra-company STO. The IV sales area assigned here is also used for cross-company code sales intercompany billing.

**Billing type proposal for NLCC deliveries:** Delivery type NLCC is assigned to default sales document type DL in Customizing. DL determines billing type IV. SPRO: *Sales and Distribution → Billing → Billing Documents → Define Billing Types*.

**Intercompany billing Customizing:** Assign the IV sales organization and distribution channel/division to the supplying plant (*Cust.Inter-Co.Bill.*). Create the business partner master record for the payer (receiving company code) with role FI Customer in the supplying company code.

**Automatic incoming invoice:** Configure EDI partner profiles and logical address (14 characters: supplying CC + payer BP number) as for cross-company code sales. SPRO: *Sales and Distribution → Billing → Intercompany Billing → Automatic Posting To Supplier Account*.

## One-Step vs Two-Step Procedure in Cross-Company STOs

As in the intra-company STO process, cross-company code stock transfers support both a one-step and a two-step procedure for goods movements:

- *Two-step procedure*: when the goods issue is posted in the supplying plant, the transferred quantity enters a *cross-company code stock in transit* state in the receiving plant. This stock is visible in MMBE. A separate goods receipt posting (movement type 101) must be made in the receiving plant when the goods arrive. The goods receipt is *valuated* (at the PO price) because the two plants belong to different company codes — unlike the intra-company case, where GR is not valuated.
- *One-step procedure*: the goods receipt is posted automatically at the moment the goods issue is processed. Used when the two plants are physically adjacent and no separate receiving confirmation is needed.

The choice between one-step and two-step is configured per issuing plant / receiving plant combination in Customizing and has direct implications for payment block timing: in the two-step procedure, an incoming invoice posted before the GR is automatically payment-blocked until the GR is posted. In a one-step setup, GR is always complete before or with the goods issue, so no payment block arises from GR sequencing.

## Conditions and Restrictions

- Document type NB must be used (not UB): UB does not support intercompany billing and cannot be used when two company codes are involved.
- The internal invoice is created by the supplying company code's sales organization — the intercompany billing flag must be set in VF04 or the delivery will not appear in a standard billing run.
- If the incoming invoice is posted before the goods receipt (two-step procedure), a payment block is applied. This block is released automatically upon GR.
- Cross-company stock in transit is visible in MMBE for the receiving plant and can optionally be included in availability checks.

## Cross-References

See also: integration-stock-transfer-order-intra-company-001 (intra-company STO; shares delivery configuration concepts)
See also: special-processes-intercompany-sales-process-001 (same IV billing type, IV sales area, and payer BP master record logic)
See also: configuration-billing-types-sap-s4hana-001 (billing type IV configuration)
See also: configuration-delivery-process-customizing-001 (delivery type configuration for NLCC)
