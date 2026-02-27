from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from ..models import main_models
from ..core.ai import AIEngine
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Features"])

class EssaySubmission(BaseModel):
    content: str
    criteria: str # e.g., "IELTS", "Scholarship SOP"

class QuestionGenRequest(BaseModel):
    subject_id: int
    topic: str
    difficulty: str
    count: int = 5

@router.post("/essay/grade")
async def grade_essay(submission: EssaySubmission, user_id: int, db: Session = Depends(get_db)):
    feedback = await AIEngine.grade_essay_or_sop(submission.content, submission.criteria)
    
    # Store in DB
    db_feedback = main_models.AIFeedback(
        user_id=user_id,
        content_type=submission.criteria,
        input_text=submission.content,
        feedback_json=feedback
    )
    db.add(db_feedback)
    db.commit()
    return feedback

@router.post("/questions/generate")
async def generate_questions(request: QuestionGenRequest, db: Session = Depends(get_db)):
    # 1. Fetch subject and associated exam
    subject = db.query(main_models.Subject).filter(main_models.Subject.id == request.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    exam_name = subject.exam.name if subject.exam else "General"
    
    # 2. Call AI Engine
    ai_questions = await AIEngine.generate_questions(
        exam_type=exam_name, 
        topic=request.topic, 
        difficulty=request.difficulty, 
        count=request.count
    )
    
    saved_questions = []
    
    # 3. Persist to DB
    for q_data in ai_questions:
        db_question = main_models.Question(
            subject_id=request.subject_id,
            text=q_data["text"],
            explanation=q_data.get("explanation", ""),
            difficulty=request.difficulty.upper(),
            topic=request.topic,
            is_ai_generated=True
        )
        db.add(db_question)
        db.flush() # Get ID
        
        for choice_data in q_data["choices"]:
            db_choice = main_models.Choice(
                question_id=db_question.id,
                text=choice_data["text"],
                is_correct=choice_data["is_correct"]
            )
            db.add(db_choice)
        
        saved_questions.append(db_question)
    
    db.commit()
    return {"message": f"Successfully generated and saved {len(saved_questions)} questions", "questions": saved_questions}

class InterviewRequest(BaseModel):
    user_id: int
    question: str
    user_answer: str

@router.post("/interview/simulate")
async def simulate_interview(request: InterviewRequest, db: Session = Depends(get_db)):
    feedback = await AIEngine.simulate_interview(request.question, request.user_answer)
    
    # Store in DB
    db_feedback = main_models.AIFeedback(
        user_id=request.user_id,
        content_type="INTERVIEW",
        input_text=f"Q: {request.question}\nA: {request.user_answer}",
        feedback_json=feedback
    )
    db.add(db_feedback)
    db.commit()
    
    return feedback
