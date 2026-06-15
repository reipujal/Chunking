# Agent Instructions — SAP SD Knowledge Base

## Mandatory first step

Before doing anything else in this repository, read the file `CLAUDE.md` in full. It defines paths, schemas, quality rules, and the provenance constraints that govern all chunk creation. Do not skip this step.

## Phase-based skill files

After reading `CLAUDE.md`, read the skill file that corresponds to your current task phase before executing that phase. Each file contains the bash commands and procedures required.

| Phase | File |
|---|---|
| Classify a document | `docs/skills/1-classify.md` |
| Extract content from PDF | `docs/skills/2-extract.md` |
| Check duplicates + decide chunking | `CLAUDE.md` (Steps 3 and 4 are in the nucleus) |
| Validate chunk + update state | `docs/skills/5-validate-log.md` |
| Close a document (coverage gate) | `docs/skills/6-coverage-review.md` |
| First chunk of a new session | also read `docs/examples.md` |

## Validator

After writing any chunk file, run:

```bash
python3 validate_chunks.py chunks/<area>/<slug>-<NNN>.md
```

Zero ERRORs required before updating the index. Warnings are advisory.

## Enforcement / setup

The chunk validator (`validate_chunks.py`) is wired as a **blocking gate** in two layers:

| Layer | Mechanism | Bypasses |
|---|---|---|
| Local pre-commit hook | `.githooks/pre-commit` | `git commit --no-verify` (logs bypass, CI still catches it) |
| GitHub Actions CI | `.github/workflows/validate.yml` — runs on every push and PR | None (machine-independent backstop) |

**Bootstrap (one-time per clone):**

```bash
git config core.hooksPath .githooks
```

`core.hooksPath` is local git config — not versioned. Every new clone must run this once. CI does not require it (the workflow calls `python validate_chunks.py` directly).

**Contract:** errors → exit 1 → commit blocked. Warnings → advisory only (AGENTS.md contract unchanged).

---

## Five rules you must not skip

1. **Provenance**: `transactions` and `tables` fields only contain identifiers that appear literally in the source text or are legibly visible in a rasterized figure. Never add from training knowledge.
2. **Physical pages**: always use physical PDF page numbers, not footer labels. Detect the offset in Step 1 (see `docs/skills/1-classify.md`).
3. **300-word minimum**: body below 300 words — merge with the nearest related chunk instead.
4. **Cross-references**: plain chunk ID only — no backticks, no quotes, no markdown link syntax.
5. **Back-matter appendix**: always scan the last 10–15 pages of any SAP course for T-code/table appendices before concluding that `transactions: []` is correct. See `docs/skills/2-extract.md`.
