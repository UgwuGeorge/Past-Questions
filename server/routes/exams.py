from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import main_models
from ..schemas import main_schemas

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.post("/", response_model=main_schemas.Exam)
def create_exam(exam: main_schemas.ExamBase, db: Session = Depends(get_db)):
    db_exam = main_models.Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.get("/", response_model=List[main_schemas.Exam])
def read_exams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exams = db.query(main_models.Exam).offset(skip).limit(limit).all()
    return exams

@router.post("/{exam_id}/subjects", response_model=main_schemas.Subject)
def create_subject(exam_id: int, subject: main_schemas.SubjectBase, db: Session = Depends(get_db)):
    db_subject = main_models.Subject(**subject.dict(), exam_id=exam_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject
