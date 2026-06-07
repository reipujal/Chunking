---
schema_version: 1
id: order-management-value-contracts-001
title: "Value Contracts in SAP SD"
area: order-management
process_tags: [order-to-cash, billing-plans]
chunk_type: process
sap_release: S/4HANA 2020
sources:
  - file: "S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    relative_path: "processed/S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf"
    pages: "114-126"
    source_type: A
    role: primary
transactions: []
tables: []
aliases:
  - value contract
  - contrato por valor
  - contrato WK1 WK2
  - partners authorized to release contract
  - como funciona un contrato por valor
  - assortment module product hierarchy contract
  - modulo surtido jerarquia producto contrato
  - release order from value contract
level: functional
status: draft
quality: high
created: 2026-06-07
last_updated: 2026-06-07
---

# Value Contracts in SAP SD

## Operational Summary
A *value contract* is an outline agreement between seller and customer specifying that the customer commits to purchasing a fixed target value of goods and services during a defined period. Value contracts can include special price agreements, customer restrictions, and material restrictions that are enforced when release orders are created. Two standard types exist: WK1 (general value contract) and WK2 (material-related value contract). Release orders consume the contract value and are processed like standard orders. Billing can target either the release orders or the contract itself.

## Questions This Chunk Answers
- What is a value contract in SAP SD?
- How can valid materials be restricted in a value contract?
- Can a value contract be billed directly without a release order?
- Which partners are authorized to release from a contract?
- How are contract dates proposed and controlled?
- What is the difference between WK1 and WK2?
- How does item category determination work for value contracts?

## When It Applies and Context
Use a value contract when the commercial agreement is based on a target amount rather than fixed schedule lines or fixed quantities. Typical scenarios include blanket purchase agreements and framework contracts where the customer can release individual orders over time until the agreed total value is consumed.

## Process Flow
1. Create the value contract for a customer and agreed target value. The system can notify users during release order entry that a valid contract exists, if configured.
2. Restrict valid materials if needed using a product hierarchy (generic search supported, e.g., `0000101*`), an assortment module, or both. If both are maintained, materials matching either are valid (logical OR).
3. Maintain partners authorized to release. Partners can be stored directly in the contract's partner screen (partner function AA for authorized releasers, AW for alternative ship-to parties).
4. Create release orders against the contract. Search for the relevant contract by partner number or by contract number. Use item selection to choose materials directly or by exploding an assortment module. Releases can be created in any currency; the total open value is tracked in the contract currency.
5. The system re-runs pricing automatically when an order is assigned to a contract at item level.
6. Bill either the release orders (order-related or delivery-related via billing type OR) or the value contract itself using a billing plan (billing type WA).
7. Use contract data and date determination rules to control validity, start/end dates, duration, and follow-up activities.

## Material Restrictions
Material restrictions define which products a customer can release against the contract:

| Restriction method | How it works |
|---|---|
| Product hierarchy | Enter first digits for generic search (e.g., `0000101*`); all materials in that hierarchy are valid |
| Assortment module | Maintained in sales master data; each material has a validity period within the module |
| Both methods combined | Materials matching either the product hierarchy OR the assortment module are valid (OR link) |

If no restrictions are defined, all materials permitted in the assigned sales area can be released (subject to copying control restrictions).

## Value Contract Types and Item Categories
Two standard value contract types are defined:

| Type | Name | Usage |
|---|---|---|
| WK1 | General value contract | Any materials and services from the restriction options |
| WK2 | Material-related value contract | Exactly one material, such as a configurable product |

WK1 and WK2 differ in Customizing only in the screen sequence group for document header and item. WK1 uses item category WKN (item category group VCIT, usage indicator VCTR). WK2 uses item category WKC. Copying control at item level determines whether the value contract material is copied to the release order (WKC) or not (WKN). The *value contract material* maintained in the item category acts as a technical vehicle for account assignment, taxes, and statistical updates.

**Pricing:** Value contracts use pricing procedure WK0001 with condition type WK00 for the agreed target value.

## Billing Options

| Billing option | How it works |
|---|---|
| Bill the release order | Use standard order type OR; billing can be order-related or delivery-related |
| Bill the value contract directly | Use billing type WA; a billing plan allows billing for several dates and partial quantities |

When the target value in a contract item changes, the system automatically adjusts open billing plan dates. SAP does not allow automatic billing of value contracts that have not been completely released.

If a release order exceeds the remaining open value of a contract item, Customizing controls the system response: no reaction, a warning message (two levels), or an error.

## Partner Authorization for Releases
Normally the sold-to party and other business partners defined in the contract are authorized to release. The *Check partner authorization* field in Customizing for the sales document type activates partner authorization control:
- **Rule A (customer list):** Partners authorized to release are stored directly in the partner screen of the contract (partner function AA). If there are already multiple sold-to parties in the customer master (functions SP and AA), a selection screen appears when the contract is created.
- **Rule B (customer hierarchy):** Authorization is checked through the customer hierarchy.

If several partners are authorized, a selection list appears when creating the release order. If the releasing partner differs from the sold-to party on the contract, copying control uses requirement 002 (Header - Diff Customer). Alternative ship-to parties are represented by partner function AW.

## Contract Data and Date Determination
Contract data can be activated in the sales document type (blank = none, X = permitted without automatic propagation to items, Y = permitted with automatic propagation if header and item data were identical). Changes under option Y are saved in a log including any inconsistencies.

Date determination rules control start and end date proposals when a contract is created. If a contract profile is assigned to the sales document type, the system automatically determines default values specific to the contract:
- Rules for start and end date determination
- Duration category (to automatically generate contract duration)
- Subsequent activities
- Cancellation procedure

## Common Errors
**Release exceeds target value and system response is wrong**
-> Review the Customizing setting for how the system reacts when a release order exceeds the open contract value (no reaction, warning, or error).

**Wrong partner can release from the contract**
-> Check the *Check partner authorization* field and the partner determination procedure; verify which partner functions are assigned (AA, AW).

**Contract dates are not proposed**
-> Assign a contract profile to the sales document type; define date determination rules and duration categories in Customizing.

**Item category not determined for release order**
-> For WK1 contracts, item category determination uses item category group VCIT. For WK2, usage indicator VCTR drives item category WKC.

## Cross-References
- Prior step: order-management-outline-agreements-scheduling-quantity-contracts-001
- See also: billing-billing-plans-concept-001
- Next step: master-data-material-determination-001
