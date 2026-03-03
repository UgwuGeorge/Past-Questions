from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import sys

# Ensure agent_core is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core.database import get_db, engine, Base
from agent_core.models import main_models
from agent_core.schemas import main_schemas
from agent_core.core.agent import ExamAgent
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Antigravity AI Exam Backend")

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
    return {"message": "Antigravity AI Exam Backend is running"}

@app.get("/api/exams", response_model=List[main_schemas.Exam])
def get_exams(db: Session = Depends(get_db)):
    exams = db.query(main_models.Exam).all()
    return exams

@app.get("/api/user/stats/{user_id}")
def get_user_stats(user_id: int):
    stats_text = agent.get_weak_topics(user_id)
    # Simple parse for demo purposes if it's jumbled text, 
    # but the agent returns a string.
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
