import json
import os
import sys
from sqlalchemy.orm import Session

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.database import SessionLocal, engine
from server.models.main_models import Exam, Subject, Question, Choice

def import_json_data(file_path: str, db: Session):
    print(f"Importing data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    exam_name = data.get("exam_name")
    subject_name = data.get("subject_name")
    year = data.get("year")
    questions_list = data.get("questions", [])

    if not all([exam_name, subject_name, year]):
        print(f"Skipping {file_path}: Missing metadata.")
        return

    # 1. Get or Create Exam
    exam = db.query(Exam).filter(Exam.name == exam_name).first()
    if not exam:
        exam = Exam(name=exam_name, description=f"{exam_name} Examination")
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

    # 3. Import Questions
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

        new_q = Question(
            subject_id=subject.id,
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
                text=choice_data['text'],
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
