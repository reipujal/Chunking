# Retrieval Eval — S4680 [semantic_long]
Generated: 2026-06-17
Gold: `eval/gold/S4680_assessments.json` (offset=6)
Retriever: semantic_long

## Dataset Summary
- Total questions extracted: 57
- Excluded (trivial/unparseable): 26
- Mappable (>=1 gold chunk): 25
- Not mappable (coverage gap): 6

## Global Metrics (mappable questions only)
| recall@1 | recall@3 | recall@5 | recall@10 | MRR |
| --- | --- | --- | --- | --- |
| 56.0% | 72.0% | 80.0% | 96.0% | 0.676 |

## By Area
| Area | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| integration | 8 | 37.5% | 75.0% | 0.576 |
| special-processes | 17 | 64.7% | 82.4% | 0.723 |

## By Chunk Type
| Type | N | recall@1 | recall@5 | MRR |
| --- | --- | --- | --- | --- |
| process | 25 | 56.0% | 80.0% | 0.676 |

## Per-Question Results
| ID | Mappable | Gold chunks | recall@1 | recall@5 | MRR | Top-1 retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| S4680-LA-U1-Q1 | YES | 1 | 0.0% | 0.0% | 0.143 | configuration-delivery-field-determination-001 |
| S4680-LA-U1-Q2 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-third-party-order-processing-001 |
| S4680-LA-U1-Q3 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-third-party-order-processing-001 |
| S4680-LA-U1-Q4 | YES | 1 | 0.0% | 0.0% | 0.111 | master-data-business-partner-master-data-001 |
| S4680-LA-U1-Q7 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-third-party-order-processing-001 |
| S4680-LA-U1-Q9 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-third-party-order-processing-001 |
| S4680-LA-U1-Q12 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-third-party-order-processing-001 |
| S4680-LA-U2-Q7 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-intercompany-sales-process-001 |
| S4680-LA-U2-Q8 | YES | 1 | 0.0% | 100.0% | 0.200 | order-management-sales-monitoring-analytics-001 |
| S4680-LA-U2-Q11 | YES | 1 | 0.0% | 100.0% | 0.500 | integration-stock-transfer-order-cross-company-001 |
| S4680-LA-U3-Q1 | YES | 1 | 100.0% | 100.0% | 1.000 | integration-stock-transfer-order-intra-company-001 |
| S4680-LA-U3-Q2 | YES | 1 | 0.0% | 100.0% | 0.500 | integration-stock-transfer-order-cross-company-001 |
| S4680-LA-U3-Q7 | YES | 1 | 0.0% | 0.0% | 0.000 | configuration-delivery-item-category-001 |
| S4680-LA-U3-Q8 | YES | 1 | 0.0% | 0.0% | 0.111 | configuration-delivery-item-category-001 |
| S4680-LA-U4-Q1 | YES | 1 | 100.0% | 100.0% | 1.000 | integration-stock-transfer-order-cross-company-001 |
| S4680-LA-U4-Q4 | YES | 1 | 0.0% | 100.0% | 0.500 | integration-stock-transfer-order-intra-company-001 |
| S4680-LA-U4-Q5 | YES | 1 | 0.0% | 100.0% | 0.500 | special-processes-intercompany-sales-process-001 |
| S4680-LA-U4-Q6 | YES | 1 | 100.0% | 100.0% | 1.000 | integration-stock-transfer-order-cross-company-001 |
| S4680-LA-U5-Q1 | NO | - | - | - | - | - |
| S4680-LA-U5-Q3 | NO | - | - | - | - | - |
| S4680-LA-U5-Q5 | NO | - | - | - | - | - |
| S4680-LA-U5-Q6 | NO | - | - | - | - | - |
| S4680-LA-U5-Q7 | NO | - | - | - | - | - |
| S4680-LA-U5-Q8 | NO | - | - | - | - | - |
| S4680-LA-U6-Q1 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-advanced-returns-management-001 |
| S4680-LA-U6-Q2 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-advanced-returns-management-001 |
| S4680-LA-U6-Q3 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-advanced-returns-management-001 |
| S4680-LA-U6-Q4 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-advanced-returns-management-001 |
| S4680-LA-U6-Q5 | YES | 1 | 100.0% | 100.0% | 1.000 | special-processes-advanced-returns-management-001 |
| S4680-LA-U6-Q6 | YES | 1 | 0.0% | 100.0% | 0.200 | configuration-delivery-field-determination-001 |
| S4680-LA-U6-Q8 | YES | 1 | 0.0% | 0.0% | 0.143 | order-management-sales-monitoring-analytics-001 |

## Coverage Notes
**6 questions not mapped to any chunk:**
- `S4680-LA-U5-Q1` (Unit 5: Subcontracting): _You often create subcontract orders for a certain material. You do not want to h_
- `S4680-LA-U5-Q3` (Unit 5: Subcontracting): _Subcontracting for MRO (Maintenance, Repair and Overhaul) supports various subco_
- `S4680-LA-U5-Q5` (Unit 5: Subcontracting): _What are some of the characteristics of special stock type O (Subcontracting Sto_
- `S4680-LA-U5-Q6` (Unit 5: Subcontracting): _You want to order a component from another supplier that should then deliver thi_
- `S4680-LA-U5-Q7` (Unit 5: Subcontracting): _What are some of the prerequisites for being able to deliver the components to t_
- `S4680-LA-U5-Q8` (Unit 5: Subcontracting): _What could be a reason why you would need to enter a subsequent adjustment for a_

## Limitations
- Gold is at **unit level** (indulgent): any chunk citing any page in the unit qualifies. Recall numbers are optimistic upper bounds.
- Retriever: **semantic_long**. TF-IDF is the lexical floor; semantic is the dense baseline.