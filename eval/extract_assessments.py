"""
extract_assessments.py — Extract SAP Learning Assessment questions from a PDF.

Gold source: only the "Learning Assessment" sections written by SAP.
gold_page_span = physical pages of the unit content (NOT the LA page itself).
Physical page = footer page + offset.

Usage:
    python eval/extract_assessments.py --src S4620
    python eval/extract_assessments.py --src S4620 --pdf "path/to/file.pdf"
"""

import re
import json
import subprocess
import argparse
from pathlib import Path
from datetime import date

SOURCE_ROOT = Path("docu sap")
OUTPUT_DIR = Path("eval/gold")


def get_pages_text(pdf_path: Path) -> list[str]:
    r = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True
    )
    return r.stdout.split("\f")


def detect_offset(pages: list[str]) -> int:
    """Return offset such that physical_page = footer_page + offset.
    Scans early pages for the one whose copyright footer reads '1'.
    """
    for phys_idx, page in enumerate(pages[:25]):
        for line in reversed(page.strip().splitlines()):
            m = re.search(r"Copyright.*reserved\.\s+1\s*$", line)
            if m:
                return phys_idx  # phys_idx+1 is the 1-indexed physical page
    return 6  # fallback


def parse_toc_units(pages: list[str], offset: int) -> dict[int, dict]:
    """Parse TOC pages to get {unit_num: {name, footer_start, phys_start}}.
    Scans pages 1-8 looking for the Contents page.
    """
    toc_text = "\n".join(pages[1:9])
    units = {}
    for m in re.finditer(
        r"^(\d+)\s+Unit\s+(\d+)[:\s]+(.+)$", toc_text, re.MULTILINE
    ):
        footer_start = int(m.group(1))
        unit_num = int(m.group(2))
        name = m.group(3).strip()
        units[unit_num] = {
            "name": name,
            "footer_start": footer_start,
            "phys_start": footer_start + offset,
        }
    return units


def get_page_footer_num(page: str) -> int | None:
    """Extract the decimal footer page number from a page."""
    for line in reversed(page.strip().splitlines()):
        m = re.search(r"Copyright.*reserved\.\s+(\d+)\s*$", line)
        if m:
            return int(m.group(1))
    return None


def get_unit_from_page(page: str) -> int | None:
    m = re.search(r"\bUnit\s+(\d+)\b", page)
    return int(m.group(1)) if m else None


def find_la_blocks(pages: list[str], units: dict[int, dict] | None = None) -> list[dict]:
    """Find LA pages and assign them to units using TOC unit boundaries.

    Assignment priority:
      1. 'Unit N' text found on the page (most reliable for answer pages).
      2. TOC boundary: whichever unit's phys_start is <= phys (highest such start wins).

    Returns list of {unit, q_pages, a_pages, phys_range}.
    phys pages are 1-indexed.
    """
    from collections import defaultdict

    # Build sorted boundary list: [(phys_start, unit_num), ...]
    sorted_boundaries: list[tuple[int, int]] = []
    if units:
        sorted_boundaries = sorted(
            (info["phys_start"], u_num) for u_num, info in units.items()
        )

    def toc_unit_for_phys(phys: int) -> int | None:
        result = None
        for phys_start, u_num in sorted_boundaries:
            if phys_start <= phys:
                result = u_num
            else:
                break
        return result

    unit_q: dict[int | None, list[int]] = defaultdict(list)
    unit_a: dict[int | None, list[int]] = defaultdict(list)

    for i, page in enumerate(pages):
        if "Learning Assessment" not in page:
            continue
        phys = i + 1
        is_answer = "Answers" in page or bool(re.search(r"(?:That's c|C)orrect\.\s", page))

        # Priority 1: explicit "Unit N" header on the page
        u: int | None = get_unit_from_page(page) if "Unit" in page else None
        # Priority 2: TOC boundary
        if u is None:
            u = toc_unit_for_phys(phys)

        if is_answer:
            unit_a[u].append(phys)
        else:
            unit_q[u].append(phys)

    # Build one block per unit
    all_unit_keys = sorted(
        set(list(unit_q.keys()) + list(unit_a.keys())),
        key=lambda x: (x is None, x or 0),
    )
    result = []
    for u in all_unit_keys:
        bq = sorted(unit_q.get(u, []))
        ba = sorted(unit_a.get(u, []))
        all_p = bq + ba
        if all_p:
            result.append({
                "unit": u,
                "q_pages": bq,
                "a_pages": ba,
                "phys_range": (min(all_p), max(all_p)),
            })
    return result


def parse_questions_from_text(text: str) -> list[dict]:
    """Parse questions from one or more LA pages (concatenated text)."""
    questions = []
    # Remove header lines
    text = re.sub(r"Learning Assessment.*\n", "", text)
    text = re.sub(r"©\s*Copyright.*\n?", "", text)

    # Split by question numbers at line-start
    parts = re.split(r"\n(?=\s*\d+\.\s)", text)

    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"(\d+)\.\s+(.*)", part, re.DOTALL)
        if not m:
            continue

        q_num = int(m.group(1))
        body = m.group(2)

        # Detect type
        has_tf = bool(re.search(r"X\s+True", body)) and bool(re.search(r"X\s+False", body))
        has_mcq = bool(re.search(r"X\s+[A-D]\s+", body))

        if has_tf:
            q_type = "tf"
            # Question text is everything before "Determine whether..." or before "X True"
            q_text = re.split(r"\s*Determine whether\s+this statement.*?false\s*\.\s*", body, flags=re.IGNORECASE)[0]
            q_text = re.split(r"\s*X\s+True", q_text)[0]
            options = {"True": "True", "False": "False"}
        elif has_mcq:
            q_type = "mcq"
            # Find first option
            first_opt = re.search(r"X\s+[A-D]\s+", body)
            q_text = body[: first_opt.start()] if first_opt else body
            # Remove instruction line
            q_text = re.sub(
                r"\s*Choose the correct answers?\.\s*$", "", q_text, flags=re.IGNORECASE
            )
            # Extract options
            options = {}
            for om in re.finditer(
                r"X\s+([A-D])\s+(.*?)(?=\n\s*X\s+[A-D]|\n\s*(?:Correct\.)|\Z)",
                body, re.DOTALL,
            ):
                letter = om.group(1)
                opt_text = re.sub(r"\s+", " ", om.group(2)).strip()
                opt_text = re.sub(r"©\s*Copyright.*", "", opt_text).strip()
                options[letter] = opt_text
        else:
            q_type = "unknown"
            q_text = body
            options = {}

        q_text = re.sub(r"\s+", " ", q_text).strip()
        # Remove trailing instruction if still there
        q_text = re.sub(
            r"\s*Determine whether this statement is true or false\.?\s*$",
            "", q_text, flags=re.IGNORECASE,
        ).strip()
        q_text = re.sub(
            r"\s*Choose the correct answers?\.\s*$",
            "", q_text, flags=re.IGNORECASE,
        ).strip()

        # Detect multi-answer MCQ (instruction says "answers" plural)
        multi_answer = q_type == "mcq" and bool(
            re.search(r"Choose the correct answers\b", part, re.IGNORECASE)
        )

        questions.append({
            "num": q_num,
            "text": q_text,
            "type": q_type,
            "options": options,
            "multi_answer": multi_answer,
        })

    return questions


def parse_answer_explanations(text: str) -> dict[int, str]:
    """Extract {question_num: explanation_text} from answer page text."""
    results: dict[int, str] = {}
    text = re.sub(r"Learning Assessment.*Answers.*\n", "", text)
    text = re.sub(r"©\s*Copyright.*\n?", "", text)

    parts = re.split(r"\n(?=\s*\d+\.\s)", text)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"(\d+)\.\s+(.*)", part, re.DOTALL)
        if not m:
            continue
        q_num = int(m.group(1))
        body = m.group(2)
        cm = re.search(r"(?:That's c|C)orrect\.\s+(.*)", body, re.DOTALL)
        if cm:
            explanation = re.sub(r"\s+", " ", cm.group(1)).strip()
            explanation = re.sub(r"©\s*Copyright.*", "", explanation).strip()
            results[q_num] = explanation
    return results


def determine_correct(q: dict, explanation: str) -> str | None:
    """Best-effort heuristic to derive the correct answer letter/bool from explanation."""
    if not explanation:
        return None

    if q["type"] == "tf":
        stmt = q["text"].lower()
        expl = explanation.lower()

        # Contradictions: if a key word in statement is replaced by its opposite
        contradiction_pairs = [
            ("manually", "automatically"),
            ("automatic", "manual"),
            ("only", "more than one"),
            ("only one", "more than"),
            ("cannot", "can"),
            ("always", "never"),
            ("never", "always"),
            ("asynchronous", "synchronous"),
            ("synchronous", "asynchronous"),
            ("outbound", "inbound"),
            ("inbound", "outbound"),
            ("replicate", "update"),
        ]
        for stmt_word, expl_word in contradiction_pairs:
            if stmt_word in stmt and expl_word in expl and stmt_word not in expl:
                return "False"

        # High word overlap → True
        stopwords = {"the", "a", "an", "is", "are", "in", "of", "to", "and",
                     "or", "for", "can", "you", "it", "this", "that", "be",
                     "has", "have", "by", "with", "at", "on", "as", "from"}
        stmt_words = set(re.findall(r"\b\w+\b", stmt)) - stopwords
        expl_words = set(re.findall(r"\b\w+\b", expl)) - stopwords
        if stmt_words:
            overlap = len(stmt_words & expl_words) / len(stmt_words)
            if overlap >= 0.45:
                return "True"

        return None  # uncertain

    elif q["type"] == "mcq":
        # Multi-answer questions: cannot reliably infer all correct letters from
        # a word-overlap heuristic — return None rather than a partial/wrong answer.
        if q.get("multi_answer"):
            return None

        expl = explanation.lower()
        stopwords = {"the", "a", "an", "is", "are", "in", "of", "to", "and",
                     "or", "for", "can", "you", "it", "this", "that", "be",
                     "has", "have", "by", "with", "at", "on", "as", "from",
                     "which", "that", "these", "those"}
        scores: dict[str, float] = {}
        expl_words = set(re.findall(r"\b\w+\b", expl)) - stopwords
        for letter, opt_text in q["options"].items():
            opt_words = set(re.findall(r"\b\w+\b", opt_text.lower())) - stopwords
            if not opt_words:
                scores[letter] = 0.0
                continue
            scores[letter] = len(opt_words & expl_words) / len(opt_words)

        if not scores:
            return None
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_letter, best_score = sorted_scores[0]
        runner_up = sorted_scores[1][1] if len(sorted_scores) > 1 else 0.0

        # Require: score above threshold AND clearly better than runner-up
        if best_score >= 0.5 and best_score >= runner_up * 1.5:
            return best_letter
        return None

    return None


def is_trivially_excludable(q: dict) -> str | None:
    """Return reason string if question should be excluded, else None."""
    text = q["text"].lower()
    # Meta-questions about the course structure
    meta_patterns = [
        r"\bwhat is the purpose of this (unit|lesson|course)\b",
        r"\bthis lesson (covers|introduces)\b",
        r"\bafter completing this (lesson|unit)\b",
    ]
    for pat in meta_patterns:
        if re.search(pat, text):
            return "meta-question about course structure"
    # Questions with no options and unknown type
    if q["type"] == "unknown" and not q["options"]:
        return "unparseable: no options detected"
    return None


def build_gold_questions(
    block: dict,
    pages: list[str],
    units: dict[int, dict],
    src: str,
    global_counter: dict,
) -> list[dict]:
    """Build gold question records for one LA block."""
    unit_num = block["unit"]
    unit_info = units.get(unit_num, {})
    unit_name = unit_info.get("name", f"Unit {unit_num}")

    # Compute gold_page_span = content pages (unit start to LA page - 1)
    la_first_phys = min(block["q_pages"]) if block["q_pages"] else min(block["a_pages"])
    unit_phys_start = unit_info.get("phys_start")
    if unit_phys_start is None:
        unit_phys_start = la_first_phys - 20  # fallback
    gold_span = [unit_phys_start, la_first_phys - 1]

    # Concatenate question page texts
    q_text_combined = "\n".join(pages[p - 1] for p in sorted(block["q_pages"]))
    # Concatenate answer page texts
    a_text_combined = "\n".join(pages[p - 1] for p in sorted(block["a_pages"]))

    questions_raw = parse_questions_from_text(q_text_combined)
    answer_map = parse_answer_explanations(a_text_combined)

    results = []
    for q in questions_raw:
        global_counter["n"] += 1
        explanation = answer_map.get(q["num"], "")
        correct = determine_correct(q, explanation)
        answer_key_found = bool(explanation)
        exclude_reason = is_trivially_excludable(q)

        q_id = f"{src}-LA-U{unit_num}-Q{q['num']}"

        multi = q.get("multi_answer", False)
        notes = "multi-answer: correct inference not attempted" if multi and correct is None else ""

        record = {
            "id": q_id,
            "unit": f"Unit {unit_num}: {unit_name}",
            "question": q["text"],
            "options": q["options"] if q["type"] == "mcq" else {},
            "question_type": q["type"],
            "multi_answer": multi,
            "correct": correct,
            "answer_key_found": answer_key_found,
            "answer_explanation": explanation if answer_key_found else "",
            "gold_page_span": gold_span,
            "mappable": True,  # will be updated in score.py
            "excluded": exclude_reason is not None,
            "exclude_reason": exclude_reason or "",
            "notes": notes,
        }
        results.append(record)

    return results


def find_pdf(src: str, explicit_path: str | None = None) -> Path:
    if explicit_path:
        return Path(explicit_path)
    candidates = list(SOURCE_ROOT.glob(f"{src}*.pdf")) + list(
        (SOURCE_ROOT / "processed").glob(f"{src}*.pdf")
    )
    if not candidates:
        raise FileNotFoundError(
            f"No PDF found for src={src!r} in {SOURCE_ROOT}"
        )
    return candidates[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Document key, e.g. S4620")
    parser.add_argument("--pdf", help="Explicit PDF path (optional)")
    args = parser.parse_args()

    pdf_path = find_pdf(args.src, args.pdf)
    print(f"PDF: {pdf_path}")

    print("Extracting pages...", flush=True)
    pages = get_pages_text(pdf_path)
    print(f"  Total physical pages: {len(pages)}")

    offset = detect_offset(pages)
    print(f"  Detected offset: {offset} (phys = footer + {offset})")

    units = parse_toc_units(pages, offset)
    print(f"  Units found in TOC: {sorted(units.keys())}")
    for u, info in sorted(units.items()):
        print(f"    Unit {u}: footer {info['footer_start']} -> phys {info['phys_start']}  [{info['name']}]")

    print("\nFinding Learning Assessment pages...")
    blocks = find_la_blocks(pages, units)
    print(f"  LA blocks found: {len(blocks)}")
    for b in blocks:
        print(f"    Unit {b['unit']}: Q={b['q_pages']}  A={b['a_pages']}")

    # Compute unit end pages (next unit start - 1)
    sorted_units = sorted(units.keys())
    for i, u in enumerate(sorted_units):
        if i + 1 < len(sorted_units):
            next_phys_start = units[sorted_units[i + 1]]["phys_start"]
            units[u]["phys_end"] = next_phys_start - 1
        else:
            units[u]["phys_end"] = len(pages)

    print("\nExtracting questions...")
    all_questions: list[dict] = []
    counter = {"n": 0}

    for block in blocks:
        if block["unit"] is None:
            print(f"  WARNING: could not determine unit for block {block['phys_range']}")
            continue
        qs = build_gold_questions(block, pages, units, args.src, counter)
        all_questions.extend(qs)
        print(f"  Unit {block['unit']}: {len(qs)} questions extracted")

    # Stats
    total = len(all_questions)
    with_key = sum(1 for q in all_questions if q["answer_key_found"])
    with_correct = sum(1 for q in all_questions if q["correct"] is not None)
    excluded = sum(1 for q in all_questions if q["excluded"])

    print(f"\nSummary:")
    print(f"  Total extracted:     {total}")
    print(f"  Answer key found:    {with_key}/{total}")
    print(f"  Correct inferred:    {with_correct}/{total}")
    print(f"  Excluded:            {excluded}")
    print(f"  Available for eval:  {total - excluded}")

    # Determine relative PDF path
    try:
        rel_path = str(pdf_path.relative_to(Path("docu sap")))
        rel_path = rel_path.replace("\\", "/")
        if not rel_path.startswith("processed/"):
            rel_path = rel_path
    except ValueError:
        rel_path = str(pdf_path)

    gold = {
        "doc": args.src,
        "pdf_relative_path": rel_path,
        "offset": offset,
        "generated_at": date.today().isoformat(),
        "total_physical_pages": len(pages),
        "questions": all_questions,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{args.src}_assessments.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(gold, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
