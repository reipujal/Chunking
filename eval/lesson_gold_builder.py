"""
lesson_gold_builder.py

Builds lesson-level gold sets from SAP course TOC structural data.

Assignment method: STRUCTURAL ONLY.
  - Lesson titles are derived from TOC (not content)
  - Page spans are derived from TOC footer page numbers + confirmed per-doc offsets
  - No content-overlap used for assignment

Queries = lesson titles (clean structural signal: consultant searches by topic)
Gold spans = [lesson_start_phys, lesson_end_phys]
"""

import json
from pathlib import Path
from datetime import date

GOLD_DIR = Path("eval/gold")

# Confirmed per-doc offsets (from processing log and spot-check validation)
OFFSETS = {
    "S4600": 8,
    "S4605": 8,
    "S4610": 6,
    "S4615": 8,
    "S4620": 6,
}

# TOC-derived lesson structure: (unit_label, lesson_title, start_footer, end_footer)
# end_footer = next entry start - 1 (for last lesson: conservative upper bound)
# Source: TOC pages extracted with pdftotext -f 1 -l 8, validated against unit-level gold
#
# Excluded: "Course Overview" stub lessons, Workshop/Appendix units (not substantive chunks)

TOC_LESSONS = {

    "S4600": [
        # Unit 1: 1 lesson
        ("Unit 1: Navigation with SAP Fiori",
         "Identifying Key Features of SAP Fiori", 2, 9),
        # Unit 2: 1 lesson
        ("Unit 2: Enterprise Structures",
         "Identifying Enterprise Structures in SAP S/4HANA Sales", 11, 22),
        # Unit 3: 5 lessons
        ("Unit 3: Overview of Sales Processes",
         "Executing SAP S/4HANA Sales Processes", 24, 30),
        ("Unit 3: Overview of Sales Processes",
         "Processing Sales Documents", 31, 33),
        ("Unit 3: Overview of Sales Processes",
         "Processing Outbound Deliveries", 34, 36),
        ("Unit 3: Overview of Sales Processes",
         "Shipping Goods", 37, 39),
        ("Unit 3: Overview of Sales Processes",
         "Processing Billing Documents", 40, 48),
        # Unit 4: 5 lessons
        ("Unit 4: Master Data",
         "Maintaining Business Partner Master Data", 50, 55),
        ("Unit 4: Master Data",
         "Maintaining Material Master Data", 56, 59),
        ("Unit 4: Master Data",
         "Maintaining Customer-Material Info Records", 60, 61),
        ("Unit 4: Master Data",
         "Maintaining Condition Master Data for Pricing", 62, 64),
        ("Unit 4: Master Data",
         "Explaining Additional Master Data Topics", 65, 74),
        # Unit 5: 2 lessons
        ("Unit 5: Automatic Data Determination and Scheduling",
         "Analyzing the Results of Automatic Data Determination", 76, 80),
        ("Unit 5: Automatic Data Determination and Scheduling",
         "Analyzing the Results of Delivery and Transportation Scheduling", 81, 87),
        # Unit 6: 2 lessons
        ("Unit 6: Availability Check",
         "Performing an Availability Check - Basics", 89, 95),
        ("Unit 6: Availability Check",
         "Performing an Availability Check - Further Topics", 96, 107),
        # Unit 7: 1 lesson
        ("Unit 7: Collective Processing",
         "Executing Collective Processing", 109, 117),
        # Unit 8: 3 lessons
        ("Unit 8: Additional Processes in Sales",
         "Using Presales Documents", 119, 121),
        ("Unit 8: Additional Processes in Sales",
         "Executing Make-to-Order Production", 122, 124),
        ("Unit 8: Additional Processes in Sales",
         "Selling Service Products", 125, 129),
        # Unit 9: 3 lessons
        ("Unit 9: Complaints Processing",
         "Creating Credit Memo Requests", 131, 134),
        ("Unit 9: Complaints Processing",
         "Cancelling Billing Documents", 135, 135),
        ("Unit 9: Complaints Processing",
         "Creating Returns", 136, 139),
        # Unit 10: 3 lessons
        ("Unit 10: Monitoring and Sales Analytics",
         "Utilizing the Sales Order Fulfillment App", 141, 147),
        ("Unit 10: Monitoring and Sales Analytics",
         "Managing Sales Plans", 148, 149),
        ("Unit 10: Monitoring and Sales Analytics",
         "Using Analytical Apps", 150, 160),
    ],

    "S4605": [
        # Unit 2: 1 lesson
        ("Unit 2: Introduction",
         "Introduction to the Sales and Distribution Process", 4, 7),
        # Unit 3: 1 lesson
        ("Unit 3: Enterprise Structures in Sales and Distribution",
         "Enterprise Structures in Sales and Distribution", 9, 20),
        # Unit 4: 2 lessons
        ("Unit 4: Sales Order Processing",
         "Source of Data", 22, 31),
        ("Unit 4: Sales Order Processing",
         "Order Processing - Special Features", 32, 38),
        # Unit 5: 3 lessons
        ("Unit 5: Controlling Sales Documents",
         "Controlling Sales Documents - Sales Document Type", 40, 44),
        ("Unit 5: Controlling Sales Documents",
         "Controlling Sales Documents - Item Category", 45, 51),
        ("Unit 5: Controlling Sales Documents",
         "Controlling Sales Documents - Schedule Line Categories", 52, 59),
        # Unit 6: 2 lessons
        ("Unit 6: Data Flow",
         "Data Flow in the Application", 61, 66),
        ("Unit 6: Data Flow",
         "Copying Control", 67, 72),
        # Unit 7: 1 lesson
        ("Unit 7: Special Business Transactions",
         "Special Business Transactions", 74, 79),
        # Unit 8: 1 lesson
        ("Unit 8: Incompletion",
         "Incompletion Check and its Configuration", 81, 87),
        # Unit 9: 2 lessons
        ("Unit 9: Partner Functions in SD",
         "Function and Significance of Partner Functions", 89, 92),
        ("Unit 9: Partner Functions in SD",
         "Configuration of Partner Functions and Partner Function Determination", 93, 99),
        # Unit 10: 2 lessons
        ("Unit 10: Outline Agreements",
         "Scheduling Agreements and Quantity Contracts", 101, 105),
        ("Unit 10: Outline Agreements",
         "Value Contracts", 106, 118),
        # Unit 11: 2 lessons
        ("Unit 11: Material Determination, Listing and Exclusion",
         "Material Determination", 120, 128),
        ("Unit 11: Material Determination, Listing and Exclusion",
         "Material Listing and Exclusion", 129, 134),
        # Unit 12: 1 lesson
        ("Unit 12: Free Goods",
         "Free Goods", 136, 144),
    ],

    "S4610": [
        # Unit 1: 1 lesson
        ("Unit 1: Idea and Function of the Delivery Document",
         "Explaining the Concept and Structure of the Delivery Document", 2, 10),
        # Unit 2: 1 lesson
        ("Unit 2: Basic Organizational Units for the Delivery Process",
         "Maintaining the Organizational Units for Delivery Processes", 12, 20),
        # Unit 3: 1 lesson
        ("Unit 3: Controlling Deliveries",
         "Controlling Delivery Documents", 22, 34),
        # Unit 4: 4 lessons
        ("Unit 4: The Goods Issue Process Based on the Delivery",
         "Adjusting Automatic Determination of Relevant Fields for Outbound Delivery Creation", 36, 41),
        ("Unit 4: The Goods Issue Process Based on the Delivery",
         "Adjusting Delivery and Transportation Scheduling", 42, 46),
        ("Unit 4: The Goods Issue Process Based on the Delivery",
         "Processing Outbound Deliveries", 47, 54),
        ("Unit 4: The Goods Issue Process Based on the Delivery",
         "Using the Outbound Delivery Monitor", 55, 62),
        # Unit 5: 4 lessons
        ("Unit 5: Processes and Functions based on the Delivery with Embedded EWM",
         "Picking Outbound Deliveries with EWM", 64, 69),
        ("Unit 5: Processes and Functions based on the Delivery with Embedded EWM",
         "Posting Goods Issue", 70, 71),
        ("Unit 5: Processes and Functions based on the Delivery with Embedded EWM",
         "Creating Inbound Deliveries in EWM", 72, 75),
        ("Unit 5: Processes and Functions based on the Delivery with Embedded EWM",
         "Using Special Functions in Deliveries", 76, 86),
    ],

    "S4615": [
        # Unit 1: 1 lesson
        ("Unit 1: Billing Documents in Sales and Distribution Processes",
         "Integrating Billing Documents in the Sales and Distribution Process", 2, 5),
        # Unit 2: 1 lesson
        ("Unit 2: Organizational Units",
         "Setting Up Organizational Units", 7, 11),
        # Unit 3: 1 lesson
        ("Unit 3: The Billing Process",
         "Controlling the Billing Process", 13, 19),
        # Unit 4: 1 lesson
        ("Unit 4: Special Billing Types",
         "Processing Special Billing Types", 21, 31),
        # Unit 5: 1 lesson
        ("Unit 5: Data Flow",
         "Setting Up the Data Flow for Billing Documents", 33, 42),
        # Unit 6: 1 lesson
        ("Unit 6: Billing Document Creation",
         "Creating Billing Documents in Different Ways", 44, 52),
        # Unit 7: 2 lessons
        ("Unit 7: Types of Settlement",
         "Analyzing Invoice Combination and Invoice Split", 54, 56),
        ("Unit 7: Types of Settlement",
         "Understanding Special Types of Settlement", 57, 66),
        # Unit 8: 3 lessons
        ("Unit 8: Special Business Processes",
         "Setting Up Billing Plans", 68, 74),
        ("Unit 8: Special Business Processes",
         "Processing Down Payments", 75, 80),
        ("Unit 8: Special Business Processes",
         "Processing Installment Payments", 81, 86),
        # Unit 9: 1 lesson
        ("Unit 9: Account Determination",
         "Setting Up the Account Determination", 88, 93),
        # Unit 10: 1 lesson
        ("Unit 10: Interface Between Sales and Distribution and Financial Accounting",
         "Adjusting the Interface Between Sales and Distribution and Financial Accounting", 95, 103),
    ],

    "S4620": [
        # Unit 1: 2 lessons
        ("Unit 1: Condition Technique in Pricing",
         "Introducing Pricing", 2, 5),
        ("Unit 1: Condition Technique in Pricing",
         "Introducing the Condition Technique", 6, 17),
        # Unit 2: 2 lessons
        ("Unit 2: Pricing Configuration",
         "Configuring Pricing", 19, 25),
        ("Unit 2: Pricing Configuration",
         "Further Options for Pricing Control", 26, 32),
        # Unit 3: 2 lessons
        ("Unit 3: Condition Records",
         "Working with Condition Records", 34, 37),
        ("Unit 3: Condition Records",
         "Reports for Condition Records", 38, 46),
        # Unit 4: 1 lesson
        ("Unit 4: Special Functions",
         "Applying Special Pricing Functions", 48, 55),
        # Unit 5: 3 lessons
        ("Unit 5: Condition Types",
         "Using Special Condition Types", 57, 65),
        ("Unit 5: Condition Types",
         "Using Statistical Condition Types", 66, 69),
        ("Unit 5: Condition Types",
         "Analyzing the Determination of Taxes", 70, 77),
        # Unit 6: 1 lesson
        ("Unit 6: Pricing Agreements",
         "Using Pricing Agreements", 79, 84),
        # Unit 7: 3 lessons
        ("Unit 7: Introduction to Condition Contract Management",
         "Introducing Condition Contract Management", 86, 93),
        ("Unit 7: Introduction to Condition Contract Management",
         "Maintaining of Condition Contracts", 94, 100),
        ("Unit 7: Introduction to Condition Contract Management",
         "Processing of Condition Contract Settlement", 101, 112),
    ],
}


def build_lesson_gold(src: str) -> dict:
    offset = OFFSETS[src]
    lessons = TOC_LESSONS[src]

    questions = []
    for i, (unit_label, lesson_title, start_footer, end_footer) in enumerate(lessons):
        phys_start = start_footer + offset
        phys_end = end_footer + offset

        q_id = f"{src}-LG-{i+1:03d}"
        questions.append({
            "id": q_id,
            "unit": unit_label,
            "lesson": lesson_title,
            "gold_page_span": [phys_start, phys_end],
            "question": lesson_title,
            "lesson_assignment_method": "toc_structural",
            "excluded": False,
        })

    return {
        "source": src,
        "offset": offset,
        "gold_level": "lesson",
        "built": date.today().isoformat(),
        "assignment_method": "toc_structural",
        "note": (
            "Queries = lesson titles from TOC (structural, no content-overlap). "
            "Spans = TOC footer page ranges converted via confirmed per-doc offset. "
            "Excluded: Course Overview, Workshop, and Appendix units."
        ),
        "questions": questions,
    }


def validate_against_unit_gold(src: str, lesson_gold: dict) -> list[str]:
    """Spot-check: lesson spans should fall within unit gold spans."""
    unit_gold_path = GOLD_DIR / f"{src}_assessments.json"
    if not unit_gold_path.exists():
        return [f"Unit gold not found: {unit_gold_path}"]

    with open(unit_gold_path, encoding="utf-8") as f:
        ug = json.load(f)

    unit_spans = {}
    for q in ug["questions"]:
        unit = q["unit"]
        span = q["gold_page_span"]
        if unit not in unit_spans:
            unit_spans[unit] = span
        else:
            existing = unit_spans[unit]
            unit_spans[unit] = [min(existing[0], span[0]), max(existing[1], span[1])]

    issues = []
    for lq in lesson_gold["questions"]:
        unit = lq["unit"]
        lspan = lq["gold_page_span"]

        # Find matching unit span (by unit label prefix)
        matched = None
        for u, uspan in unit_spans.items():
            if lq["unit"].split(":")[0].strip() in u or u.split(":")[0].strip() in lq["unit"]:
                matched = (u, uspan)
                break

        if matched is None:
            continue  # Unit not in unit gold (e.g. Unit 10 of S4600 not mapped to original)

        u, uspan = matched
        # Lesson span start should be >= unit span start and end should be reasonable
        if lspan[0] < uspan[0] - 2:
            issues.append(f"{lq['id']}: lesson start {lspan[0]} < unit start {uspan[0]}")

    return issues


def main():
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    for src in ["S4600", "S4605", "S4610", "S4615", "S4620"]:
        print(f"\n=== Building lesson gold: {src} ===")
        lg = build_lesson_gold(src)

        n = len(lg["questions"])
        print(f"  {n} lesson queries")
        print(f"  Offset: {lg['offset']} (phys = footer + {lg['offset']})")

        # Show first 3 entries
        for q in lg["questions"][:3]:
            print(f"  {q['id']}: '{q['lesson']}' span={q['gold_page_span']}")

        # Validate
        issues = validate_against_unit_gold(src, lg)
        if issues:
            print(f"  VALIDATION ISSUES:")
            for iss in issues:
                print(f"    - {iss}")
        else:
            print("  Validation: OK (lesson spans consistent with unit gold)")

        # Write
        out_path = GOLD_DIR / f"{src}_lesson_gold.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(lg, f, indent=2, ensure_ascii=False)
        print(f"  Written: {out_path}")

    print("\nDone. Run lesson_gold_probe.py to score A/B/C.")


if __name__ == "__main__":
    main()
