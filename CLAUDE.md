# SAP SD Knowledge Base — Chunking Agent

## Project Paths

| Variable | Value |
|---|---|
| **Workspace** | `c:\Users\aranu\Desktop\IA\Chunking` |
| **Source PDFs** | `c:\Users\aranu\Desktop\IA\Chunking\docu sap` |
| **Chunks output** | `c:\Users\aranu\Desktop\IA\Chunking\chunks\` |
| **Preferred shell** | PowerShell (Windows) — use Bash tool for POSIX commands |

> In bash protocol commands, the working directory is always the workspace.
> All `chunks/` paths are relative to the workspace.

---

## Mandatory Session Startup

Run these steps in order. Do not skip any.

### 1. Filesystem Orientation

```bash
pwd
ls -la
cat chunks/_processing_log.md 2>/dev/null | tail -40 || echo "Log empty"
cat chunks/_index.md 2>/dev/null | head -40 || echo "Index empty"
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
Show the stored SOURCE_ROOT, propose reusing it to the user, and wait for explicit confirmation before proceeding.

```bash
# Only after confirmation:
SOURCE_ROOT="[path confirmed by user]"

[ -d "$SOURCE_ROOT" ] || { echo "ERROR: path not resolvable — use forward slashes (/c/Users/...) not backslashes"; exit 1; }
echo "SOURCE_ROOT: $SOURCE_ROOT"

mkdir -p chunks
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md

printf "source_root: '%s'\nconfirmed_at: '%s'\n" "$SOURCE_ROOT" "$(date +%Y-%m-%d)" > chunks/_project_state.md
echo "SOURCE_ROOT saved to chunks/_project_state.md"
cat chunks/_project_state.md
```

### 3. Verify Tools

```bash
for tool in pdfinfo pdftotext pdffonts; do
  command -v "$tool" >/dev/null 2>&1 && echo "OK: $tool" || echo "MISSING: $tool"
done
command -v pdftoppm >/dev/null 2>&1 && echo "OK: pdftoppm" || echo "OPTIONAL MISSING: pdftoppm"
command -v python3 >/dev/null 2>&1 && echo "OK: python3" || echo "OPTIONAL MISSING: python3"
```

- If `pdfinfo`, `pdftotext`, or `pdffonts` are missing: stop. Explain what is missing and why it is needed.
- If `pdftoppm` is missing: text documents can be processed, but not visual Type B documents.
- If `python3` is missing: the index regeneration script will not be available.

### 4. Inventory Sources

```bash
find "$SOURCE_ROOT" -type f -iname "*.pdf" | sed "s|$SOURCE_ROOT/||" | sort
find "$SOURCE_ROOT" -type f -iname "*.pdf" | wc -l
```

### 5. Present Proposal to User

After the steps above, present:
- How many PDFs are in SOURCE_ROOT and their listing
- Which documents are already processed according to the log
- A concrete proposal: "I propose processing [document] because [reason]. Confirm?"

Do not ask open-ended questions. One specific proposal, wait for confirmation.

---

## Absolute Rules

**Reading allowed:**
- `$SOURCE_ROOT` and its subfolders
- `chunks/`
- `/tmp/` only for agent-generated temporaries

**Writing allowed:**
- `chunks/`
- `/tmp/` only for temporaries

**Prohibited:**
- Modifying, moving, renaming, or deleting source documents
- Overwriting existing chunks without explicit confirmation
- Inventing content not supported by the source
- Copying extensive verbatim text from SAP documentation
- Creating duplicate chunks on the same topic
- Writing final outputs outside `chunks/`

---

## Output Structure

Create directory structure (`mkdir -p` is idempotent — safe in any session):

```bash
for area in enterprise-structure master-data order-management pricing shipping billing credit-management configuration integration special-processes; do
  mkdir -p "chunks/$area"
done
touch chunks/_index.md chunks/_processing_log.md chunks/_source_inventory.md
```

```
chunks/
├── _index.md
├── _processing_log.md
├── _source_inventory.md
├── _project_state.md       ← confirmed SOURCE_ROOT and start date
├── enterprise-structure/
├── master-data/
├── order-management/
├── pricing/
├── shipping/
├── billing/
├── credit-management/
├── configuration/
├── integration/
└── special-processes/
```

---

## Document Priority

### High — Process First
```
S4600_EN_Col17  Business Processes in SAP S4HANA Sales
S4601_EN_Col17  Business Processes in SAP S4HANA Supply Chain Execution
S4605_EN_Col17  Sales Processes in SAP S4HANA Sales
S4610_EN_Col17  Delivery Processing in SAP S4HANA
S4615_EN_Col17  Billing in SAP S4HANA Sales
S4620_EN_Col17  Pricing in SAP S4HANA Sales
S4650_EN_Col17  Cross-Functional Topics in SAP S4HANA Sales
S4680_EN_Col17  Cross-Application Processes in SAP S4HANA Sales and Procurement
SD - Shipment.pdf
Variant Configuration with SAP.pdf
SAP FI-MM-SD INTEGRATION A SPECIAL REPORT
Transportation Management with SAP TM
```

### Medium — Process Second
```
S4F30_EN_Col12 Order to Cash Optimizations
TSCM60, TSCM62 and parts   → mark sap_release: "ECC 6.0"
Process diagrams (Type B): BD6, BDD, BKA, BDA, BKL, BDQ, BJE, BKZ, BD9
```

### Low — Only If Not Duplicate of High Priority
```
__SAP SD.pdf
SD - User Manual.pdf
sap_sd_tutorial / sap-sd-training-tutorial
Sales and Distribution in SAP ERP Practical Guide
```

### Skip by Default (unless explicitly instructed)
```
certification questions / material
dumps / sample certification
pdfcoffee certification
sap-s-4hana-sales-dumps
```

---

## Step 1 — Classify the Document

> ⚠️ **Shell context**: If `$SOURCE_ROOT` is empty (new subprocess), recover it before continuing:
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT not resolvable — confirm with user"; exit 1; }
> ```

```bash
DOC="$SOURCE_ROOT/[name].pdf"

pdfinfo "$DOC"
pdffonts "$DOC" | head -10
pdftotext -f 1 -l 4 "$DOC" - 2>/dev/null | head -120

# Word/page ratio — sample from p.30 to avoid cover, copyright, and TOC
# SAP manuals have 15-20 preambule pages with very low density
pages=$(pdfinfo "$DOC" 2>/dev/null | awk '/^Pages:/{print $2}')
[ -z "$pages" ] && { echo "ERROR: pdfinfo returned no page count — PDF encrypted, damaged, or invalid export"; exit 1; }
sample_start=$(( pages > 30 ? 30 : (pages > 10 ? 10 : 1) ))
sample_end=$(( pages < (sample_start + 15) ? pages : (sample_start + 15) ))
sample_words=$(pdftotext -f "$sample_start" -l "$sample_end" "$DOC" - 2>/dev/null | wc -w)
sample_pages=$(( sample_end - sample_start + 1 ))
echo "Sample ratio (p.$sample_start-$sample_end): $((sample_words / sample_pages)) words/page"
```

| Type | Name | Criterion | Strategy |
|---|---|---|---|
| A | Official SAP course | Prefix S4600-S4680, TSCM60/62; >200 words/page | Extract by chapters/units |
| A* | Mixed document | 80-200 words/page → treat as Type A with visual page detection active | Extract text + rasterize visual pages |
| B | Visual slide deck | "Process Diagrams" in name, or <80 words/page | Rasterize with pdftoppm |
| C | Community manual | "User Manual", "tutorial", "training", BBP | Extract, validate quality first |
| D | Specialized | "Shipment", "Variant Config", "FI-MM-SD", "Transportation" | Same as Type A |
| E | Certification/dumps | "certification", "dumps", "sample questions" | Skip by default |

**Note for HTML→PDF corpus (Edge/Chromium exports):**
`pdfinfo` will show `Producer: Skia/PDF` or another Chromium engine.
In that case, words/page heuristics are indicators, not definitive criteria.
Confirm the type visually by rasterizing 2-3 representative pages before proceeding.
Document the origin in `_source_inventory.md` (Producer from pdfinfo).

Communicate to the user before continuing:
```
Document: [name]
Type: [A/B/C/D/E]
Pages: N
Ratio: N words/page
Extractable text: high/medium/low
Proposal: process [section/range] because [reason]. Confirm?
```

---

## Step 2 — Extract Content

> ⚠️ **Shell context**: If `$SOURCE_ROOT` is empty (new subprocess), recover it before continuing:
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT not resolvable — confirm with user"; exit 1; }
> ```

### Type A, C, D — Text Documents

**Extraction rule**: never more than 30 pages in a single call.
Extracting larger blocks saturates context and degrades chunking decisions
("Lost in the Middle" effect).

**First time with any Type A, C, or D document: map the index**
```bash
pdftotext -f 1 -l 12 "$DOC" - | head -250
```
Identify chapters, titles, and page numbers. Record the map before continuing.
This step does not apply to Type B documents — they have visual structure, not textual.
For Type B, go directly to the rasterization section.

**Extract in blocks of maximum 30 pages**
```bash
pdftotext -layout -f [start] -l [end] "$DOC" /tmp/block.txt
wc -w /tmp/block.txt
head -80 /tmp/block.txt
```

**Noise to ignore:** headers/footers ("© SAP SE", page numbers),
watermarks ("For Internal Use Only"), slide references
("As shown in the figure above").

**If text has broken encoding** (signals: `Ã©`, `â€™`):
```bash
pdftoppm -jpeg -r 150 -f [page] -l [page] "$DOC" /tmp/broken_page
ls /tmp/broken_page-*.jpg
```
If the environment allows visual inspection, read the image.
If not: do not invent content.
Record the page as unprocessed in the log and mark it for later review.
Do not create the chunk until it can be visually reviewed.

### Type B — Visual Slide Decks

```bash
DOC_SLUG="$(basename "$DOC" .pdf | tr ' ' '-' | tr -cd '[:alnum:]-_')"
rm -rf "/tmp/slides-$DOC_SLUG"
mkdir -p "/tmp/slides-$DOC_SLUG"

pages=$(pdfinfo "$DOC" | awk '/^Pages:/ {print $2}')
echo "Total pages: $pages — rasterize in blocks of 30"

pdftoppm -jpeg -r 150 -f [start] -l [end] "$DOC" "/tmp/slides-$DOC_SLUG/page"
ls "/tmp/slides-$DOC_SLUG/"
```

Process one block, analyze the images, extract the knowledge,
then move to the next block. Same principle as text extraction.

If the environment allows visual inspection, read each image extracting:
- Visible SAP transactions
- Key fields in SAP GUI screens
- Superimposed text annotations
- Implicit flow between screens

If visual inspection is not possible: record the document as
`blocked` in `_source_inventory.md` and consult the user.

A Type B document is divided by process or sub-process function,
not by document or slide:
- Do not create one chunk per slide.
- Do not force a single chunk per document.
- Create one chunk per continuous, coherent functional flow.
- If the deck contains multiple distinct processes, create multiple chunks.

Group slides that form a complete operational sub-process into
a single chunk of type `process`.

**Mixed documents (Type A/C/D with visual pages):**

`pdftotext` separates pages with the control character `\f` (form feed).
To detect visual pages within an extracted block, parse that character explicitly:

```bash
pdftotext -layout -f [start] -l [end] "$DOC" /tmp/block.txt

python3 - << 'PY'
import sys
text = open("/tmp/block.txt", encoding="utf-8", errors="replace").read()
pages = [p for p in text.split("\f") if p.strip()]
BUTTON_SET = {"save","cancel","execute","ok","back","enter","help",
              "display","change","create","delete","post","check",
              "continue","exit","refresh","print","previous","next"}
for i, page in enumerate(pages, start=[start]):
    tokens = page.lower().split()
    words = len(tokens)
    all_buttons = len(tokens) > 0 and set(tokens).issubset(BUTTON_SET)
    status = "VISUAL" if (words < 40 or all_buttons) else "text"
    print(f"  Page {i}: {words} words — {status}")
PY
```

If a page appears as VISUAL or contains only button labels:
1. Discard that plain text — do not use it for chunking
2. Note the page number
3. Rasterize only that page:
```bash
pdftoppm -jpeg -r 150 -f [page_number] -l [page_number] "$DOC" /tmp/visual
ls /tmp/visual-*.jpg
```
4. Read the image visually to extract relevant information

Do not rasterize the entire document — only pages that trigger these signals.

---

## Step 3 — Detect Duplicates and Manage SAP Versions

Search terms must be specific to the topic being processed.
Build the search using T-codes, tables, SAP terms in English,
Spanish aliases, and business objects identified in the source:

```bash
grep -RniE "TERM1|TERM2|TCODE|TABLE|spanish_alias" chunks/ --include="*.md" || true
```

Example for a Pricing topic:
```bash
grep -RniE "pricing procedure|esquema de precios|condition type|clase de condicion|access sequence|secuencia de acceso|V/08|VK11|KONV|KONP" chunks/ --include="*.md" || true
```

Example for a Delivery topic:
```bash
grep -RniE "outbound delivery|entrega de salida|\bVL01N\b|\bVL10E\b|\bLIKP\b|\bLIPS\b|shipping point|punto de expedicion" chunks/ --include="*.md" || true
```

### Case 1 — Same Topic, Same SAP Version, Different Source
Do not modify the chunk directly. Present an update plan:

```
Existing chunk: [id]
New source: [file], p. [N-M]
Proposed changes:
  - [section to be expanded or corrected]
  - add source to frontmatter
Confirm update?
```

Only after explicit confirmation: update the chunk, add the source to the
`sources` array, document in the log: "updated with [source]".
Do not create a new chunk.

### Case 2 — Same Topic, Different SAP Versions (S/4HANA vs ECC)

Is the difference functionally significant?
→ Create two separate chunks by version:
  `shipping/goods-issue-s4hana-001.md`  → sap_release: "S/4HANA 2020"
  `shipping/goods-issue-ecc-001.md`     → sap_release: "ECC 6.0"
→ Add a `## Differences from [other version]` section to each.

Is the difference only cosmetic?
→ Single chunk with `sap_release: generic`
→ Add a `## Version Notes` section.

Unknown significance?
→ Create separate chunks by version. Safer than merging.

### Case 3 — Same Version, Contradictory Sources
→ Type A source takes priority over B, C, D.
→ Between two Type A: the more recent takes priority.
→ Document the contradiction in the log.

### Case 4 — Pure Duplicate
→ Skip. Document in the log: "skipped — duplicate of [id]".

**Golden rule**: one concept = one chunk (per SAP version if there are
significant differences). The chunk must be complete: synthesizes all
available sources. A consultant should not find information about the same
topic spread across multiple chunks.

---

## Step 4 — Decide How to Chunk

### Core Principle
A chunk is correct if it can answer a concrete functional search intent
without needing to read any other chunk.

### When to Create a New Chunk
- Change of business process (Delivery Creation ≠ Goods Issue)
- Change of audience: functional concept vs. SPRO configuration
- Change of customizing area (Output Determination ≠ Partner Determination)
- Topic exceeds 1500 words → subdivide by coherent sub-topics

### When to Group in a Single Chunk
- Content that cannot be separated conceptually
- Result would be fewer than 150 words
- Only transaction lists without functional context

### Division Example — Pricing
```
pricing/condition-types-001.md      → what they are, structure, categories
pricing/access-sequences-001.md     → how the system searches for prices
pricing/pricing-procedures-001.md   → calculation schema, routines, V/08
pricing/condition-records-001.md    → where prices are maintained, VK11
```

### Grouping Example — Shipping Point and Loading Point
Related in configuration and usage. One chunk is more useful than two
that require each other.

### Before Writing: Present Plan to User
```
Section: Unit 1 — Delivery Processing (p. 12-67)
Chunks identified:
  1. shipping/delivery-creation-individual-001
     type: process | p. 15-28
     intent: "How is an individual delivery created?"
  2. shipping/delivery-creation-collective-001
     type: process | p. 29-41
     intent: "How are bulk deliveries created with VL10E?"
  3. shipping/delivery-types-concept-001
     type: concept | p. 12-14
     intent: "What delivery types exist in SAP SD?"
Proceed?
```
Wait for confirmation before writing anything to disk.

---

## Step 5 — Write the Chunk

### Language and Terminology
Write in English. SAP official terms appear in italics in the body text.
Include Spanish equivalents in the `aliases` field to improve RAG recall
for Spanish-speaking consultants.

Correct: "The *Pricing Procedure* uses an *Access Sequence* to search
for *Condition Records*."

`aliases` must include both English and Spanish terms:
```yaml
aliases:
  - pricing procedure
  - esquema de precios
  - access sequence
  - secuencia de acceso
  - condition record
  - registro de condición
```

### ID and Path Convention — Critical

```
Physical path:  chunks/{area}/{slug}-{NNN}.md
Logical ID:     {area}-{slug}-{NNN}

Examples:
  Path: chunks/shipping/delivery-creation-individual-001.md
  ID:   shipping-delivery-creation-individual-001

  Path: chunks/pricing/condition-types-001.md
  ID:   pricing-condition-types-001
```

The ID never contains `/`.
The ID always includes the area as prefix.
The area in the ID always matches the folder where the file lives.
Check the index before assigning the sequential number.

### Mandatory Frontmatter Format

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
    pages: "[N-M]"       # CRITICAL: always a quoted string, even single page (e.g., "15" not 15)
    source_type: "[A|B|C|D]"
    role: "[primary|secondary]"
transactions: [VA01, VL01N]
tables: [VBAK, LIKP]
aliases:
  - english term
  - spanish term
  - spanish variant
level: [functional|technical|both]
status: draft
quality: [high|medium|low]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

### Quality Criteria

**high**: reliable source (Type A or D), exact pages identified,
complete content, no contradictions, no significant inferences.
For Type B: only if the visual flow is unambiguous, transactions
and fields are clearly readable, and no functional inferences were made.

**medium**: reliable but partial source; Type B source by default;
minor inference required; requires functional validation.
Default value for Type B unless all `high` criteria are met.

**low**: community source (Type C); OCR issues; incomplete content;
unresolved contradiction; uncertain visual interpretation.

`quality` reflects the net outcome of the chunk: combines source
reliability with content completeness.

All new chunks start with `status: draft`. Full lifecycle:
- `draft`: just created, pending human review
- `reviewed`: validated by user — content correct
- `validated`: verified against a real SAP system or additional source
- `deprecated`: obsolete (SAP version changed, content superseded)

### Note on sap_release

- `S/4HANA 2020`: document explicitly specifies this version
- `ECC 6.0`: document is clearly ECC (TSCM60/62, pre-2015)
- `generic`: concept applies stably to both ECC and S/4HANA without significant functional differences
- `not specified`: source does not indicate version and it cannot be determined — mark `quality: medium` at minimum

### Valid Values for process_tags

```
order-to-cash, delivery-processing, billing, pricing,
returns, credit-management, transportation, consignment,
third-party, free-of-charge, complaints, credit-memo,
debit-memo, invoice-correction, make-to-order,
stock-transfer, intercompany, none
```

### Content Sections by chunk_type

**process:**
```
## Operational Summary
## Questions This Chunk Answers
## When It Applies and Context
## Process Flow  (numbered steps with T-codes)
## Conditions and Restrictions
## Common Errors  (Symptom → Cause → Solution)
## Cross-References
```

**configuration:**
```
## Operational Summary
## Questions This Chunk Answers
## What This Configuration Controls
## SPRO Path or Direct T-code
## Key Parameters  (table: Field | Description | Typical Values)
## Configuration Impact
## Common Configuration Errors
## Cross-References
```

**concept:**
```
## Operational Summary
## Questions This Chunk Answers
## Definition
## Purpose in the SD Process
## Structure and Variants
## Relationship with Other SAP SD Objects
## Cross-References
```

**transaction:**
```
## Operational Summary
## Questions This Chunk Answers
## When to Use This Transaction
## Affected Business Object
## Key Fields on the Main Screen  (table)
## Typical Usage Flow
## Alternatives and Variants
## Restrictions
## Common Errors
## Cross-References
```

**integration:**
```
## Operational Summary
## Questions This Chunk Answers
## What It Integrates
## Involved Modules or Systems
## Affected SAP Objects
## Data Flow  (table: Source | Object/Data | Destination | When)
## Relevant Configuration Points
## Functional Impact
## Common Integration Errors
## Cross-References
```

### Writing Rules
- Your own words. Do not copy text from the PDF.
- SAP terms in English in italics in the body. Spanish equivalents in `aliases`.
- Be specific: "The *selection date* determines which *schedule lines* are included" is useful. "The date is important" is not.
- Do not invent. If the source does not mention it, do not include it.
- Omit sections with no source content. No filler.
- **SAP tables in `tables`**: include only tables that appear explicitly in the source or that the document clearly associates with the described technical object. If a table is relevant but not in the source, annotate it as a comment and mark for validation: `<!-- inferred table, pending validation: VBAK -->`.

---

## Step 6 — Validate Consistency

After writing each chunk and before updating the index.
Assign variables first:

```bash
AREA="shipping"
SLUG="delivery-creation-individual"
NNN="001"
FILE="chunks/$AREA/$SLUG-$NNN.md"
ID="$AREA-$SLUG-$NNN"
```

**Pre-validation — run BEFORE writing the chunk:**
```bash
mkdir -p "chunks/$AREA"

if [ -f "$FILE" ]; then
  echo "WARNING: $FILE already exists — present update plan and wait for confirmation"
  exit 1
fi

matches=$(grep -Rni "^id: ${ID}$" chunks/ --include="*.md" | wc -l)
if [ "$matches" -gt 0 ]; then
  echo "WARNING: ID $ID already exists in $matches chunk(s)"
  grep -Rni "^id: ${ID}$" chunks/ --include="*.md"
fi
```

**Post-validation — run AFTER writing the chunk:**
```bash
ls "$FILE" || { echo "ERROR: $FILE was not written correctly"; exit 1; }

matches=$(grep -Rni "^id: ${ID}$" chunks/ --include="*.md" | wc -l)
if [ "$matches" -ne 1 ]; then
  echo "ERROR: $ID must appear exactly once. Occurrences: $matches"
fi

grep "^area:" "$FILE"
```

**YAML validation (if python3 + pyyaml available):**
```bash
export AREA SLUG NNN
python3 - << 'VALIDATE'
import os, yaml, sys, pathlib

area = os.environ.get("AREA", "")
slug = os.environ.get("SLUG", "")
nnn  = os.environ.get("NNN", "")

if not area or not slug or not nnn:
    sys.exit("ERROR: AREA, SLUG, or NNN not defined in environment")

path = pathlib.Path(f"chunks/{area}/{slug}-{nnn}.md")
if not path.exists():
    sys.exit(f"ERROR: file not found at {path}")
text = path.read_text(encoding="utf-8")

if not text.startswith("---"):
    sys.exit("ERROR: YAML frontmatter missing")

meta = yaml.safe_load(text.split("---", 2)[1])

required = ["schema_version","id","title","area","process_tags",
            "chunk_type","sap_release","sources","transactions",
            "tables","aliases","level","status","quality",
            "created","last_updated"]
for field in required:
    if field not in meta:
        sys.exit(f"ERROR: required field missing: {field}")

valid_areas = {"enterprise-structure","master-data","order-management",
               "pricing","shipping","billing","credit-management",
               "configuration","integration","special-processes"}
valid_types = {"concept","process","configuration","transaction","integration"}
valid_status = {"draft","reviewed","validated","deprecated"}
valid_quality = {"high","medium","low"}
valid_release = {"S/4HANA 2020","ECC 6.0","generic","not specified"}
valid_level = {"functional","technical","both"}
valid_source_type = {"A","B","C","D"}
valid_role = {"primary","secondary"}
valid_tags = {"order-to-cash","delivery-processing","billing","pricing",
              "returns","credit-management","transportation","consignment",
              "third-party","free-of-charge","complaints","credit-memo",
              "debit-memo","invoice-correction","make-to-order",
              "stock-transfer","intercompany","none"}

if meta["area"] not in valid_areas: sys.exit(f"ERROR: invalid area: {meta['area']}")
if meta["chunk_type"] not in valid_types: sys.exit(f"ERROR: invalid chunk_type: {meta['chunk_type']}")
if meta["status"] not in valid_status: sys.exit(f"ERROR: invalid status: {meta['status']}")
if meta["quality"] not in valid_quality: sys.exit(f"ERROR: invalid quality: {meta['quality']}")
if meta["sap_release"] not in valid_release: sys.exit(f"ERROR: invalid sap_release: {meta['sap_release']}")
if meta["level"] not in valid_level: sys.exit(f"ERROR: invalid level: {meta['level']}")

invalid_tags = set(meta.get("process_tags",[])) - valid_tags
if invalid_tags: sys.exit(f"ERROR: invalid process_tags: {invalid_tags}")

for s in meta.get("sources", []):
    for k in ["file","relative_path","pages","source_type","role"]:
        if k not in s:
            sys.exit(f"ERROR: source missing field: {k}")
    if s.get("source_type") not in valid_source_type:
        sys.exit(f"ERROR: invalid source_type: {s.get('source_type')}")
    if s.get("role") not in valid_role:
        sys.exit(f"ERROR: invalid role: {s.get('role')}")
    if not isinstance(s.get("pages",""), str):
        sys.exit(f"ERROR: pages must be a quoted string, not a number: {s.get('pages')}")

print("YAML OK — chunk valid")
VALIDATE
```

If any check fails: fix the chunk before continuing.
Do not update the index with a defective chunk.

---

## Step 7 — Update State

### `_processing_log.md` — append-only, never rewrite

```markdown
## YYYY-MM-DD — [exact PDF name]
- Relative path: [path from SOURCE_ROOT]
- Type: A/B/C/D/E
- Total pages: N
- Processed range: p. X-Y
- Next pending page: p. Z  (or "none — completed")
- Extractable text: high/medium/low
- Encoding issues: [problematic pages, or "none"]
- Chunks created: N
  - [id] → chunks/area/file.md
- Chunks updated:
  - [id] → reason
- Duplicates found and decision:
  - [existing id] → [skipped/merged/separated by SAP version]
- Omitted content: [what and why, or "none"]
- Non-obvious chunking decisions: [decision and justification]
- Status: not started / partial / completed / skipped
```

### `_index.md` — regenerate with script

```bash
python3 << 'PYEOF'
import os, sys
try:
    import yaml
except ImportError:
    print("WARNING: pyyaml not available.")
    print("MANUAL ACTION REQUIRED: add the row directly at the end of chunks/_index.md")
    print("Format: | {id} | chunks/{area}/{slug}-{NNN}.md | {title} | ... |")
    sys.exit(0)

import datetime
chunks_dir = "chunks"
rows = []
for root, _, files in os.walk(chunks_dir):
    for f in sorted(files):
        if not f.endswith(".md") or f.startswith("_"):
            continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        if not content.startswith("---"):
            continue
        try:
            parts = content.split("---", 2)
            meta = yaml.safe_load(parts[1])

            def esc(v):
                return str(v).replace("|", "\\|").replace("\n", " ")

            t_codes = esc(", ".join(str(t) for t in meta.get("transactions", [])))
            sources = meta.get("sources", [])
            src_files = esc(", ".join(s.get("file", "") for s in sources))
            src_pages = esc(", ".join(str(s.get("pages", "")) for s in sources))
            tags = esc(", ".join(str(t) for t in meta.get("process_tags", [])))
            rows.append(
                f"| {meta.get('id','')} "
                f"| {path} "
                f"| {meta.get('title','')} "
                f"| {meta.get('area','')} "
                f"| {meta.get('chunk_type','')} "
                f"| {meta.get('sap_release','')} "
                f"| {tags} "
                f"| {src_files} "
                f"| {src_pages} "
                f"| {t_codes} "
                f"| {meta.get('status','')} "
                f"| {meta.get('quality','')} |"
            )
        except Exception as e:
            print(f"Error in {path}: {e}")

today = datetime.date.today()
header = [
    "# SAP SD Knowledge Base — Index\n",
    f"Last updated: {today}  |  Total chunks: {len(rows)}\n",
    "| ID | Path | Title | Area | Type | SAP Release | Process Tags"
    " | Sources | Pages | T-codes | Status | Quality |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|",
]
rows.sort(key=lambda r: r.lower())
seen_ids = {}
for row in rows:
    parts = row.split("|")
    id_val = parts[1].strip() if len(parts) > 1 else ""
    path_val = parts[2].strip() if len(parts) > 2 else ""
    if id_val in seen_ids:
        print(f"ERROR: duplicate ID — {id_val}")
        sys.exit(1)
    else:
        seen_ids[id_val] = path_val
with open(os.path.join(chunks_dir, "_index.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(header + rows) + "\n")
print(f"Index regenerated: {len(rows)} chunks.")
PYEOF
```

### `_source_inventory.md`

```markdown
# Source Inventory — SAP SD Knowledge Base
Last updated: YYYY-MM-DD

| File | Relative Path | Type | Priority | Pages | Words/Page | Status | Notes |
|---|---|---|---|---|---|---|---|
| S4610_EN_Col17 Delivery Processing.pdf | S4610_EN_Col17 ... | A | high | 178 | 320 | partial | p.68 pending |
```

Statuses: `not started` / `partial` / `completed` / `skipped` / `blocked`

---

## Session Limit

### First Two Sessions — Calibration Mode
- Maximum one logical unit (closed chapter or functional block)
- Or maximum 5 chunks, whichever comes first
- Stop and request human validation

### After Calibration
- Maximum one complete document per session
- Or one complete logical block in documents >300 pages
- Do not use "up to halfway" — use the logical boundary of the document
- Always record the next pending page in the log

### At the End of Each Session, Present:
```
Chunks created/updated this session:
  - [id] → [path]
Pending validation:
  - [what the user should review]
Next recommendation:
  - [concrete proposal for the next session]
```

---

## Reference Examples

Manually validated chunks from `SD - Shipment.pdf` (Type B).
Use as reference for technical density, format, and criteria.

### Example 1 — chunk_type: process

```markdown
---
schema_version: 1
id: shipping-delivery-creation-process-001
title: "Creating Outbound Deliveries in SAP SD"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: process
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2-9"
    source_type: B
    role: primary
transactions: [VL01N, VL10E, VL02N, VL03N, VL06O]
tables: []
aliases:
  - outbound delivery
  - entrega de salida
  - crear entrega
  - delivery creation
  - creación entrega
level: functional
status: draft
quality: high
created: 2026-06-01
last_updated: 2026-06-01
---

# Creating Outbound Deliveries in SAP SD

<!-- inferred tables, pending validation: LIKP, LIPS, VBUK -->

## Operational Summary
An *outbound delivery* is the document that initiates the physical shipping process against a customer order. SAP allows creating it individually for a specific order or collectively for a set of pending orders. Only *schedule lines* confirmed up to the *selection date* are included.

## Questions This Chunk Answers
- How is an outbound delivery created in SAP SD?
- What is the difference between creating deliveries individually and collectively?
- Why are no items generated in the delivery even though there is stock?
- What is the *selection date* and how does it affect deliveries?

## When It Applies and Context
The delivery is created after the order has confirmed *schedule lines*. It is the step before picking, packing, and *Goods Issue*. Without a delivery there is no GI, and without GI there is no invoice.

## Process Flow

### Option 1 — Individual Delivery from the Order (VA02)
1. Open the order with **VA02**
2. Menu: *Sales document > Deliver*
3. SAP redirects to the same screen as VL01N with the order pre-filled
4. Verify *Shipping point* and *Selection date*
5. Confirm → delivery created

### Option 2 — Direct Individual Delivery (VL01N)
1. Run **VL01N**
2. Enter *Shipping point*, *Selection date*, and order number
3. Confirm → delivery overview screen

### Option 3 — Collective Deliveries (VL10E — Delivery Due List)
1. Run **VL10E**
2. Criteria: *Shipping point*, date range; optional: route, *ship-to*, sales org.
3. System shows *schedule lines* confirmed up to the date
4. Select lines and choose mode:
   - **Dialog**: creates deliveries manually, same as VL01N
   - **Background**: creates all automatically in batch

## Conditions and Restrictions
- Only confirmed *schedule lines* (ATP approved)
- *Selection date* filters: only lines confirmed up to that date
- *Shipping point* must be assigned to the order's plant

## Common Errors

**"No schedule lines due for delivery up to the selected date"**
→ *Selection date* is earlier than the order confirmation date.
→ Extend the *selection date* to cover the confirmed date.

**Order does not appear in VL10E**
→ Verify that the *Shipping point* matches the order's shipping point.
→ Verify that *schedule lines* are not blocked.

## Cross-References
- See also: shipping-delivery-types-concept-001
- Next step: shipping-goods-issue-001
```

### Example 2 — chunk_type: concept

```markdown
---
schema_version: 1
id: shipping-delivery-types-concept-001
title: "Outbound Delivery in SAP SD — Concept and Structure"
area: shipping
process_tags: [order-to-cash, delivery-processing]
chunk_type: concept
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "2, 10"
    source_type: B
    role: primary
transactions: [VL01N, VL02N, VL03N]
tables: []
aliases:
  - outbound delivery
  - entrega de salida
  - delivery document
  - documento de entrega
level: functional
status: draft
quality: medium
created: 2026-06-01
last_updated: 2026-06-01
---

# Outbound Delivery in SAP SD — Concept and Structure

<!-- inferred tables, pending validation: LIKP, LIPS -->

## Operational Summary
The outbound delivery is the logistics document representing the physical shipment of goods against a customer order. It has a header with recipient data and items with the materials. It has no *schedule lines*. It is the pivot between order management (SD) and the warehouse (WM/EWM).

## Questions This Chunk Answers
- What is an outbound delivery in SAP SD?
- What structure does the delivery document have?
- How does the delivery differ from the sales order?

## Definition
SAP SD document representing the intent and execution of sending goods to a customer. Created with reference to a sales order, inheriting its shipping data.

## Purpose in the SD Process
Enables initiating picking, recording packing and loading, executing *Goods Issue* (reduces stock and generates an accounting document in FI), and serves as the basis for the invoice.

## Structure and Variants

| Level | Data Contained |
|---|---|
| Header | *Ship-to party*, delivery date, *shipping point*, total weight, packages |
| Item | Material, quantity, unit of measure, batch, picking status |

Unlike the order, the delivery **has no *schedule lines***.

## Relationship with Other SAP SD Objects

| Object | Relationship |
|---|---|
| Sales Order | Delivery created with reference; inherits *ship-to*, materials, confirmed quantities |
| *Transfer Order* (WM) | If warehouse management active, generates a *transfer order* for picking |
| *Goods Issue* | Executed on the delivery in VL02N |
| Invoice | Created with reference to the delivery after GI |

## Cross-References
- Creation process: shipping-delivery-creation-process-001
- Next step: shipping-goods-issue-001
```

### Example 3 — chunk_type: transaction

```markdown
---
schema_version: 1
id: shipping-goods-issue-cancel-vl09-001
title: "Cancelling Goods Issue with VL09"
area: shipping
process_tags: [returns, delivery-processing]
chunk_type: transaction
sap_release: generic
sources:
  - file: "SD - Shipment.pdf"
    relative_path: "SD/SD - Shipment.pdf"
    pages: "15"
    source_type: B
    role: primary
transactions: [VL09]
tables: []
aliases:
  - cancel GI
  - cancelar GI
  - reverse goods issue
  - VL09
  - cancelar salida de mercancías
  - revertir GI
level: functional
status: draft
quality: medium
created: 2026-06-01
last_updated: 2026-06-01
---

# Cancelling Goods Issue with VL09

<!-- inferred tables, pending validation: LIKP, MKPF -->

## Operational Summary
**VL09** reverses a *Goods Issue* posted in error. Undoes the stock decrease and cancels the accounting document in FI. Only possible within the same accounting period in which the original GI was posted.

## Questions This Chunk Answers
- How do you cancel a *Goods Issue* posted in error?
- When is VL09 no longer possible?
- What is the alternative if the accounting period is closed?

## When to Use This Transaction
When a GI has been posted against an outbound delivery in error and the GI's accounting period is still open in FI.

## Affected Business Object
Outbound delivery with a posted GI.

## Key Fields on the Main Screen

| Field | Description | Notes |
|---|---|---|
| *Shipping point* | Shipping point | Required |
| *Inbound/Outbound delivery* | Delivery number | Enter directly |
| *Define date* | Reversal date | Defaults to today |

## Typical Usage Flow
1. Run **VL09**
2. Enter *Shipping point* and delivery number
3. Select the line shown in the results
4. Execute *Cancel/Reverse*
5. System reverses the GI; delivery returns to open status

## Restrictions
Only possible in the **same accounting period** in which the original GI was posted.
If the period is closed in FI: use a customer return (*Returns Order* + *Return Delivery* + GR).

## Common Errors

**"Reversal not possible — period already closed"**
→ Accounting period closed. Proceed with customer return.

**Delivery does not appear in the selection**
→ Verify that the GI is posted and that the *Shipping point* matches.

## Cross-References
- Prior step: shipping-goods-issue-001
- Alternative if period closed: special-processes-customer-returns-001
```

---

## What to Observe in These Examples

**Operational Summary**: 3-5 lines with the complete concept. If you cannot write it without filler, the chunk is poorly delimited.

**Real questions**: not generic, but questions a consultant would ask on a real project.

**No empty sections**: example 3 does not include sections the source did not cover. No invented filler.

**Terminology**: SAP terms in English in italics in the body. Spanish equivalents in `aliases`.

**quality: medium vs high for Type B**: `medium` is the default for Type B. Only raise to `high` if the visual flow is unambiguous, transactions and fields are clearly readable, and no functional inferences were required.

**Correct chunk_type**: VL09 is `transaction`, not `configuration`.

---

## Project Context

Goal: RAG system to answer questions from a functional SAP SD consultant.
The user is learning SAP SD and RAG techniques simultaneously.
Quality over speed. 20 excellent chunks are worth more than 200 mediocre ones.
Do not generate chunks if you cannot provide exact source and pages.
When in doubt between two reasonable options, propose both and wait for confirmation.
