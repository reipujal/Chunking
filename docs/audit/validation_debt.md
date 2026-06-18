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

### DEB-003 — S4680 U1 + U6: 2nd Provenance Audit (status: resolved)

| Field | Value |
|---|---|
| **id** | DEB-003 |
| **document** | S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf |
| **units audited** | U1 (third-party, phys pp 8-21 / 33-38) and U6 L1 (ARM customer returns, phys pp 155-163) |
| **chunks audited** | special-processes-third-party-order-processing-001, special-processes-advanced-returns-management-001 |
| **decision type** | provenance audit — verification pass |
| **decided by** | agent-judgment + pdftotext extraction against cited page ranges |
| **status** | resolved |

**Audit method:** pdftotext extraction of exact cited page ranges; grep for target tokens. Cross-checked 190 physical pages for "consignment", "SPRO" (0 hits each). Checked U1 pp 8-21/33-38 for "intercompany", "billing type IV", "1Z3", "billing block" (0 hits each). Checked U6 pp 155-163 for "billing block" (0 hits).

**Findings and fixes applied (2026-06-18):**

**Type A — Cross-unit citations (U1 body stated facts from other units):**
- *Intercompany billing type IV*: present in U2 (pp 46-68), not U1. Body paragraph removed. Cross-reference to special-processes-intercompany-sales-process-001 preserved.
- *Scope item 1Z3*: present at phys p 174 only, not U1 cited range. Body paragraph removed. Cross-reference to special-processes-advanced-returns-management-001 preserved.
- The entire `## Integration with Other SAP Processes` section was deleted; an HTML comment documents the excision and reasons.

**Type B — Inserted terms/concepts absent from source:**
- *Consignment*: 0 occurrences across 190 pages. "Consignment stock interaction" paragraph deleted. No replacement cross-reference (no consignment chunk exists; MM/SD consignment is out of S4680 scope).
- *"SPRO"*: source consistently uses "Customizing" and "SAP Customizing Implementation Guide". The term "SPRO" never appears. All 4 occurrences in U1 relabeled: "SPRO path:" → "Customizing path:"; "SPRO:" → "Customizing:"; "in SPRO copying control" → "in Customizing (copying control)".
- *"billing block"* (U6): source (p 150) describes ECC RE returns as having no refund codes, no automatic follow-up activities, no automatic credit memo request creation — the term "billing block" does not appear. Two occurrences replaced with paraphrase from source: process-flow sentence updated; comparison table cell "Manual billing block + credit memo" → "Manual credit memo — no refund codes, no automatic follow-up activities".

**Density impact:**
- U1 (third-party): 83 w/p → 87.1 w/p after removals (Integration section excised ~180 words; body was already below the removed content's weight). Band: 80-99 w/p. `quality: medium` confirmed correct.
- U6 (ARM): substitutions only; density unchanged.

**Conclusion:** No fabrication found. Two categories of insertion error: cross-unit citation (IV/1Z3 from other units) and absent-term insertion (consignment, SPRO, billing block). All corrected. Validator: 0 errors (92 OK).

---

### DEB-004 — Credit Management chunked from S4F30 (2019) + BD6: HIGH RISK

| Field | Value |
|---|---|
| **id** | DEB-004 |
| **document** | S4F30_EN_Col12 Order to Cash Optimizations with SAP Receivables Management in SAP S4 HANA.pdf + BD6 scope item |
| **units** | U2 L1-L4 (phys 20-43); U2 L5-L6 and U3-U5 deferred (scope: FI-AR / cloud) |
| **chunks produced** | credit-management-credit-master-data-001, credit-management-credit-check-sd-integration-001, credit-management-credit-rules-engine-001 |
| **decision type** | scope + provenance + version risk |
| **decided by** | agent-judgment (no expert sign-off) |
| **status** | needs-review — HIGH RISK |

**Risk factors:**
1. **Source release 2019 (S/4HANA 1909):** FSCM credit management is relatively stable 1909→2020, but UI details (Fiori app names, T-code aliases, configuration paths), BAdI names, and reporting structures may have changed. No version delta was available for formal comparison.
2. **Provenance audit (manual, 2026-06-18) — COMPLETED:** Affirmation-by-affirmation audit performed against pdftotext of S4F30 cited page ranges (phys 20-43). All technical identifiers traced to source (UKM000 p26; FUKM001/TUKM001/TUKMSB0/TUKMSBG p29; UKM_COMMITMENTS p29; UKM_ITEM + commitment types 100/200/300/400/500 p31; UKM_TRANSFER_ITEMS p31; UKM_TRANSFER_VECTOR p32). Four provenance findings identified and corrected (F1–F4): F1 — "S/4HANA Cloud" specificity absent from source, replaced with "external credit information"; F2 — "levels" → "hierarchies" (source: "max. 10 hierarchies"); F3 — "(for document blocks)" parenthetical absent from source, removed; F4 — WS-RM row in Common Errors sourced from p23 (outside original 30-38 range): pages field extended to "23, 30-38" and row text scoped to distributed-system context. credit-rules-engine-001 clean — no findings. Residual trust level: provenance_audited for F1–F4 scope; functional_review still pending.
3. **No functional sign-off:** No SAP SD/FSCM credit consultant has reviewed the chunks for functional accuracy.
4. **High insertion-temptation domain:** Credit management (VKM*, UKM_*, credit group Customizing paths, risk class tables) is a domain where a knowledgeable agent could easily insert "known" SAP facts not present in the cited pages. Regla 9 was followed, but trust level is structurally_validated only — not provenance_audited.

**Scope decisions made (agent-judgment):**
- U2 L5 (phys 44-48, external credit agency SCP integration): deferred as non-core O2C. No SD document generated; requires SAP Cloud Platform license. Scope: advanced/optional.
- U2 L6 (phys 49-58, reporting and mass changes): deferred as operational credit management tools (BW queries, Fiori exposure reports, mass update of check rules). Not part of the credit-check-in-O2C flow.
- U3 (phys 59-66, SAP S/4HANA Cloud for Customer Payments + Digital Payments): deferred — FI-AR cloud payment solution, not SD credit check.
- U4 (phys 67-97, Collections Management): deferred — FI-AR post-O2C. OUT OF SCOPE per standing rule.
- U5 (phys 98-132, Dispute Resolution): deferred — FI-AR dispute management. OUT OF SCOPE per standing rule.
- U1 (phys 8-17, Receivables Management suite overview): not chunked — promotional/business case; no unique SD credit check content; too thin for a standalone functional chunk.

**BD6 scope:** BD6 (Basic Credit Management, process diagrams) used as secondary source for credit-check-sd-integration-001 (pages 1-2, 5 cited). BD6 is current (no version mismatch detected — process flow matches S4F30 description).

**What would resolve this entry:**
- A SAP FSCM credit consultant reviews the 3 chunks against current S/4HANA system behavior (functional sign-off) — this is the remaining open gate
- If divergences 1909→current are found during functional review: update sap_release notes or split into version chunks
- Note: provenance audit (F1–F4) completed 2026-06-18. The remaining HIGH RISK designation is driven by functional_review: pending and release_confidence: low (source 1909) — the provenance audit does NOT substitute for consultant review.

---

## Summary

| Entry | Document | Unit | Type | Decision | Status |
|---|---|---|---|---|---|
| DEB-001 | S4680 | U3 Intra-Company STO | scope | In-scope as SD integration | needs-review |
| DEB-002 | S4680 | U6 L2 ARM Supplier Returns | scope + provenance | Deferred (MM pure); provenance fix applied | needs-review |
| DEB-003 | S4680 | U1 + U6 (2nd audit) | provenance audit | Cross-unit citations + absent terms corrected | resolved |
| DEB-004 | S4F30 + BD6 | U2 L1-L4 (credit management) | scope + provenance + version risk | 3 chunks; provenance audit done (F1-F4 corrected); HIGH RISK: functional_review pending + release_confidence low (1909) | needs-review |

---

## Process Backlog

### P4 — Validator entity-in-cited-range check (not implemented)

**Item:** Extend the validator to flag body-level named entities (T-codes, document types, scope item IDs, movement types, SAP-specific terms) that do not appear in the pdftotext extraction of the chunk's cited page ranges.

**Motivation:** The consignment paragraph and the cross-unit IV/1Z3 facts in the U1 third-party chunk would have been caught automatically by this check — none of those tokens appear in the pdftotext output of pages 8-21/33-38. Similarly, "SPRO" and "billing block" would have been flagged on first write.

**Current gap:** The validator checks structure, density, and cross-reference targets — not whether body tokens trace to cited pages.

**Implementation sketch:** For each chunk, extract body noun phrases matching known SAP entity patterns (T-codes: uppercase 2-6 chars; doc types: 2-4 char uppercase; scope items: digit+Z+digit format; movement types: 3-digit). For each, check presence in pdftotext of cited pages. Flag as WARN if absent. Requires a pre-built pdftotext cache per document.

**Why not implemented now:** Would require changing validate_chunks.py (outside current session scope per user instruction). Logged here for future sprint.
