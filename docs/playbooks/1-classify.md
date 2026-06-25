# Skill 1 — Classify the Document

> Shell context: if `$SOURCE_ROOT` is empty (new subprocess), recover it:
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT not resolvable"; exit 1; }
> ```

```bash
DOC="$SOURCE_ROOT/[name].pdf"

pdfinfo "$DOC"
pdffonts "$DOC" | head -10
pdftotext -f 1 -l 4 "$DOC" - 2>/dev/null | head -120

# Word/page ratio — sample from p.30 to skip cover, copyright, TOC
pages=$(pdfinfo "$DOC" 2>/dev/null | awk '/^Pages:/{print $2}')
[ -z "$pages" ] && { echo "ERROR: pdfinfo returned no page count"; exit 1; }
sample_start=$(( pages > 30 ? 30 : (pages > 10 ? 10 : 1) ))
sample_end=$(( pages < (sample_start + 15) ? pages : (sample_start + 15) ))
sample_words=$(pdftotext -f "$sample_start" -l "$sample_end" "$DOC" - 2>/dev/null | wc -w)
sample_pages=$(( sample_end - sample_start + 1 ))
echo "Sample ratio (p.$sample_start-$sample_end): $((sample_words / sample_pages)) words/page"
```

| Type | Name | Criterion | Strategy |
|---|---|---|---|
| A | Official SAP course | Prefix S4600-S4680, TSCM60/62; >200 w/p | Extract by chapters/units |
| A* | Mixed | 80-200 w/p | Extract text + rasterize visual pages |
| B | Visual slide deck | "Process Diagrams" in name, or <80 w/p | Rasterize with pdftoppm |
| C | Community manual | "User Manual", "tutorial", "training", BBP | Extract, validate quality first |
| D | Specialized | "Shipment", "Variant Config", "FI-MM-SD", "Transportation" | Same as Type A |
| E | Certification/dumps | "certification", "dumps", "sample questions" | Skip by default |

**HTML→PDF (Edge/Chromium exports):** `pdfinfo` shows `Producer: Skia/PDF`. Words/page heuristics are indicators only. Rasterize 2-3 pages visually before deciding. Document Producer in `_source_inventory.md`.

**Detect physical page offset** (record in log):
```bash
for p in $(seq 1 20); do
  lbl=$(pdftotext -layout -f $p -l $p "$DOC" - | grep -oE 'Copyright.*reserved\.[[:space:]]*[0-9]+' | grep -oE '[0-9]+$' | head -1)
  [ "$lbl" = "1" ] && { echo "Offset: printed 1 = physical $p  (printed N = physical N+$((p-1)))"; break; }
done
```

**Report to user before continuing:**
```
Document: [name]
Type: [A/B/C/D/E]
Pages: N  |  Ratio: N words/page  |  Extractable: high/medium/low
Proposal: process [section/range] because [reason]. Confirm?
```
