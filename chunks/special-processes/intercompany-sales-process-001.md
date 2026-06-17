---
schema_version: 1
id: special-processes-intercompany-sales-process-001
title: "Cross-Company Code Sales: Intercompany Billing Process"
area: special-processes
process_tags: [order-to-cash, intercompany, billing]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    relative_path: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
    pages: "46-68"
    source_type: A
    role: primary
transactions: [VA01, VF04, VF01]
tables: []
aliases:
  - cross-company code sales
  - intercompany billing
  - facturación intercompañía
  - venta entre sociedades
  - billing type IV
  - tipo de factura IV
  - intercompany price PI01
  - internal invoice cross-company
  - proceso venta entre códigos de sociedad
  - IV sales area
level: functional
status: draft
quality: medium
created: 2026-06-17
last_updated: 2026-06-17
---

# Cross-Company Code Sales: Intercompany Billing Process

## Operational Summary

A cross-company code sales process occurs when a sales organization belonging to one company code delivers goods from a plant assigned to a different company code. Two financial settlements are required: a standard customer invoice issued by the selling company code, and an intercompany billing document (internal invoice, billing type IV) issued by the delivering company code to the selling company code. This arrangement enables separate profit recognition, cost tracking, and general ledger postings in each company code while presenting a single sales transaction to the external customer.

## Questions This Chunk Answers

- What determines whether a sales order item triggers a cross-company code sales process?
- What are the two invoices created in a cross-company code sales process, and who receives each?
- What condition types carry the intercompany price in the sales order and in the internal invoice?
- How is the pricing procedure for the internal invoice determined?
- What Customizing settings connect the delivering plant to the intercompany billing sales area?
- How can the incoming invoice in the selling company code be posted automatically?
- Where are general ledger postings made for the customer invoice and the internal invoice?

## When It Applies and Context

A cross-company code sales process is triggered when the delivering plant of a sales order item is assigned to a different company code than the sales organization that received the order. This is possible only because allowed delivering plants are configured per combination of sales organization and distribution channel. One plant can be assigned as an allowed delivering plant to multiple sales organizations and distribution channels; conversely, one sales organization can use plants from different company codes.

The scenario requires careful setup of organizational assignments and business partner master data. The selling company code posts revenue to its general ledger from the customer invoice; the delivering company code posts revenue from the internal invoice and records costs from the goods issue. The intercompany price establishes the transfer price between the two company codes, which feeds profitability analysis (CO-PA) for both.

## Process Flow

1. **Sales order creation (VA01):** A standard sales order is entered in the selling sales organization (e.g., French organization 90FR). The delivering plant is determined from the customer-material info record, the ship-to party business partner master, or the material master — in that priority order. The system checks whether the combination of sales organization and determined plant is present in the *Allowed Delivering Plants* Customizing table. If the plant belongs to a different company code than the sales organization, the system recognizes this as a cross-company code sales item.

   Two prices are visible in the sales order: condition type PR00 represents the gross price for the end customer; condition type PI01 (*Inter-company Price*) represents the internal transfer price agreed between the two company codes. PI01 is *statistical* in the sales order and in the customer invoice — it influences profitability analysis for the selling company code but does not affect the net price billed to the customer.

2. **Outbound delivery and goods issue:** When the delivery creation date is reached, the cross-company code sales order appears automatically in the delivery due list for the shipping point assigned to the delivering plant. An outbound delivery is created and processed in the delivering plant. Standard shipping activities (picking, packing, goods issue) are executed. The goods issue posts a decrease in stock and an accounting document in the delivering company code; it does not affect the selling company code at this point.

3. **Customer invoice (selling company code):** After the goods issue, the outbound delivery appears in the billing due list of the selling sales organization. The customer invoice is created with reference to the outbound delivery. Billing types F2 or F1 are standard for document type OR. The invoice is posted in the selling company code (the company code to which the selling sales organization is assigned). The payer, sales area, and company code are all copied from the sales order. PI01 is statistical in this document — it appears as an informational cost figure for CO-PA, not as a billing line for the customer.

4. **Internal invoice — intercompany billing (IV billing type):** When the customer invoice is created in the selling company code, the outbound delivery simultaneously enters the billing due list of the sales organization responsible for intercompany billing in the delivering company code. This sales organization is assigned to the delivering plant in Customizing (*Cust.Inter-Co.Bill.* field). The internal invoice is created using billing type IV and uses the intercompany billing sales area (IV sales area) assigned to the delivering plant.

   In VF04 (Maintain Billing Due List), the *Intercompany Billing* flag must be set when selecting documents for the internal invoice — it is not included in a standard billing run without this flag. The standard billing sequence is: customer invoice first, intercompany invoice second (see SAP Note 38501 for reversing this sequence).

5. **Pricing in the internal invoice:** The internal invoice uses a separate pricing procedure (determined from the IV billing type's document pricing procedure, the IV sales area, and the customer pricing procedure in the payer's business partner master record). In this procedure, condition type IV01 (*Inter-company Price*) replaces PI01. IV01 references PI01 so no separate condition records are needed for IV01 — its value is taken directly from PI01. Unlike PI01, IV01 is *not statistical* in the internal invoice: it represents actual revenue for the delivering company code. Condition type PR00 (the customer price) is inactive in the internal invoice. The two condition types serve separate CO-PA purposes: PI01 transfers costs to the selling company code, IV01 transfers revenue to the delivering company code.

6. **Payer for the internal invoice:** The payer of the intercompany billing document is the selling company code (represented by a business partner master record with role FI Customer, created in the delivering company code). This business partner must be assigned to the IV sales area. The company code in which the internal invoice is posted is the delivering company code.

7. **Incoming invoice in the selling company code:** The selling company code must post the internal invoice as an incoming invoice in its accounts payable. Two approaches:
   - *Manual posting*: the selling company code receives the internal invoice and posts it manually.
   - *Automatic posting via EDI/IDOC*: the creation of the intercompany billing document triggers an automatic credit-side posting in the selling company code via EDI configuration. The logical address for the EDI partner profile is constructed from the invoicing company code and the payer's business partner number. For BRF+-based output, a dedicated output type (assigned to billing type IV) controls the automatic IDOC dispatch. For traditional Output Determination, output type RD04 triggers the automatic posting; output type RD00 delivers the invoice document to the payer.

## Account Postings

**Delivering company code (goods issue):** Stock account credited, cost of goods sold (COGS) account debited.

**Delivering company code (internal invoice):** Customer (payer — selling CC) account debited, revenue account credited using the IV01 intercompany price.

**Selling company code (customer invoice):** Customer (external customer) account debited, revenue account credited using PR00. PI01 is posted to a cost account used for CO-PA (not a balance-sheet account).

**Selling company code (incoming invoice):** Supplier (delivering CC) account credited, offsetting GR/IR or expense account debited.

## Customizing Configuration Points

- **Allowed delivering plants:** Assign each plant × sales organization × distribution channel combination. SPRO: *Enterprise Structure → Assignment → Sales and Distribution → Assign Sales Organization / Distribution Channel / Plant*.
- **Intercompany billing sales area (IV sales area):** Assign the sales organization for intercompany billing and its distribution channel and division to the delivering plant (*Cust.Inter-Co.Bill.* field). This same sales area is shared by intra- and cross-company stock transport orders.
- **Payer business partner master record:** Create in the delivering company code (role FI Customer). Assign to the IV sales area. Contains the intercompany billing currency.
- **Pricing procedure for internal invoice:** Assign via the IV billing type's document pricing procedure + IV sales area + customer pricing procedure of the payer's BP record.
- **Automatic incoming invoice posting (EDI):** Configure partner profiles and logical addresses in Customizing for intercompany billing (*Sales and Distribution → Billing → Intercompany Billing → Automatic Posting To Supplier Account*). Assign vendor/supplier number in the selling company code to receive the open item.

## Common Errors

| Symptom | Cause | Solution |
|---|---|---|
| Delivering plant not allowed for this sales org | Plant not in the allowed delivering plants table | Add the combination in Customizing |
| Internal invoice not appearing in billing due list | *Intercompany Billing* flag not set in VF04 | Set the flag when processing the billing due list for IV invoices |
| Wrong pricing procedure in internal invoice | IV billing type's document pricing procedure or IV sales area not correctly assigned | Verify pricing procedure determination: IV billing type + IV sales area + customer pricing procedure of payer |
| Automatic incoming invoice not posted | EDI partner profile missing or logical address incorrect | Check partner profile and logical address format (14 chars: CC code + BP number with leading zeros) |

## Cross-References

See also: special-processes-third-party-order-processing-001 (related SD-MM cross-application process)
See also: integration-stock-transfer-order-cross-company-001 (shares the IV billing type and IV sales area concept for cross-company STOs)
See also: configuration-billing-types-sap-s4hana-001 (billing type IV configuration)
See also: order-management-sales-distribution-process-001 (standard O2C baseline)
