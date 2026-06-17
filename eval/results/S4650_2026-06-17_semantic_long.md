# Retrieval Eval — S4650 [semantic_long]
Generated: 2026-06-17
Gold: `eval/gold/S4650_assessments.json` (offset=6)
Retriever: semantic_long

## Dataset Summary
- Total questions extracted: 27
- Excluded (trivial/unparseable): 0
- Mappable (>=1 gold chunk): 14
- Not mappable (coverage gap): 13

## Global Metrics (mappable questions only)
| recall@1 | recall@3 | recall@5 | recall@10 | MRR |
| --- | --- | --- | --- | --- |
| 50.0% | 71.4% | 78.6% | 100.0% | 0.646 |

## By Area
| Area | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| configuration | 12 | 50.0% | 83.3% | 0.656 |
| enterprise-structure | 2 | 50.0% | 50.0% | 0.583 |

## By Chunk Type
| Type | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| concept | 2 | 50.0% | 50.0% | 0.583 |
| configuration | 12 | 50.0% | 83.3% | 0.656 |

## Per-Question Results
| ID | Mappable | Gold chunks | recall@1 | recall@5 | MRR | Top-1 retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| S4650-LA-U1-Q1 | YES | 1 | 0.0% | 0.0% | 0.167 | enterprise-structure-sales-distribution-enterprise-structure-001 |
| S4650-LA-U1-Q2 | YES | 1 | 100.0% | 100.0% | 1.000 | enterprise-structure-shared-master-data-cross-division-001 |
| S4650-LA-U2-Q1 | NO | - | - | - | - | - |
| S4650-LA-U2-Q2 | NO | - | - | - | - | - |
| S4650-LA-U2-Q3 | NO | - | - | - | - | - |
| S4650-LA-U2-Q4 | NO | - | - | - | - | - |
| S4650-LA-U3-Q1 | YES | 2 | 0.0% | 0.0% | 0.125 | order-management-sales-monitoring-analytics-001 |
| S4650-LA-U3-Q2 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-text-sources-sd-001 |
| S4650-LA-U3-Q3 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-text-control-determination-001 |
| S4650-LA-U3-Q4 | YES | 2 | 0.0% | 100.0% | 0.250 | configuration-sales-copying-control-001 |
| S4650-LA-U3-Q5 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-text-control-determination-001 |
| S4650-LA-U4-Q1 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-output-determination-sd-001 |
| S4650-LA-U4-Q2 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-output-determination-sd-001 |
| S4650-LA-U4-Q3 | YES | 2 | 0.0% | 100.0% | 0.333 | pricing-condition-technique-overview-001 |
| S4650-LA-U4-Q4 | YES | 2 | 100.0% | 100.0% | 1.000 | configuration-output-management-s4hana-001 |
| S4650-LA-U4-Q5 | YES | 2 | 0.0% | 0.0% | 0.167 | order-management-sales-order-special-features-001 |
| S4650-LA-U4-Q6 | YES | 2 | 0.0% | 100.0% | 0.500 | configuration-billing-output-management-brfplus-001 |
| S4650-LA-U4-Q7 | YES | 2 | 0.0% | 100.0% | 0.500 | configuration-billing-output-management-brfplus-001 |
| S4650-LA-U5-Q1 | NO | - | - | - | - | - |
| S4650-LA-U5-Q2 | NO | - | - | - | - | - |
| S4650-LA-U5-Q3 | NO | - | - | - | - | - |
| S4650-LA-U5-Q4 | NO | - | - | - | - | - |
| S4650-LA-U5-Q5 | NO | - | - | - | - | - |
| S4650-LA-U5-Q6 | NO | - | - | - | - | - |
| S4650-LA-U5-Q7 | NO | - | - | - | - | - |
| S4650-LA-U5-Q8 | NO | - | - | - | - | - |
| S4650-LA-U5-Q9 | NO | - | - | - | - | - |

## Coverage Notes
**13 questions not mapped to any chunk:**
- `S4650-LA-U2-Q1` (Unit 2: Copy Control): _Which of the following levels are used in copying control for sales documents?_
- `S4650-LA-U2-Q2` (Unit 2: Copy Control): _Which of the following options can be customized in the copying control at the i_
- `S4650-LA-U2-Q3` (Unit 2: Copy Control): _Which of the following options do you have in the details of the header level co_
- `S4650-LA-U2-Q4` (Unit 2: Copy Control): _Which of the following options do you have in the details of the schedule line l_
- `S4650-LA-U5-Q1` (Unit 5: Enhancements and Modifications): _Which of the following objects belong to enhancement technology?_
- `S4650-LA-U5-Q2` (Unit 5: Enhancements and Modifications): _A BAdI (Business Add-In) is a defined section in source code that SAP provides t_
- `S4650-LA-U5-Q3` (Unit 5: Enhancements and Modifications): _Which of the following functions in Sales and Distribution use the condition tec_
- `S4650-LA-U5-Q4` (Unit 5: Enhancements and Modifications): _You can find reserve fields in the master data objects of the customer master an_
- `S4650-LA-U5-Q5` (Unit 5: Enhancements and Modifications): _In material master field selection, which are valid statuses that can be set for_
- `S4650-LA-U5-Q6` (Unit 5: Enhancements and Modifications): _Which factors can influence the status of fields in field selection in material _
- `S4650-LA-U5-Q7` (Unit 5: Enhancements and Modifications): _For which of the following functions can you create and process routines using t_
- `S4650-LA-U5-Q8` (Unit 5: Enhancements and Modifications): _An SAP enhancement can be reused several times in one and the same customer enha_
- `S4650-LA-U5-Q9` (Unit 5: Enhancements and Modifications): _Which of the following statements are true about Business Transaction Events (BT_

## Limitations
- Gold is at **unit level** (indulgent): any chunk citing any page in the unit qualifies. Recall numbers are optimistic upper bounds.
- Retriever: **semantic_long**. TF-IDF is the lexical floor; semantic is the dense baseline.