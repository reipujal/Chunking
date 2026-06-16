# Lesson-Level Gold Re-Evaluation — P3 Retrieval Verdict
Generated: 2026-06-16
Model B & C: `BAAI/bge-m3` (8192-token context) — SAME model, cached from granularity probe
Corpus: 82 chunks | Docs: S4600, S4605, S4610, S4615, S4620
Gold: Lesson-title queries (TOC structural assignment, no content-overlap)


## Pre-Registered Decision Criterion
*Written BEFORE examining results.*

**Context:** Unit-gold B-C delta = +3.0 pp @1 / +0.022 MRR (non-conclusive due to
indulgent gold spans). Lesson-gold uses TIGHTER spans (lesson-level, ~3-8 pages each
vs 8-22 pages at unit level). Queries are lesson TITLES (structural, not LA questions).

**If lesson-gold C@1 - B@1 >= 8 pp** (or MRR delta >= 0.06):
  => Window-pooling helps materially at lesson granularity.
  => P3 (hierarchical chunking / finer retrieval units) JUSTIFIED by retrieval evidence.

**If lesson-gold C@1 - B@1 < 5 pp** (similar to unit-gold +3.0 pp):
  => Window-pooling does not help even with tighter gold.
  => CLOSE the P3 retrieval axis. Evaluate P3 via generation quality arm
     (faithfulness, answer precision on long chunks) if motivation remains.
  => Do NOT create further refined gold sets — this is the terminal retrieval test.

**Non-conclusive condition:** non-mappable rate > 25% of lesson queries.
  (Signals corpus coverage gap, not retrieval weakness.)

**B regression caveat:** if B drops significantly vs unit-gold (>5 pp), suspect gold
quality mismatch (lesson-title queries may systematically favor different chunks than
the LA questions used for unit-gold). Flag but do not invalidate.


## Correctness Checklist

- Gold assignment method: TOC structural (lesson titles + footer page ranges)
- Offsets reused (NOT re-detected): S4600/S4605/S4615=+8, S4610/S4620=+6
- Spot-checks (first phys page of lesson span shows lesson title):
  - S4600 phys 10: 'Unit 1 Lesson 1 Identifying Key Features of SAP Fiori' OK
  - S4610 phys 28: 'Unit 3 Lesson 1 Controlling Delivery Documents' OK
  - S4615 phys 65: 'Unit 7 Lesson 2 Understanding Special Types of Settlement' OK
  - S4620 phys 25: 'Unit 2 Lesson 1 Configuring Pricing' OK
- Unit gold preserved: yes (separate files, lesson gold is additive)
- Retrievers: UNCHANGED — using cached bge-m3 embeddings from granularity probe
- Model B = C: BAAI/bge-m3 (verified in granularity probe, cache reused)

## Assignment Method Breakdown

Total lesson queries: 82 across 5 docs
Assignment method for ALL queries: `toc_structural` (lesson title from TOC)
unit_fallback: 0 (lesson-objective approach creates new queries for EVERY lesson)

**Note:** These are NEW queries (lesson titles), not refinements of LA questions.
Unit-level LA gold (134 questions) is preserved for comparison.

| Doc | Lesson queries | Offset | Multi-lesson units |
| --- | --- | --- | --- |
| S4600 | 26 | +8 | 23 lessons in multi-lesson units |
| S4605 | 18 | +8 | 13 lessons in multi-lesson units |
| S4610 | 11 | +6 | 8 lessons in multi-lesson units |
| S4615 | 13 | +8 | 5 lessons in multi-lesson units |
| S4620 | 14 | +6 | 12 lessons in multi-lesson units |

## Mappable Queries per Doc (lesson spans vs chunk page ranges)

| Doc | Total | Mappable | Not mappable | Map rate |
| --- | --- | --- | --- | --- |
| S4600 | 26 | 15 | 11 | 57.7% |
| S4605 | 18 | 18 | 0 | 100.0% |
| S4610 | 11 | 11 | 0 | 100.0% |
| S4615 | 13 | 12 | 1 | 92.3% |
| S4620 | 14 | 14 | 0 | 100.0% |
| **TOTAL** | **82** | **70** | **12** | **85.4%** |

Non-mappable rate 14.6%: within confidence threshold (< 25%).

## Global Results — Lesson Gold

| Doc | N | A@1 | A@5 | A@10 | A-MRR | B@1 | B@5 | B@10 | B-MRR | C@1 | C@5 | C@10 | C-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S4600 | 15 | 53.3% | 100.0% | 100.0% | 0.744 | 73.3% | 100.0% | 100.0% | 0.844 | 86.7% | 100.0% | 100.0% | 0.906 |
| S4605 | 18 | 66.7% | 88.9% | 100.0% | 0.754 | 83.3% | 94.4% | 100.0% | 0.885 | 88.9% | 88.9% | 94.4% | 0.898 |
| S4610 | 11 | 45.5% | 90.9% | 90.9% | 0.617 | 81.8% | 90.9% | 90.9% | 0.864 | 72.7% | 90.9% | 90.9% | 0.818 |
| S4615 | 12 | 50.0% | 66.7% | 75.0% | 0.594 | 66.7% | 75.0% | 75.0% | 0.683 | 50.0% | 75.0% | 75.0% | 0.597 |
| S4620 | 14 | 21.4% | 64.3% | 92.9% | 0.459 | 64.3% | 92.9% | 100.0% | 0.752 | 50.0% | 71.4% | 78.6% | 0.619 |
| **TOTAL** | **70** | **48.6%** | **82.9%** | **92.9%** | **0.644** | **74.3%** | **91.4%** | **94.3%** | **0.812** | **71.4%** | **85.7%** | **88.6%** | **0.780** |

## By Chunk Type (aggregate across all docs, lesson gold)

| Type | N | A@1 | B@1 | delta(B-A) | C@1 | delta(C-B) | A-MRR | B-MRR | C-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| concept | 27 | 44.4% | 66.7% | +0.2pp | 59.3% | -0.1pp | 0.557 | 0.712 | 0.667 |
| configuration | 15 | 80.0% | 86.7% | +0.1pp | 80.0% | -0.1pp | 0.880 | 0.922 | 0.867 |
| process | 28 | 35.7% | 75.0% | +0.4pp | 78.6% | +0.0pp | 0.601 | 0.849 | 0.842 |

## B vs C Question-Level Diff (lesson gold @1)

- both_hit  (B=1, C=1): 47
- c_fixed   (B=0, C=1 — window recovers): 3
- b_regression (B=1, C=0 — window loses): 5
- both_miss (B=0, C=0): 15

C recovers (sample):
  - S4600-LG-018: _Using Presales Documents_
  - S4600-LG-019: _Executing Make-to-Order Production_
  - S4605-LG-008: _Data Flow in the Application_

B-regressions (sample):
  - S4610-LG-011: _Using Special Functions in Deliveries_
  - S4615-LG-004: _Processing Special Billing Types_
  - S4615-LG-005: _Setting Up the Data Flow for Billing Documents_
  - S4620-LG-002: _Introducing the Condition Technique_
  - S4620-LG-011: _Using Pricing Agreements_

## Lesson-Gold vs Unit-Gold: B-C Delta Comparison

| Metric | Unit-gold B-C | Lesson-gold B-C | Change |
| --- | --- | --- | --- |
| C-B @1 | +3.0 pp | -2.9 pp | -5.9 pp |
| C-B MRR | +0.0220 | -0.0321 | -0.0541 |
| A@1 | 62.7% | 48.6% | — |
| B@1 | 75.4% | 74.3% | — |
| C@1 | 78.4% | 71.4% | — |

## Verdicts

### Verdict 1 — Semantic vs Lexical (A vs B, lesson gold)
Semantic still wins at lesson granularity: B@1 - A@1 = +25.7 pp. Confirming bge-m3 advantage holds.

### Verdict 2 — P3 Granularity (B vs C, lesson gold)
C@1 - B@1 (lesson gold) = **-2.9 pp**
C-MRR - B-MRR (lesson gold) = **-0.0321**
Reference (unit gold): C@1 - B@1 = +3.0 pp | C-MRR - B-MRR = +0.022

**VERDICT: CLOSE THE RETRIEVAL AXIS FOR P3.**
C-B delta at lesson gold (-2.9 pp) is similar to unit-gold (+3.0 pp).
Window-pooling does not help even with tighter gold spans. The +3.0 pp unit-gold signal
does not amplify when spans are narrowed to lesson level.

**Implication:** If P3 (hierarchical chunking) is still desired, motivate it via:
  1. Generation quality arm: answer faithfulness / precision on long chunks
  2. Index efficiency: O(N×M) window vectors vs O(N) chunk vectors
  3. Maintainability: finer chunks easier to update/version
  Do NOT refine gold further — this is the terminal retrieval test.

**Confidence gate:** Non-mappable rate 14.6% < 25% — verdict is reliable.

## Limitations

- Queries are lesson TITLES (not LA questions) — different query distribution than unit gold.
  Comparison with unit-gold numbers is informative but not apples-to-apples.
- Lesson titles are shorter and more topic-focused than LA questions → may systematically
  favor or disfavor certain retrieval strategies.
- Unit-gold LA questions may be harder/subtler; lesson-title queries are easier (topic match).
  A smaller B-C delta here may not fully generalize to harder queries.
- 5 documents, ~82 lesson queries: moderate sample size. Add more docs for higher confidence.
- Window parameters (400 tok / stride 300) not tuned for this corpus.

## How to Run

```bash
cd 'c:/Users/aranu/Desktop/IA/Chunking'
# Build lesson gold files (one-time):
python3 eval/lesson_gold_builder.py
# Run probe (all 5 docs):
python3 eval/lesson_gold_probe.py
# Single doc via score.py:
python3 eval/score.py --src S4620 --retriever semantic_long --gold eval/gold/S4620_lesson_gold.json
python3 eval/score.py --src S4620 --retriever semantic_window --gold eval/gold/S4620_lesson_gold.json
```