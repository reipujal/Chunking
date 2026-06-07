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

**Folder convention:**
- `$SOURCE_ROOT/` — PDFs pending processing (root only, not subdirectories)
- `$SOURCE_ROOT/processed/` — PDFs already processed; do not reprocess unless explicitly asked

```bash
echo "=== PENDING (root) ===" && find "$SOURCE_ROOT" -maxdepth 1 -iname "*.pdf" | sed "s|$SOURCE_ROOT/||" | sort
echo "=== PROCESSED ===" && find "$SOURCE_ROOT/processed" -iname "*.pdf" 2>/dev/null | sed "s|$SOURCE_ROOT/||" | sort
echo "=== TOTAL ===" && find "$SOURCE_ROOT" -iname "*.pdf" | wc -l
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

## Phase Navigation

| Step | Where rules live | When to read |
|---|---|---|
| 1 — Classify | `docs/skills/1-classify.md` | Before classifying a new document |
| 2 — Extract | `docs/skills/2-extract.md` | Before extracting any block |
| 3 — Deduplicate | **This file — see below** | Rules are in the nucleus (short enough) |
| 4 — Decide how to chunk | **This file — see below** | Rules are in the nucleus (short enough) |
| 5 — Write the chunk | **This file — see below** | Rules are in the nucleus |
| 6+7 — Validate & Log | `docs/skills/5-validate-log.md` | After writing each chunk and before closing a document |
| Examples | `docs/examples.md` | First chunk of a new session — read before writing |

---

## Step 3 — Detect Duplicates and Manage SAP Versions

Search terms must be specific to the topic. Use T-codes, tables, SAP terms in English, Spanish aliases, and business objects from the source.

> The T-codes/tables in the examples below are **search seeds**, not a checklist for the new chunk's frontmatter. Provenance rules govern what goes in the fields.

```bash
grep -RniE "TERM1|TERM2|TCODE|TABLE|spanish_alias" chunks/ --include="*.md" || true
```

**Example — Pricing:** `grep -RniE "pricing procedure|esquema de precios|V/08|VK11|KONV|KONP" chunks/ --include="*.md"`

**Example — Delivery:** `grep -RniE "outbound delivery|entrega de salida|VL01N|VL10E|LIKP|LIPS" chunks/ --include="*.md"`

**Case 1 — Same topic, same version, different source**: present an update plan, wait for confirmation, then update + add source to `sources` array.

**Case 2 — Same topic, different SAP versions**: functionally significant → two chunks with `## Differences from [version]`. Cosmetic only → single chunk `sap_release: generic` + `## Version Notes`. Unknown → separate (safer).

**Case 3 — Contradictory sources**: Type A > B, C, D. Between two Type A: more recent wins. Document in log.

**Case 3b — Internal factual conflict within a single chunk**: when the same chunk uses a SAP document type token (order type, delivery type, billing type) inconsistently — e.g., using the order type abbreviation where the billing type should appear — verify the correct values in the source before writing. SAP document types have distinct roles: order type (creates the sales order) ≠ delivery type (creates the delivery) ≠ billing type (creates the billing document). They may share an abbreviation (e.g., BV for both delivery type and billing type in cash sales) but must be named in the correct functional context.

**Case 4 — Pure duplicate**: skip. Log: "skipped — duplicate of [id]."

**Golden rule**: one concept = one chunk per SAP version. A consultant must not find the same topic spread across multiple chunks.

**Search by business process name, not only T-codes.** When the new topic is a business process (cash sale, rush order, consignment, returns, etc.), search aliases AND titles in addition to T-codes:

```bash
grep -RniE "cash.sale|venta.al.contado|rush.order|pedido.urgente|BUSINESS_PROCESS_NAME" chunks/ --include="*.md" || true
```

Overlap detected → apply the relevant Case above before creating a new chunk.

---

## Step 4 — Decide How to Chunk

**Core principle**: a chunk answers a concrete functional search intent without needing any other chunk.

**Create a new chunk when**: business process changes (Delivery Creation ≠ Goods Issue) · audience changes (functional vs. SPRO config) · customizing area changes · topic exceeds 1500 words.

**Group in one chunk when**: content is inseparable conceptually · body would be under 300 words even with full extraction (300w is the hard floor) · only transaction lists with no functional context.

**Workshop and exercise chapters**: do NOT create a standalone workshop chunk covering multiple unrelated business processes. Instead, extract the useful application context from each scenario and merge it into the existing chunk for that process. If no chunk exists for the process yet and the content exceeds 300 words standalone, create a proper process or configuration chunk. A chunk titled "Workshop scenarios: A, B, and C" is always wrong.

**Before writing — present plan to user:**
```
Section: [Unit N — Title] (p. X-Y)
Chunks identified:
  1. area/slug-001  |  type: process  |  p. 15-28  |  "How is X done?"
  2. area/slug-001  |  type: concept  |  p. 12-14  |  "What is X?"
Proceed?
```
Wait for explicit confirmation before writing anything to disk.

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
    relative_path: "[relative path from SOURCE_ROOT]"   # use forward slashes; prefix with "processed/" if the PDF is already in SOURCE_ROOT/processed/
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

**process_tags valid values** (canonical list — must stay in sync with `VALID_TAGS` in `validate_chunks.py`):
`order-to-cash, delivery-processing, billing, pricing, returns, credit-management, transportation, consignment, third-party, free-of-charge, complaints, credit-memo, debit-memo, invoice-correction, make-to-order, stock-transfer, intercompany, billing-plans, invoice-list, pro-forma, none`

Use **differentiating tags**, not just the area generic. A billing credit memo chunk → `[billing, credit-memo]`, not just `[billing]`.

**Exception — generic billing infrastructure chunks**: chunks covering billing document structure, billing creation methods, billing FI integration, or technical billing tables have no matching sub-tag in the valid list. For these, `[billing, order-to-cash]` is correct and complete — the validator will not warn. Do not force-fit an incorrect sub-tag.

### Quality Criteria

**high**: reliable source (Type A or D), exact pages identified, complete content, no inferences, **and body density ≥ 100 words/page** (buffer above the 80 w/p validator threshold). For Type B: only if visual flow is unambiguous and all T-codes legibly readable.

**medium**: reliable but partial; Type B by default; minor inference required; requires functional validation. Caps to `medium` if: any `<!-- inferred -->` comment present, provenance warning raised, page range not fully read, **or density < 80 w/p** (the validator enforces this as an error).

**low**: community source (Type C); OCR issues; incomplete content; unresolved contradiction.

`quality: high` is **earned, not default.** Uniform `high` across a large batch is a calibration smell — re-examine each chunk independently.

**Density check before finalizing quality.** After writing the body, calculate `word_count / page_count`:
- ≥ 100 w/p → `quality: high` is eligible (if other criteria are met)
- 80–99 w/p → `quality: medium`, no exceptions. Attempt expansion — if density reaches ≥ 100 after expansion, upgrade to `high`. If not, `medium` is final.
- < 80 w/p → `quality: medium` mandatory; re-read source pages using rasterization (see below)

**Rasterization protocol for low-density pages.** When density < 100 w/p, re-read the exact page range before accepting the chunk:
```bash
PAGES_START=[physical_start] && PAGES_END=[physical_end]
pdftoppm -r 200 -f $PAGES_START -l $PAGES_END "docu sap/processed/[filename].pdf" /tmp/chunk_pages
# Examine each /tmp/chunk_pages-*.ppm visually:
# - Extract text from tables row by row (field | value | description)
# - Describe process diagrams (box → arrow → box → decision → ...)
# - Extract exercise questions and their correct answers (functional information)
# - Extract figure captions and legends
```
Re-extract content and expand the chunk body. Only accept density < 80 w/p after rasterization confirms the pages are diagram-only with no extractable text.

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
- When **modifying an existing chunk** (adding cross-refs, correcting metadata, expanding content): always update `last_updated` to today's date.
- **Active voice, no source attribution in body**: write "The *selection date* determines…" not "The source states that the selection date determines…". Provenance is captured in the frontmatter — the body speaks in the present tense as a reference document, not as a summary of what a course says.
- **SPRO section when T-code not in source**: write `Not stated in source.` (5 words) on a single line. Do NOT write a paragraph explaining why no T-code was found. If the IMG path is inferrable from context, add it on a second line: `Navigate via IMG: [path].`
- **Every question listed in "Questions This Chunk Answers" must be answered explicitly in the chunk body.** If the source does not cover the answer, do not list the question.

### Aliases (minimum 4 per chunk)
At least 2 in Spanish, at least 1 natural query variant (how a consultant would search, not just the SAP term). Sparse aliases defeat RAG recall.

**Alias specificity rule**: do NOT include aliases that are so generic they would match dozens of chunks (e.g., "plant", "material", "company code", "sales order", "factura"). Every alias should be specific enough that, if a user searches for it, this chunk is the right result — not one of 20. Bad: `- plant`. Good: `- delivering plant determination`, `- delivering plant EWM`.

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

## Cadencia de Auditorías

Ejecutar `/audit-board docs/audit/audit_board_profile.md` ante cualquiera de estos triggers.
**No esperar a que el usuario lo pida** — proponer la ejecución cuando se cumple alguno.

| Trigger | Tier |
|---------|------|
| Tras cada documento procesado | Quick (ROL 2, 4, 6, 10) |
| ≥ 3 documentos nuevos o mensual | Standard (ROL 1, 2, 4, 5, 6, 7, 9, 10) |
| Trimestral o antes de integrar corpus en RAG de producción | Full (ROL 1–12 + síntesis) |

Antes de ejecutar: actualizar `docs/audit/audit_context_shared.md` con el estado actual.

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
