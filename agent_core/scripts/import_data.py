import json
import os
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

load_dotenv(os.path.join(project_root, ".env"))

from agent_core.database import SessionLocal, engine, Base
from agent_core.models.main_models import Exam, Subject, Question, Choice, QuestionPaper, QuestionContext, ExamCategory

# Create SQLite tables if they don't exist
Base.metadata.create_all(bind=engine)

# Mapping for Automatic Categorization
EXAM_MAP = {
    # Academics
    "WAEC": ExamCategory.ACADEMICS, "JAMB": ExamCategory.ACADEMICS, 
    "NABTEB": ExamCategory.ACADEMICS, "NECO": ExamCategory.ACADEMICS, 
    "NDA": ExamCategory.ACADEMICS, "POLAC": ExamCategory.ACADEMICS,
    # Professional
    "ICAN": ExamCategory.PROFESSIONAL, "BAR": ExamCategory.PROFESSIONAL,
    "NURSING": ExamCategory.PROFESSIONAL, "MEDICINE": ExamCategory.PROFESSIONAL, 
    "TRCN": ExamCategory.PROFESSIONAL, "COREN": ExamCategory.PROFESSIONAL,
    # scholarships
    "IELTS": ExamCategory.SCHOLARSHIPS, "PTDF": ExamCategory.SCHOLARSHIPS,
    "BEA": ExamCategory.SCHOLARSHIPS, "NNPC": ExamCategory.SCHOLARSHIPS,
    "TOTAL": ExamCategory.SCHOLARSHIPS, "CHEVENING": ExamCategory.SCHOLARSHIPS,
    "COMMONWEALTH": ExamCategory.SCHOLARSHIPS, "DAAD": ExamCategory.SCHOLARSHIPS,
    "ERASMUS": ExamCategory.SCHOLARSHIPS
}

def import_json_data(file_path: str, db: Session):
    print(f"Importing data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    exam_name = data.get("exam_name", "").upper()
    subject_name = data.get("subject_name")
    year = data.get("year")
    questions_list = data.get("questions", [])

    if not all([exam_name, subject_name, year]):
        print(f"Skipping {file_path}: Missing metadata.")
        return

    # 1. Get or Create Exam
    exam = db.query(Exam).filter(Exam.name.ilike(exam_name)).first()
    if not exam:
        # Determine category from map or folder
        category = EXAM_MAP.get(exam_name.split()[0], ExamCategory.ACADEMICS)
        if "Professional" in file_path:
            category = ExamCategory.PROFESSIONAL
        elif "Academic" in file_path:
            category = ExamCategory.ACADEMICS
        elif "Scholarship" in file_path or "scholarship" in file_path:
            category = ExamCategory.SCHOLARSHIPS
            
        exam = Exam(
            name=exam_name, 
            category=category,
            sub_category=data.get("sub_category"),
            description=f"{exam_name} Examination"
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)

    # 2. Get or Create Subject (Linked to Exam)
    subject = db.query(Subject).filter(
        Subject.name == subject_name, 
        Subject.exam_id == exam.id
    ).first()
    if not subject:
        subject = Subject(name=subject_name, exam_id=exam.id)
        db.add(subject)
        db.commit()
        db.refresh(subject)

    # 3. Get or Create Question Paper
    term = data.get("term", "Standard")
    paper_number = data.get("paper_number", "1")
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.subject_id == subject.id,
        QuestionPaper.year == year,
        QuestionPaper.paper_number == paper_number
    ).first()
    
    if not paper:
        paper = QuestionPaper(
            subject_id=subject.id,
            year=year,
            term=term,
            paper_number=paper_number,
            instructions=data.get("instructions")
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)

    # 4. Import Questions
    count_added = 0
    count_skipped = 0

    for q_data in questions_list:
        # Check for duplicates by text and subject
        existing_q = db.query(Question).filter(
            Question.text == q_data['text'],
            Question.subject_id == subject.id
        ).first()

        if existing_q:
            count_skipped += 1
            continue

        # Handle Context (Passage/Shared Instruction)
        context_id = None
        if q_data.get('context'):
            context_data = q_data['context']
            context = db.query(QuestionContext).filter(
                QuestionContext.content == context_data.get('content')
            ).first()
            if not context:
                context = QuestionContext(
                    title=context_data.get('title'),
                    content=context_data.get('content'),
                    image_url=context_data.get('image_url')
                )
                db.add(context)
                db.commit()
                db.refresh(context)
            context_id = context.id

        new_q = Question(
            subject_id=subject.id,
            paper_id=paper.id,
            context_id=context_id,
            question_num=q_data.get('number'),
            section=q_data.get('section'),
            text=q_data['text'],
            topic=q_data.get('topic'),
            difficulty=q_data.get('difficulty', 'MEDIUM'),
            explanation=q_data.get('explanation'),
            year=year,
            is_ai_generated=False
        )
        db.add(new_q)
        db.flush() # Get ID for choices

        # 4. Add Choices
        for choice_data in q_data.get('choices', []):
            choice = Choice(
                question_id=new_q.id,
                label=choice_data.get('label'),
                text=choice_data['text'],
                image_url=choice_data.get('image_url'),
                is_correct=choice_data['is_correct']
            )
            db.add(choice)
        
        count_added += 1

    db.commit()
    print(f"Finished {file_path}: Added {count_added} questions, Skipped {count_skipped} duplicates.")

def run_import():
    db = SessionLocal()
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data")
    
    for root, dirs, files in os.walk(data_dir):
        if "templates" in root:
            continue
            
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    import_json_data(file_path, db)
                except Exception as e:
                    print(f"Error importing {file_path}: {e}")
                    db.rollback()
    
    db.close()

if __name__ == "__main__":
    run_import()
