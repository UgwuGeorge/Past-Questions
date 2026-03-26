"""
Data Import Pipeline for Reharz
================================
Supports:
  - JSON files: structured question data (already used)  
  - Markdown files: question files in the format:
      **1.** Question text
         A) Option A
         B) Option B
         **Answer: A**

Run with:
  python agent_core/scripts/import_data.py             # import everything
  python agent_core/scripts/import_data.py --changed   # only git-changed files in data/
"""

import json
import os
import re
import sys
import argparse
import io

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

load_dotenv(os.path.join(project_root, ".env"))

from agent_core.database import SessionLocal, engine, Base
from agent_core.models.main_models import (
    Exam, Subject, Question, Choice, QuestionPaper, QuestionContext,
    ExamCategory, DifficultyLevel
)

Base.metadata.create_all(bind=engine)

# ─── Category Mapping ────────────────────────────────────────────────────────
EXAM_MAP = {
    "WAEC": ExamCategory.ACADEMICS, "JAMB": ExamCategory.ACADEMICS,
    "NABTEB": ExamCategory.ACADEMICS, "NECO": ExamCategory.ACADEMICS,
    "NDA": ExamCategory.ACADEMICS, "POLAC": ExamCategory.ACADEMICS,
    "ICAN": ExamCategory.PROFESSIONAL, "BAR": ExamCategory.PROFESSIONAL,
    "NURSING": ExamCategory.PROFESSIONAL, "MEDICINE": ExamCategory.PROFESSIONAL,
    "TRCN": ExamCategory.PROFESSIONAL, "COREN": ExamCategory.PROFESSIONAL,
    "PCN": ExamCategory.PROFESSIONAL, "CIBN": ExamCategory.PROFESSIONAL,
    "BAR-FINALS": ExamCategory.PROFESSIONAL, "MED-NURSING": ExamCategory.PROFESSIONAL,
    "IELTS": ExamCategory.SCHOLARSHIPS, "PTDF": ExamCategory.SCHOLARSHIPS,
    "BEA": ExamCategory.SCHOLARSHIPS, "NNPC": ExamCategory.SCHOLARSHIPS,
    "TOTAL": ExamCategory.SCHOLARSHIPS, "CHEVENING": ExamCategory.SCHOLARSHIPS,
    "COMMONWEALTH": ExamCategory.SCHOLARSHIPS, "DAAD": ExamCategory.SCHOLARSHIPS,
    "ERASMUS": ExamCategory.SCHOLARSHIPS, "SHELL": ExamCategory.SCHOLARSHIPS,
    "NNPC-TOTAL": ExamCategory.SCHOLARSHIPS,
}

DIFFICULTY_MAP = {
    "EASY": DifficultyLevel.EASY,
    "MEDIUM": DifficultyLevel.MEDIUM,
    "HARD": DifficultyLevel.HARD,
}

def get_category_from_path(file_path: str) -> ExamCategory:
    if "Professional" in file_path:
        return ExamCategory.PROFESSIONAL
    elif "Academics" in file_path or "Academic" in file_path:
        return ExamCategory.ACADEMICS
    elif "Scholarship" in file_path or "scholarship" in file_path or "International" in file_path:
        return ExamCategory.SCHOLARSHIPS
    return ExamCategory.ACADEMICS

def get_or_create_exam(db: Session, exam_name: str, file_path: str, sub_category: str = None) -> Exam:
    exam = db.query(Exam).filter(Exam.name.ilike(exam_name)).first()
    
    # Calculate target category
    key = exam_name.split()[0].upper()
    target_category = EXAM_MAP.get(key, get_category_from_path(file_path))

    if not exam:
        exam = Exam(
            name=exam_name.upper(),
            category=target_category,
            sub_category=sub_category,
            description=f"{exam_name} Examination"
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)
        cat_val = exam.category.value if exam.category else "None"
        print(f"  [+] Created Exam: {exam.name} ({cat_val})")
    else:
        # Update category if it's different and we have a target
        if exam.category != target_category:
            old_cat = exam.category.value if exam.category else "None"
            new_cat = target_category.value if target_category else "None"
            print(f"  [~] Updating Exam category for {exam.name}: {old_cat} -> {new_cat}")
            exam.category = target_category
            if sub_category:
                exam.sub_category = sub_category
            db.commit()
            db.refresh(exam)
            
    return exam

def get_or_create_subject(db: Session, subject_name: str, exam_id: int) -> Subject:
    subject = db.query(Subject).filter(
        Subject.name == subject_name,
        Subject.exam_id == exam_id
    ).first()
    if not subject:
        subject = Subject(name=subject_name, exam_id=exam_id)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        print(f"  [+] Created Subject: {subject_name}")
    return subject

# ─── JSON Importer ───────────────────────────────────────────────────────────
def import_json_file(file_path: str, db: Session):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    exam_name = data.get("exam_name", "").upper()
    subject_name = data.get("subject_name")
    year = data.get("year")
    questions_list = data.get("questions", [])

    if not all([exam_name, subject_name, year]):
        print(f"  ⚠ Skipping {file_path}: Missing exam_name/subject_name/year.")
        return 0, 0

    exam = get_or_create_exam(db, exam_name, file_path, data.get("sub_category"))
    subject = get_or_create_subject(db, subject_name, exam.id)

    term = data.get("term", "Standard")
    paper_number = str(data.get("paper_number", "1"))
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.subject_id == subject.id,
        QuestionPaper.year == year,
        QuestionPaper.paper_number == paper_number
    ).first()
    if not paper:
        paper = QuestionPaper(
            subject_id=subject.id, year=year, term=term,
            paper_number=paper_number, instructions=data.get("instructions")
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)

    added, skipped = 0, 0
    for q_data in questions_list:
        existing = db.query(Question).filter(
            Question.text == q_data['text'],
            Question.subject_id == subject.id
        ).first()
        if existing:
            skipped += 1
            continue

        context_id = None
        if q_data.get('context'):
            ctx_data = q_data['context']
            ctx = db.query(QuestionContext).filter(QuestionContext.content == ctx_data.get('content')).first()
            if not ctx:
                ctx = QuestionContext(
                    title=ctx_data.get('title'),
                    content=ctx_data.get('content'),
                    image_url=ctx_data.get('image_url')
                )
                db.add(ctx)
                db.commit()
                db.refresh(ctx)
            context_id = ctx.id

        diff_raw = q_data.get('difficulty', 'MEDIUM').upper()
        difficulty = DIFFICULTY_MAP.get(diff_raw, DifficultyLevel.MEDIUM)

        new_q = Question(
            subject_id=subject.id, paper_id=paper.id,
            context_id=context_id,
            question_num=q_data.get('number'),
            section=q_data.get('section'),
            text=q_data['text'],
            topic=q_data.get('topic'),
            difficulty=difficulty,
            explanation=q_data.get('explanation'),
            year=year, is_ai_generated=False
        )
        db.add(new_q)
        db.flush()

        for choice_data in q_data.get('choices', []):
            choice = Choice(
                question_id=new_q.id,
                label=choice_data.get('label'),
                text=choice_data['text'],
                image_url=choice_data.get('image_url'),
                is_correct=choice_data['is_correct']
            )
            db.add(choice)
        added += 1

    db.commit()
    return added, skipped

# ─── Markdown Importer ───────────────────────────────────────────────────────
def parse_markdown_file(file_path: str) -> dict | None:
    """
    Parses markdown files in this format:
    # Exam Subject (Year)
    **1.** Question text
       A) Choice A
       B) Choice B
       **Answer: A**
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Derive metadata from filename and path.  e.g: NDA_Past_Questions_2023.md
    filename = os.path.basename(file_path)
    parts = filename.replace('.md', '').split('_')

    # Extract year from filename
    year_match = re.search(r'(\d{4})', filename)
    year = int(year_match.group(1)) if year_match else None

    # Extract exam name from folder name
    folder = os.path.basename(os.path.dirname(file_path))  # e.g. NDA, POLAC, PCN_PEP
    exam_name = folder.replace('_', ' ').split()[0]  # e.g. NDA, POLAC, PCN

    # Subject from folder name or heading
    heading_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    subject_name = heading_match.group(1).strip() if heading_match else folder

    # Remove year from subject name if present
    subject_name = re.sub(r'\s*\([^)]*\)$', '', subject_name).strip()

    # Parse questions
    # Pattern: (**)?N.(**)? question text ... A) ... (**)?Answer: X(**)?
    question_blocks = re.split(r'\n(?=\**\d+\.\**)', content)
    questions = []

    for block in question_blocks:
        # Get question number and text - supports both **N.** and N.
        q_match = re.match(r'(?:\*\*|)(\d+)\.(?:\*\*|)\s+(.+?)(?=\n\s*[A-D]\))', block, re.DOTALL)
        if not q_match:
            continue

        q_num = int(q_match.group(1))
        q_text = q_match.group(2).strip().replace('\n', ' ')

        # Get choices - patterns like "A) text" or "A. text"
        choices_raw = re.findall(r'([A-E])[)\.]\s+(.+?)(?=\n\s*[A-E][).]|(?:\*\*|)Answer|(?:\*\*|)Explanation|\Z)', block, re.DOTALL)

        # Get correct answer - supports both **Answer: X** and Answer: X
        answer_match = re.search(r'(?:\*\*|)Answer:\s*([A-E])(?:\*\*|)', block)
        correct_label = answer_match.group(1).strip() if answer_match else None

        if not choices_raw or not correct_label:
            continue

        choices = [
            {
                "label": c[0].strip(),
                "text": c[1].strip().replace('\n', ' '),
                "is_correct": c[0].strip() == correct_label
            }
            for c in choices_raw
        ]

        questions.append({
            "number": q_num,
            "text": q_text,
            "choices": choices,
            "topic": None,
            "difficulty": "MEDIUM",
            "explanation": None
        })

    if not questions:
        # Check for Theory Section fallback
        theory_match = re.search(r'## Theory .*?Section\n\n(.+)', content, re.DOTALL | re.IGNORECASE)
        if theory_match:
            theory_text = theory_match.group(1).strip()
            questions.append({
                "number": 1,
                "text": theory_text,
                "choices": [],
                "topic": "Theory",
                "difficulty": "MEDIUM",
                "section": "Theory",
                "explanation": None
            })
        else:
            return None

    return {
        "exam_name": exam_name,
        "subject_name": subject_name,
        "year": year,
        "questions": questions,
        "file_path": file_path
    }

def import_markdown_file(file_path: str, db: Session):
    data = parse_markdown_file(file_path)
    if not data:
        print(f"  [x] No parseable questions in {file_path}")
        return 0, 0

    exam_name = data['exam_name'].upper()
    subject_name = data['subject_name']
    year = data['year']

    if not year:
        print(f"  ⚠ Skipping {file_path}: Could not detect year.")
        return 0, 0

    exam = get_or_create_exam(db, exam_name, file_path)
    subject = get_or_create_subject(db, subject_name, exam.id)

    paper = db.query(QuestionPaper).filter(
        QuestionPaper.subject_id == subject.id,
        QuestionPaper.year == year
    ).first()
    if not paper:
        paper = QuestionPaper(subject_id=subject.id, year=year, term="Standard", paper_number="1")
        db.add(paper)
        db.commit()
        db.refresh(paper)

    added, skipped = 0, 0
    for q_data in data['questions']:
        existing = db.query(Question).filter(
            Question.text == q_data['text'],
            Question.subject_id == subject.id
        ).first()
        if existing:
            skipped += 1
            continue

        new_q = Question(
            subject_id=subject.id, paper_id=paper.id,
            question_num=q_data.get('number'),
            text=q_data['text'],
            topic=q_data.get('topic'),
            difficulty=DifficultyLevel.MEDIUM,
            explanation=q_data.get('explanation'),
            year=year, is_ai_generated=False,
            section=q_data.get('section')
        )
        db.add(new_q)
        db.flush()

        for choice_data in q_data.get('choices', []):
            choice = Choice(
                question_id=new_q.id,
                label=choice_data.get('label'),
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
            db.add(choice)
        added += 1

    db.commit()
    return added, skipped

# ─── ALOC Importer ───────────────────────────────────────────────────────────
def import_aloc_file(file_path: str, db: Session):
    """
    Imports raw ALOC JSON data which is a list of question objects.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        questions_list = json.load(f)
    
    if not isinstance(questions_list, list):
        # Handle if it's a single object (from first draft of scraper)
        questions_list = [questions_list]

    if not questions_list:
        return 0, 0

    # Meta from the first item
    sample = questions_list[0]
    exam_type = sample.get('examtype', 'JAMB').upper()
    if exam_type == 'UTME':
        exam_type = 'JAMB'

    year = int(sample.get('examyear')) if sample.get('examyear') else None
    
    # Infer subject from filename
    filename = os.path.basename(file_path)
    subject_raw = filename.split('_')[0].capitalize()
    
    exam = get_or_create_exam(db, exam_type, file_path)
    subject = get_or_create_subject(db, subject_raw, exam.id)

    # ALOC questions don't strictly have papers in the same way, but we map to paper "1"
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.subject_id == subject.id,
        QuestionPaper.year == year
    ).first()
    if not paper:
        paper = QuestionPaper(subject_id=subject.id, year=year, term="Standard", paper_number="1")
        db.add(paper)
        db.commit()
        db.refresh(paper)

    added, skipped = 0, 0
    for q_data in questions_list:
        text = q_data.get('question', '').strip()
        if not text: continue

        # For ALOC, we just add the question instead of checking exact text 
        # (ALOC has different sections and images, exact match is tricky)
        
        new_q = Question(
            subject_id=subject.id,
            paper_id=paper.id,
            question_num=q_data.get('questionNub'),
            section=q_data.get('section'),
            text=text,
            topic=q_data.get('category'),
            difficulty=DifficultyLevel.MEDIUM,
            explanation=q_data.get('solution'),
            year=year,
            is_ai_generated=False
        )
        db.add(new_q)
        db.flush()

        # Handle options
        options = q_data.get('option', {})
        correct_label = q_data.get('answer', '').strip().upper()

        for label, val in options.items():
            if not val or not val.strip(): continue
            choice = Choice(
                question_id=new_q.id,
                label=label.upper(),
                text=val.strip(),
                is_correct=(label.upper() == correct_label)
            )
            db.add(choice)
        added += 1

    db.commit()
    return added, skipped

# ─── Core Runner ─────────────────────────────────────────────────────────────
def import_file(file_path: str, db: Session):
    if file_path.endswith('_aloc.json'):
        a, s = import_aloc_file(file_path, db)
    elif file_path.endswith('.json'):
        a, s = import_json_file(file_path, db)
    elif file_path.endswith('.md') and 'README' not in file_path and 'templates' not in file_path:
        a, s = import_markdown_file(file_path, db)
    else:
        return

    if a > 0 or s > 0:
        status = f"[+] Added {a}" + (f", [~] Skipped {s} duplicates" if s > 0 else "")
        print(f"  {status}  <-  {os.path.relpath(file_path, project_root)}")
    else:
        print(f"  [~] No new content  <-  {os.path.relpath(file_path, project_root)}")

def get_changed_data_files() -> list[str]:
    """Returns list of files in data/ changed in the last git commit."""
    import subprocess
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
        cwd=project_root, capture_output=True, text=True
    )
    changed = result.stdout.strip().splitlines()
    data_files = []
    for f in changed:
        if f.startswith('data/') and (f.endswith('.json') or f.endswith('.md')):
            full = os.path.join(project_root, f.replace('/', os.sep))
            if os.path.exists(full):
                data_files.append(full)
    return data_files

def run_import(changed_only: bool = False):
    db = SessionLocal()
    total_added = 0

    if changed_only:
        files = get_changed_data_files()
        print(f"\n[*] Reharz Data Sync -- {len(files)} changed file(s) detected\n")
    else:
        data_dir = os.path.join(project_root, "data")
        files = []
        for root, dirs, filenames in os.walk(data_dir):
            if "templates" in root:
                continue
            for file in filenames:
                if file.endswith('.json') or (file.endswith('.md') and 'README' not in file):
                    files.append(os.path.join(root, file))
        print(f"\n[*] Reharz Data Sync -- Full import of {len(files)} file(s)\n")

    for file_path in files:
        try:
            import_file(file_path, db)
        except Exception as e:
            print(f"  [x] Error importing {file_path}: {e}")
            db.rollback()

    db.close()
    print(f"\n[+] Reharz Data Sync Complete.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reharz Data Import Pipeline")
    parser.add_argument('--changed', action='store_true', help='Only import files changed in last git commit')
    args = parser.parse_args()
    run_import(changed_only=args.changed)
