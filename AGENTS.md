# Agent Instructions — SAP SD Knowledge Base

This project uses CLAUDE.md as its authoritative instruction file.

**MANDATORY FIRST STEP**: Before doing anything else, read `CLAUDE.md` in full.
It defines paths, schemas, quality rules, and the provenance constraints that govern all chunk creation.

```
Read: CLAUDE.md
```

## Phase-Based Skill Files

After reading CLAUDE.md, read the skill file that corresponds to your current task phase. Do not skip this step — the skill files contain the bash commands and procedures required for each phase.

| Phase | File to read |
|---|---|
| Classify a document | `docs/skills/1-classify.md` |
| Extract content from PDF | `docs/skills/2-extract.md` |
| Check for duplicate chunks | `docs/skills/3-deduplicate.md` |
| Decide how to split content | `docs/skills/4-chunk.md` |
| Validate chunk + update state | `docs/skills/5-validate-log.md` |
| First chunk this session | `docs/examples.md` (reference examples) |

## Validator

After writing any chunk, run:
```bash
python3 validate_chunks.py chunks/<area>/<slug>-<NNN>.md
```

Zero ERRORs required before updating the index. Warnings are advisory.

## Critical Rules (do not skip)

1. **Provenance**: `transactions` and `tables` fields only contain identifiers that appear literally in the source text or are legibly visible in a rasterized figure. Do not add T-codes or table names from your training data.
2. **Pages**: always use physical PDF page numbers (not footer labels). Detect offset in Step 1.
3. **300-word minimum**: body below 300 words → merge with nearest related chunk.
4. **Cross-references**: plain chunk ID format only — no backticks, no quotes.
5. **Read the back-matter appendix** (see `docs/skills/2-extract.md`) before concluding that `transactions: []` is correct for any SAP course document.
