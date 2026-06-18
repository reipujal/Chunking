# Retrieval Eval — S4F30 [semantic_long]
Generated: 2026-06-18
Gold: `eval/gold/S4F30_assessments.json` (offset=6)
Retriever: semantic_long

## Dataset Summary
- Total questions extracted: 7
- Excluded (trivial/unparseable): 1
- Mappable (>=1 gold chunk): 4
- Not mappable (coverage gap): 2

## Global Metrics (mappable questions only)
| recall@1 | recall@3 | recall@5 | recall@10 | MRR |
| --- | --- | --- | --- | --- |
| 100.0% | 100.0% | 100.0% | 100.0% | 1.000 |

## By Area
| Area | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| credit-management | 4 | 100.0% | 100.0% | 1.000 |

## By Chunk Type
| Type | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| concept | 1 | 100.0% | 100.0% | 1.000 |
| configuration | 1 | 100.0% | 100.0% | 1.000 |
| process | 2 | 100.0% | 100.0% | 1.000 |

## Per-Question Results
| ID | Mappable | Gold chunks | recall@1 | recall@5 | MRR | Top-1 retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| S4F30-LA-U2-Q1 | YES | 3 | 100.0% | 100.0% | 1.000 | credit-management-credit-master-data-001 |
| S4F30-LA-U2-Q2 | YES | 1 | 100.0% | 100.0% | 1.000 | credit-management-credit-master-data-001 |
| S4F30-LA-U2-Q3 | YES | 2 | 100.0% | 100.0% | 1.000 | credit-management-credit-master-data-001 |
| S4F30-LA-U2-Q4 | YES | 1 | 100.0% | 100.0% | 1.000 | credit-management-credit-rules-engine-001 |
| S4F30-LA-U2-Q5 | NO | - | - | - | - | - |
| S4F30-LA-U2-Q6 | NO | - | - | - | - | - |

## Coverage Notes
**2 questions not mapped to any chunk:**
- `S4F30-LA-U2-Q5` (Unit 2: Credit Evaluation and Management): _Which master data can be updated automatically per standard configuration when u_
- `S4F30-LA-U2-Q6` (Unit 2: Credit Evaluation and Management): _Which capabilities does the SAP Credit Management application provide to mass ch_

## Limitations
- Gold is at **unit level** (indulgent): any chunk citing any page in the unit qualifies. Recall numbers are optimistic upper bounds.
- Retriever: **semantic_long**. TF-IDF is the lexical floor; semantic is the dense baseline.