"""Append S4680 ontology extension proposals to topics.yaml and authority_registry.yaml.
PROPOSAL entries only — not governing. Marked clearly. 2026-06-17."""

TOPICS_APPEND = """
  # ─────────────────────────────────────────────────────────────────────────────
  # PROPOSALS — S4680 (2026-06-17) — NOT GOVERNING
  # These topics were discovered during S4680 processing and were UNREGISTERED
  # in the authority registry. Added as proposals pending editorial review before
  # elevating to governing status.
  # ─────────────────────────────────────────────────────────────────────────────

  # PROPOSAL: o2c.third_party
  - id: o2c.third_party
    label: "Third-Party Order Processing"
    process_area: special-processes
    sap_reference: ""
    proposal: true
    proposal_status: pending_review
    notes: >
      PROPOSAL (2026-06-17) — S4680 Unit 1 (in-scope lessons only: L1 automatic
      third-party, L3 ALES variant). L2 pure MM individual PO: DEFERRED.
      TAS item category, BANS item category group, schedule line category CS,
      billing relevance B vs F, billing quantity E vs F, ALES auto-PO.
      Primary source: S4680 (first document processed for this topic).
      NOT GOVERNING until elevated after review.

  # PROPOSAL: o2c.intercompany
  - id: o2c.intercompany
    label: "Cross-Company Code Sales and Intercompany Billing"
    process_area: special-processes
    sap_reference: ""
    proposal: true
    proposal_status: pending_review
    notes: >
      PROPOSAL (2026-06-17) — S4680 Unit 2. Cross-company code sales process:
      allowed delivering plants, PI01/IV01 condition types, billing type IV,
      IV sales area, payer BP master record, automatic incoming invoice via EDI.
      Primary source: S4680 (first document processed for this topic).
      NOT GOVERNING until elevated after review.

  # PROPOSAL: integration.sto
  - id: integration.sto
    label: "Stock Transport Orders with SD Delivery (Intra- and Cross-Company)"
    process_area: integration
    sap_reference: ""
    proposal: true
    proposal_status: pending_review
    notes: >
      PROPOSAL (2026-06-17) — S4680 Units 3 and 4.
      Intra-company STO: document type UB, delivery type NL, no billing.
      Cross-company STO: document type NB, delivery type NLCC, billing type IV.
      Shared: sales area assignment to supplying plant, goods recipient BP master,
      one-step vs two-step procedure.
      Primary source: S4680 (first document processed for this topic).
      NOT GOVERNING until elevated after review.

  # PROPOSAL: o2c.returns.arm
  - id: o2c.returns.arm
    label: "Advanced Returns Management (ARM) — Customer Returns"
    process_area: special-processes
    sap_reference: ""
    proposal: true
    proposal_status: pending_review
    notes: >
      PROPOSAL (2026-06-17) — S4680 Unit 6 L1 + L3 (in scope: customer returns).
      S4680 U6 L2 (supplier returns) DEFERRED — MM pure.
      Covers: RE2 sales document type, refund codes, follow-up activities,
      Returns Overview, BKP (Accelerated Customer Returns), BDD (without ARM).
      OPS_ADVRETURNS always-on in S/4HANA (no separate activation).
      Primary source: S4680 (first document processed for this topic).
      NOT GOVERNING until elevated after review.

  # PROPOSAL: mm.subcontracting (DEFERRED — MM pure)
  - id: mm.subcontracting
    label: "Subcontracting"
    process_area: integration
    in_scope: deferred
    sap_reference: ""
    proposal: true
    proposal_status: pending_review
    notes: >
      PROPOSAL (2026-06-17) — S4680 Unit 5. DEFERRED: MM pure process.
      No customer-facing SD sales order, no SD delivery, no customer billing.
      Subcontracting purchase order (item category L), BOM explosion,
      component delivery, GR with automatic component consumption.
      If corpus scope extends to MM integration topics, this is the entry point.
      NOT GOVERNING; not chunked.
"""

REGISTRY_APPEND = """
  # ─────────────────────────────────────────────────────────────────────────
  # PROPOSALS — S4680 (2026-06-17) — NOT GOVERNING
  # ─────────────────────────────────────────────────────────────────────────

  # PROPOSAL: o2c.third_party
  - topic_id: o2c.third_party
    label: "Third-Party Order Processing"
    proposal: true
    proposal_status: pending_review
    authority_pattern: single
    authoritative_sources:
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 1 L1+L3 (phys 8-21, 33-38)"
    authoritative_chunks:
      - special-processes-third-party-order-processing-001
    supplementary_sources: []
    supplementary_chunks: []
    conflict: false
    notes: >
      PROPOSAL — first authoritative source for this topic is S4680.
      S4601 and S4605 may add supplementary coverage.
      NOT GOVERNING until reviewed.

  # PROPOSAL: o2c.intercompany
  - topic_id: o2c.intercompany
    label: "Cross-Company Code Sales and Intercompany Billing"
    proposal: true
    proposal_status: pending_review
    authority_pattern: single
    authoritative_sources:
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 2 (phys 46-68)"
    authoritative_chunks:
      - special-processes-intercompany-sales-process-001
    supplementary_sources: []
    supplementary_chunks: []
    conflict: false
    notes: >
      PROPOSAL — first authoritative source for this topic is S4680.
      NOT GOVERNING until reviewed.

  # PROPOSAL: integration.sto
  - topic_id: integration.sto
    label: "Stock Transport Orders with SD Delivery"
    proposal: true
    proposal_status: pending_review
    authority_pattern: faceted
    authoritative_sources:
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 3 intra-company (phys 76-92)"
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 4 cross-company (phys 100-117)"
    authoritative_chunks:
      - integration-stock-transfer-order-intra-company-001
      - integration-stock-transfer-order-cross-company-001
    supplementary_sources: []
    supplementary_chunks: []
    conflict: false
    notes: >
      PROPOSAL — S4680 is the primary source; two chunks for two STO variants.
      NOT GOVERNING until reviewed.

  # PROPOSAL: o2c.returns.arm
  - topic_id: o2c.returns.arm
    label: "Advanced Returns Management (ARM) — Customer Returns"
    proposal: true
    proposal_status: pending_review
    authority_pattern: single
    authoritative_sources:
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 6 L1+L3 (phys 155-163, 173-176)"
    authoritative_chunks:
      - special-processes-advanced-returns-management-001
    supplementary_sources: []
    supplementary_chunks: []
    conflict: false
    notes: >
      PROPOSAL — S4680 is the primary source for ARM customer returns.
      BD6 (BKP) and BDD process diagrams provide supplementary visual context.
      NOT GOVERNING until reviewed.

  # PROPOSAL: mm.subcontracting (DEFERRED — no chunk created)
  - topic_id: mm.subcontracting
    label: "Subcontracting"
    proposal: true
    proposal_status: pending_review
    in_scope: deferred
    authority_pattern: single
    authoritative_sources:
      - file: "S4680_EN_Col17 Cross-Application Processes in SAP S4HANA Sales and Procurement.pdf"
        facet: "Unit 5 (phys 118-154) — MM pure, not chunked"
    authoritative_chunks: []
    supplementary_sources: []
    supplementary_chunks: []
    conflict: false
    notes: >
      PROPOSAL — S4680 Unit 5 covers subcontracting but scope is MM pure.
      No chunk created. Entry point if corpus scope extends to MM integration.
      NOT GOVERNING until reviewed.
"""

with open('ontology/topics.yaml', 'a', encoding='utf-8') as f:
    f.write(TOPICS_APPEND)
print("topics.yaml updated")

with open('ontology/authority_registry.yaml', 'a', encoding='utf-8') as f:
    f.write(REGISTRY_APPEND)
print("authority_registry.yaml updated")
