# Lexical vs Semantic Retrieval Comparison
Generated: 2026-06-16
Model: `BAAI/bge-small-en-v1.5` via sentence-transformers
Corpus: 82 chunks
Truncated chunks (>512 tokens): 82/82

## Pre-Registered Decision Criterion (P3)

Written BEFORE examining results:

**(a) Embeddings adequate** — sem closes >=80% of @1 gap AND resolves S4615 unreachables @10.
**(b) Non-conclusive → refine gold** — both retrievers already high @5, sem uplift @1 < 10 pp,
    AND S4615 unreachables remain. Unit-level gold too coarse to decide P3.
**(c) Granularity bottleneck → P3 justified** — sem leaves substantial @10 misses, especially
    in S4615. Chunk granularity is the constraint, not retriever quality.

**Transversal (hybrid signal):** if regressions concentrate in token-exact queries (T-codes,
table names) -> recommend lexical+semantic hybrid regardless of above branch.

## Global Results — All Docs
| Doc | N | lex@1 | lex@5 | lex@10 | lex-MRR | sem@1 | sem@5 | sem@10 | sem-MRR | hyb@1 | hyb@5 | hyb@10 | hyb-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S4600 | 21 | 57.1% | 85.7% | 95.2% | 0.718 | 61.9% | 81.0% | 90.5% | 0.709 | 71.4% | 85.7% | 90.5% | 0.786 |
| S4605 | 31 | 61.3% | 93.5% | 96.8% | 0.747 | 87.1% | 96.8% | 100.0% | 0.900 | 71.0% | 96.8% | 96.8% | 0.828 |
| S4610 | 26 | 61.5% | 92.3% | 92.3% | 0.727 | 73.1% | 96.2% | 96.2% | 0.833 | 73.1% | 92.3% | 92.3% | 0.821 |
| S4615 | 30 | 70.0% | 83.3% | 90.0% | 0.762 | 73.3% | 93.3% | 93.3% | 0.797 | 66.7% | 90.0% | 93.3% | 0.767 |
| S4620 | 26 | 61.5% | 96.2% | 100.0% | 0.755 | 65.4% | 96.2% | 96.2% | 0.782 | 73.1% | 96.2% | 100.0% | 0.835 |
| **TOTAL** | 134 | **62.3%** | **90.2%** | **94.9%** | **0.742** | **72.2%** | **92.7%** | **95.2%** | **0.804** | **71.0%** | **92.2%** | **94.6%** | **0.807** |

## By Chunk Type (aggregate across all docs)
| Type | N | lex@1 | sem@1 | delta@1 | lex@5 | sem@5 | lex-MRR | sem-MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| concept | 52 | 67.3% | 61.5% | -5.8pp | 88.5% | 86.5% | 0.761 | 0.717 |
| configuration | 44 | 59.1% | 77.3% | +18.2pp | 93.2% | 97.7% | 0.718 | 0.862 |
| process | 38 | 60.5% | 84.2% | +23.7pp | 89.5% | 97.4% | 0.749 | 0.881 |

## Per-Question Diff (@1) — Aggregate
- both_hit:   71 (53.0%)
- sem_fixed:  27 (lexical@1 miss, semantic@1 hit)
- regression: 13 (lexical@1 hit, semantic@1 miss)
- both_miss:  23

### sem_fixed — Semantic recovers where lexical failed
| ID | Token-exact | Question (first 90 chars) |
| --- | --- | --- |
| S4600-LA-U7-Q1 | no | When you want to create follow-up documents of sales orders, you can often do this via col |
| S4600-LA-U7-Q2 | no | To speed up the process of creating billing documents, you can create multiple billing doc |
| S4600-LA-U7-Q3 | no | Apart from efficiency and speed, an additional advantage of collective processing is that  |
| S4600-LA-U10-Q2 | no | Which one of the following options offers a hybrid view for sales orders in which you can  |
| S4605-LA-U2-Q1 | YES | Every sales activity that you undertake in the SAP system is recorded with a sales documen |
| S4605-LA-U4-Q4 | no | In order to cancel an order, you assign an order reason. |
| S4605-LA-U5-Q3 | no | The item category determines if you can change the default incoterms on item level. |
| S4605-LA-U5-Q4 | no | The item category controls whether pricing can be carried out or not. |
| S4605-LA-U6-Q1 | no | Any sales document can be created with reference to any other existing sales document. |
| S4605-LA-U7-Q1 | no | When you save the rush order, the system automatically creates a delivery and prints a doc |
| S4605-LA-U8-Q3 | no | The incompleteness procedure always contain the fields: customer reference, currency, and  |
| S4605-LA-U10-Q1 | no | Which of the following statements on Scheduling agreement is correct? |
| S4605-LA-U10-Q5 | YES | The item category determination for the General value contract (WK1) is done with the help |
| S4610-LA-U1-Q3 | YES | As of SAP S/4HANA 1709, SAP Transportation Management is included in the core. |
| S4610-LA-U4-Q8 | no | If you create an outbound delivery manually, with or without reference to a particular ord |
| S4610-LA-U4-Q10 | YES | As per the RETA rule, the system determines the picking location based on the shipping poi |
| S4610-LA-U5-Q5 | no | It is possible to calculate freight or shipping costs in a sales document and transfer the |
| S4615-LA-U4-Q2 | no | In which of the following ways can you create credit memo requests? |
| S4615-LA-U5-Q2 | no | Which of the following copying control options are available at the item level? |
| S4615-LA-U6-Q1 | no | You want to create an invoice. What options are available? |
| S4615-LA-U6-Q2 | no | You want to create billing documents regularly on specific dates. How do you achieve this? |
| S4620-LA-U1-Q2 | no | What is controlled by the condition type? |
| S4620-LA-U3-Q1 | no | What can you do for or with a condition record? |
| S4620-LA-U3-Q2 | no | You can create new pricing condition records today for next year. |
| S4620-LA-U3-Q3 | YES | What options do you have for the condition record maintenance besides the condition type b |
| S4620-LA-U3-Q4 | no | You can export and import condition record with the help of the manage-price sales app? |
| S4620-LA-U5-Q4 | no | Which condition types are statistical? |

### Regressions — Lexical hits, Semantic misses @1
| ID | Token-exact | Question (first 90 chars) |
| --- | --- | --- |
| S4600-LA-U1-Q1 | no | Which of the following apps gives you a visual overview of complex topics for monitoring o |
| S4600-LA-U4-Q6 | no | If you do not need the master data to be differentiated according to divisions, you have t |
| S4600-LA-U8-Q3 | YES | The material type DIEN is the appropriate choice for service products and simplifies the d |
| S4605-LA-U7-Q2 | no | Which statement is true in the consignment process? |
| S4610-LA-U4-Q1 | no | If the system finds a customer-material information record which contains a plant, this pl |
| S4615-LA-U8-Q4 | no | In Customizing, the billing plan type is determined from the item category by the field re |
| S4615-LA-U10-Q2 | no | When you set up the reference and allocation number in Customizing, what do you need to co |
| S4615-LA-U11-Q1 | YES | SAP S/4HANA is based on Business Rule Framework Plus, and it includes cloud qualities such |
| S4620-LA-U2-Q1 | no | Which of the following provides a method to modify the standard pricing logic to meet uniq |
| S4620-LA-U2-Q4 | no | New fields can be added to the pricing field catalog. |
| S4620-LA-U5-Q2 | no | In customer hierarchies, you can assign price or rebate agreements only to a low-level nod |
| S4620-LA-U5-Q5 | no | Which of the following factors are considered when determining tax rates? |
| S4620-LA-U5-Q6 | no | The tax procedure is assigned according to country in the basic settings of the Financial  |

Token-exact regressions: 2/13 (low)

## S4615 Unreachable Diagnosis
3 question(s) with lex recall@10 = 0:

### S4615-LA-U3-Q1
**Question:** Can you create a billing document which refers simultaneously to an order and a delivery?
**gold_page_span:** [20, 25]
**lex @10:** 0.0 | **sem @1:** 0.0 @5: 0.0 @10: 0.0

**Gold chunk:** `enterprise-structure-billing-organizational-assignment-001` (enterprise-structure/concept)
*Snippet:* # Organizational Unit Assignments for Billing in SAP SD  ## Operational Summary For billing to post correctly to Financial Accounting, the key organizational units — *company code*, *sales organizatio...

**Diagnosis:** Both retrievers miss. Check: chunk anemic / gold_page_span outside all chunk ranges?

### S4615-LA-U3-Q2
**Question:** With reference to which of the following elements will you create an invoice to ensure that goods have already been shipped before you create the billing document?
**gold_page_span:** [20, 25]
**lex @10:** 0.0 | **sem @1:** 0.0 @5: 0.0 @10: 0.0

**Gold chunk:** `enterprise-structure-billing-organizational-assignment-001` (enterprise-structure/concept)
*Snippet:* # Organizational Unit Assignments for Billing in SAP SD  ## Operational Summary For billing to post correctly to Financial Accounting, the key organizational units — *company code*, *sales organizatio...

**Diagnosis:** Both retrievers miss. Check: chunk anemic / gold_page_span outside all chunk ranges?

### S4615-LA-U5-Q1
**Question:** How can you create a billing document?
**gold_page_span:** [40, 48]
**lex @10:** 0.0 | **sem @1:** 0.0 @5: 1.0 @10: 1.0

**Gold chunk:** `configuration-billing-copying-control-001` (configuration/configuration)
*Snippet:* # Copying Control in SAP SD Billing  ## Operational Summary Copying control defines how data flows from a reference document (sales order, delivery, or prior billing document) into the newly created b...

**Gold chunk:** `configuration-billing-data-flow-001` (configuration/concept)
*Snippet:* # Data Flow and Reference Documents in Billing  ## Operational Summary Every billing document (except external transactions) requires a reference document from which it copies data. The rules governin...

**Diagnosis:** Semantic retrieves this chunk (sem@10>0). Lexical failure is vocabulary mismatch.

## Truncation Impact
Model max tokens: 512. All 82/82 chunks
exceed this limit (min 543 tokens, max ~1832 tokens in the corpus).
Sentence-transformers silently truncates at encode time.
Implication: the tail of every chunk is invisible to the semantic retriever.
For long configuration chunks where key T-codes appear late in the body, this may
explain semantic regressions vs lexical (which indexes the full body).

## P3 Verdict

**Data summary:**
- Avg @1 uplift (sem - lex): +9.9 pp (threshold for branch a: >=10 pp)
- Avg @5: lex=90.2%, sem=92.7%
- S4615 unreachables: 3 total; sem resolves: 1
- Token-exact regressions: 2/13

**Verdict: (b) NON-CONCLUSIVE -> REFINE GOLD FIRST. Both retrievers already high @5; semantic uplift @1 is modest (<10 pp); S4615 unreachables persist. The unit-level gold set is too coarse to discriminate retriever quality at the relevant operating point. Recommended next step: build lesson-level gold (Stage 1) before deciding on P3 hierarchical chunking.**

**Transversal:** Token-exact regression rate is low (2/13). Pure semantic retrieval does not show systematic weakness on exact-token queries.

## How to Run
```bash
cd 'c:/Users/aranu/Desktop/IA/Chunking'
# Single doc, single retriever:
python3 eval/score.py --src S4620 --retriever semantic
# Full comparison:
python3 eval/compare.py
```

## Limitations
- Gold at **unit level** (indulgent). Lesson-level gold would give tighter signal.
- bge-small-en-v1.5 truncates all 82 chunks at 512 tokens. Larger model or
  chunking at <=512 tokens would improve semantic recall for long chunks.
- Hybrid RRF uses k=60 (Cormack 2009); not tuned for this corpus.