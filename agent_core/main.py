from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

# Ensure agent_core is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core.database import get_db, engine, Base
from agent_core.models import main_models
from agent_core.schemas import main_schemas
from agent_core.core.agent import ExamAgent
from typing import List
from pydantic import BaseModel
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reharz AI Exam Backend")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ExamAgent()

@app.get("/")
def read_root():
    return {"message": "Reharz AI Exam Backend is running"}

@app.get("/api/categories")
def get_categories():
    return [c.value for c in main_models.ExamCategory]

@app.get("/api/exams", response_model=List[main_schemas.Exam])
def get_exams(category: str = None, sub_category: str = None, db: Session = Depends(get_db)):
    query = db.query(main_models.Exam)
    if category:
        query = query.filter(main_models.Exam.category == category)
    if sub_category:
        query = query.filter(main_models.Exam.sub_category == sub_category)
    return query.all()

@app.get("/api/exams/{exam_id}/subjects")
def get_subjects(exam_id: int, db: Session = Depends(get_db)):
    subjects = db.query(main_models.Subject).filter(
        main_models.Subject.exam_id == exam_id
    ).all()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found for this exam")
    return [{"id": s.id, "name": s.name, "exam_id": s.exam_id} for s in subjects]

@app.get("/api/subjects/{subject_id}/questions")
def get_questions(subject_id: int, limit: int = 20, db: Session = Depends(get_db)):
    questions = db.query(main_models.Question).filter(
        main_models.Question.subject_id == subject_id
    ).limit(limit).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this subject")
    
    result = []
    for q in questions:
        choices = db.query(main_models.Choice).filter(
            main_models.Choice.question_id == q.id
        ).all()
        result.append({
            "id": q.id,
            "text": q.text,
            "topic": q.topic,
            "year": q.year,
            "explanation": q.explanation,
            "choices": [
                {"id": c.id, "label": c.label, "text": c.text, "is_correct": c.is_correct}
                for c in choices
            ]
        })
    return result

@app.get("/api/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(main_models.Question).filter(main_models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    choices = db.query(main_models.Choice).filter(main_models.Choice.question_id == question.id).all()
    return {
        "id": question.id,
        "text": question.text,
        "topic": question.topic,
        "year": question.year,
        "explanation": question.explanation,
        "subject_id": question.subject_id,
        "choices": [
            {"id": c.id, "label": c.label, "text": c.text, "is_correct": c.is_correct}
            for c in choices
        ]
    }

class SubmitPayload(BaseModel):
    user_id: int
    question_id: int
    selected_label: str
    is_correct: bool
    topic: str
    difficulty: str = "medium"

@app.post("/api/submit")
def submit_answer(payload: SubmitPayload, db: Session = Depends(get_db)):
    diff_map = {
        "easy": main_models.DifficultyLevel.EASY,
        "medium": main_models.DifficultyLevel.MEDIUM,
        "hard": main_models.DifficultyLevel.HARD,
    }
    progress = main_models.UserProgress(
        user_id=payload.user_id,
        question_id=payload.question_id,
        topic=payload.topic or "General",
        difficulty=diff_map.get(payload.difficulty, main_models.DifficultyLevel.MEDIUM),
        is_correct=payload.is_correct,
        attempt_date=datetime.utcnow()
    )
    db.add(progress)
    db.commit()
    return {"status": "ok", "is_correct": payload.is_correct}

class EssayPayload(BaseModel):
    content: str
    criteria: str = "IELTS"

@app.post("/api/grade-essay")
async def grade_essay(payload: EssayPayload):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Essay content cannot be empty")
    try:
        from agent_core.core.ai import AIEngine
        result = await AIEngine.grade_essay_or_sop(payload.content, payload.criteria)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class InterviewPayload(BaseModel):
    question: str
    answer: str

@app.post("/api/interview-evaluate")
async def interview_evaluate(payload: InterviewPayload):
    if not payload.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    try:
        from agent_core.core.ai import AIEngine
        result = await AIEngine.simulate_interview(payload.question, payload.answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatPayload(BaseModel):
    message: str
    history: list = []

@app.get("/api/user/stats/{user_id}")
def get_user_stats(user_id: int):
    stats_text = agent.get_weak_topics(user_id)
    return {"stats_raw": stats_text}

@app.post("/api/chat/{user_id}")
async def chat_with_agent(user_id: int, request: dict):
    message = request.get("message")
    history = request.get("history", [])
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    response = await agent.chat(user_id=user_id, message=message, history=history)
    return {"response": response}

@app.get("/api/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(main_models.UserProgress).filter(
        main_models.UserProgress.user_id == user_id
    ).order_by(main_models.UserProgress.attempt_date.desc()).limit(10).all()
    
    return [
        {
            "id": h.id,
            "topic": h.topic,
            "difficulty": h.difficulty.value if hasattr(h.difficulty, 'value') else str(h.difficulty),
            "is_correct": h.is_correct,
            "date": h.attempt_date.strftime("%Y-%m-%d %H:%M:%S")
        } for h in history
    ]

@app.get("/api/waec")
def get_waec_catalogue():
    catalogue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "waec_catalogue.json")
    if not os.path.exists(catalogue_path):
        raise HTTPException(status_code=404, detail="WAEC catalogue not generated")
    with open(catalogue_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
