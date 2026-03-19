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
from agent_core.core import auth
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reharz AI Exam Backend")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/register")
def register(user_data: main_schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(main_models.User).filter(
        (main_models.User.username == user_data.username) | 
        (main_models.User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    # Create new user
    new_user = main_models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=auth.get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    access_token = auth.create_access_token(data={"sub": new_user.username, "user_id": new_user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    }

@app.post("/api/auth/login")
def login(login_data: dict, db: Session = Depends(get_db)):
    # Simplified login_data as dict for now, or could use a schema
    username = login_data.get("username")
    password = login_data.get("password")
    
    user = db.query(main_models.User).filter(main_models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }

@app.get("/api/user/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(main_models.ExamSession).filter(
        main_models.ExamSession.user_id == user_id,
        main_models.ExamSession.end_time != None
    ).all()
    
    if not sessions:
        return {
            "exams_completed": 0,
            "avg_score": 0,
            "study_hours": 0,
            "mastery_level": 0
        }
    
    total_score = sum(s.score for s in sessions if s.score is not None)
    avg_score = round(total_score / len(sessions), 1) if sessions else 0
    
    # Estimate time: session end - session start
    total_duration_secs = 0
    for s in sessions:
        if s.end_time and s.start_time:
            diff = s.end_time - s.start_time
            total_duration_secs += diff.total_seconds()
            
    study_hours = round(total_duration_secs / 3600, 1)
    
    # Simple mastery mapping
    mastery = round((avg_score / 100) * 100, 1)
    
    return {
        "exams_completed": len(sessions),
        "avg_score": avg_score,
        "study_hours": study_hours,
        "mastery_level": mastery
    }

@app.get("/api/exams", response_model=List[main_schemas.Exam])
def get_exams(category: str = None, sub_category: str = None, name: str = None, db: Session = Depends(get_db)):
    query = db.query(main_models.Exam)
    if name:
        query = query.filter(main_models.Exam.name.ilike(f"%{name}%"))
    if category and category.lower() != 'any':
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

@app.get("/api/subjects/{subject_id}/profile")
def get_subject_profile(subject_id: int, user_id: int = 1):
    return json.loads(agent.get_subject_profile(subject_id, user_id=user_id))

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
    userId: int
    content: str
    criteria: str = "IELTS"

@app.post("/api/grade-essay")
async def grade_essay(payload: EssayPayload, db: Session = Depends(get_db)):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Essay content cannot be empty")
    try:
        from agent_core.core.ai import AIEngine
        result = await AIEngine.grade_essay_or_sop(payload.content, payload.criteria)
        
        # Persist feedback
        feedback = main_models.AIFeedback(
            user_id=payload.userId,
            content_type=f"essay_{payload.criteria}",
            input_text=payload.content,
            feedback_json=result
        )
        db.add(feedback)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class InterviewPayload(BaseModel):
    userId: int
    question: str
    answer: str

@app.post("/api/interview-evaluate")
async def interview_evaluate(payload: InterviewPayload, db: Session = Depends(get_db)):
    if not payload.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    try:
        from agent_core.core.ai import AIEngine
        result = await AIEngine.simulate_interview(payload.question, payload.answer)
        
        # Persist feedback
        feedback = main_models.AIFeedback(
            user_id=payload.userId,
            content_type="interview",
            input_text=payload.answer,
            feedback_json=result
        )
        db.add(feedback)
        db.commit()
        
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
    subject_context = request.get("subject_context")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    response = await agent.chat(user_id=user_id, message=message, history=history, subject_context=subject_context)
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

# --- NEW SIMULATION ENDPOINTS ---

class SimulationStartPayload(BaseModel):
    user_id: int
    exam_id: int
    subject_id: Optional[int] = None
    question_count: int = 50
    duration_minutes: int = 60
    topics: Optional[List[str]] = None
    section: Optional[str] = None
    year: Optional[int] = None

@app.post("/api/simulation/start")
def start_simulation(payload: SimulationStartPayload, db: Session = Depends(get_db)):
    # 1. Select questions
    query = db.query(main_models.Question)
    if payload.subject_id:
        query = db.query(main_models.Question).filter(
            main_models.Question.subject_id == payload.subject_id
        )
    else:
        # All subjects for this exam
        subjects = db.query(main_models.Subject).filter(
            main_models.Subject.exam_id == payload.exam_id
        ).all()
        sub_ids = [s.id for s in subjects]
        query = db.query(main_models.Question).filter(
            main_models.Question.subject_id.in_(sub_ids)
        )
    
    # Topic filter (exact match on stored topic values)
    if payload.topics:
        # Use LIKE for partial matching so "Algebra" matches "Algebra" or any topic containing it
        from sqlalchemy import or_
        topic_filters = [main_models.Question.topic.ilike(f"%{t}%") for t in payload.topics]
        query = query.filter(or_(*topic_filters))
    
    # Section filter - try DB section field first, but fall back to choice-based detection
    # since many questions have section=NULL in the database
    all_questions = query.all()
    
    if payload.section and payload.section.lower() != 'full exam':
        if any(q.section for q in all_questions):
            # DB has section data - use it
            filtered = [q for q in all_questions if q.section and payload.section.lower() in q.section.lower()]
            if filtered:
                all_questions = filtered
            # Otherwise keep all_questions (no section match = don't restrict)
        else:
            # Section not stored in DB - infer from choices:
            # objective = questions with multiple-choice options
            # theory/practical = questions without choices (or all if no split)
            q_ids_with_choices = {
                row[0] for row in db.query(main_models.Choice.question_id).distinct().all()
            }
            if payload.section.lower() == 'objective':
                theory_filtered = [q for q in all_questions if q.id in q_ids_with_choices]
                if theory_filtered:
                    all_questions = theory_filtered
            elif payload.section.lower() in ('theory', 'practical'):
                theory_filtered = [q for q in all_questions if q.id not in q_ids_with_choices]
                if theory_filtered:
                    all_questions = theory_filtered
    
    if payload.year:
        year_filtered = [q for q in all_questions if q.year == payload.year]
        if year_filtered:
            all_questions = year_filtered

    if not all_questions:
        raise HTTPException(status_code=404, detail="No questions found for this configuration")
    
    # Use random.choices (with replacement) to ALWAYS return exactly question_count items
    selected = random.choices(all_questions, k=payload.question_count)
    
    # 2. Create Session
    session = main_models.ExamSession(
        user_id=payload.user_id,
        exam_id=payload.exam_id,
        start_time=datetime.utcnow(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # 3. Format response
    result_questions = []
    for q in selected:
        choices = db.query(main_models.Choice).filter(main_models.Choice.question_id == q.id).all()
        result_questions.append({
            "id": q.id,
            "text": q.text,
            "topic": q.topic,
            "difficulty": str(q.difficulty.value),
            "choices": [{"id": c.id, "label": c.label, "text": c.text} for c in choices]
        })
    
    return {
        "session_id": session.id,
        "questions": result_questions,
        "duration_seconds": payload.duration_minutes * 60,
        "start_time": session.start_time
    }

class SimulationSubmitPayload(BaseModel):
    session_id: int
    answers: dict  # {question_id: selected_label}

@app.post("/api/simulation/submit")
def submit_simulation(payload: SimulationSubmitPayload, db: Session = Depends(get_db)):
    session = db.query(main_models.ExamSession).get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.end_time = datetime.utcnow()
    
    # Calculate score
    correct_count = 0
    total_count = len(payload.answers)
    topics_stats = {} # {topic: {correct, total}}
    
    for q_id, label in payload.answers.items():
        q = db.query(main_models.Question).get(int(q_id))
        if not q: continue
        
        correct_choice = db.query(main_models.Choice).filter(
            main_models.Choice.question_id == q.id,
            main_models.Choice.is_correct == True
        ).first()
        
        is_correct = (correct_choice and correct_choice.label == label)
        if is_correct: correct_count += 1
        
        # Topic tracking
        topic = q.topic or "General"
        if topic not in topics_stats:
            topics_stats[topic] = {"correct": 0, "total": 0}
        topics_stats[topic]["total"] += 1
        if is_correct: topics_stats[topic]["correct"] += 1
        
        # Log to user progress
        progress = main_models.UserProgress(
            user_id=session.user_id,
            question_id=q.id,
            topic=topic,
            difficulty=q.difficulty,
            is_correct=is_correct
        )
        db.add(progress)

    session.score = (correct_count / total_count * 100) if total_count > 0 else 0
    session.results_json = {
        "correct": correct_count,
        "total": total_count,
        "topics": topics_stats,
        "duration_seconds": (session.end_time - session.start_time).total_seconds()
    }
    
    db.commit()
    return session.results_json

@app.get("/api/simulation/sessions/{user_id}")
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(main_models.ExamSession).filter(
        main_models.ExamSession.user_id == user_id
    ).order_by(main_models.ExamSession.start_time.desc()).all()
    
    return [
        {
            "id": s.id,
            "exam_name": s.exam.name if s.exam else "Unknown",
            "score": s.score,
            "date": s.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": s.results_json
        } for s in sessions
    ]

@app.get("/api/simulation/{session_id}/analyze")
async def analyze_simulation(session_id: int, db: Session = Depends(get_db)):
    session = db.query(main_models.ExamSession).get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.results_json:
        raise HTTPException(status_code=400, detail="Session is not completed yet")
    
    try:
        from agent_core.core.ai import AIEngine
        analysis = await AIEngine.analyze_exam_result(session.results_json)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/ai-feedback/{user_id}")
def get_user_ai_feedback(user_id: int, db: Session = Depends(get_db)):
    feedback = db.query(main_models.AIFeedback).filter(
        main_models.AIFeedback.user_id == user_id
    ).order_by(main_models.AIFeedback.created_at.desc()).all()
    
    return [
        {
            "id": f.id,
            "type": f.content_type,
            "input": f.input_text[:120] + "..." if len(f.input_text) > 120 else f.input_text,
            "date": f.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "data": f.feedback_json
        } for f in feedback
    ]

# --- ADMIN ENDPOINTS ---

@app.get("/api/admin/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(main_models.User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for u in users
    ]

@app.post("/api/admin/user/{user_id}/toggle_admin")
def toggle_admin(user_id: int, db: Session = Depends(get_db)):
    user = db.query(main_models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = not user.is_admin
    db.commit()
    return {"id": user.id, "username": user.username, "is_admin": user.is_admin}

@app.get("/api/admin/system_stats")
def get_system_stats(db: Session = Depends(get_db)):
    total_users = db.query(main_models.User).count()
    total_sessions = db.query(main_models.ExamSession).count()
    total_exams = db.query(main_models.Exam).count()
    total_subjects = db.query(main_models.Subject).count()
    total_questions = db.query(main_models.Question).count()
    
    return {
        "users": total_users,
        "sessions": total_sessions,
        "exams": total_exams,
        "subjects": total_subjects,
        "questions": total_questions
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
