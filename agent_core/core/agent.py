import os
import json
import google.generativeai as genai
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from agent_core.database import SessionLocal
from agent_core.models import main_models
from agent_core.core.ai import AIEngine

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

class ExamAgent:
    """
    A local AI Agent that uses tools to interact with your exam database.
    """
    
    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def list_available_exams(self) -> str:
        """Lists all exams and their subjects currently in the local database."""
        exams = self.db.query(main_models.Exam).all()
        if not exams:
            return "No exams found in the database."
        
        result = []
        for e in exams:
            subjects = [s.name for s in e.subjects]
            result.append(f"- {e.name}: {', '.join(subjects)}")
        return "\n".join(result)

    def get_practice_question(self, subject_name: str) -> str:
        """Fetches a random practice question for a given subject."""
        subject = self.db.query(main_models.Subject).filter(main_models.Subject.name.ilike(subject_name)).first()
        if not subject:
            return f"Subject '{subject_name}' not found. Try one from the list."
        
        question = self.db.query(main_models.Question).filter(main_models.Question.subject_id == subject.id).first()
        if not question:
            return f"No questions found for {subject_name}."
            
        choices_text = "\n".join([f"{c.id}) {c.text}" for c in question.choices])
        return f"Question: {question.text}\n\nOptions:\n{choices_text}\n\n(I know the answer, tell me when you're ready for the explanation!)"

    async def chat(self, user_id: int, message: str, history: List[Dict] = []) -> str:
        # Define the tools
        tools = [self.list_available_exams, self.get_practice_question]
        
        # Initialize model with tools
        agent_model = genai.GenerativeModel("gemini-1.5-flash", tools=tools)
        
        # Start a chat session
        chat_session = agent_model.start_chat(
            history=[
                * [{"role": h["role"], "parts": [h["text"]]} for h in history]
            ],
            enable_automatic_function_calling=True
        )
        
        response = await chat_session.send_message_async(message)
        return response.text
