# Ontology Completeness Report — S4680 Processing (P2 Authority Registry Test)
Date: 2026-06-17
Document: S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement
Test objective: All S4680 topics were UNREGISTERED before this session → tests fallback-judgment path and ontology extension mechanism.

---

## Q1: How many topics exist in the registry, and how many S4680 topics were unregistered?

**Registry state before session:** 42 governing topics + 0 proposals = 42 entries.
**Registry state after session:** 42 governing + 5 proposals = 47 entries.

**S4680 units inspected:** 6 (U1–U6; U7 = Appendix).
**In-scope logical topics identified from S4680:** 5 (third-party processing, intercompany sales, intra-company STO, cross-company STO, ARM customer returns).
**Deferred topics:** 1 (subcontracting — MM pure) + partial (U6 L2 ARM supplier returns — MM pure).

**Result:** 5/5 in-scope S4680 topics were UNREGISTERED → 100% fallback-judgment rate for this document. All 5 were added as PROPOSAL entries (not governing) after chunking. The deferred MM topic (subcontracting) was also added as a PROPOSAL with `in_scope: deferred`.

---

## Q2: Which S4680 topics were registered vs unregistered, and what was the registry decision for each?

| S4680 Unit | Topic | Registry Status | Decision Made |
|---|---|---|---|
| U1 L1+L3 | Third-party order processing | UNREGISTERED | Fallback: new chunk, no existing chunk for this topic → create |
| U1 L2 | Individual PO (MM pure) | UNREGISTERED | Fallback: out of SD scope → DEFERRED |
| U2 | Cross-company code sales / intercompany billing | UNREGISTERED | Fallback: new chunk → create |
| U3 | Intra-company STO with SD delivery | UNREGISTERED | Fallback: new chunk (scope-gated with user) → create |
| U4 | Cross-company STO with billing | UNREGISTERED | Fallback: new chunk → create |
| U5 | Subcontracting | UNREGISTERED | Fallback: out of SD scope → DEFERRED |
| U6 L1+L3 | ARM customer returns (RE2, refund codes, BKP, BDD) | UNREGISTERED | Fallback: new chunk (scope-gated with user) → create |
| U6 L2 | ARM supplier returns | UNREGISTERED | Fallback: MM pure → DEFERRED (body context only in ARM chunk) |

**Registry error found and corrected:** Entry `o2c.credit` incorrectly listed S4680 as a prospective authoritative source for credit management. S4680 is SD-MM cross-application, not FSCM credit. Corrected to S4F30 + BD6. This was a registry-build error (S4680 was assumed to cover credit before the document was read).

---

## Q3: How well did the fallback judgment perform for unregistered topics?

**Methodology:** For each unregistered topic, the fallback path required:
1. Content grep for existing chunks (none found for any S4680 topic)
2. Scope gate: SD/SD↔MM = in scope; MM pure = defer; doubt = flag for user
3. Create new chunk with standard quality gates

**Outcomes:**
- **Scope gate accuracy:** All decisions were correct on inspection. The two user-gated decisions (U3 intra-company STO, U6 ARM) were approved without modification.
- **No duplicate creation:** grep confirmed 0 existing chunks for these topics before writing.
- **0 validator errors** at gate close (after three density/cross-ref fixes during validation).
- **Registry error detection:** The o2c.credit error was caught during the pre-session registry review, not during chunk writing. This shows the registry pre-read step has value even when all topics are unregistered.

**Conclusion:** Fallback judgment performed correctly. The main cost was the explicit scope-gate loop with the user for the two borderline cases (U3, U6). With a governing registry entry for `integration.sto` and `o2c.returns.arm`, future documents covering these topics would bypass the scope-gate loop.

---

## Q4: What gaps remain in the ontology after adding S4680 proposals?

**Known gaps as of 2026-06-17:**

| Gap | Evidence | Status |
|---|---|---|
| `o2c.consignment` | Consignment stock sales process (fill-up, issue, return, pick-up) | Not registered; expected in S4605 or S4601 |
| `o2c.make_to_order` | Make-to-order with individual customer stock | Not registered; expected in S4600 or S4605 |
| `integration.fi_sd` | SD→FI integration (revenue account determination, reconciliation) | Not registered; expected in S4615 or a dedicated integration document |
| `o2c.complaints` | Complaint processing (returns + credit memo request workflow) | Partially overlaps `o2c.returns.arm` (proposed); standalone concept chunk may be needed |
| `o2c.free_of_charge` | Free-of-charge deliveries and subsequent deliveries | Not registered |
| `integration.sto` | Governing entry pending editorial review | Currently only PROPOSAL |
| `o2c.third_party` | Governing entry pending editorial review | Currently only PROPOSAL |
| `o2c.intercompany` | Governing entry pending editorial review | Currently only PROPOSAL |
| `o2c.returns.arm` | Governing entry pending editorial review | Currently only PROPOSAL |

**Documents likely to fill gaps:** S4601 (supply chain execution), S4605 supplement, the BD* process diagrams corpus.

---

## Q5: What is the recommended next step to improve registry coverage?

**Priority 1 — Elevate S4680 proposals to governing.** The 4 in-scope proposals (third-party, intercompany, intra-STO, cross-STO, ARM) are based on a single source (S4680). Before making them governing, process one corroborating document (e.g., S4601 which may cover STOs from the supply chain side) to confirm the topic boundaries and check for conflicting authority claims.

**Priority 2 — Register missing o2c topics** before processing S4601 or other high-priority pending documents (consignment, make-to-order, free-of-charge, complaints). Building registry entries from corpus knowledge before reading the next document prevents the same all-unregistered scenario that occurred with S4680.

**Priority 3 — Add `integration.fi_sd` topic.** The SD↔FI integration topic (revenue account determination, account assignment groups, posting keys) appeared as cross-references in multiple S4615 chunks but has no registry entry. S4615 is already processed, so this entry can be added now from existing chunk data.

**Mechanism proposal:** Run a "registry gap audit" before each new document: extract all process_tags used in existing chunks, compare against registered topic IDs, and add stub PROPOSAL entries for any unregistered tag. This would have pre-populated the registry for S4680 topics before the session.

---

## Summary

| Dimension | Value |
|---|---|
| Governing topics before session | 42 |
| Proposals added | 5 (4 in-scope + 1 deferred) |
| S4680 topics unregistered at session start | 100% (8/8 topics) |
| Chunks created | 5 |
| Validator errors at gate | 0 (after fixes) |
| Registry error found and corrected | 1 (o2c.credit: incorrect prospective entry) |
| Recall@10 (TF-IDF lexical) | 92.0% — healthy |
| Recall@1 (TF-IDF lexical) | 20.0% — investigate (low precision; semantic eval pending) |
| MRR (TF-IDF lexical) | 0.488 — investigate (consistent with low recall@1) |
