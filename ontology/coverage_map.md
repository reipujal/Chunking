# SD Ontology Coverage Map — P2 v0
Generated: 2026-06-16
Corpus: 82 chunks across 5 processed documents (S4600, S4605, S4610, S4615, S4620)
Topics: 42 total | **4 with 0 chunks** | 5 with 1 chunk

> Chunks are counted by primary topic assignment (highest confidence).
> Multi-topic chunks appear once in the primary topic count; see chunk_topic_map.json for full mapping.
> `★` = confirmed gap (0 chunks, prospective primary source known)
> `☆` = deferred gap (0 chunks, scope decision required)
> `⚠` = single-chunk coverage (low redundancy; authority may be thin)
> `[D]` = distributed authority (multiple authoritative sources for facets)
> `[I]` = authority inversion pending (existing chunk will become supplementary)

---

## Enterprise Setup

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| ent.org.sales | Sales Org Structure | 3 | [D] distributed | S4605 (general) + S4615 (billing facet) |
| ent.org.shipping | Shipping Point / Loading Point | ⚠ 1 | single | S4610 |
| ent.org.warehouse | Warehouse Org Units (EWM/IM) | ⚠ 1 | single | S4610 |
| **ent.org.cross_div** ★ | **Cross-Division Sales** | **0** | prospective | S4650 Unit 1 L2 (not yet chunked) |
| ent.master.bp | Business Partner Master Data | ⚠ 1 | single | S4600 |
| ent.master.material | Material Master (SD Views) | ⚠ 1 | single | S4600 |
| ent.master.partner | Partner Functions | ⚠ 1 | single | S4605 |

---

## Order-to-Cash

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| o2c.presales | Presales Documents | ⚠ 1 | single | S4600 |
| o2c.order.basic | Basic Sales Order Processing | 4 | single | S4605 |
| o2c.order.special | Special Order Types | 2 | [D] distributed | S4605 (process) + S4615 (billing types) |
| o2c.order.outline | Outline Agreements | 2 | single | S4605 |
| o2c.order.atp | Availability Check + BOP | 2 | single | S4600 |
| o2c.order.collective | Collective Processing | ⚠ 1 | single | S4600 |
| o2c.delivery.outbound | Outbound Delivery | 5 | single | S4610 |
| o2c.delivery.picking | Picking (EWM) + GI | 2 | single | S4610 |
| o2c.delivery.inbound | Inbound Delivery (EWM) | ⚠ 1 | single | S4610 |
| o2c.delivery.special | Special Delivery Functions | ⚠ 1 | single | S4610 |
| o2c.billing.standard | Standard Billing | 4 | single | S4615 |
| o2c.billing.special | Special Billing Types | 5 | single | S4615 |
| o2c.billing.settlement | Invoice List / Split | 3 | single | S4615 |
| o2c.billing.complaints | Complaints Billing | 5 | single | S4615 (uniform) |
| o2c.billing.fi | Billing–FI Integration | 3 | single | S4615 |
| o2c.credit | Credit Management | 3 | single | S4F30 (Col12, 2019) primary + BD6 scope item (sap_reference) |

---

## Pricing & Conditions

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| price.technique | Condition Technique Overview | ⚠ 1 | single | S4620 |
| price.config | Pricing Procedure Config | ⚠ 1 | single | S4620 |
| price.records | Condition Records | ⚠ 1 | single | S4620 |
| price.special | Special Condition Types + Functions | 2 | single | S4620 |
| price.ccm | Condition Contract Management | 3 | single | S4620 |
| price.agreements | Pricing Agreements | ⚠ 1 | single | S4620 |
| price.free_goods | Free Goods Determination | ⚠ 1 | single | S4605 |

---

## Document Type Control

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| ctrl.sales | Sales Doc Type / Item Cat / Sched Line | 3 | single | S4605 |
| ctrl.delivery | Delivery Type + Item Category | 2 | single | S4610 |
| ctrl.billing_type | Billing Type Configuration | 2 | single | S4615 |

---

## Cross-Functional

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| xfunc.copy | Copy Control (all chains) | 3 | [D] distributed | S4605 + S4610 + S4615 (by facet) |
| xfunc.incompletion | Incompletion Check | ⚠ 1 | single | S4605 |
| xfunc.material_det | Material Det / Listing / Exclusion | 2 | single | S4605 |
| **xfunc.text** ★ | **Text Control** | **0** | prospective | S4650 Unit 3 (not yet chunked) |
| xfunc.output | Output Determination | 0+⚠[I] | [I] inversion | S4650 Unit 4 = primary (pending); S4615 billing BRFplus = supplementary |
| **xfunc.enhance** ☆ | **Enhancements / Modifications** | **0** | deferred | S4650 Unit 5 — technical audience; scope decision required |

> `xfunc.output` note: `configuration-billing-output-management-brfplus-001` covers the billing BRFplus
> facet only. Counts as supplementary coverage, not primary. Topic is effectively a gap until S4650 Unit 4
> is chunked and becomes the authoritative primary.

---

## Analytics

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| analytics.sales | Sales Monitoring / CDS Analytics | ⚠ 1 | single | S4600 |

---

## Integration

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| integration.gbi | General Billing Interface | ⚠ 1 | single | S4615 |

---

## Platform

| Topic ID | Label | Primary Chunks | Auth Pattern | Sources |
|---|---|---|---|---|
| platform.fiori | SAP Fiori Launchpad / UX | ⚠ 1 | single | S4600 |

---

## Gap Summary

| Gap type | Topic | Priority | Action |
|---|---|---|---|
| ✓ Filled | `o2c.credit` | — | 3 chunks created from S4F30 (2019) + BD6; DEB-004 in ledger (high-risk: pending provenance audit + expert review) |
| ★ Gap | `ent.org.cross_div` | MEDIUM | Chunk S4650 Unit 1 Lesson 2 (phys 14-19) |
| ★ Gap | `xfunc.text` | MEDIUM | Chunk S4650 Unit 3 (phys 32-48) |
| ★ Gap (near) | `xfunc.output` | MEDIUM | Chunk S4650 Unit 4 (phys 49-73); update authority |
| ☆ Deferred | `xfunc.enhance` | — | User decision: extend corpus to technical audience? |

---

## Distributed Authority Topics (require care in dedup)

| Topic | Facets | P2 Finding |
|---|---|---|
| `ent.org.sales` | S4605 (general) / S4615 (billing org) | No conflict; query-based routing |
| `o2c.order.special` | S4605 (process) / S4615 (billing types) | Conflict: CS vs BV — registered in authority_registry |
| `xfunc.copy` | S4605 (sales) / S4610 (delivery) / S4615 (billing) | **Structural fragmentation**: one concept, 3 chunks. S4650 Unit 2 provides unified view (supplementary). |

---

## Trust Gate Check

- **Ontology not induced from corpus:** 3 topics have 0 chunks (ent.org.cross_div, xfunc.text, xfunc.enhance); o2c.credit filled 2026-06-18. ✓
- **CS/BV conflict registered:** o2c.order.special — conflict: true with resolution note. ✓
- **Inversion pattern documented:** xfunc.output — S4650 Unit 4 will supersede existing S4615 chunk as primary. ✓
- **Technical scope clearly flagged:** xfunc.enhance — audience: technical, in_scope: deferred. ✓
- **Corpus source count (primary):** S4615→29, S4605→22, S4610→15, S4600→10, S4620→10 across 82 chunks. Billing-heavy corpus reflects processing order, not ontology bias.
