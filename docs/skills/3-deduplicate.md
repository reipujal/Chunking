# Skill 3 — Detect Duplicates and Manage SAP Versions

Search terms must be specific to the topic. Use T-codes, tables, SAP terms in English, Spanish aliases, and business objects from the source.

> The T-codes and tables in the examples below are **search seeds for finding existing chunks**, not a checklist for the new chunk's frontmatter. What goes into `transactions`/`tables` is governed solely by provenance (literal presence in the current source).

```bash
grep -RniE "TERM1|TERM2|TCODE|TABLE|spanish_alias" chunks/ --include="*.md" || true
```

**Example — Pricing:**
```bash
grep -RniE "pricing procedure|esquema de precios|condition type|clase de condicion|access sequence|secuencia de acceso|V/08|VK11|KONV|KONP" chunks/ --include="*.md" || true
```

**Example — Delivery:**
```bash
grep -RniE "outbound delivery|entrega de salida|\bVL01N\b|\bVL10E\b|\bLIKP\b|\bLIPS\b|shipping point|punto de expedicion" chunks/ --include="*.md" || true
```

---

## Case 1 — Same Topic, Same SAP Version, Different Source
Present an update plan — do not modify directly:
```
Existing chunk: [id]
New source: [file], p. [N-M]
Proposed changes: [section to expand or correct]
Confirm update?
```
Only after confirmation: update, add source to `sources` array, log "updated with [source]."

## Case 2 — Same Topic, Different SAP Versions
Functionally significant difference → two chunks by version with a `## Differences from [version]` section each.
Only cosmetic → single chunk with `sap_release: generic` + `## Version Notes`.
Unknown → separate by version (safer).

## Case 3 — Same Version, Contradictory Sources
Type A > B, C, D. Between two Type A: the more recent wins. Document contradiction in log.

## Case 4 — Pure Duplicate
Skip. Log: "skipped — duplicate of [id]."

**Golden rule**: one concept = one chunk per SAP version. Complete: synthesizes all sources. A consultant must not find the same topic across multiple chunks.
