# Processing Log — SAP SD Knowledge Base

## 2026-06-05 — S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf
- Relative path: processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf
- Type: A* (mixed — PDFKit, 152-195 words/page depending on section)
- Total pages: 88
- Processed range: p. 9-14 (Unit 1 — Idea and Function of the Delivery Document)
- Next pending page: p. 18 (Unit 2 — Basic Organizational Units for the Delivery Process)
- Extractable text: high — standard Helvetica, no encoding issues
- Encoding issues: none
- Visual pages detected in Unit 1: p.4 (blank page), p.6 (empty Course Overview), p.17 (Unit 1/Unit 2 separator)
- Chunks created: 2
  - shipping-delivery-document-concept-001 → chunks/shipping/delivery-document-concept-001.md
  - shipping-delivery-document-structure-001 → chunks/shipping/delivery-document-structure-001.md
- Chunks updated: none
- Duplicates found and decision: none
- Omitted content:
  - p.1-8: cover, copyright, typographic conventions, TOC, Course Overview, Unit 1 objectives — no functional content
  - p.15-16: Learning Assessment (exercise questions and answers) — no new functional content
- Non-obvious chunking decisions:
  - Unit 1 covers a single lesson but content is naturally split into "what is a delivery" (concept+types) and "how is it structured" (structure+vs shipment). Split into 2 chunks due to different search intent.
  - Figures 1-6 were not rasterized because surrounding text is sufficient (pages with >140 words each).
- Status: partial — calibration session, Unit 1 only

## 2026-06-05 — S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf (continued)
- Relative path: processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf
- Type: A*
- Total pages: 88
- Processed range: p. 19-24 (Unit 2 — Basic Organizational Units for the Delivery Process)
- Next pending page: p. 28 (Unit 3 — Controlling Deliveries)
- Extractable text: high
- Encoding issues: none
- Visual pages detected in Unit 2: p.27 (Unit 2/Unit 3 separator)
- Chunks created: 2
  - enterprise-structure-shipping-point-loading-point-001 → chunks/enterprise-structure/shipping-point-loading-point-001.md
  - enterprise-structure-warehouse-org-units-ewm-001 → chunks/enterprise-structure/warehouse-org-units-ewm-001.md
- Chunks updated: none
- Duplicates found and decision: none
- Omitted content:
  - p.18: lesson overview/objectives — no functional content
  - p.25-26: learning assessment — no new functional content
  - p.27: visual separator
- Non-obvious chunking decisions:
  - IM hierarchy (client/company code/plant/storage location) and EWM hierarchy grouped in one chunk because they are presented together in the source and a consultant asking about warehouse org units needs both. IM-only content (p.20 first half) is too short (~half page) to stand alone.
  - Shipping Point and Loading Point grouped per CLAUDE.md example (related in configuration and usage).
- Status: partial — Unit 2 completed, Unit 3 pending

## 2026-06-05 — S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf (continued)
- Relative path: processed/S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf
- Type: A*
- Total pages: 88
- Processed range: Units 3-5 (PDF p.29-37, p.43-52, p.55-63, p.71-88)
- Next pending page: none — document completed
- Extractable text: high
- Encoding issues: none
- Visual pages detected: p.38 (Unit 3/4 separator), p.75 (within Unit 5 Lesson 1)
- Chunks created: 11
  - configuration-delivery-type-001 → chunks/configuration/delivery-type-001.md
  - configuration-delivery-item-category-001 → chunks/configuration/delivery-item-category-001.md
  - configuration-delivery-process-customizing-001 → chunks/configuration/delivery-process-customizing-001.md
  - configuration-delivery-field-determination-001 → chunks/configuration/delivery-field-determination-001.md
  - configuration-delivery-scheduling-001 → chunks/configuration/delivery-scheduling-001.md
  - shipping-outbound-delivery-creation-process-001 → chunks/shipping/outbound-delivery-creation-process-001.md
  - shipping-outbound-delivery-monitor-001 → chunks/shipping/outbound-delivery-monitor-001.md
  - shipping-ewm-picking-process-001 → chunks/shipping/ewm-picking-process-001.md
  - shipping-goods-issue-ewm-001 → chunks/shipping/goods-issue-ewm-001.md
  - shipping-inbound-delivery-ewm-001 → chunks/shipping/inbound-delivery-ewm-001.md
  - shipping-delivery-special-functions-001 → chunks/shipping/delivery-special-functions-001.md
- Chunks updated: none
- Duplicates found and decision: none
- Omitted content:
  - All learning assessment pages (p.39-40, p.57-68, p.80-82, p.85-88) — no functional content
  - All lesson overview/objective pages — no functional content
  - Unit title separator pages
- Non-obvious chunking decisions:
  - Unit 4 Lessons 1 and 2 (field determination + scheduling) split into separate chunks despite being in the same lesson group — search intents are orthogonal (configuration of determination logic vs. scheduling parameters)
  - Outbound Delivery Monitor (Unit 4 Lesson 4) kept as own chunk despite being short — it is a standalone transaction with a specific search intent
  - Goods Issue (Unit 5 Lesson 2) kept separate from EWM picking — GI trigger options and delivery split logic are distinct from the picking warehouse task flow
  - Delivery special functions (pricing + interface + incompletion) grouped into one chunk — each topic alone is too short (<300 words); together they form a coherent "additional delivery capabilities" reference
- Status: completed — full document processed (Units 1-5)

## 2026-06-05 — CORRECTION: S4610_EN_Col17 Delivery Processing in SAP S4HANA.pdf
- Trigger: provenance audit of generated chunks against extracted source text (pdftotext -layout) + figure review.
- Finding: S4610 is a conceptual course. It names transactions only by function ("Create Outbound Delivery", "Delivery Due List", "outbound/inbound delivery monitor") and prints no T-codes. No database table names appear (the token "MARA" present is the picking RULE, not the table). Only literal technical token in text: "VL10" as the VALUE of parameter ID LE_VL10_SZENARIO — not an invoked transaction.
- Chunks corrected (hallucinated T-codes removed from frontmatter, aliases, body prose, headings, and tables; relevant codes preserved as inferred-pending comments):
  - shipping-outbound-delivery-creation-process-001 → transactions: [VL10E] → []  (VL10E parked in <!-- inferred -->)
  - shipping-outbound-delivery-monitor-001 → transactions: [VL06O, VL06I] → []  (both parked in <!-- inferred -->)
- Preserved (correctly sourced): table row "LE_VL10_SZENARIO | VL10" in creation-process chunk (VL10 is the literal parameter value in the source).
- Other 13 chunks: transactions already [] — confirmed correct (true negatives), no change.
- Index regenerated; T-codes column cleared for the two chunks; path column normalized to chunks/ forward-slash form.
- Root cause addressed in CLAUDE.md: added literal-extraction provenance rule for transactions/tables, automated provenance grep in Step 6, caveats on reference examples and duplicate-search seeds, explicit figure-only exception for unsourced codes.
- Status: completed (correction). Chunks remain status: draft pending human/revisor review of the inferred-pending T-codes.

## 2026-06-05 — S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf
- Relative path: processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf
- Type: A (official SAP course; Producer PDFKit, HTML→PDF export)
- Total pages: 131 (physical)
- Page offset: printed label N = physical N+8 (printed 1 = physical 9). All citations below use PHYSICAL pages.
- Processed range: physical p.18-132 (lesson content + appendix)
- Appendix / reference tables: physical p.124-126 "Frequently Used Menu Paths" — mined for T-codes (VF01/03/04/05/06/11/24/25, VFX3, F-29, FBL5, VK13/33, VL02N/VL23). Not chunked as a standalone chunk; its codes were distributed into the relevant topic chunks.
- Next pending page: none — completed
- Extractable text: high
- Encoding issues: none
- Chunks created: 31 (this batch was generated in a prior session; this entry documents it retroactively + the correction below)
- CORRECTION applied 2026-06-05:
  - Page citations: ALL 31 chunks were citing printed labels; converted to physical pages (+8). This was a silent corpus-wide traceability defect — re-extracting a cited "page 120" landed on physical 120, eight pages before the content.
  - Under-extraction (appendix omission): the T-code appendix had been skipped, leaving 29/31 chunks with transactions:[] despite the source naming codes explicitly. Distributed appendix T-codes to matching chunks by task:
    - billing-document-cancellation-001 → [VF11]  (appendix p.125 added to sources)
    - billing-document-creation-methods-001 → [VF01, VF04, VF06]  (VF01/VF04 in-page 52-59; VF06 appendix p.125)
    - invoice-list-001 → [VF25, VF24]  (appendix p.125 added)
    - down-payment-processing-001 → [F-29]  (appendix p.126 added)
    - billing-data-flow-001 → [VOFM]  (page range extended to physical 45 where VOFM appears)
    - Each added T-code also added to aliases and given a sourced body mention.
  - Over-extraction (hallucination): removed table VBRL from document-table-structure-001 (frontmatter + body). The other 8 tables (VBRK, VBRP, VBPA, SADR, VBFA, PRCD_COND, STXH, STXL) verified present in physical p.128-129 — retained.
  - Verified-correct, no change: table "001" in billing-negative-postings-001 (source p.108 literally says "controlled in table 001"); aliases FAZ/AZWR in down-payment (both in source).
  - Quality recalibration: batch was 31/31 high. Re-rated to 25 high / 6 medium. Medium = chunks that gained cross-page appendix codes or had a hallucination removed (cancellation, creation-methods, invoice-list, down-payment, data-flow, document-table-structure) — flagged for human/revisor glance.
- Duplicates found and decision: none (no prior billing chunks existed)
- Omitted content: Learning Assessment pages (contain quiz-form T-code references, e.g. "You use transaction VF01" on physical p.72/74 — intentionally not used as chunk anchors); lesson overview/objective pages; unit separators.
- Non-obvious chunking decisions: appendix mined-but-not-chunked (its value is the task→code mapping, distributed into topic chunks rather than isolated as a low-context list).
- Status: completed

## 2026-06-05 — UPDATE: S4615 chunks — Cross-References + missing sections
- Trigger: post-process evaluation found systemic gaps beyond transactions/tables.
- Cross-References: all 31 S4615 chunks lacked the mandatory section (the template requires it for every chunk_type). Added a topical cross-reference graph using real chunk IDs only. Verified: 0 broken targets, 0 isolated nodes corpus-wide (every chunk has ≥1 inbound link). Added a few reciprocal links (e.g. shipping-goods-issue-ewm → cash-sales) for batch cohesion across S4610/S4615.
- Common Errors: 7 process chunks lacked the section (cancellation, creation-methods, fiori, credit-debit, down-payment, invoice-correction, returns, cash-sales). Added source-grounded errors only — no invented failure modes; where the source documents a constraint (e.g. cash sale requires a G/L account; return credit memo references the order not the delivery) it is reflected.
- No content invented; all added error text traces to source statements already used in the chunk bodies.
- Validation: 31/31 pass YAML + structural (Cross-References present, process chunks have Common Errors) + provenance. Index regenerated.
- Tooling note: the batch-audit cross-ref regex was corrected (now allows digits in slugs, e.g. "s4hana") in CLAUDE.md; the earlier "isolated node" flag on billing-types was a regex false positive, not a real gap.
- Status: completed (content update). Chunks remain status: draft pending human/revisor review.
## 2026-06-07 — CORRECTION: S4615 chunks — Overhaul (post adversarial review)
- Relative path: processed/S4615_EN_Col17 Billing in SAP S4HANA Sales.pdf
- Type: A
- Total pages: 132 (physical)
- Processed range: p. 1-132 (complete)
- Appendix / reference tables: p.124-126 mined in prior session; no new appendix
- Next pending page: none — completed
- Extractable text: high
- Encoding issues: none
- Chunks created: 0 (overhaul of existing 31 S4615 chunks, no new IDs)
- Chunks updated: all 31 S4615 chunks — see detail below
  - H1 title added to all 31 (was missing)
  - Body word count: 147-436w → 425-639w (avg 262 → ~530)
  - Questions: 2 → 4-6+ per chunk (distinct search intents)
  - Aliases: 2-4 → 6-12+ per chunk (>=2 Spanish, >=1 natural query variant)
  - Concept chunks: added Definition, Purpose, Structure/Variants, Relationship sections
  - Configuration chunks: added SPRO Path, Configuration Impact, Common Configuration Errors
  - Cross-refs: normalized from backtick format to plain chunk IDs
  - process_tags: billing-plans/invoice-list/pro-forma tags added to 5 chunks
  - BUG FIX: tables: ["001"] in billing-negative-postings-001 → tables: [] + inferred comment
  - BUG FIX: delivery-document-structure-001 missing Relationship section — added
- Duplicates found and decision: none
- Omitted content: none
- Non-obvious decisions: "001" is FI Customizing table ID, not an ABAP dictionary table — excluded from tables field
- Status: completed

## 2026-06-07 — S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf
- Relative path: S4605_EN_Col17 Sales Processes in SAP S4HANA Sales.pdf
- Type: A (official SAP course; Producer PDFKit)
- Total pages: 168 (physical)
- Page offset: printed label N = physical N+8 (printed 1 = physical 9). All citations below use PHYSICAL pages.
- Processed range: p. 11-168 (complete lesson content from Unit 2 through appendix; cover/TOC/overview pages read for classification but not chunked)
- Appendix / reference tables: p. 166-168 mined and chunked as integration-sales-document-technical-tables-001. Tables verified in source: VBAK, VBKD, VEDA, VBPA, VBUV, VBFA, STXH, STXL, VBAP, VBEP, VBBE.
- Next pending page: none — completed
- Extractable text: high
- Encoding issues: none
- Chunks created: 19
  - order-management-sales-distribution-process-001 -> chunks/order-management/sales-distribution-process-001.md
  - enterprise-structure-sales-distribution-enterprise-structure-001 -> chunks/enterprise-structure/sales-distribution-enterprise-structure-001.md
  - order-management-sales-order-source-of-data-001 -> chunks/order-management/sales-order-source-of-data-001.md
  - order-management-sales-order-special-features-001 -> chunks/order-management/sales-order-special-features-001.md
  - configuration-sales-document-type-control-001 -> chunks/configuration/sales-document-type-control-001.md
  - configuration-sales-item-category-control-001 -> chunks/configuration/sales-item-category-control-001.md
  - configuration-schedule-line-category-control-001 -> chunks/configuration/schedule-line-category-control-001.md
  - order-management-sales-document-data-flow-001 -> chunks/order-management/sales-document-data-flow-001.md
  - configuration-sales-copying-control-001 -> chunks/configuration/sales-copying-control-001.md
  - special-processes-sales-special-business-transactions-001 -> chunks/special-processes/sales-special-business-transactions-001.md
  - configuration-sales-incompletion-check-001 -> chunks/configuration/sales-incompletion-check-001.md
  - master-data-sd-partner-functions-001 -> chunks/master-data/sd-partner-functions-001.md
  - order-management-outline-agreements-scheduling-quantity-contracts-001 -> chunks/order-management/outline-agreements-scheduling-quantity-contracts-001.md
  - order-management-value-contracts-001 -> chunks/order-management/value-contracts-001.md
  - master-data-material-determination-001 -> chunks/master-data/material-determination-001.md
  - master-data-material-listing-exclusion-001 -> chunks/master-data/material-listing-exclusion-001.md
  - pricing-free-goods-001 -> chunks/pricing/free-goods-001.md
  - special-processes-sales-workshop-scenarios-001 -> chunks/special-processes/sales-workshop-scenarios-001.md
  - integration-sales-document-technical-tables-001 -> chunks/integration/sales-document-technical-tables-001.md
- Chunks updated: none
- Duplicates found: none requiring skip or merge. Related existing chunks were linked where appropriate (delivery, billing, returns, billing plans).
- Omitted content: Course cover/copyright/typographic convention pages, unit objective separators, and learning assessment pages. Lesson content, workshop content, and appendix tables were processed.
- Non-obvious decisions: transactions remain empty except pricing-free-goods-001 where VOFM appears literally on p. 147 physical; appendix table names were kept only in integration-sales-document-technical-tables-001 to avoid over-extraction into functional chunks.
- Validation: 19/19 chunks pass with 0 ERRORs. Remaining warnings are advisory density warnings on long figure-heavy ranges and area-level isolated-node warnings; source ranges were read and appendix provenance was verified.
- Status: completed


## 2026-06-07 — S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf
- Relative path: S4620_EN_Col17 Pricing in SAP S4HANA Sales.pdf
- Type: A
- Total pages: ~128 physical (printed pages 1-122 + 6 page offset)
- Page offset: physical = printed + 6
- Processed range: p. 8-114 (Units 1-7)
- Back matter: Unit 9 Appendix (phys 119-128) — mined for T-codes (VK11-14, VK31-34), IMG paths, SAP Notes. Not chunked separately.
- Unprocessed: Unit 8 (phys 115-118) — exercises-only workshop, content absorbed into existing chunks; Unit 9 (phys 119-128) — appendix only.
- Extractable text: medium (course is figure-heavy; many pages have short text paragraphs alongside diagrams)
- Encoding issues: none
- Chunks created: 10
  - pricing-condition-technique-overview-001 → chunks/pricing/condition-technique-overview-001.md
  - configuration-pricing-procedure-configuration-001 → chunks/configuration/pricing-procedure-configuration-001.md
  - pricing-condition-records-001 → chunks/pricing/condition-records-001.md
  - pricing-special-pricing-functions-001 → chunks/pricing/special-pricing-functions-001.md
  - pricing-special-condition-types-001 → chunks/pricing/special-condition-types-001.md
  - pricing-statistical-condition-types-001 → chunks/pricing/statistical-condition-types-001.md
  - pricing-pricing-agreements-001 → chunks/pricing/pricing-agreements-001.md
  - pricing-condition-contract-management-concept-001 → chunks/pricing/condition-contract-management-concept-001.md
  - pricing-condition-contract-maintenance-001 → chunks/pricing/condition-contract-maintenance-001.md
  - pricing-condition-contract-settlement-001 → chunks/pricing/condition-contract-settlement-001.md
- Non-obvious decisions:
  - Chunks 1,3,5,6 have quality:medium (pages are diagram-heavy; density 77-80 w/p after expansion)
  - Secondary source removed from condition-records: appendix T-codes VK14/31-34 not in primary page range (40-53)
  - Unit 8 workshop skipped per CLAUDE.md rule (exercises only)
  - Condition technique and pricing procedure split into 2 chunks (conceptual vs. Customizing)
  - CCM split into 3 chunks: concept overview, maintenance, settlement
- Status: completed — next pending page: none

## 2026-06-08 — S4605 Unit 13 coverage gap closure (phys 154-165)

- **Trigger:** analysis doc `analisis_estrategia_pdf_a_chunk_2026-06-08.md` confirmed pages 154-165 uncovered after workshop chunk dissolution.
- **Chunks modified (no new chunks created):**
  - `special-processes/sales-special-business-transactions-001.md` → added secondary source pages 154-156 (Sales-to-Employee scenario already merged in prior session)
  - `configuration/sales-item-category-control-001.md` → added secondary source pages 157-160 + BOM explosion step sequence + business context (distributor model, no ATP, component-level POs, delivery/invoice content)
  - `master-data/material-determination-001.md` → added secondary source pages 161-165 + analysis menu path (Environment → Analysis → Material Determination On) + order confirmation content options
- **Coverage result:** all 12 pages (154-165) covered. 0 uncovered pages with ≥100w content.
- **Validator:** 74 OK / 0 errors / 3 warnings (max-page advisory × 2 + density warning on pricing-procedure-config)
- **Decisions:**
  - No new chunks created: BOM scenario (phys 157-160) merges into item-category-control (mechanics already there, added functional context ~150w + step sequence); employee sales (phys 154-156) and material determination (phys 161-165) content already present, source citation added.
  - sales-item-category-control quality remains high (expanded from 95 to 115 w/p after adding step sequence).

## 2026-06-16 — S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf
- Relative path: processed/S4600_EN_Col17 Business Processes in SAP S4HANA Sales.pdf
- Type: A (SAP official, S/4HANA 2020, ~134 w/p)
- Physical pages: 163 | Offset: 8 (footer 1 = phys 9) | Page count method: pdftotext binary search
- Next pending page: none — document completed
- Status: completed
- Chunks created (8 new):
  - order-management/availability-check-atp-001 — ATP concept, scope of check, material availability date, transfer of requirements, partial/complete delivery (U6 L1, phys 97-103)
  - order-management/backorder-processing-001 — 4 ATP scenarios, BOP segments/variants/runs (U6 L2, phys 104-112)
  - order-management/collective-processing-001 — Worklists, split criteria, collective delivery/picking/billing (U7, phys 117-124)
  - master-data/business-partner-master-data-001 — BP approach, structure, roles, mandatory partner functions (U4 L1, phys 58-63)
  - master-data/material-master-sd-001 — Material master views for SD + CMiR concept and priority (U4 L2+L3, phys 64-68)
  - order-management/sales-monitoring-analytics-001 — Sales Order Fulfillment App, SAP Smart Business, sales plans, CDS analytics (U10, phys 149-161)
  - configuration/sap-fiori-launchpad-001 — Fiori UX paradigm, launchpad, app types (U1, phys 10-15)
  - order-management/presales-additional-processes-001 — Inquiries, quotations, MTO, service products DIEN/LEIS (U8, phys 127-134)
- Secondary source updates (3):
  - billing/returns-process-001 — added returns stock category + subsequent free-of-charge delivery alternative (U9 L3, phys 144-145)
  - billing/credit-debit-memo-process-001 — added secondary source citation (U9 L1, phys 139-141; content already covered by S4615 primary)
  - enterprise-structure/sales-distribution-enterprise-structure-001 — added secondary source citation (U2, phys 18-22; content confirmed by S4605 primary)
- Skipped (justification):
  - U3 Overview: subsumed by existing chunks from S4605/S4610/S4615/S4620
  - U5 (plant/shipping point/route determination, scheduling): S4610 covers same topics at greater depth — S4600 secondary source would dilute density without adding content; skipped
  - U9 L2 Cancellation: identical to billing-document-cancellation-001
  - U4 L4/L5 Condition Master + Output/BRFplus: S4620/S4615 more complete; added as secondary source to enterprise-structure only
  - U2 EWM: warehouse-org-units-ewm-001 from S4610 more complete; not updated
- Validator: 82 OK / 0 errors / 4 warnings (max-page advisory; density warnings on 2 pre-existing chunks)

## 2026-06-17 — S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf
- Relative path: processed/S4650_EN_Col17 Cross-Functional Topics in SAP S4HANA Sales.pdf
- Type: A (SAP official, S/4HANA 2020)
- Physical pages: 114 | Offset: +6 (footer 1 = phys 7) | Page count: 114 phys pages (footer 1–107 + front-matter/TOC)
- Processing governed by: ontology/authority_registry.yaml (P2 registry-first dedup — PROSPECTIVE VALIDATION)
- Next pending page: none — document completed (Units 1-5)
- Status: completed

### Dedup decisions from registry (registry-first, no re-judgment):

| Unit | Registry decision | Outcome |
|---|---|---|
| U1 L1 (phys 8-13) | ent.org.sales → SECONDARY | Cross-reference only (density guardrail: 1041w / (13+6)p = 54.8 w/p < 80) |
| U1 L2 (phys 14-19) | ent.org.cross_div → PRIMARY (gap) | NEW chunk: enterprise-structure/shared-master-data-cross-division-001 |
| U2 (phys 20-31) | xfunc.copy → SECONDARY (unified view) | Cross-references to 3 authoritative facet chunks only (density guardrail: all 3 would drop to ~40-47 w/p) |
| U3 L1 (phys 32-35) | xfunc.text → PRIMARY (gap) | NEW chunk: configuration/text-sources-sd-001 |
| U3 L2 (phys 36-48) | xfunc.text → PRIMARY (gap) | NEW chunk: configuration/text-control-determination-001 |
| U4 L1+L2 (phys 49-64) | xfunc.output → PRIMARY (authority inversion) | NEW chunk: configuration/output-determination-sd-001 |
| U4 L3 (phys 65-73) | xfunc.output → PRIMARY (new output mgmt, no prior chunk) | NEW chunk: configuration/output-management-s4hana-001 |
| U5 (phys 74-113) | xfunc.enhance → DEFERRED (technical audience) | NOT chunked; decision registered below |

### U5 DEFERRED — Enhancements and Modifications (phys 74-113)
- Topics: BAdI, Enhancement Framework, field exits, user exits — technical ABAP content
- Registry decision: xfunc.enhance → in_scope: deferred, audience: technical
- Reason: this corpus targets functional SD consultants; U5 content (BAdI implementations, Enhancement Framework, field exits) requires ABAP development knowledge and is out of scope for a functional RAG corpus.
- Action required to chunk U5: user must explicitly confirm that the corpus scope extends to technical/ABAP content.
- This is NOT a functional gap — it is a deliberate scope decision. Do not treat as a gap to fill with functional content.

### Chunks created (5 new):
- enterprise-structure/shared-master-data-cross-division-001 (U1 L2, phys 14-19, 828w, 138 w/p, quality:high)
- configuration/text-sources-sd-001 (U3 L1, phys 32-35, 669w, 167 w/p, quality:high)
- configuration/text-control-determination-001 (U3 L2, phys 36-48, 1352w, 104 w/p, quality:high)
- configuration/output-determination-sd-001 (U4 L1+L2, phys 49-64, 1623w, 101 w/p, quality:high)
- configuration/output-management-s4hana-001 (U4 L3, phys 65-73, 1009w, 112 w/p, quality:high)

### Secondary updates (cross-references only — density guardrail applied):
- configuration/sales-copying-control-001: added cross-refs to delivery + billing facet chunks + S4650 U2 note
- configuration/delivery-process-customizing-001: added cross-refs to sales + billing facet chunks + S4650 U2 note
- configuration/billing-copying-control-001: added cross-refs to sales + delivery facet chunks + S4650 U2 note
- enterprise-structure/sales-distribution-enterprise-structure-001: added cross-ref to new shared-master-data chunk + S4650 U1 L1 note

### Authority inversion (U4 — mutación mínima):
- configuration/billing-output-management-brfplus-001: added Cross-References pointing to configuration-output-determination-sd-001 and configuration-output-management-s4hana-001 as the primary scope. Billing BRFplus chunk remains accurate for its billing facet.

### P2 registry prospective validation findings:
1. Registry-first dedup produced correct decisions without re-judgment in 5/5 cases.
2. S4650 touched no topics absent from the registry — registry coverage was complete for this document.
3. No registry decision was found incorrect on application. Copy control density guardrail (U2) was the only runtime constraint, but this is a guardrail, not a registry error.
4. Secondary updates (U1 L1, U2): 2/2 were Cross-Reference-only due to density guardrail. Registry correctly identified these as secondary; density guardrail prevented regression.

### Coverage (pages not chunked — justified):
| Range | Content | Decision |
|---|---|---|
| phys 7-13 | Unit 1 TOC + L1 org elements overview | U1 L1 secondary (S4605 primary); cross-ref only per density guardrail |
| phys 18-19 | U1 Learning Assessment | Assessment pages — not chunked |
| phys 20-31 | U2 Copy Control | Secondary/unified view; cross-ref only per density guardrail |
| phys 22-25 | U2 Learning Assessment | Assessment pages — not chunked |
| phys 32 | U3 Unit TOC | Included in text-sources chunk page range |
| phys 39-48 | U3 Learning Assessment | Included in source page range; answers informing body written |
| phys 49 | U4 Unit TOC | Included in output-determination chunk page range |
| phys 68-73 | U4 Learning Assessment | Included in source page range; body content informed by assessment answers |
| phys 74-113 | U5 Enhancements | DEFERRED — technical scope (see above) |
| phys 114 | End matter / copyright | Not chunked |

## 2026-06-17 — S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf

- Relative path: processed/S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf
- Type: A (SAP official course material, S/4HANA 2020)
- Total pages: 190 (physical)
- Physical page offset: **+6** (footer label + 6 = physical page; confirmed at 2 independent points: phys 10 = L1 content, phys 52 = intercompany lesson header)
- Processed range: see chunks below
- Next pending page: N/A — all in-scope units processed

### Chunks created:
| ID | Path | Pages (physical) | Words | Density |
|---|---|---|---|---|
| special-processes-third-party-order-processing-001 | chunks/special-processes/third-party-order-processing-001.md | 8-21, 33-38 (20p) | ~2100 | ~105 w/p |
| special-processes-intercompany-sales-process-001 | chunks/special-processes/intercompany-sales-process-001.md | 46-68 (23p) | ~1575 | 68 w/p — quality:medium (below 80 w/p; expansion without rasterization would fabricate content) |
| integration-stock-transfer-order-intra-company-001 | chunks/integration/stock-transfer-order-intra-company-001.md | 76-92 (17p) | ~1750 | ~103 w/p |
| integration-stock-transfer-order-cross-company-001 | chunks/integration/stock-transfer-order-cross-company-001.md | 100-117 (18p) | ~1950 | ~108 w/p |
| special-processes-advanced-returns-management-001 | chunks/special-processes/advanced-returns-management-001.md | 155-163, 173-176 (13p) | ~1400 | ~108 w/p |

### Scope decisions:
| Unit | Content | Decision | Reason |
|---|---|---|---|
| U1 L1 | Third-party order processing (SD sales + MM purchase) | IN SCOPE | SD/SD↔MM integration — core SD process |
| U1 L2 | Individual purchase order (pure MM, no sales order) | DEFERRED | MM pure — no SD delivery, no customer billing |
| U1 L3 | Automatic third-party processing (ALES, SD config) | IN SCOPE | SD configuration variant — merged into U1 L1 chunk |
| U2 | Cross-company code sales (intercompany billing) | IN SCOPE | Core SD process — intercompany sales invoice (IV) |
| U3 | Intra-company STO with SD delivery | IN SCOPE (confirmed by user) | SD delivery type NL, BP master config — SD consultant scope |
| U4 | Cross-company STO with intercompany billing | IN SCOPE | SD delivery type NLCC + billing type IV — SD consultant scope |
| U5 | Subcontracting | DEFERRED | MM pure — no customer-facing SD process |
| U6 L1 | ARM overview + customer returns (RE2, refund codes) | IN SCOPE (confirmed by user) | Core SD returns process in S/4HANA |
| U6 L2 | ARM supplier returns | DEFERRED (mentioned in body) | MM pure core; intercompany variant noted in ARM chunk body without citation |
| U6 L3 | BKP/BDD variants | IN SCOPE | SD returns variants — merged into U6 L1 chunk |

### Dedup / registry notes:
All S4680 topics were UNREGISTERED in the P2 authority registry at the start of this session (registry was built before S4680 was inspected → intentional completeness test). Fallback judgment applied throughout:
- No existing chunk covered any of these 5 in-scope topics.
- Registry fix: `o2c.credit` entry was incorrectly listing S4680 as a prospective source. Corrected to S4F30 + BD6 (FSCM credit management). See ontology/authority_registry.yaml correction note.

### Quality notes:
- intercompany-sales-process-001: quality:medium (68 w/p). Pages 46-68 include significant diagram coverage (pricing procedure determination diagrams, document flow diagrams, account assignment overview). Rasterization not run; downgrade to medium is the correct call. To upgrade: rasterize phys 46-68 and extract diagram content.
- All other chunks: quality:high (≥100 w/p after expansion).

### Coverage (pages not chunked — justified):
| Range | Content | Decision |
|---|---|---|
| phys 7 | Cover page | Not chunked |
| phys 8-9 | Course Overview / TOC | Not chunked |
| phys 22-32 | U1 L2 individual PO processing | DEFERRED (MM pure) |
| phys 39-45 | U1 Learning Assessment + unit divider | Not chunked |
| phys 69-75 | U2 Learning Assessment + unit divider | Not chunked |
| phys 93-99 | U3 Learning Assessment + unit divider | Not chunked |
| phys 118-154 | U5 Subcontracting (entire unit) | DEFERRED (MM pure) |
| phys 164-172 | U6 L2 ARM supplier returns | DEFERRED (MM pure); brief context in ARM chunk body |
| phys 177-190 | U6 Learning Assessment + Appendix | Not chunked |

### Status: completed

## S4680 — Eval harness (2026-06-17)

| Retriever | Mapeables | @1 | @3 | @5 | @10 | MRR |
|---|---|---|---|---|---|---|
| lexical | 25/31 | 20.0% | — | 84.0% | 92.0% | 0.488 |
| semantic_long (bge-m3) | 25/31 | 60.0% | 76.0% | 76.0% | 96.0% | 0.700 |

Not-mappable: 6/31 available questions (U5 subcontracting = DEFERRED, U6 L2 ARM supplier returns = DEFERRED; assessment questions from those units).

Observation: lexical @1 (20%) is the lowest in the corpus by a large margin; semantic @1 (60%) is healthy. The delta (@1 +40 pp) is the largest semantic uplift seen across all documents. This is expected for new chunks with specialized vocabulary that the lexical scorer underweights. The new chunks' aliases and body vocabulary are correctly calibrated for semantic retrieval but not dominant in TF-IDF.

Extraction ratios (Skill 6): all 5 chunks show ratio <0.5 (range 0.30-0.45). Consistent with SAP course material where diagrams, exercises, and objectives pages constitute ~50-60% of page content. Accepted as normal for this source type; not a gap.

Coverage table: all uncovered page clusters (≥3p, ≥100w) are either learning assessment pages or DEFERRED MM pure units. Coverage gate: PASS.

Ontology completeness report: docs/audit/ontology_completeness_report_S4680.md

---

## 2026-06-18 — S4F30 + BD6 (credit-management area)

### Status: completed

Source: S4F30_EN_Col12 (132 pages, © 2019 SAP SE, Col12 → release S/4HANA 1909) + BD6 scope item (8 pages)
Offset: +6 (física = footer + 6), verified at 3 points (phys7=footer1, phys18=footer12, phys30=footer24)

### Chunks created (3)

| Chunk ID | Path | Pages (phys) | Density | Quality |
|---|---|---|---|---|
| credit-management-credit-master-data-001 | credit-management/credit-master-data-001.md | 20-29 | 118.6 w/p | high |
| credit-management-credit-check-sd-integration-001 | credit-management/credit-check-sd-integration-001.md | 30-38 (+BD6 pp1-2,5) | 117.4 w/p | high |
| credit-management-credit-rules-engine-001 | credit-management/credit-rules-engine-001.md | 39-43 | 229.2 w/p | high |

### Scope decisions

- IN SCOPE: U2 L1-L4 (phys 20-43) — credit master data, SD-credit check integration, credit rules engine
- DEFERRED (not chunked): U2 L5 (external SCP credit agency integration), U2 L6 (reporting/mass changes), U1 (overview — too thin), U3 (Cloud for Customer Payments — FI-AR cloud), U4 (Collections Management — FI-AR), U5 (Dispute Resolution — FI-AR)
- All deferred units logged in DEB-004 (docs/audit/validation_debt.md)

### Version handling (S4F30 2019 vs BD6 current)

No functional divergences detected between S4F30 (1909) and BD6 (current scope item). Process flow (SO → credit check → block → DCD → release/reject) is consistent. sap_release: S/4HANA 1909 tagged in all 3 chunks.

### Enum change

validate_chunks.py VALID_RELEASE expanded: added "S/4HANA 1909" (line 28). Self-grep confirmed.

### Risk flag

HIGH RISK: source is 2019; no provenance audit (statement-by-statement); no expert sign-off. DEB-004 in validation_debt.md. Chunks are structurally_validated + retrieval_tested only.

### Next pending

Eval results: see eval/results/ (S4F30 score run after this log entry). Next doc: TBD — S4601 EXCLUIDO (Supply Chain Execution, fuera de scope SD, decisión cerrada 2026-06-23).
