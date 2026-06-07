# SAP SD Knowledge Base — Chunking Agent

## Project Paths

| Variable | Value |
|---|---|
| **Workspace** | `c:\Users\aranu\Desktop\IA\Chunking` |
| **Source PDFs** | `c:\Users\aranu\Desktop\IA\Chunking\docu sap` |
| **Chunks output** | `c:\Users\aranu\Desktop\IA\Chunking\chunks\` |
| **Validator** | `python3 validate_chunks.py` |
| **Preferred shell** | PowerShell (Windows) — use Bash tool for POSIX commands |

> Working directory is always the workspace. All `chunks/` paths are workspace-relative.

---

## Placeholder Convention

- `[name]`, `[start]`, `[end]`, `[page]` — **bash values**: substitute before executing. `[start]` → `45`
- `{area}`, `{slug}`, `{NNN}` in bash — **shell variables**: assign first (`AREA=shipping`), then use `$AREA`
- `{field}` inside Python heredocs (`<< 'PY'`) — **Python variables via os.environ**: do not substitute

Executing a literal placeholder without substituting causes incorrect results. Always verify before running.

---

## Mandatory Session Startup

Run in order. Do not skip any step.

### 1. Filesystem Orientation

```bash
pwd && ls -la
# Compact log: status lines and next-pending markers only
grep -E "^## 20|Status:|Next pending" chunks/_processing_log.md 2>/dev/null | tail -20 || echo "Log empty"
cat chunks/_index.md 2>/dev/null | head -5 || echo "Index empty"
```

### 2. Locate Source Folder

The source folder is confirmed: **`docu sap`** (workspace-relative).

At the start of a new session, if `chunks/_project_state.md` exists:

```bash
python3 -c "
import yaml
state = yaml.safe_load(open('chunks/_project_state.md'))
print('Previous SOURCE_ROOT:', state.get('source_root'))
print('Confirmed on:', state.get('confirmed_at'))
" 2>/dev/null || grep "source_root:" chunks/_project_state.md
```

Show the stored SOURCE_ROOT, propose reusing it, wait for explicit confirmation.

```bash
# Only after confirmation:
SOURCE_ROOT="[path confirmed by user]"
[ -d "$SOURCE_ROOT" ] || { echo "ERROR: path not resolvable — use forward slashes"; exit 1; }
mkdir -p chunks
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md
printf "source_root: '%s'\nconfirmed_at: '%s'\n" "$SOURCE_ROOT" "$(date +%Y-%m-%d)" > chunks/_project_state.md
cat chunks/_project_state.md
```

### 3. Verify Tools

```bash
for tool in pdfinfo pdftotext pdffonts; do
  command -v "$tool" >/dev/null 2>&1 && echo "OK: $tool" || echo "MISSING: $tool"
done
command -v pdftoppm >/dev/null 2>&1 && echo "OK: pdftoppm" || echo "OPTIONAL MISSING: pdftoppm"
```

If `pdfinfo`, `pdftotext`, or `pdffonts` are missing: stop and explain.

### 4. Inventory Sources

```bash
find "$SOURCE_ROOT" -type f -iname "*.pdf" | sed "s|$SOURCE_ROOT/||" | sort
find "$SOURCE_ROOT" -type f -iname "*.pdf" | wc -l
```

### 5. Present Proposal

Present: PDFs found, which are already processed, one concrete proposal. Wait for confirmation.

---

## Absolute Rules

**Reading allowed:** `$SOURCE_ROOT`, `chunks/`, `/tmp/` (agent temporaries only)
**Writing allowed:** `chunks/`, `/tmp/` (temporaries only)

**Prohibited:**
- Modifying, moving, renaming, or deleting source documents
- Overwriting existing chunks without explicit confirmation
- Inventing content not supported by the source
- Copying extensive verbatim text from SAP documentation
- Creating duplicate chunks on the same topic
- Writing final outputs outside `chunks/`

---

## Output Structure

```bash
for area in enterprise-structure master-data order-management pricing shipping billing credit-management configuration integration special-processes; do
  mkdir -p "chunks/$area"
done
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md
```

---

## Document Priority

**High:** S4600, S4601, S4605, S4610, S4615, S4620, S4650, S4680, SD-Shipment.pdf, Variant Configuration with SAP, SAP FI-MM-SD INTEGRATION, Transportation Management with SAP TM

**Medium:** S4F30, TSCM60/62 (mark `sap_release: "ECC 6.0"`), Process diagrams (Type B: BD6, BDD, BKA…)

**Low:** __SAP SD.pdf, SD-User Manual, sap_sd_tutorial, Sales and Distribution in SAP ERP Practical Guide

**Skip by default:** certification questions, dumps, sample questions, pdfcoffee certification

---

## Phase Navigation — Read the Skill File Before Each Step

Before executing any step, read the corresponding skill file:

| Step | Skill file | When to read |
|---|---|---|
| 1 — Classify | `docs/skills/1-classify.md` | Before classifying a new document |
| 2 — Extract | `docs/skills/2-extract.md` | Before extracting any block |
| 3 — Deduplicate | `docs/skills/3-deduplicate.md` | Before deciding to create/update a chunk |
| 4 — Chunk | `docs/skills/4-chunk.md` | Before presenting the chunk plan to the user |
| 5 — Write | (this file — see below) | Rules are here in the nucleus |
| 6+7 — Validate & Log | `docs/skills/5-validate-log.md` | After writing each chunk and before closing a document |
| Examples | `docs/examples.md` | At the start of Step 5, if this is your first chunk this session |

---

## Step 5 — Write the Chunk

### ID and Path Convention

```
Physical path:  chunks/{area}/{slug}-{NNN}.md
Logical ID:     {area}-{slug}-{NNN}

Examples:
  chunks/shipping/delivery-creation-individual-001.md  →  shipping-delivery-creation-individual-001
  chunks/pricing/condition-types-001.md                →  pricing-condition-types-001
```

The ID never contains `/`. The area in the ID always matches the folder. Check the index before assigning the sequential number.

### Mandatory Frontmatter

```yaml
---
schema_version: 1
id: {area}-{slug}-{NNN}
title: "[Descriptive title]"
area: [enterprise-structure|master-data|order-management|pricing|
       shipping|billing|credit-management|configuration|
       integration|special-processes]
process_tags: [order-to-cash, delivery-processing]
chunk_type: [concept|process|configuration|transaction|integration]
sap_release: [S/4HANA 2020|ECC 6.0|generic|not specified]
sources:
  - file: "[exact PDF name]"
    relative_path: "[relative path from SOURCE_ROOT]"
    pages: "[N-M]"       # always a quoted string; physical PDF page numbers (not footer labels)
    source_type: "[A|B|C|D]"
    role: "[primary|secondary]"
transactions: []         # EXTRACTION FIELD — see Provenance Rule below
tables: []               # EXTRACTION FIELD — see Provenance Rule below
aliases:
  - english term
  - spanish term
  - natural query variant
level: [functional|technical|both]
status: draft
quality: [high|medium|low]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

### Valid Values

| Field | Valid values |
|---|---|
| area | enterprise-structure, master-data, order-management, pricing, shipping, billing, credit-management, configuration, integration, special-processes |
| chunk_type | concept, process, configuration, transaction, integration |
| sap_release | S/4HANA 2020, ECC 6.0, generic, not specified |
| level | functional, technical, both |
| status | draft, reviewed, validated, deprecated |
| quality | high, medium, low |
| source_type | A, B, C, D |
| role | primary, secondary |

**process_tags valid values:**
`order-to-cash, delivery-processing, billing, pricing, returns, credit-management, transportation, consignment, third-party, free-of-charge, complaints, credit-memo, debit-memo, invoice-correction, make-to-order, stock-transfer, intercompany, none`

Use **differentiating tags**, not just the area generic. A billing credit memo chunk → `[billing, credit-memo]`, not just `[billing]`.

### Quality Criteria

**high**: reliable source (Type A or D), exact pages identified, complete content, no inferences. For Type B: only if visual flow is unambiguous and all T-codes legibly readable.

**medium**: reliable but partial; Type B by default; minor inference required; requires functional validation. Caps to `medium` if: any `<!-- inferred -->` comment present, provenance warning raised, page range not fully read.

**low**: community source (Type C); OCR issues; incomplete content; unresolved contradiction.

`quality: high` is **earned, not default.** Uniform `high` across a large batch is a calibration smell — re-examine each chunk independently.

**sap_release notes:** `not specified` → mark `quality: medium` at minimum. Physical page offset must be detected once per document (see `docs/skills/1-classify.md`) and recorded in the log.

### Content Sections by chunk_type

**process:** Operational Summary · Questions This Chunk Answers · When It Applies and Context · Process Flow (numbered steps with T-codes) · Conditions and Restrictions · Common Errors (Symptom → Cause → Solution) · Cross-References

**configuration:** Operational Summary · Questions This Chunk Answers · What This Configuration Controls · SPRO Path or Direct T-code · Key Parameters (table: Field | Description | Typical Values) · Configuration Impact · Common Configuration Errors · Cross-References

**concept:** Operational Summary · Questions This Chunk Answers · Definition · Purpose in the SD Process · Structure and Variants · Relationship with Other SAP SD Objects · Cross-References

**transaction:** Operational Summary · Questions This Chunk Answers · When to Use This Transaction · Affected Business Object · Key Fields on the Main Screen (table) · Typical Usage Flow · Alternatives and Variants · Restrictions · Common Errors · Cross-References

**integration:** Operational Summary · Questions This Chunk Answers · What It Integrates · Involved Modules or Systems · Affected SAP Objects · Data Flow (table: Source | Object/Data | Destination | When) · Relevant Configuration Points · Functional Impact · Common Integration Errors · Cross-References

### Writing Rules

- Your own words. Do not copy text from the PDF.
- SAP terms in English in **italics** in the body. Spanish equivalents in `aliases`.
- Be specific: "The *selection date* determines which *schedule lines* are included" — not "the date is important."
- Do not invent. If the source does not mention it, do not include it.
- Omit sections with no source content — **except `Cross-References`, which is mandatory.**
- Every chunk must start with a `# Title` H1 heading matching the frontmatter title.
- Body minimum: **300 words**. Under 300 words → merge with the nearest related topic.

### Aliases (minimum 4 per chunk)
At least 2 in Spanish, at least 1 natural query variant (how a consultant would search, not just the SAP term). Sparse aliases defeat RAG recall.

### Questions This Chunk Answers (minimum 4)
Each must cover a **distinct** search intent. "What is X?" and "How is X defined?" count as one question, not two.

### Cross-References (mandatory)
Every chunk ends with `## Cross-References`. Write at least one: `Prior step:`, `Next step:`, or `See also:` pointing to real chunk IDs. If no related chunk exists yet, write `See also: None identified yet`.

**Format**: plain chunk ID, no backticks, no quotes, no markdown link syntax.
- Correct: `See also: billing-invoice-list-001`
- Wrong: `` See also: `billing-invoice-list-001` ``

### Provenance Rule — EXTRACTION FIELDS (most common failure mode)

`transactions` and `tables` record what the **source text literally contains** — never what a consultant would know is relevant.

- **`transactions`**: include a T-code only if the exact token appears in the extracted text or is legibly visible in a rasterized figure. Functional prose ("Create Outbound Delivery") is **not** a T-code.
- **`tables`**: include only if the exact all-caps token is explicitly presented as a database table in the source.
- **Default is empty.** `transactions: []` and `tables: []` are correct for most S46xx conceptual material. An empty field is not a defect.
- **If relevant but not in the source**: add a comment in the body — `<!-- inferred transaction, pending validation: VL06O -->` — never put it in the field.
- **Self-check**: for each token you are about to list, can you point to the exact line of extracted text it came from? If not, it goes in a comment.

**Two failure modes — guard both:**
1. *Over-extraction*: listing a correct-but-unsourced identifier → remove or move to `<!-- inferred -->`.
2. *Under-extraction*: the source names a T-code (often in the back-matter appendix) but the field is left empty → populate from the source.

---

## Session Limit

**First two sessions (calibration):** max one logical unit or 5 chunks — stop and request validation.

**After calibration:** max one complete document, or one logical block in documents >300 pages. Always record the next pending page in the log.

**End-of-session summary:**
```
Chunks created/updated: [id] → [path]
Pending validation: [what to review]
Next recommendation: [concrete proposal]
```

---

## Project Context

Goal: RAG system for a functional SAP SD consultant.
Quality over speed. 20 excellent chunks > 200 mediocre ones.
Do not generate chunks without exact source and pages.
When uncertain between two reasonable options, propose both and wait for confirmation.

**Provenance over completeness.** A chunk that omits a T-code because the source didn't name it is *correct*. A chunk that adds a T-code the source didn't name is *wrong*, even if the T-code is real and on-topic.
