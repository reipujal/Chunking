---
schema_version: 1
id: pricing-statistical-condition-types-001
title: "Statistical Condition Types and Tax Determination in SAP SD"
area: pricing
process_tags: [order-to-cash, pricing]
chunk_type: concept
sap_release: S/4HANA 2020
sources:
  - file: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    relative_path: "S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf"
    pages: "76-84"
    source_type: A
    role: primary
transactions: []
tables: [T052, T001R]
aliases:
  - VPRS cost condition SAP
  - coste condición estadística SAP
  - SKTO cash discount pricing
  - descuento por pronto pago condición SAP
  - EDI1 EDI2 customer expected price SAP
  - precio esperado cliente SAP
  - MWST tax condition SAP
  - determinación de impuestos SAP SD
  - tax determination SAP sales order
  - impuesto en pedido de ventas SAP
  - statistical condition pricing procedure
  - condición estadística esquema precios
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Statistical Condition Types and Tax Determination in SAP SD

## Operational Summary
*Statistical condition types* participate in pricing but do not affect the net value of the document — they are marked as statistical in the pricing procedure. SAP SD delivers condition types for cost (VPRS), cash discount (SKTO), and customer expected price (EDI1/EDI2) as standard statistical conditions. Tax determination uses the condition technique through MWST or TTX1, with the tax procedure assigned at country level in FI; US-specific procedures (TAXUS, TAXUSJ, TAXUSX) provide different calculation models. Statistical conditions can optionally be flagged for posting to CO-PA.

## Questions This Chunk Answers
- What is VPRS and how does it determine the cost of a material in pricing?
- What is SKTO and how does it retrieve the cash discount rate?
- How does customer expected price (EDI1/EDI2) work and what happens when prices differ?
- How is tax determined in SAP SD sales orders?
- What is the priority rule for determining the sales tax ID when payer, sold-to, and ship-to differ?
- Which US-specific tax procedures exist and how do they differ?
- What does "Statistical and Relevant for Account Determination" mean for CO-PA?

## Definition

### VPRS — Cost (Standard Cost / Moving Average Price)
*VPRS* retrieves the cost of the material from the material master valuation segment. In the pricing procedure, VPRS is marked as statistical so it does not reduce the net value. Condition category controls which cost is accessed:
- **Category G:** standard cost or moving average, as specified in the material master
- **Category S:** always standard cost
- **Category T:** always moving average cost

Formula 11 in the pricing procedure calculates the profit margin: net value minus the cost retrieved by VPRS.

### SKTO — Cash Discount
*SKTO* retrieves the cash discount rate from table T052 using condition category E. The system calculates the discount amount from the first percentage rate of the item's payment terms. SKTO is marked as statistical in the pricing procedure.

### EDI1 / EDI2 — Customer Expected Price
Customers in industries such as consumer packaged goods can submit an expected price during order entry to avoid later invoice disputes. The expected price is entered:
- Manually in the double-line overview screen of the sales order
- Directly on the pricing screen using condition type EDI1 (customer expected price) or EDI2 (customer expected value)

Formula 8 (SAP standard) compares the expected price with the actual price. If the difference exceeds the specified threshold, SAP assigns an *incompletion status* to the order: the order cannot be processed for delivery or billing until the discrepancy is resolved.

Resolution options in the *Manage Sales Documents with Customer-Expected Price* app:
- **Accept:** manually adjust the net price within the app.
- **Decline:** release the item for further processing at the existing net price.
- **Reject:** exclude the item from further processing (customer and supplier cannot agree).

The app also displays customer contact information relevant to the item and allows navigation to related apps.

### VPRS and SKTO as Statistical
Both VPRS and SKTO are statistical: they appear on the pricing screen for information and for downstream calculations (profit margin via formula 11; payment terms reference), but they do not affect the customer-facing net value of the order.

## Statistical and Relevant for Account Determination (CO-PA)
The *Statistical and Relevant for Account Determination* indicator on a condition type defines whether that statistical condition is posted to account-based CO-PA (Profitability Analysis). When set, the statistical condition value is posted as a journal entry to an extension ledger of Financial Accounting. Use cases include warranties, delivery costs, surcharges, discounts, and commissions that must appear in management reporting but not in the customer-facing document value.

## Tax Determination

### Sales Tax ID Priority Rules
The rule for determining the sales tax identification number is assigned at sales organization level (blank / A / B):

**Rule blank (standard priority):**
1. If the payer (PY) has a sales tax ID and differs from the sold-to party (SP): take tax ID and classification from PY; ship-to party (SH) is irrelevant.
2. If rule 1 does not apply and SH has a sales tax ID: take from SH.
3. If rule 2 does not apply: take from SP.

**Rule A:** always take from SP per tax destination country.
**Rule B:** always take from PY using the same method as rule A.

### Tax Rate Determination
The tax rate in the order or billing document is based on three criteria:
- Business transaction type (domestic, export, or import)
- Tax liability of the ship-to party
- Tax liability of the material

### Tax Condition Types
Standard condition types: **MWST** (standard tax) and **TTX1** (alternative). The tax condition type is entered in the pricing procedure. The access sequence finds the appropriate condition record based on the current key combination.

### Tax Procedure Assignment
The tax procedure is assigned to a country in the basic settings of Financial Accounting. For the United States, three procedures are available:

| Procedure | Behavior |
|---|---|
| TAXUS | Tax calculated in SD |
| TAXUSJ | Jurisdictional tax; uses tax jurisdiction code from ship-to party master; pricing procedure RVAJUS; condition types UTXJ, JR1–JR4 |
| TAXUSX | Tax calculated via RFC to a central tax system; pricing procedure RVAXUS; condition types UTXJ, XR1–XR6 |

In both TAXUSJ and TAXUSX, condition type UTXJ initiates the tax calculation.

## Relationship with Other SAP SD Objects
- *VPRS* reads the material master (valuation segment); requires material master to have standard cost or moving average cost maintained
- *SKTO* reads payment terms table T052; the payment terms on the sales order determine the cash discount percentage
- *EDI1/EDI2* interact with the incompletion procedure: a price discrepancy sets the order to incomplete, blocking delivery and billing
- *MWST/TTX1* are controlled by the tax procedure assigned to the country in FI; the ship-to party's tax liability field in the customer master is a key input
- Statistical conditions marked for CO-PA are posted to account-based CO-PA via extension ledgers in Financial Accounting

## Cross-References
- Prior step: pricing-special-condition-types-001
- Next step: pricing-pricing-agreements-001
- See also: pricing-condition-technique-overview-001
- See also: integration-general-billing-interface-001
