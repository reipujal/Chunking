# Reference Examples — Validated Chunks

From `SD - Shipment.pdf` (Type B). Use as reference for **technical density, section format, and writing style** — not as a template for which T-codes or tables to list.

> These examples come from a visual deck whose figures show SAP GUI screens, so T-code lists were read off legible screenshots. A conceptual S46xx course that only names transactions by function yields `transactions: []` — which is correct. Do NOT copy T-code lists into a new chunk. Apply the provenance rule: list only what the current source literally contains. The `<!-- inferred -->` comments are the right place for relevant-but-unsourced identifiers.

---

## Example 1 — chunk_type: process

```markdown
---
schema_version: 1
id: shipping-delivery-creation-process-001
title: "Creating Outbound Deliveries in SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2-9"
    source_type: B
    role: primary
transactions: [VL01N, VL10E, VL02N, VL03N, VL06O]
tables: []
aliases:
  - outbound delivery
  - entrega de salida
  - crear entrega
  - delivery creation
  - creación entrega
level: functional
status: draft
quality: high
created: 2026-06-01
last_updated: 2026-06-01
---

# Creating Outbound Deliveries in SAP SD

<!-- inferred tables, pending validation: LIKP, LIPS, VBUK -->

## Operational Summary
An *outbound delivery* is the document that initiates the physical shipping process against a customer order. SAP allows creating it individually for a specific order or collectively for a set of pending orders. Only *schedule lines* confirmed up to the *selection date* are included.

## Questions This Chunk Answers
- How is an outbound delivery created in SAP SD?
- What is the difference between creating deliveries individually and collectively?
- Why are no items generated in the delivery even though there is stock?
- What is the *selection date* and how does it affect deliveries?

## When It Applies and Context
The delivery is created after the order has confirmed *schedule lines*. It is the step before picking, packing, and *Goods Issue*.

## Process Flow

### Option 1 — Individual Delivery from the Order (VA02)
1. Open the order with **VA02**
2. Menu: *Sales document > Deliver*
3. SAP redirects to VL01N with the order pre-filled
4. Verify *Shipping point* and *Selection date* → Confirm

### Option 2 — Direct Individual Delivery (VL01N)
1. Run **VL01N**
2. Enter *Shipping point*, *Selection date*, and order number → Confirm

### Option 3 — Collective Deliveries (VL10E)
1. Run **VL10E**
2. Criteria: *Shipping point*, date range; optional: route, *ship-to*, sales org.
3. Select lines → choose **Dialog** (manual) or **Background** (batch)

## Conditions and Restrictions
- Only confirmed *schedule lines* (ATP approved)
- *Selection date* filters: only lines confirmed up to that date
- *Shipping point* must be assigned to the order's plant

## Common Errors
**"No schedule lines due for delivery up to the selected date"**
→ Selection date earlier than confirmation date. Extend it.

**Order does not appear in VL10E**
→ Verify Shipping point match and that schedule lines are not blocked.

## Cross-References
- See also: shipping-delivery-types-concept-001
- Next step: shipping-goods-issue-001
```

---

## Example 2 — chunk_type: concept

```markdown
---
schema_version: 1
id: shipping-delivery-types-concept-001
title: "Outbound Delivery in SAP SD — Concept and Structure"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2, 10"
    source_type: B
    role: primary
transactions: [VL01N, VL02N, VL03N]
tables: []
aliases:
  - outbound delivery
  - entrega de salida
  - delivery document
  - documento de entrega
level: functional
status: draft
quality: medium
created: 2026-06-01
last_updated: 2026-06-01
---

# Outbound Delivery in SAP SD — Concept and Structure

<!-- inferred tables, pending validation: LIKP, LIPS -->

## Operational Summary
The outbound delivery is the logistics document representing the physical shipment of goods against a customer order. It has a header with recipient data and items with the materials. It has no *schedule lines*. It is the pivot between order management (SD) and the warehouse (WM/EWM).

## Questions This Chunk Answers
- What is an outbound delivery in SAP SD?
- What structure does the delivery document have?
- How does the delivery differ from the sales order?

## Definition
SAP SD document representing the intent and execution of sending goods to a customer. Created with reference to a sales order, inheriting its shipping data.

## Purpose in the SD Process
Enables picking, packing, recording loading, executing *Goods Issue* (reduces stock, generates FI document), and serves as billing basis.

## Structure and Variants

| Level | Data Contained |
|---|---|
| Header | Ship-to party, delivery date, shipping point, total weight, packages |
| Item | Material, quantity, unit of measure, batch, picking status |

Unlike the order, the delivery **has no schedule lines**.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order | Delivery created with reference; inherits ship-to, materials, confirmed quantities |
| Transfer Order (WM) | If WM active, generates a transfer order for picking |
| Goods Issue | Executed on the delivery in VL02N |
| Invoice | Created with reference to the delivery after GI |

## Cross-References
- Creation process: shipping-delivery-creation-process-001
- Next step: shipping-goods-issue-001
```

---

## Example 3 — chunk_type: transaction

```markdown
---
schema_version: 1
id: shipping-goods-issue-cancel-vl09-001
title: "Cancelling Goods Issue with VL09"
area: shipping
process_tags: [returns, delivery-processing]
chunk_type: transaction
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "15"
    source_type: B
    role: primary
transactions: [VL09]
tables: []
aliases:
  - cancel GI
  - cancelar GI
  - reverse goods issue
  - VL09
  - cancelar salida de mercancias
  - revertir GI
level: functional
status: draft
quality: medium
created: 2026-06-01
last_updated: 2026-06-01
---

# Cancelling Goods Issue with VL09

<!-- inferred tables, pending validation: LIKP, MKPF -->

## Operational Summary
**VL09** reverses a *Goods Issue* posted in error. Undoes the stock decrease and cancels the FI accounting document. Only possible within the same accounting period as the original GI.

## Questions This Chunk Answers
- How do you cancel a Goods Issue posted in error?
- When is VL09 no longer possible?
- What is the alternative if the accounting period is closed?

## When to Use This Transaction
When a GI was posted in error and the accounting period is still open in FI.

## Affected Business Object
Outbound delivery with a posted GI.

## Key Fields on the Main Screen

| Field | Description | Notes |
|---|---|---|
| Shipping point | Shipping point | Required |
| Delivery number | Number of the delivery | Enter directly |
| Define date | Reversal date | Defaults to today |

## Typical Usage Flow
1. Run **VL09**
2. Enter Shipping point and delivery number
3. Select the line → Execute *Cancel/Reverse*
4. Delivery returns to open status

## Restrictions
Only in the **same accounting period** as the original GI. If period closed: use customer return (Returns Order + Return Delivery + GR).

## Common Errors
**"Reversal not possible — period already closed"** → Proceed with customer return.

## Cross-References
- Prior step: shipping-goods-issue-001
- Alternative if period closed: special-processes-customer-returns-001
```

---

## What to Observe in These Examples

- **Operational Summary**: 3-5 lines with the complete concept. If you cannot write it without filler, the chunk is poorly delimited.
- **Real questions**: specific, what a consultant would ask on a real project — not generic.
- **No empty sections**: example 3 omits sections the source did not cover. No invented filler.
- **Terminology**: SAP terms in English in italics in the body. Spanish equivalents in `aliases`.
- **quality: medium vs high for Type B**: `medium` is the default for Type B.
- **Correct chunk_type**: VL09 is `transaction`, not `configuration`.
