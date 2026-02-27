from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import main_models
from ..schemas import main_schemas

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=main_schemas.Question)
def create_question(question: main_schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = main_models.Question(
        text=question.text,
        explanation=question.explanation,
        difficulty=question.difficulty,
        topic=question.topic,
        subject_id=question.subject_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    for choice in question.choices:
        db_choice = main_models.Choice(**choice.dict(), question_id=db_question.id)
        db.add(db_choice)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/{subject_id}", response_model=List[main_schemas.Question])
def read_questions_by_subject(subject_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    questions = db.query(main_models.Question).filter(main_models.Question.subject_id == subject_id).offset(skip).limit(limit).all()
    return questions
