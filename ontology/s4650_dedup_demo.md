# S4650 Dedup Demonstration — P2 v0
Generated: 2026-06-16
Document: S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf
Offset: +6 (phys = footer + 6) | Total: 114 phys pages (footer 1–107)

## Purpose

Demonstrate that the P2 authority registry lookup reproduces (or improves on) the
dedup decisions that Skill 6 runtime judgment would make for each S4650 unit.
Highlights Copy Control and Output as the structurally interesting cases.

---

## Dedup Decision Table — S4650 vs. Registry

| Unit / Lesson | Pages (phys) | Topic lookup | Existing coverage | Lookup decision | Expected Skill-6 judgment | Match? |
|---|---|---|---|---|---|---|
| U1 L1: Creating Org Elements | 8–13 | `ent.org.sales` | `sales-distribution-enterprise-structure-001` (S4605 primary) | **SECONDARY** — S4605 is authoritative for general SD org structure; S4650 adds no new depth here | Skip or add as secondary source to existing chunk | ✓ YES |
| U1 L2: Shared Master Data / Cross-Division | 14–19 | `ent.org.cross_div` | 0 chunks — GAP | **PRIMARY** — first coverage of cross-division sales; create new chunk | Create new chunk | ✓ YES |
| U2: Modifying Copy Control | 20–31 | `xfunc.copy` | 3 chunks (S4605/S4610/S4615 by facet) | **SUPPLEMENTARY (unified view)** — see analysis below | "Secondary to existing 3 chunks" (rough match) | ⚠ PARTIAL — see below |
| U3 L1: Identifying Text Sources | 32–36 | `xfunc.text` | 0 chunks — GAP | **PRIMARY** — first coverage of text sources | Create new chunk | ✓ YES |
| U3 L2: Configuring Text Control | 37–48 | `xfunc.text` | 0 chunks — GAP | **PRIMARY** — first coverage of text configuration | Create new chunk | ✓ YES |
| U4 L1: Adjusting Output Determination | 49–58 | `xfunc.output` | `billing-output-management-brfplus-001` (billing facet only) | **PRIMARY** — S4650 covers full output determination; S4615 chunk becomes supplementary | "Secondary to billing-brfplus chunk" (WRONG) | ✗ DIVERGENCE — see below |
| U4 L2: Adjusting Output Types | 59–64 | `xfunc.output` | (same as above) | **PRIMARY** (same inversion) | "Secondary" (WRONG) | ✗ DIVERGENCE |
| U4 L3: New Output Management | 65–73 | `xfunc.output` | (same; new output mgmt not in existing chunk) | **PRIMARY** — no existing chunk for new output management | "Create new chunk" (partial correct) | ⚠ PARTIAL |
| U5 all lessons: Enhancements | 74–113 | `xfunc.enhance` | 0 chunks — DEFERRED | **DEFERRED** — technical audience; scope decision required before chunking | "Gap → create chunks" (WRONG: treats as functional gap) | ✗ DIVERGENCE — see below |

---

## Copy Control (U2) — Key Structural Finding

### What the lookup says

`xfunc.copy` has **distributed authority**: S4605 (sales facet), S4610 (delivery facet),
S4615 (billing facet). Each authoritative chunk is correct and complete for its domain.
S4650 Unit 2 covers all three chains in a single lesson — it is **supplementary** (unified view),
not a replacement or primary.

Decision: when chunked, S4650 Unit 2 → `role: secondary`, note = "unified cross-chain view;
see authoritative facet chunks for configuration depth."

### What Skill-6 runtime judgment would say

"Topic already covered by 3 chunks. S4650 Unit 2 = secondary source."

The destinations are the same, but the lookup adds a structural diagnosis that judgment alone
would not surface:

> **P2 Structural Finding:** copy control is a coherent single concept currently fragmented
> across 3 domain-specific chunks. A consultant searching "copy control" receives 3 partial
> answers. S4650 Unit 2 could serve as the source for a unified `xfunc.copy` overview chunk
> that cross-references the 3 facet chunks. This is not a defect in the existing chunks — it
> is a chunking-strategy observation that only becomes visible when topic is the unit of
> analysis (not area/slug).

**Recommendation:** add `## Cross-References` entries to the 3 existing copy-control chunks
pointing to each other. Consider a unified overview chunk in a future pass using S4650 Unit 2
as primary source.

---

## Output Determination (U4) — Authority Inversion

### What the lookup says

`xfunc.output` authority pattern = `inversion_pending`.
- **S4650 Unit 4** → PRIMARY (covers output determination for ALL SD documents: sales,
  delivery, billing — plus new Output Management)
- **`configuration-billing-output-management-brfplus-001`** → SUPPLEMENTARY (billing BRFplus
  facet only; was written before S4650 was processed; remains accurate for its narrow topic)

Decision: chunk S4650 Unit 4 as the authoritative `xfunc.output` chunk. Update
`configuration-billing-output-management-brfplus-001` to `role: secondary` for this topic.

### What Skill-6 runtime judgment would say

"An existing chunk covers output management (billing-output-management-brfplus-001).
S4650 Unit 4 adds depth → mark as secondary source."

**This judgment is WRONG.** The existing chunk covers only the billing BRFplus facet
(one output medium for one document type). S4650 Unit 4 covers output determination
procedure, output types across all SD documents, condition records for output, and the
new Output Management framework — a fundamentally broader scope.

> **P2 Authority Inversion Pattern:** a domain-specific chunk (billing BRFplus, S4615)
> was created first because no cross-functional source had been processed. When S4650 is
> processed, the scope relationship inverts: the narrow chunk becomes supplementary to the
> broader one. Runtime judgment (Skill 6) without a registry would wrongly preserve the
> original narrow chunk as "the" authority — causing under-extraction of the broader S4650
> content. The registry makes the correct scope relationship explicit at design time.

---

## Enhancements (U5) — Scope Gate

### What the lookup says

`xfunc.enhance` → `in_scope: deferred`, `audience: technical`.
Decision: **do not chunk Unit 5** until the user explicitly confirms that the corpus scope
extends to technical content (BAdI, Enhancement Framework, field exits).

### What Skill-6 runtime judgment would say

"Unit 5 = 0 matching chunks on these topics → gap → create new chunks."

**This is wrong in context.** The corpus is functional. Unit 5 is technical. Skill 6 alone
cannot see the audience scope because it is not encoded anywhere in the current process —
it would treat a technical gap identically to a functional gap and proceed to chunk it.

> **P2 Scope Gate:** the registry makes the audience and scope decision explicit.
> Without it, corpus scope creep would happen silently — Unit 5 would be chunked, the
> corpus would drift toward a mixed functional/technical audience, and quality/relevance
> for functional RAG queries would degrade.

---

## Divergence Summary

| Case | Judgment | Lookup | Lookup advantage |
|---|---|---|---|
| U2 Copy Control | "Secondary to 3 chunks" | "Supplementary (unified view) — structural fragmentation found" | Surfaces the 3-chunk fragmentation as a finding; recommends cross-ref and future unified chunk |
| U4 Output (L1/L2) | "Secondary to billing-brfplus" ✗ | "Primary — authority inversion; brfplus becomes supplementary" | Prevents under-extraction; preserves scope relationship correctly |
| U4 Output (L3) | "Create new chunk" ✓ (partial) | "Primary — no existing chunk for new output mgmt" | Same conclusion, but for the right reason |
| U5 Enhancements | "Gap → create chunks" ✗ | "Deferred — technical audience, scope decision needed" | Prevents corpus scope creep; flags decision to user |

---

## Decisions That Reproduce Existing Trusted Judgments

| Case | Lookup | Matches trusted prior judgment? |
|---|---|---|
| U1 L1 (org elements) | Secondary to S4605 | ✓ Matches — S4605 is the org structure authority |
| U1 L2 (cross-division) | Primary (new gap) | ✓ Matches — no prior chunk, new content |
| U3 L1/L2 (text control) | Primary (new gap) | ✓ Matches — no prior chunk, new content |

---

## Verdict

The registry lookup **reproduces** trusted decisions in 3 of 5 units and **improves** on
runtime judgment in 2 of 5 (output inversion, scope gate for enhancements) plus surfaces
a structural finding in 1 (copy control fragmentation).

No divergence goes unexplained. The 2 divergences (output, enhancements) are cases where
the registry is demonstrably more correct than judgment — not cases where the registry
may be wrong.

**Confidence in the registry for S4650 dedup: HIGH.**
When S4650 is chunked, this demo serves as the pre-approved dedup plan.
