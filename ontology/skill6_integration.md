# P2 Integration with Skill 6 — Design Document
Generated: 2026-06-16

## Context

Skill 6 (`docs/skills/6-coverage-review.md`) currently performs dedup via runtime judgment:
the model searches existing chunks by topic keywords and decides primary/secondary/discard
based on domain knowledge. This is correct but not reproducible and loses design-time
decisions that were previously made.

P2 v0 produces a registry that encodes those decisions explicitly. This document describes
how Skill 6 should consult the registry, with minimum changes to the existing skill.

---

## Integration Model

**Registry-first, judgment-fallback.**

1. **Lookup first.** Before evaluating a new source section against existing chunks, look up
   its topic in `ontology/authority_registry.yaml`.

2. **If topic is in registry:** the dedup decision follows from the registry:
   - `authority_pattern: single` + source matches `authoritative_sources` → PRIMARY
   - `authority_pattern: single` + source does not match → SUPPLEMENTARY (if additive) or SKIP
   - `authority_pattern: distributed` → PRIMARY for its specific facet; SUPPLEMENTARY otherwise
   - `authority_pattern: inversion_pending` → new source is PRIMARY; existing chunk demoted to supplementary
   - `authority_pattern: prospective` → new source is PRIMARY (fills the gap)
   - `authority_pattern: deferred` + `in_scope: deferred` → **FLAG for user, do not chunk**
   - `conflict: true` → note the conflict token in the chunk body; do not pick a winner

3. **If topic is NOT in registry:** apply the current Skill-6 judgment. Then **add the topic
   and decision to `ontology/topics.yaml` and `ontology/authority_registry.yaml`** before
   closing the document. This is how the registry grows — every new judgment extends it.

4. **One update per document.** Run the registry update at the end of processing each
   document (after all chunks are written), not after each individual chunk. This keeps
   the registry update atomic per document.

---

## Modified Skill-6 Dedup Protocol (diff from current)

Add this block at the START of the dedup step (Step 3):

```
### 3a — Registry Lookup (NEW, runs before content search)

For each section/unit/lesson being evaluated:

1. Identify the SD topic (business process / function).
2. Look up the topic in ontology/authority_registry.yaml.
   grep -i "TOPIC_KEYWORD" ontology/authority_registry.yaml | head -20
3. Read the authority_pattern and authoritative_sources for the match.
4. Apply the decision rule from the integration model above.
5. Record: topic_id | decision | reason | existing_chunk (if any).

Only if no registry match → proceed to Step 3b (content search / judgment).

### 3b — Judgment (UNCHANGED, fallback only)

Current Skill-6 content search and judgment applies here, unchanged.
After making a judgment: add the new topic to the registry (Step 3c).

### 3c — Registry Update (NEW, after judgment)

When judgment is used (no prior registry entry):
  - Add topic to ontology/topics.yaml (id, label, process_area, notes)
  - Add authority entry to ontology/authority_registry.yaml
  - Add mapping to ontology/chunk_topic_map.json
Run: python3 ontology/_build_chunk_map.py  (or update JSON directly)
```

---

## Lookup Command Reference

```bash
# Look up a topic by keyword
grep -A 20 "topic_id: xfunc.copy" ontology/authority_registry.yaml

# Find the authority for a specific PDF file
grep -B5 "S4650" ontology/authority_registry.yaml | grep "topic_id:"

# Check coverage for a topic
grep -A3 "topic_id: o2c.credit" ontology/coverage_map.md

# Find all topics with 0 chunks (gaps)
grep "| \*\*0\*\*\|★\|☆" ontology/coverage_map.md
```

---

## Cases That Require Human Review (not automatic)

These should be flagged in the processing log, not decided by the agent:

| Condition | Action |
|---|---|
| `conflict: true` in registry | Note conflict in chunk body; do not silently resolve |
| `in_scope: deferred` | Stop; ask user before chunking |
| `authority_pattern: distributed` and new source covers multiple facets | Propose split plan; wait for confirmation |
| New source contradicts a registered authoritative chunk | Register as conflict; document both tokens |
| New topic that spans two existing topic IDs | Propose new ID before registering |

---

## Governance

**The registry is a proposal until validated.** It governs dedup only after explicit user sign-off.

**Validation criteria (this pass — P2 v0):**
- [ ] User reviews topics.yaml for topic granularity and missing topics
- [ ] User reviews authority_registry.yaml for correctness of authoritative_sources
- [ ] User confirms CS/BV conflict resolution is acceptable
- [ ] User confirms xfunc.enhance is correctly deferred
- [ ] User confirms xfunc.output inversion is correct before S4650 Unit 4 is chunked

**After validation:** the registry moves from PROPOSAL to OPERATIVE and Skill 6 uses it
as described above. Record the validation date in a `validated_at` field in topics.yaml.

---

## What the Registry Does NOT Replace

- **Source quality judgment** (Type A vs B vs C vs D): Skill 6 still evaluates this.
- **Density check** (words/page): unchanged.
- **Content-in-source verification**: the agent still reads the actual pages.
- **Coverage gate** (Skill 6 close step): unchanged; the registry informs dedup but
  does not replace the per-page coverage map.

---

## File Locations

| Artifact | Path | How used |
|---|---|---|
| Topic ontology | `ontology/topics.yaml` | Defines valid topic IDs and labels |
| Chunk-topic map | `ontology/chunk_topic_map.json` | Lookup: which chunks cover a topic |
| Authority registry | `ontology/authority_registry.yaml` | Lookup: which source is primary |
| Coverage map | `ontology/coverage_map.md` | Human-readable gap overview |
| S4650 demo | `ontology/s4650_dedup_demo.md` | Reference for S4650 chunking decisions |
