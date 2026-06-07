#!/usr/bin/env python3
"""
SAP SD Knowledge Base — Chunk Validator
========================================
Runs structural, quality, and batch-level checks on all chunks.

Usage:
  python3 validate_chunks.py                  # validate all chunks
  python3 validate_chunks.py --area billing   # only billing/ folder
  python3 validate_chunks.py --json           # machine-readable output
  python3 validate_chunks.py --no-batch       # skip cross-chunk audit
  python3 validate_chunks.py chunks/billing/billing-document-cancellation-001.md  # single file

Exit code: 0 = all pass, 1 = any ERROR.
"""

import pathlib, yaml, re, sys, json, collections, argparse

# ── Valid value sets ────────────────────────────────────────────────────────
VALID_AREAS = {
    "enterprise-structure", "master-data", "order-management", "pricing",
    "shipping", "billing", "credit-management", "configuration",
    "integration", "special-processes",
}
VALID_TYPES   = {"concept", "process", "configuration", "transaction", "integration"}
VALID_STATUS  = {"draft", "reviewed", "validated", "deprecated"}
VALID_QUALITY = {"high", "medium", "low"}
VALID_RELEASE = {"S/4HANA 2020", "ECC 6.0", "generic", "not specified"}
VALID_LEVEL   = {"functional", "technical", "both"}
VALID_SRC_TYPE = {"A", "B", "C", "D"}
VALID_ROLE    = {"primary", "secondary"}
# Canonical tag list — must stay in sync with process_tags in CLAUDE.md
VALID_TAGS    = {
    "order-to-cash", "delivery-processing", "billing", "pricing", "returns",
    "credit-management", "transportation", "consignment", "third-party",
    "free-of-charge", "complaints", "credit-memo", "debit-memo",
    "invoice-correction", "make-to-order", "stock-transfer", "intercompany",
    "billing-plans", "invoice-list", "pro-forma", "none",
}

# Mandatory sections per chunk_type (substring match against ## headings)
REQUIRED_SECTIONS = {
    "process":       ["Operational Summary", "Process Flow"],
    "concept":       ["Operational Summary", "Definition", "Relationship"],
    "configuration": ["Operational Summary", "SPRO"],
    "transaction":   ["Operational Summary", "Typical Usage Flow"],
    "integration":   ["Operational Summary", "Data Flow"],
}

# ── Spanish heuristic ───────────────────────────────────────────────────────
_ES = re.compile(
    r'[áéíóúñü]'                         # accented vowels or ñ/ü
    r'|ción\b|ción '                      # -ción suffix (facturación, cancelación)
    r'|izar\b'                            # -izar verbs
    r'|\bde \w+'                          # "de X" prep phrase
    r'|ento\b|ados?\b|idos?\b|encia\b'   # Spanish noun/adj endings
    r'|\bpor \w+|\bcon \w+|\bsin \w+'    # common prepositions + noun
    r'|\bcómo\b|\bqué\b|\bcuál'          # interrogatives
    r'|\bfactur\w+|\bcontabil\w+'        # high-frequency SAP-Spanish roots (no accent needed)
    r'|\bsucursal\b|\bpagador\b|\bcompras?\b|\bcuenta\b|\bmayor\b'
    r'|\bsociedad\b|\bpedido\b|\bentrega\b|\balmacén\b|\bcancelac',
    re.I,
)

def _looks_spanish(s: str) -> bool:
    return bool(_ES.search(s))


# ── Page count parser ───────────────────────────────────────────────────────
def _count_pages(pages_str: str) -> int:
    """
    Parse a pages string and return the total number of physical pages cited.
    Handles: '19', '44-47', '52-56, 59, 125', '29-30, 125', '83-88, 126'.
    """
    total = 0
    for part in str(pages_str).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                a, b = part.split("-", 1)
                total += abs(int(b.strip()) - int(a.strip())) + 1
            except ValueError:
                total += 1
        else:
            try:
                int(part)
                total += 1
            except ValueError:
                pass
    return max(total, 1)


# ── ANSI colours (fall back gracefully on Windows without colorama) ─────────
def _colour(code: str, text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

def _red(s):    return _colour("31", s)
def _yellow(s): return _colour("33", s)
def _green(s):  return _colour("32", s)
def _bold(s):   return _colour("1",  s)


# ── Result class ────────────────────────────────────────────────────────────
class ChunkResult:
    def __init__(self, label: str):
        self.label   = label
        self.errors  : list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str): self.errors.append(msg)
    def warn (self, msg: str): self.warnings.append(msg)
    def ok   (self) -> bool:   return not self.errors


# ── Per-chunk validation ────────────────────────────────────────────────────
def validate_chunk(path: pathlib.Path, all_ids: set[str]) -> ChunkResult:
    area     = path.parent.name
    label    = f"{area}/{path.name}"
    r        = ChunkResult(label)

    text = path.read_text(encoding="utf-8", errors="replace")

    # ── Frontmatter ─────────────────────────────────────────────────────────
    if not text.startswith("---"):
        r.error("No YAML frontmatter (file does not start with ---)")
        return r

    parts = text.split("---", 2)
    if len(parts) < 3:
        r.error("Malformed frontmatter — no closing ---")
        return r

    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        r.error(f"YAML parse error: {exc}")
        return r

    if not isinstance(meta, dict):
        r.error("Frontmatter is not a YAML mapping")
        return r

    body = parts[2]

    # ── Required fields ──────────────────────────────────────────────────────
    REQUIRED = [
        "schema_version", "id", "title", "area", "process_tags", "chunk_type",
        "sap_release", "sources", "transactions", "tables", "aliases",
        "level", "status", "quality", "created", "last_updated",
    ]
    missing = [f for f in REQUIRED if f not in meta]
    for f in missing:
        r.error(f"Missing required field: '{f}'")
    if missing:
        return r  # can't safely continue without basics

    # ── Enum validation ──────────────────────────────────────────────────────
    checks = [
        ("area",        meta["area"],         VALID_AREAS),
        ("chunk_type",  meta["chunk_type"],   VALID_TYPES),
        ("status",      meta["status"],       VALID_STATUS),
        ("quality",     meta["quality"],      VALID_QUALITY),
        ("sap_release", meta["sap_release"],  VALID_RELEASE),
        ("level",       meta["level"],        VALID_LEVEL),
    ]
    for field, val, valid_set in checks:
        if val not in valid_set:
            r.error(f"Invalid {field}: '{val}'")

    bad_tags = set(meta.get("process_tags", [])) - VALID_TAGS
    if bad_tags:
        r.error(f"Invalid process_tags: {bad_tags} — check VALID_TAGS list")

    # ── ID / path consistency ────────────────────────────────────────────────
    expected_id = f"{area}-{path.stem}"
    if meta["id"] != expected_id:
        r.error(f"ID mismatch: frontmatter '{meta['id']}' ≠ expected '{expected_id}'")
    if meta["area"] != area:
        r.error(f"Area mismatch: frontmatter '{meta['area']}' ≠ folder '{area}'")

    # ── Sources ──────────────────────────────────────────────────────────────
    sources = meta.get("sources", [])
    if not sources:
        r.error("No sources defined (sources: [])")
    for i, s in enumerate(sources):
        for k in ["file", "relative_path", "pages", "source_type", "role"]:
            if k not in s:
                r.error(f"sources[{i}]: missing field '{k}'")
        if s.get("source_type") not in VALID_SRC_TYPE:
            r.error(f"sources[{i}]: invalid source_type '{s.get('source_type')}'")
        if s.get("role") not in VALID_ROLE:
            r.error(f"sources[{i}]: invalid role '{s.get('role')}'")
        if not isinstance(s.get("pages", ""), str):
            r.error(f"sources[{i}]: pages must be a quoted string, got {type(s.get('pages')).__name__} — wrap in quotes")

    # ── Body: H1 title ───────────────────────────────────────────────────────
    h1_matches = re.findall(r'^#\s+([^#].+)$', body, re.M)
    headings   = re.findall(r'^##\s+(.+)$', body, re.M)

    if not h1_matches:
        r.error("Missing H1 title (# Title). Every chunk must have a top-level heading.")
    else:
        h1 = h1_matches[0].strip()
        title_fm = meta.get("title", "").strip()
        if h1 != title_fm:
            r.warn(f"H1 '{h1}' ≠ frontmatter title '{title_fm}' — consider aligning them")

    # ── Body: word count ─────────────────────────────────────────────────────
    body_words = len(body.split())
    if body_words < 300:
        r.error(f"Body has only {body_words} words (minimum 300). Merge or expand coverage.")
    elif body_words < 400:
        r.warn(f"Body has {body_words} words — above the floor but thin for RAG (recommend >=400)")

    # ── Extraction density: body words per cited page ────────────────────────
    # Only meaningful when >= 3 pages are cited (single-page chunks are always
    # dense by construction). Thresholds calibrated from observed corpora:
    #   S4610/Sonnet: ~140-185 w/p  (good)
    #   S4615/Codex original: ~47 w/p  (clearly superficial)
    #   S4615/fixed:  ~74-90 w/p  (acceptable — SAP courses include figures
    #                               and assessment pages that don't yield text)
    total_cited_pages = sum(_count_pages(str(s.get("pages", "1"))) for s in sources)
    if total_cited_pages >= 3:
        wpp = body_words / total_cited_pages
        if wpp < 50:
            r.warn(
                f"[DENSITY] {wpp:.0f} words/page ({body_words}w / {total_cited_pages}p). "
                "Very low — strongly suspect superficial extraction. "
                "Re-read source pages and expand content."
            )
        elif wpp < 80:
            r.warn(
                f"[DENSITY] {wpp:.0f} words/page ({body_words}w / {total_cited_pages}p). "
                "Below 80 w/p — verify all source pages were fully read "
                "(figures, tables, back-matter appendix)."
            )

    # ── Mandatory sections per chunk_type ─────────────────────────────────────
    ctype = meta.get("chunk_type", "")
    for need in REQUIRED_SECTIONS.get(ctype, []):
        found = any(need.lower() in h.lower() for h in headings)
        alt   = (need == "Process Flow" and any("usage flow" in h.lower() for h in headings))
        if not found and not alt:
            r.error(f"[{ctype}] missing required section containing '{need}'")
        elif found and need == "Process Flow":
            # Check Process Flow has actual content (steps), not just a heading.
            # Accepts: numbered list items (1.), ### sub-headings, or bullet points (-/*).
            pf_m = re.search(r'^## (?:Process Flow|Typical Usage Flow)(.*?)(?=^## [^#]|\Z)',
                             body, re.M | re.S)
            if pf_m:
                pf_body = pf_m.group(1)
                has_steps = (
                    re.search(r'^\d+\.', pf_body, re.M) or
                    re.search(r'^###', pf_body, re.M) or
                    re.search(r'^\s*[-*]\s', pf_body, re.M)
                )
                if not has_steps and len(pf_body.split()) < 20:
                    r.warn("Process Flow section has no numbered steps, sub-headings, or bullet points")

    # ── Questions section ─────────────────────────────────────────────────────
    q_heads = [h for h in headings if "question" in h.lower()]
    if not q_heads:
        r.error("Missing '## Questions This Chunk Answers' section")
    else:
        q_m = re.search(r'^## Questions This Chunk Answers(.*?)(?=^## [^#]|\Z)', body, re.M | re.S)
        if q_m:
            q_count = len(re.findall(r'^\s*[-*]', q_m.group(1), re.M))
            if q_count < 4:
                r.warn(f"Only {q_count} questions — minimum 4 distinct search intents recommended")

    # ── Cross-References section ──────────────────────────────────────────────
    xref_heads = [h for h in headings if re.match(r'cross[- ]?ref', h, re.I)]
    if not xref_heads:
        r.error("Missing '## Cross-References' section (mandatory for all chunk types)")
    else:
        xref_m = re.search(r'^## Cross-References(.*?)(?=^## [^#]|\Z)', body, re.M | re.S)
        if xref_m:
            xref_body = xref_m.group(1)
            # Backtick IDs
            if re.search(r'`[a-z][a-z0-9-]+-\d{3}`', xref_body):
                r.error("Cross-references use backtick format — use plain IDs (e.g. billing-invoice-list-001)")
            # Quoted IDs
            if re.search(r'"[a-z][a-z0-9-]+-\d{3}"', xref_body):
                r.warn("Cross-references use quoted format — prefer plain IDs without quotes")
            # Resolvability of referenced IDs
            ref_ids = set(re.findall(r'\b[a-z][a-z0-9-]+-\d{3}\b', xref_body))
            broken  = ref_ids - all_ids
            for rid in sorted(broken):
                r.warn(f"Cross-reference '{rid}' does not match any known chunk ID")

    # ── Aliases quality ───────────────────────────────────────────────────────
    aliases = [str(a) for a in meta.get("aliases", [])]
    if len(aliases) < 4:
        r.warn(f"Only {len(aliases)} aliases (minimum 4: >=2 Spanish, >=1 natural query variant)")
    else:
        es_count = sum(1 for a in aliases if _looks_spanish(a))
        if es_count < 2:
            r.warn(f"Only {es_count} Spanish-looking aliases — need >=2 for Spanish-language RAG recall")

    # ── process_tags: warn for billing/ chunks with only generic tags ────────
    # Suggestion intentionally omits specific tag names — the right tag depends
    # on the chunk's topic and the agent must decide, not copy from the warning.
    tags = set(meta.get("process_tags", []))
    if area == "billing" and tags == {"order-to-cash", "billing"}:
        r.warn(
            "process_tags uses only generic tags ['billing', 'order-to-cash']. "
            "If the chunk has a specific sub-topic (credit memos, billing plans, "
            "invoice lists, returns, etc.) add the matching tag from the valid list in CLAUDE.md."
        )

    # ── inferred comment → quality must not be high ───────────────────────────
    if "<!-- inferred" in body and meta.get("quality") == "high":
        r.error(
            "quality: high is incompatible with an '<!-- inferred ... -->' comment. "
            "An unverified element is present — downgrade to quality: medium."
        )

    # ── Date format: created and last_updated must be YYYY-MM-DD ─────────────
    date_re = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    for field in ("created", "last_updated"):
        val = str(meta.get(field, ""))
        if not date_re.match(val):
            r.error(f"'{field}' is not a valid YYYY-MM-DD date: '{val}'")

    # ── Schema version ────────────────────────────────────────────────────────
    if meta.get("schema_version") != 1:
        r.warn(f"schema_version is {meta.get('schema_version')!r} — expected 1")

    return r


# ── Batch-level audit ────────────────────────────────────────────────────────
def batch_audit(all_paths_metas: list[tuple]) -> list[str]:
    issues = []

    all_ids  = {m.get("id", "") for _, m in all_paths_metas}
    ref_counts: collections.Counter = collections.Counter()

    for path, meta in all_paths_metas:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            body = text.split("---", 2)[2] if text.count("---") >= 2 else ""
        except Exception:
            continue
        for ref in re.findall(r'\b[a-z][a-z0-9-]+-\d{3}\b', body):
            ref_counts[ref] += 1

    # Isolated nodes (no other chunk links to them)
    isolated = sorted(
        m.get("id", path.stem)
        for path, m in all_paths_metas
        if m.get("id", "") not in ref_counts
    )
    if isolated:
        preview = ", ".join(isolated[:4]) + ("…" if len(isolated) > 4 else "")
        issues.append(
            f"{len(isolated)} chunks are never referenced by any sibling "
            f"(isolated nodes): {preview}"
        )

    # Quality distribution sanity
    q_dist: collections.Counter = collections.Counter(
        m.get("quality") for _, m in all_paths_metas
    )
    total = sum(q_dist.values())
    if total > 5 and len(q_dist) == 1:
        issues.append(
            f"All {total} chunks share the same quality '{list(q_dist)[0]}' — "
            "uniform distribution is a calibration smell, re-check each chunk independently"
        )
    elif total > 10:
        pct_high = q_dist.get("high", 0) / total
        if pct_high > 0.90:
            issues.append(
                f"{q_dist['high']}/{total} chunks rated 'high' ({pct_high:.0%}) — "
                "unusually high proportion; verify quality criteria were applied strictly"
            )

    # Max page cited (sanity check for printed-vs-physical offset)
    max_page = 0
    for _, m in all_paths_metas:
        for s in m.get("sources", []):
            for n in re.findall(r'\d+', str(s.get("pages", ""))):
                max_page = max(max_page, int(n))
    if max_page > 0:
        issues.append(
            f"Max cited page across corpus: {max_page}. "
            "Compare to physical page count; if well below, you may be citing printed labels instead of physical pages."
        )

    return issues


# ── Entry point ──────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="SAP SD KB Chunk Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "target", nargs="?", default="chunks",
        help="Chunks directory OR single .md file (default: chunks/)",
    )
    parser.add_argument("--area",     help="Restrict to one area folder (e.g. billing)")
    parser.add_argument("--no-batch", action="store_true", help="Skip batch-level audit")
    parser.add_argument("--json",     action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()

    target = pathlib.Path(args.target)

    # Collect paths
    if target.is_file():
        chunk_paths = [target]
    elif target.is_dir():
        chunk_paths = sorted(
            p for p in target.rglob("*.md")
            if not p.name.startswith("_")
        )
        if args.area:
            chunk_paths = [p for p in chunk_paths if p.parent.name == args.area]
    else:
        print(f"ERROR: '{target}' is not a file or directory", file=sys.stderr)
        sys.exit(1)

    if not chunk_paths:
        print("No chunk files found.")
        sys.exit(0)

    # First pass: collect ALL chunk IDs for cross-reference resolution.
    # Always scan the root chunks/ directory regardless of filtering, so cross-refs
    # to other areas resolve correctly when --area or a subdirectory path is used.
    all_ids: set[str] = set()
    # Resolve root chunks dir: walk up from target until we find chunks/ or hit cwd
    def _find_chunks_root(p: pathlib.Path) -> pathlib.Path:
        candidate = p if p.is_dir() else p.parent
        while candidate != candidate.parent:
            if candidate.name == "chunks":
                return candidate
            if (candidate / "chunks").is_dir():
                return candidate / "chunks"
            candidate = candidate.parent
        return pathlib.Path("chunks")  # fallback to cwd-relative
    global_chunks_dir = _find_chunks_root(target)
    for p in global_chunks_dir.rglob("*.md"):
        if p.name.startswith("_"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            if text.startswith("---") and text.count("---") >= 2:
                m = yaml.safe_load(text.split("---", 2)[1])
                if isinstance(m, dict) and "id" in m:
                    all_ids.add(m["id"])
        except Exception:
            pass

    # Build all_paths_metas only for the chunks being validated
    all_paths_metas: list[tuple] = []
    for p in chunk_paths:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            if text.startswith("---") and text.count("---") >= 2:
                m = yaml.safe_load(text.split("---", 2)[1])
                if isinstance(m, dict) and "id" in m:
                    all_paths_metas.append((p, m))
        except Exception:
            pass

    # Second pass: validate
    results: list[ChunkResult] = [validate_chunk(p, all_ids) for p in chunk_paths]

    # ── JSON output ──────────────────────────────────────────────────────────
    if args.json:
        out = {
            "chunks": [
                {
                    "label":    r.label,
                    "ok":       r.ok(),
                    "errors":   r.errors,
                    "warnings": r.warnings,
                }
                for r in results
            ]
        }
        if not args.no_batch and all_paths_metas:
            out["batch"] = batch_audit(all_paths_metas)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(0 if all(r.ok() for r in results) else 1)

    # ── Human output ─────────────────────────────────────────────────────────
    errors_total = warns_total = 0

    for r in results:
        if r.errors:
            print(_red(_bold(f"FAIL  {r.label}")))
            for e in r.errors:
                print(f"      {_red('ERROR')} {e}")
            for w in r.warnings:
                print(f"      {_yellow('WARN')}  {w}")
        elif r.warnings:
            print(_yellow(f"WARN  {r.label}"))
            for w in r.warnings:
                print(f"      {_yellow('WARN')}  {w}")
        else:
            print(_green(f"OK    {r.label}"))

        errors_total += len(r.errors)
        warns_total  += len(r.warnings)

    # -- Batch audit -----------------------------------------─────────────────
    if not args.no_batch and all_paths_metas:
        batch_issues = batch_audit(all_paths_metas)
        if batch_issues:
            print()
            print(_bold("-- Batch audit -----------------------------------------"))
            for issue in batch_issues:
                print(f"  {_yellow('WARN')}  {issue}")
            warns_total += len(batch_issues)

    # -- Summary ---------------------------------------------─────────────────
    passed = sum(1 for r in results if r.ok())
    failed = len(results) - passed

    print()
    print(_bold("-- Summary ---------------------------------------------"))
    status_str = _green("ALL PASS") if failed == 0 else _red(f"{failed} FAIL")
    print(
        f"  {len(results)} chunks   "
        f"{_green(str(passed))} OK   "
        f"{status_str}   "
        f"{errors_total} errors   "
        f"{_yellow(str(warns_total))} warnings"
    )

    sys.exit(0 if errors_total == 0 else 1)


if __name__ == "__main__":
    main()
