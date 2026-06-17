# Validation Debt Ledger
Created: 2026-06-17
Purpose: Record judgment calls made without sign-off from a domain expert (functional SAP SD consultant). Each entry describes the decision, the evidence used, who made it, and its current review status. When an expert hour becomes available, start here — not with the full corpus.

## How to use
- Entries are added whenever a scope, provenance, or classification decision is made by agent judgment alone without explicit user confirmation.
- Status `needs-review` = no expert has validated this decision. Status `reviewed` = a functional consultant has confirmed or corrected it.
- Do NOT add decisions that are unambiguous (e.g., U5 subcontracting = MM pure, U7 appendix = not chunkable). Only genuine judgment calls belong here.

---

## Entries

### DEB-001 — U3 Intra-Company STO: Scope decision (in-scope as SD integration)

| Field | Value |
|---|---|
| **id** | DEB-001 |
| **document** | S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf |
| **unit** | Unit 3 — Intra-Company STO with SD Delivery (phys pages 76-92) |
| **chunk produced** | integration-stock-transfer-order-intra-company-001 |
| **decision type** | scope |
| **decided by** | agent-judgment (no expert sign-off) |
| **status** | needs-review |

**Decision:** Intra-company stock transport order (STO with document type UB) classified as IN SCOPE for the SD corpus.

**Evidence cited from source:**
- UB-type STOs generate an outbound delivery (delivery type NL) processed through SD shipping (picking, packing, goods issue via VL10G).
- The shipping side of the STO is an SD process: the supplying plant's shipping point, the outbound delivery document, and the goods issue are all native SD objects.
- No customer-facing billing is generated (intra-company, same legal entity), but the delivery processing is SD-standard.
- SAP S4680 U3 places this process in the S4HANA Sales and Procurement cross-application course alongside cross-company STOs that do have SD billing.

**Residual doubt:** A strict SD scope definition (SD = processes that originate from a customer sales order and end with a customer invoice) would exclude intra-company STOs. The classification as "integration" (SD-MM boundary) rather than "order-to-cash" was the agent's way of acknowledging the borderline. A consultant may decide these belong in an MM corpus instead.

**What would change the decision:** Expert confirms that intra-company STOs with SD delivery are routinely covered in SD functional training → keep. Expert confirms they belong exclusively to MM/SCM training → move chunk to MM scope, mark deprecated in SD corpus.

---

### DEB-002 — U6 L2 ARM Supplier Returns: Scope decision (deferred) + provenance fix applied

| Field | Value |
|---|---|
| **id** | DEB-002 |
| **document** | S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf |
| **unit** | Unit 6 Lesson 2 — ARM Supplier Returns (phys pages 164-172, estimated) |
| **chunk produced** | none (deferred) |
| **decision type** | scope + provenance |
| **decided by** | agent-judgment (no expert sign-off) |
| **status** | needs-review |

**Decision:** U6 L2 (supplier-side returns) classified as OUT OF SCOPE (MM pure). No standalone chunk created. Supplier returns are referenced in the ARM customer chunk body as context only.

**Evidence cited from source:**
- U6 L2 covers returning goods to the original vendor: movement type 122 (GR reversal), supplier return purchase orders. No SD sales order, no customer-facing document.
- The customer-side ARM (U6 L1 + L3) is clearly SD: RE2 returns order, SD credit memo request, SD billing.
- Supplier returns are logically downstream of the customer return (the company decides to return defective goods to vendor) but are executed entirely in MM procurement.

**Provenance fix applied (2026-06-17):**
During S4680 processing, content from U6 L2 was incorrectly summarised into the body of `special-processes-advanced-returns-management-001`:
- "movement type 122 for GR reversal or separate supplier return orders" — MM-specific detail from uncited pages
- Note about intercompany ARM variant ("noted in the source material as a further extension but not detailed in the pages in scope") — explicitly referenced content outside the cited range

Both passages were removed from the body. The remaining scope boundary statement ("supplier-side returns are MM processes outside the scope of this chunk") is correct and sourced from the overall framing of U6 in S4680. Audit trail preserved via `<!-- L2 content removed -->` comment in the chunk file.

**Residual doubt:** A fuller SD corpus might include supplier returns as a cross-reference chunk (type: integration) because returns consultants need to understand the end-to-end flow. The current decision defers to MM — but there is no MM corpus yet.

**What would change the decision:** Expert confirms supplier returns are regularly part of SD returns consulting scope → create integration chunk with MM caveat. Expert confirms supplier returns belong exclusively to MM → current decision is correct.

---

## Summary

| Entry | Document | Unit | Type | Decision | Status |
|---|---|---|---|---|---|
| DEB-001 | S4680 | U3 Intra-Company STO | scope | In-scope as SD integration | needs-review |
| DEB-002 | S4680 | U6 L2 ARM Supplier Returns | scope + provenance | Deferred (MM pure); provenance fix applied | needs-review |
