# Skill 5 — Validate, Batch Audit, and Update State

## Step 6 — Validate Each Chunk

**Pre-validation** (before writing the file):
```bash
AREA="shipping"
SLUG="delivery-creation-individual"
NNN="001"
FILE="chunks/$AREA/$SLUG-$NNN.md"

mkdir -p "chunks/$AREA"
if [ -f "$FILE" ]; then
  echo "WARNING: $FILE already exists — present update plan and wait for confirmation"
  exit 1
fi
matches=$(grep -Rni "^id: ${AREA}-${SLUG}-${NNN}$" chunks/ --include="*.md" | wc -l)
[ "$matches" -gt 0 ] && echo "WARNING: ID already exists in $matches chunk(s)"
```

**Post-validation** (after writing the file):
```bash
python3 validate_chunks.py "$FILE"
```

`validate_chunks.py` checks all structural, schema, and quality rules. If it reports any ERROR: fix before continuing. Do not update the index with a defective chunk.

**Provenance check** (advisory — requires extracted source text):
```bash
# Re-extract if needed: pdftotext -layout -f [start] -l [end] "$DOC" /tmp/chunk_src.txt
SRC_TXT="/tmp/chunk_src.txt"
export FILE SRC_TXT
python3 - << 'PROV'
import os, re, yaml, pathlib

chunk = pathlib.Path(os.environ["FILE"])
src_path = pathlib.Path(os.environ["SRC_TXT"])
meta = yaml.safe_load(chunk.read_text(encoding="utf-8").split("---", 2)[1])
src = src_path.read_text(encoding="utf-8", errors="replace").upper() if src_path.exists() else ""

problems = []
for field in ("transactions", "tables"):
    for tok in meta.get(field, []):
        tok = str(tok).strip()
        if tok and not re.search(r"(?<![A-Z0-9_])" + re.escape(tok.upper()) + r"(?![A-Z0-9])", src):
            problems.append(f"  {field}: '{tok}' NOT in source text (possible hallucination)")

TCODE_RE = re.compile(r"(?<![A-Z0-9_])(V[AFL][0-9]{2,3}[A-Z]?|F[BK][0-9]{2,3}|VK[0-9]{2})(?![A-Z0-9])")
TABLE_RE = re.compile(r"(?<![A-Z0-9_])(VBRK|VBRP|VBFA|VBPA|VBAK|VBAP|VBUK|VBUP|LIKP|LIPS|KONV|PRCD_COND|BSEG|BKPF|ACDOCA|FPLT|FPLA)(?![A-Z0-9])")
listed = {str(t).strip().upper() for t in (meta.get("transactions") or []) + (meta.get("tables") or [])}
body_upper = chunk.read_text(encoding="utf-8").split("---", 2)[2].upper()
for tok in sorted(({m.group(0) for m in TCODE_RE.finditer(src)} | {m.group(0) for m in TABLE_RE.finditer(src)}) - listed):
    if re.search(r"(?<![A-Z0-9_])" + re.escape(tok) + r"(?![A-Z0-9])", body_upper):
        problems.append(f"  OMISSION: '{tok}' in source AND in chunk body but not in transactions/tables")

print("PROVENANCE WARNINGS:" if problems else "PROVENANCE OK")
for p in problems: print(p)
PROV
```

---

## Step 6b — Batch Audit (before closing a document)

```bash
python3 validate_chunks.py --area [area]
```

Read the full output. Fix systemic findings (uniform quality, broken cross-refs, isolated nodes, page offset suspects) before writing the log.

---

## Step 6c — Source-Coverage Gate + Write-Integrity (before closing a document)

"0 validator errors" does NOT mean the document is complete. Two checks gate document closure.

**A. Write-integrity (corruption guard).** A file watcher on this workspace can truncate in-place writes. After the batch, confirm no chunk is corrupted or truncated:
```bash
grep -rlP '\x00' chunks/ --include="*.md" && echo "NUL CORRUPTION" || echo "no NUL"
# truncated headers / unresolved cross-refs are caught by the validator (ERROR)
python3 validate_chunks.py chunks/ 2>&1 | tail -3
```
If any chunk was written and a later edit shows a shorter file, re-read it — prefer atomic writes (write to /tmp, then move) and re-read to confirm persistence.

**B. Source-coverage gate.** Run **Skill 6 — `docs/playbooks/6-coverage-review.md`** (coverage-map + extraction-ratio + triaje). No marques el documento `completed` hasta que su criterio de "hecho" se cumpla: cada página ≥100w o chunkeada o justificada en el log, y los outliers de ratio triados.

## Step 7 — Update State

### `_processing_log.md` — append-only

```markdown
## YYYY-MM-DD — [exact PDF name]
- Relative path: [path from SOURCE_ROOT]
- Type: A/B/C/D/E
- Total pages: N
- Processed range: p. X-Y
- Appendix / reference tables: [page range mined, or "none present"]
- Next pending page: p. Z  (or "none — completed")
- Extractable text: high/medium/low
- Encoding issues: [problematic pages, or "none"]
- Chunks created: N
  - [id] → chunks/area/file.md
- Chunks updated: [id] → reason
- Duplicates found: [id] → [decision]
- Omitted content: [what and why, or "none"]
- Non-obvious decisions: [decision and justification]
- Status: not started / partial / completed / skipped
```

**Coverage self-check before writing `Status: completed`**: every page in range was read; appendix mined; no unexplained gaps in content pages.

### `_index.md` — regenerate with script

```bash
python3 << 'PYEOF'
import os, sys, datetime, pathlib
try: import yaml
except ImportError:
    print("pyyaml missing — add row manually to chunks/_index.md"); sys.exit(0)

chunks_dir = "chunks"
rows = []
for root, _, files in os.walk(chunks_dir):
    for f in sorted(files):
        if not f.endswith(".md") or f.startswith("_"): continue
        path = os.path.join(root, f)
        content = open(path, encoding="utf-8").read()
        if not content.startswith("---"): continue
        try:
            meta = yaml.safe_load(content.split("---", 2)[1])
            def esc(v): return str(v).replace("|", r"\|").replace("\n", " ")
            rows.append(
                f"| {meta.get('id','')} | {path} | {meta.get('title','')} "
                f"| {meta.get('area','')} | {meta.get('chunk_type','')} "
                f"| {meta.get('sap_release','')} "
                f"| {esc(', '.join(str(t) for t in meta.get('process_tags',[])))} "
                f"| {esc(', '.join(s.get('file','') for s in meta.get('sources',[])))} "
                f"| {esc(', '.join(str(s.get('pages','')) for s in meta.get('sources',[])))} "
                f"| {esc(', '.join(str(t) for t in meta.get('transactions',[])))} "
                f"| {meta.get('status','')} | {meta.get('quality','')} |"
            )
        except Exception as e:
            print(f"Error in {path}: {e}")

rows.sort(key=str.lower)
seen = {}
for row in rows:
    id_val = row.split("|")[1].strip()
    if id_val in seen:
        print(f"ERROR: duplicate ID {id_val}"); sys.exit(1)
    seen[id_val] = True

header = [
    "# SAP SD Knowledge Base — Index\n",
    f"Last updated: {datetime.date.today()}  |  Total chunks: {len(rows)}\n",
    "| ID | Path | Title | Area | Type | SAP Release | Tags | Sources | Pages | T-codes | Status | Quality |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|",
]
open(os.path.join(chunks_dir, "_index.md"), "w", encoding="utf-8").write("\n".join(header + rows) + "\n")
print(f"Index regenerated: {len(rows)} chunks.")
PYEOF
```

### `_source_inventory.md`

```markdown
| File | Relative Path | Type | Priority | Pages | Words/Page | Status | Notes |
|---|---|---|---|---|---|---|---|
| [filename] | [path] | A | high | N | N | partial | p.X pending |
```

Statuses: `not started` / `partial` / `completed` / `skipped` / `blocked`
