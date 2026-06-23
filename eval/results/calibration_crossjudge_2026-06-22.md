# Cross-Judge Calibration — 2026-06-22

**Reference judge**: claude-opus-4-8 (Anthropic)
**New judge**: gpt-4.1-mini (provider: openai)
**Generator**: claude-sonnet-4-6 (same for both — responses reused, not re-generated)
**Source**: `faithfulness_full_2026-06-22.json` (positive_results)

## Results

| ID | gf_opus | gf_new | delta |
|---|---|---|---|
| S4600-LA-U1-Q1 | 0.2 | 0.0 | -0.2 |
| S4600-LA-U1-Q2 | 1.0 | 0.0 | -1.0 |
| S4600-LA-U4-Q1 | 0.8 | 0.75 | -0.05 |
| S4600-LA-U4-Q2 | 0.833 | 0.75 | -0.083 |
| S4600-LA-U4-Q3 | 0.0 | 0.0 | 0.0 |
| S4610-LA-U1-Q1 | 0.929 | 0.25 | -0.679 |
| S4610-LA-U1-Q2 | 1.0 | 0.333 | -0.667 |
| S4610-LA-U1-Q3 | 0.0 | 0.0 | 0.0 |
| S4610-LA-U2-Q1 | 0.7 | 0.333 | -0.367 |
| S4610-LA-U2-Q2 | 1.0 | 0.667 | -0.333 |

**Mean delta**: -0.338
**Conclusion**: NO -- |mean_delta| >= 0.15, judges diverge

## Interpretation

- delta = gf_new − gf_opus (positive → new judge is more generous)
- Comparability threshold: |mean_delta| < 0.10 → comparable; > 0.15 → divergent
- Note: individual question deltas may be large; only the mean matters for comparability.