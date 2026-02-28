import os
import json
import google.generativeai as genai
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, Float
from agent_core.database import SessionLocal
from agent_core.models import main_models
from agent_core.models.main_models import Exam, Subject, Question, Choice, UserProgress, DifficultyLevel
from agent_core.core.ai import AIEngine

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)
model_name = "gemini-1.5-flash"

class ExamAgent:
    """
    A senior AI-powered agent with Adaptive Learning, Weakness Detection, 
    and Professional Examination Support.
    """
    
    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def get_weak_topics(self, user_id: int) -> str:
        """Analyzes user performance and returns a string breakdown of accuracy per topic."""
        stats = self.db.query(
            UserProgress.topic,
            func.avg(UserProgress.is_correct.cast(Float)).label('accuracy')
        ).filter(UserProgress.user_id == user_id)\
         .group_by(UserProgress.topic).all()
        
        if not stats:
            return "No performance history available yet. Start practicing!"
        
        report = "Performance Statistics (Weakness Detection):\n"
        for topic, accuracy in stats:
            report += f"- {topic}: {round(accuracy * 100, 1)}% Accuracy\n"
        return report

    def log_answer(self, user_id: int, question_id: int, is_correct: bool) -> str:
        """Records a user attempt in the database to track learning progress."""
        q = self.db.query(Question).get(question_id)
        if not q:
            return "Error: Question not found in database."
        
        progress = UserProgress(
            user_id=user_id,
            question_id=question_id,
            topic=q.topic,
            difficulty=q.difficulty,
            is_correct=is_correct
        )
        self.db.add(progress)
        self.db.commit()
        return f"Successfully logged performance for {q.topic}."

    def list_available_exams(self) -> str:
        """Lists all supported exams and certifications in the local database."""
        exams = self.db.query(Exam).all()
        if not exams:
            return "No exams found in the local database."
        
        result_lines = ["Current Database Catalog:"]
        for e in exams:
            subjects = [s.name for s in e.subjects]
            result_lines.append(f"- {e.name} ({e.category}): {', '.join(subjects)}")
        return "\n".join(result_lines)

    def get_adaptive_v2(self, user_id: int, exam_name: str) -> str:
        """
        Fetches a question specifically tailored to the user's current weakness level.
        Includes correct answer metadata for internal AI verification.
        """
        # 1. Identify raw accuracy for topic selection
        stats = self.db.query(
            UserProgress.topic,
            func.avg(UserProgress.is_correct.cast(Float)).label('accuracy')
        ).filter(UserProgress.user_id == user_id)\
         .group_by(UserProgress.topic).all()
        
        weak_topics = {topic: acc for topic, acc in stats}
        
        # 2. Find exam context
        exam = self.db.query(Exam).filter(Exam.name.ilike(exam_name)).first()
        if not exam:
            return f"The database doesn't have content for '{exam_name}' yet. Please ask me to generate some!"

        # 3. Targeted selection
        target_topic = None
        if weak_topics:
            sorted_topics = sorted(weak_topics.items(), key=lambda x: x[1])
            target_topic = sorted_topics[0][0]
        
        target_diff = DifficultyLevel.MEDIUM
        if target_topic and weak_topics[target_topic] < 0.4:
            target_diff = DifficultyLevel.EASY
        elif target_topic and weak_topics[target_topic] > 0.75:
            target_diff = DifficultyLevel.HARD

        # 4. Filter logic
        subids = [s.id for s in exam.subjects]
        query = self.db.query(Question).filter(Question.subject_id.in_(subids))
        if target_topic:
            query = query.filter(Question.topic == target_topic)
        
        question = query.filter(Question.difficulty == target_diff).first() or query.first()

        if not question:
            return "No more questions for this topic/exam in the local database."

        # 5. Result with internal metadata (for the AI's use)
        choices = []
        correct_choice_text = ""
        for c in question.choices:
            choices.append(f"[{c.id}] {c.text}")
            if c.is_correct:
                correct_choice_text = c.text

        response = {
            "question_id": question.id,
            "topic": question.topic,
            "difficulty": str(question.difficulty.value),
            "text": question.text,
            "options": choices,
            "internal_correct_answer": correct_choice_text
        }
        return json.dumps(response)

    async def grade_essay(self, content: str, criteria: str) -> str:
        """Grades an IELTS essay, Scholarship SOP, or academic writing."""
        result = await AIEngine.grade_essay_or_sop(content, criteria)
        return json.dumps(result, indent=2)

    async def run_interview_coach(self, scenario: str, user_text: str) -> str:
        """Provides expert feedback on an interview response."""
        result = await AIEngine.simulate_interview(scenario, user_text)
        return json.dumps(result, indent=2)

    async def chat(self, user_id: int, message: str, history: List[Dict] = []) -> str:
        # Architect-level tool registry
        tools = [
            self.list_available_exams, 
            self.get_weak_topics, 
            self.get_adaptive_v2,
            self.log_answer,
            self.grade_essay,
            self.run_interview_coach
        ]
        
        agent_model = genai.GenerativeModel(model_name, tools=tools)
        
        chat_session = agent_model.start_chat(
            history=[
                {"role": "user", "parts": [
                    f"You are the 'Antigravity Exam Architect', an expert AI Agent managing local exam systems. "
                    f"You are currently assisting User ID: {user_id}. "
                    f"Use tool 'get_adaptive_v2' to find tailored practice content. "
                    f"The tool returns a JSON including the 'internal_correct_answer' for you to verify their response. "
                    f"Always use 'log_answer' after the user responds to update their profile."
                ]},
                {"role": "model", "parts": ["Architect protocol active. I will use the established database and feedback tools to guide the user's learning path."]},
                * [{"role": h["role"], "parts": [h["text"]]} for h in history]
            ],
            enable_automatic_function_calling=True
        )
        
        response = await chat_session.send_message_async(message)
        return response.text
