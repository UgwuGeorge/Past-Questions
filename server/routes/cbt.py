from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from ..database import get_db
from ..models import main_models
from ..schemas import main_schemas
from ..core.auth import oauth2_scheme

router = APIRouter(prefix="/cbt", tags=["CBT Simulation"])

# In a real app, we'd have a get_current_user dependency
# For now, let's assume a dummy user_id or implement a simple one

@router.post("/session/start", response_model=Dict)
def start_session(exam_id: int, user_id: int, db: Session = Depends(get_db)):
    db_session = main_models.ExamSession(
        user_id=user_id,
        exam_id=exam_id,
        start_time=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {"session_id": db_session.id, "start_time": db_session.start_time}

@router.post("/session/{session_id}/submit", response_model=Dict)
def submit_session(session_id: int, answers: List[Dict], db: Session = Depends(get_db)):
    db_session = db.query(main_models.ExamSession).filter(main_models.ExamSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_session.end_time = datetime.utcnow()
    
    # Simple grading logic
    correct_count = 0
    total_questions = len(answers)
    topic_performance = {} # {topic: {correct: 0, total: 0}}

    for ans in answers:
        question_id = ans.get("question_id")
        choice_id = ans.get("choice_id")
        
        db_question = db.query(main_models.Question).filter(main_models.Question.id == question_id).first()
        if not db_question: continue
        
        topic = db_question.topic
        if topic not in topic_performance:
            topic_performance[topic] = {"correct": 0, "total": 0}
        topic_performance[topic]["total"] += 1
        
        db_choice = db.query(main_models.Choice).filter(
            main_models.Choice.id == choice_id, 
            main_models.Choice.question_id == question_id
        ).first()
        
        if db_choice and db_choice.is_correct:
            correct_count += 1
            topic_performance[topic]["correct"] += 1

    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    db_session.score = score
    db_session.results_json = topic_performance
    
    db.commit()
    return {
        "score": score, 
        "correct": correct_count, 
        "total": total_questions,
        "topic_breakdown": topic_performance
    }

@router.get("/analytics/weak-topics/{user_id}")
def get_weak_topics(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(main_models.ExamSession).filter(main_models.ExamSession.user_id == user_id).all()
    
    aggregated_performance = {} # {topic: {accuracy: float, total_attempts: int}}
    
    for session in sessions:
        if not session.results_json: continue
        for topic, stats in session.results_json.items():
            if topic not in aggregated_performance:
                aggregated_performance[topic] = {"correct": 0, "total": 0}
            aggregated_performance[topic]["correct"] += stats["correct"]
            aggregated_performance[topic]["total"] += stats["total"]
            
    weak_topics = []
    for topic, stats in aggregated_performance.items():
        accuracy = (stats["correct"] / stats["total"]) if stats["total"] > 0 else 0
        if accuracy < 0.6: # Threshold for weak topic
            weak_topics.append({"topic": topic, "accuracy": accuracy, "total_questions": stats["total"]})
            
    return sorted(weak_topics, key=lambda x: x["accuracy"])
