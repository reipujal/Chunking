# Skill 2 — Extract Content

> Shell context: recover SOURCE_ROOT if empty (new subprocess):
> ```bash
> SOURCE_ROOT=$(python3 -c "import yaml; print(yaml.safe_load(open('chunks/_project_state.md'))['source_root'])" 2>/dev/null || grep "source_root:" chunks/_project_state.md | awk -F"'" '{print $2}')
> [ -d "$SOURCE_ROOT" ] || { echo "ERROR: SOURCE_ROOT not resolvable"; exit 1; }
> ```

## Type A, C, D — Text Documents

**Rule: never more than 30 pages per extraction call.** Larger blocks trigger "Lost in the Middle" degradation.

**First time with any document: map TOC and back matter.**

```bash
# Front: table of contents
pdftotext -f 1 -l 12 "$DOC" - | head -250
```

**Then scan back matter for T-code/table appendix** (last 10-15 pages):
```bash
pages=$(pdfinfo "$DOC" | awk '/^Pages:/{print $2}')
back_start=$(( pages > 15 ? pages - 14 : 1 ))
pdftotext -layout -f "$back_start" -l "$pages" "$DOC" - \
  | grep -inE 'TX:|transaction code|menu path|^[[:space:]]*V[AFL][0-9]{2}|appendix|glossary' \
  | head -40
```

If this surfaces a T-code/menu-path table: treat as first-class source. Mine it for identifiers for every lesson chunk. Record the appendix page range in the log. If not chunked separately, log: "appendix p.X-Y mined for T-codes, not chunked."

**Extract in 30-page blocks:**
```bash
pdftotext -layout -f [start] -l [end] "$DOC" /tmp/block.txt
wc -w /tmp/block.txt
head -80 /tmp/block.txt
```

Ignore: headers/footers ("© SAP SE", page numbers), watermarks ("For Internal Use Only"), slide refs ("As shown above").

**Broken encoding** (`Ã©`, `â€™`):
```bash
pdftoppm -jpeg -r 150 -f [page] -l [page] "$DOC" /tmp/broken_page
ls /tmp/broken_page-*.jpg
```
If visual inspection not possible: record page as unprocessed in log. Do not invent.

---

## Type B — Visual Slide Decks

```bash
DOC_SLUG="$(basename "$DOC" .pdf | tr ' ' '-' | tr -cd '[:alnum:]-_')"
rm -rf "/tmp/slides-$DOC_SLUG" && mkdir -p "/tmp/slides-$DOC_SLUG"
pages=$(pdfinfo "$DOC" | awk '/^Pages:/ {print $2}')
echo "Total pages: $pages — rasterize in blocks of 30"
pdftoppm -jpeg -r 150 -f [start] -l [end] "$DOC" "/tmp/slides-$DOC_SLUG/page"
ls "/tmp/slides-$DOC_SLUG/"
```

From each image extract: visible T-codes (read exactly as shown in command field), SAP table names in data-model figures, key GUI fields, superimposed text, implicit screen flow.

A figure is the **only** source from which a T-code may enter `transactions` without appearing in extracted text. If unreadable with certainty: treat as absent, add `<!-- inferred -->` comment.

If visual inspection not possible: record as `blocked` in `_source_inventory.md`, consult user.

Type B chunking: one chunk per coherent functional flow, not one per slide.

---

## Mixed Documents (Type A*/C/D with visual pages)

Detect visual pages in extracted block:
```bash
pdftotext -layout -f [start] -l [end] "$DOC" /tmp/block.txt
export INICIO=[start]
python3 - << 'PY'
import os
text = open("/tmp/block.txt", encoding="utf-8", errors="replace").read()
inicio = int(os.environ.get("INICIO", "1"))
pages = text.split("\f")
BUTTON_SET = {"save","cancel","execute","ok","back","enter","help",
              "display","change","create","delete","post","check",
              "continue","exit","refresh","print","previous","next"}
for i, page in enumerate(pages, start=inicio):
    if not page.strip(): continue
    tokens = page.lower().split()
    words = len(tokens)
    all_buttons = len(tokens) > 0 and set(tokens).issubset(BUTTON_SET)
    status = "VISUAL" if (words < 40 or all_buttons) else "text"
    print(f"  Page {i}: {words} words -- {status}")
PY
```

For each VISUAL page: discard plain text, note page number, rasterize only that page:
```bash
pdftoppm -jpeg -r 150 -f [page_number] -l [page_number] "$DOC" /tmp/visual
ls /tmp/visual-*.jpg
```
Do not rasterize the entire document — only pages that trigger the signal.
