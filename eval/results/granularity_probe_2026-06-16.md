# Granularity Probe — Truncation Fix + P3 (Window-Pooled)
Generated: 2026-06-16
Model B & C: `BAAI/bge-m3` (8192-token context)
Corpus: 82 chunks | Docs: S4600, S4605, S4610, S4615, S4620

## Pre-Registered Decision Criterion

*Written BEFORE examining results.*

### A vs B — Truncation verdict
If B@1 − A@1 ≥ ~10 pp corpus-wide AND concept-type regression resolves (concept delta flips positive) → v4 borderline was a truncation artifact; whole-chunk long-context wins clearly.

### B vs C — P3 granularity probe (model identical; only granularity varies)
**If C@1 − B@1 ≥ ~10 pp (or substantial at operative k)** → finer retrieval units help materially → P3 (hierarchical chunking) justified by retrieval evidence.
**If C@1 − B@1 is small (< ~3–5 pp)** → NON-CONCLUSIVE. Unit-level gold is indulgent (@5 already high); B≈C here does NOT rule out P3 benefit. Recommended next: build lesson-level gold and repeat B vs C before discarding P3.

## Correctness Checklist

- Model B (LongContextRetriever): `BAAI/bge-m3`
- Model C (WindowPooledRetriever): `BAAI/bge-m3` ← SAME model
- B = C model: YES ✓
- B prefix: none (BAAI/bge-m3 symmetric — no instruction prefix)
- C prefix: none (same)
- B max_context: 8192 tokens
- C window size: 400 tokens, stride 300 (~25% overlap)
- Max chunk tokens vs B context: 2070 << 8192 -> NO TRUNCATION OK
- Max window tokens (incl special): 403 ≤ 512 → OK ✓
- Total windows: 339 across 82 chunks (avg 4.1 windows/chunk)
- Smoke test B: PASS ✓ | query='Canceling Billing Documents in SAP SD' -> rank-1=billing-billing-document-cancellation-001 (expected billing-billing-document-cancellation-001)
- Smoke test C: PASS ✓ | query='Canceling Billing Documents in SAP SD' -> rank-1=billing-billing-document-cancellation-001 (expected billing-billing-document-cancellation-001)
- Lexical A re-run vs v4 reference: matches ✓

## Global Results — All Docs

| Doc | N | A@1 | A@5 | A@10 | A-MRR | B@1 | B@5 | B@10 | B-MRR | C@1 | C@5 | C@10 | C-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S4600 | 21 | 57.1% | 85.7% | 95.2% | 0.718 | 71.4% | 85.7% | 95.2% | 0.791 | 76.2% | 95.2% | 100.0% | 0.856 |
| S4605 | 31 | 61.3% | 93.5% | 96.8% | 0.747 | 87.1% | 100.0% | 100.0% | 0.907 | 87.1% | 93.5% | 100.0% | 0.906 |
| S4610 | 26 | 61.5% | 92.3% | 92.3% | 0.727 | 69.2% | 92.3% | 96.2% | 0.787 | 73.1% | 92.3% | 96.2% | 0.814 |
| S4615 | 30 | 70.0% | 83.3% | 90.0% | 0.762 | 66.7% | 86.7% | 93.3% | 0.749 | 73.3% | 80.0% | 86.7% | 0.767 |
| S4620 | 26 | 61.5% | 96.2% | 100.0% | 0.755 | 80.8% | 96.2% | 96.2% | 0.873 | 80.8% | 100.0% | 100.0% | 0.881 |
| **TOTAL** | **134** | **62.7%** | **90.3%** | **94.8%** | **0.744** | **75.4%** | **92.5%** | **96.3%** | **0.823** | **78.4%** | **91.8%** | **96.3%** | **0.845** |

## By Chunk Type (aggregate across all docs)

| Type | N | A@1 | B@1 | delta(B-A) | C@1 | delta(C-B) | A-MRR | B-MRR | C-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| concept | 52 | 67.3% | 69.2% | +1.9pp | 73.1% | +3.8pp | 0.761 | 0.770 | 0.809 |
| configuration | 44 | 59.1% | 77.3% | +18.2pp | 77.3% | +0.0pp | 0.718 | 0.846 | 0.836 |
| process | 38 | 60.5% | 81.6% | +21.1pp | 86.8% | +5.3pp | 0.749 | 0.870 | 0.903 |

## A vs B — Truncation Analysis

*A = TF-IDF (indexes full body). B = BAAI/bge-m3 whole-chunk (8192 ctx, no truncation).*
*v4 bge-small truncated 82/82 chunks. BAAI/bge-m3 truncates 0/82.*

- Global B@1 − A@1: **+12.7 pp** (threshold ≥ ~10 pp for 'clear win')
- Global B@5 − A@5: +2.2 pp
- Global B-MRR − A-MRR: +0.080

### Concept-type regression status (key signal)
v4 concept delta was −5.8 pp (semantic bge-small WORSE than lexical on concept queries).
Under Jina-v2 (no truncation), concept delta = **+1.9 pp** → regression **resolved** — was a truncation artifact. ✓

### Per-doc A@1 vs B@1
| Doc | A@1 | B@1 | delta |
| --- | --- | --- | --- |
| S4600 | 57.1% | 71.4% | +14.3pp |
| S4605 | 61.3% | 87.1% | +25.8pp |
| S4610 | 61.5% | 69.2% | +7.7pp |
| S4615 | 70.0% | 66.7% | -3.3pp |
| S4620 | 61.5% | 80.8% | +19.2pp |

## B vs C — P3 Granularity Probe

*B = whole-chunk (1 vector/chunk). C = window-pooled (max-pool over windows).*
*Model B = C: BAAI/bge-m3. Only variable: indexing granularity.*

- Global C@1 − B@1: **+3.0 pp**
- Global C@5 − B@5: **-0.7 pp**
- Global C-MRR − B-MRR: +0.021

### Per-doc B@1 vs C@1
| Doc | B@1 | C@1 | delta |
| --- | --- | --- | --- |
| S4600 | 71.4% | 76.2% | +4.8pp |
| S4605 | 87.1% | 87.1% | +0.0pp |
| S4610 | 69.2% | 73.1% | +3.8pp |
| S4615 | 66.7% | 73.3% | +6.7pp |
| S4620 | 80.8% | 80.8% | +0.0pp |

### Per-question diff B vs C (@1)
- both_hit (B=1, C=1): 93
- c_fixed  (B=0, C=1 — window-pool recovers): 12
- b_regression (B=1, C=0 — window-pool loses): 8
- both_miss (B=0, C=0): 21

#### C recovers (window-pool finds, whole-chunk misses)
| ID | Token-exact | Question (first 90 chars) |
| --- | --- | --- |
| S4600-LA-U4-Q2 | no | Which one of the following partner functions is applicable for a customer who receives the |
| S4600-LA-U10-Q1 | YES | With SAP Smart Business, you can jump directly from a data point in the chart to the relev |
| S4610-LA-U1-Q1 | no | Which delivery document refers to a sales document? |
| S4610-LA-U1-Q3 | YES | As of SAP S/4HANA 1709, SAP Transportation Management is included in the core. |
| S4610-LA-U3-Q1 | no | Order items that are due for delivery and have the same delivery split criteria may be shi |
| S4610-LA-U4-Q9 | no | The delivery due list is a worklist of all operations requiring deliveries. |
| S4615-LA-U5-Q2 | no | Which of the following copying control options are available at the item level? |
| S4615-LA-U6-Q2 | no | You want to create billing documents regularly on specific dates. How do you achieve this? |
| S4620-LA-U1-Q1 | no | You can limit a pricing agreement to a certain period. |
| S4620-LA-U2-Q3 | no | Which of the following elements contains keys that are used to create dependent condition  |
| S4620-LA-U5-Q1 | no | Which of the following condition types are group conditions and are divided among all the  |
| S4620-LA-U5-Q6 | no | The tax procedure is assigned according to country in the basic settings of the Financial  |

#### B-regressions (whole-chunk finds, window-pool loses)
| ID | Token-exact | Question (first 90 chars) |
| --- | --- | --- |
| S4600-LA-U4-Q5 | no | Which of the following options are included in the condition master data? |
| S4610-LA-U4-Q2 | no | You can issue an outbound delivery from two different shipping points. |
| S4610-LA-U5-Q1 | YES | For sales order items which need to be processed in an SAP EWM warehouse, an LE outbound d |
| S4610-LA-U5-Q4 | no | Posting a goods issue requires the picking quantity to equal the delivery quantity . |
| S4620-LA-U1-Q2 | no | What is controlled by the condition type? |
| S4620-LA-U2-Q1 | no | Which of the following provides a method to modify the standard pricing logic to meet uniq |
| S4620-LA-U3-Q1 | no | What can you do for or with a condition record? |
| S4620-LA-U3-Q2 | no | You can create new pricing condition records today for next year. |

## Verdicts

### Verdict 1 — Truncation (A vs B)
**CLEAR WIN for embeddings.** B@1 − A@1 = +12.7 pp (≥ 10 pp threshold). Concept regression resolved (+1.9 pp). The v4 borderline result was a truncation artifact from bge-small's 512-token limit. Long-context whole-chunk embeddings outperform TF-IDF clearly.

### Verdict 2 — P3 Granularity (B vs C)
**NON-CONCLUSIVE (B ≈ C).** C@1 − B@1 = +3.0 pp. Window-pooling neither helps nor hurts materially at this gold granularity. Unit-level gold is indulgent — B≈C here does NOT rule out P3. Recommended next step: build lesson-level gold (Stage 1) and repeat B vs C.

## How to Run

```bash
cd 'c:/Users/aranu/Desktop/IA/Chunking'
# Full probe (all 5 docs, all 3 retrievers):
python3 eval/granularity_probe.py
# Single doc, single retriever (via score.py):
python3 eval/score.py --src S4620 --retriever semantic_long
python3 eval/score.py --src S4620 --retriever semantic_window
# Force index rebuild:
python3 eval/granularity_probe.py --no-cache  # deletes eval/index/bge-m3* and rebuilds
```

## Limitations
- Gold at **unit level** (indulgent). Lesson-level gold would give tighter B vs C signal.
- First run downloads BAAI/bge-m3 (~1.2 GB). Subsequent runs use cache.
- Window parameters: 400 tokens, stride 300. Not tuned for this corpus.
- Max-pool aggregation is a simple heuristic; mean-pool or learned-pool could differ.