"""
Build WAEC Catalogue
Scans all WAEC .md files in data/, parses questions, and outputs
data/waec_catalogue.json for the API to serve.
"""

import os
import json
import re
import sys

# Canonical WAEC data directory (deduplicated — use Academic/Secondary/WAEC as the source of truth)
WAEC_DIRS = [
    os.path.join("data", "Academic", "Secondary", "WAEC"),
    os.path.join("data", "Academics", "WAEC"),
    # Misplaced ones in NECO folder
    os.path.join("data", "Academics", "NECO"),
]

OUTPUT_FILE = os.path.join("data", "waec_catalogue.json")


def extract_year_subject(filename):
    """Extract year and subject from filename like WAEC_Biology_2010.md"""
    base = os.path.splitext(os.path.basename(filename))[0]
    # Pattern: WAEC_Subject_Year or WAEC_Subject_More_Year
    match = re.match(r"WAEC_(.+?)_(\d{4})$", base)
    if match:
        subject = match.group(1).replace("_", " ")
        year = int(match.group(2))
        return subject, year
    return None, None


def parse_questions_from_md(filepath):
    """Parse MCQ questions from markdown file."""
    questions = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Split on question numbers: **1.** **2.** etc.
    blocks = re.split(r"\n\*\*(\d+)\.\*\*", content)

    for i in range(1, len(blocks), 2):
        q_num = int(blocks[i])
        body = blocks[i + 1].strip() if i + 1 < len(blocks) else ""

        lines = [l.strip() for l in body.split("\n") if l.strip()]
        if not lines:
            continue

        # First line is question text
        q_text = re.sub(r"^\*\*|\*\*$", "", lines[0]).strip()

        choices = {}
        answer = None
        explanation = ""

        for line in lines[1:]:
            # Choice lines: A) ... or A) ...
            choice_match = re.match(r"^([A-Da-d])\)\s+(.+)", line)
            if choice_match:
                choices[choice_match.group(1).upper()] = choice_match.group(2).strip()
                continue

            # Answer line: **Answer: B** or Answer: B
            ans_match = re.search(r"\*?Answer:\s*([A-Da-d])\*?", line, re.IGNORECASE)
            if ans_match:
                answer = ans_match.group(1).upper()
                continue

            # Explanation line: *Explanation: ...*
            exp_match = re.match(r"\*?Explanation:\s*(.+?)\*?$", line, re.IGNORECASE)
            if exp_match:
                explanation = exp_match.group(1).strip()

        if q_text and choices and answer:
            questions.append({
                "number": q_num,
                "text": q_text,
                "choices": choices,
                "answer": answer,
                "explanation": explanation,
            })

    return questions


def build_catalogue():
    catalogue = {}  # { subject: { year: [questions] } }
    seen_files = set()  # Avoid duplicating same file from multiple dirs

    for root_dir in WAEC_DIRS:
        if not os.path.exists(root_dir):
            continue
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in sorted(filenames):
                if not fname.startswith("WAEC_") or not fname.endswith(".md"):
                    continue

                full_path = os.path.join(dirpath, fname)
                # Deduplicate by filename
                if fname in seen_files:
                    continue
                seen_files.add(fname)

                subject, year = extract_year_subject(fname)
                if not subject or not year:
                    continue

                questions = parse_questions_from_md(full_path)
                if not questions:
                    # Still include file as empty slot
                    questions = []

                if subject not in catalogue:
                    catalogue[subject] = {}
                catalogue[subject][str(year)] = {
                    "year": year,
                    "subject": subject,
                    "question_count": len(questions),
                    "questions": questions,
                }

    # Sort subjects and years
    sorted_catalogue = {}
    for subject in sorted(catalogue.keys()):
        sorted_catalogue[subject] = dict(
            sorted(catalogue[subject].items(), key=lambda x: int(x[0]))
        )

    # Build summary
    summary = []
    for subject, years in sorted_catalogue.items():
        total_q = sum(y["question_count"] for y in years.values())
        summary.append({
            "subject": subject,
            "years": sorted([int(y) for y in years.keys()]),
            "total_questions": total_q,
        })

    output = {
        "subjects": summary,
        "data": sorted_catalogue,
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[OK] WAEC catalogue built: {OUTPUT_FILE}")
    print(f"   Subjects: {len(sorted_catalogue)}")
    for s in summary:
        print(f"   - {s['subject']}: {len(s['years'])} years, {s['total_questions']} questions")


if __name__ == "__main__":
    # Run from project root
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    build_catalogue()
