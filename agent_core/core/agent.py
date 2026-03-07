import os
import json
from openai import OpenAI, AsyncOpenAI
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, Float
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agent_core.database import SessionLocal
from agent_core.models.main_models import Exam, Subject, Question, Choice, UserProgress, DifficultyLevel, ExamSession
from agent_core.core.ai import AIEngine

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
async_client = AsyncOpenAI(api_key=api_key)
MODEL_ID = "gpt-4o"

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

    def get_practice_batch(self, user_id: int, exam_name: str, count: int = 5) -> str:
        """
        Fetches a batch of tailored questions for a practice session.
        Use this when the user asks for a specific number of questions.
        """
        exam = self.db.query(Exam).filter(Exam.name.ilike(exam_name)).first()
        if not exam:
            return f"Error: Exam '{exam_name}' not found."

        # Fetch up to 'count' questions
        subids = [s.id for s in exam.subjects]
        questions = self.db.query(Question).filter(Question.subject_id.in_(subids)).limit(count).all()
        
        if not questions:
            return "No questions available for this exam yet."

        results = []
        for q in questions:
            choices = [f"[{c.id}] {c.text}" for c in q.choices]
            correct_choice = next((c.text for c in q.choices if c.is_correct), "")
            results.append({
                "question_id": q.id,
                "topic": q.topic,
                "text": q.text,
                "options": choices,
                "internal_correct_answer": correct_choice
            })
        
        return json.dumps(results)

    def get_session_summary(self, user_id: int, last_n: int) -> str:
        """
        Analyzes the last N logged answers and provides a score.
        Use this to 'score' the user after they finish a set of questions.
        """
        recent_progress = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).order_by(UserProgress.attempt_date.desc()).limit(last_n).all()
        
        if not recent_progress:
            return "No recent practice attempts found."
        
        correct = sum(1 for p in recent_progress if p.is_correct)
        total = len(recent_progress)
        percentage = round((correct / total) * 100, 1)
        
        report = {
            "score": f"{correct}/{total}",
            "percentage": f"{percentage}%",
            "remarks": "Excellent!" if percentage >= 70 else "Good effort! Keep practicing."
        }
        
        return json.dumps(report)

    def get_simulation_history(self, user_id: int) -> str:
        """Retrieves and analyzes the user's past full exam simulation scores."""
        sessions = self.db.query(ExamSession).filter(
            ExamSession.user_id == user_id
        ).order_by(ExamSession.start_time.desc()).limit(5).all()
        
        if not sessions:
            return "No full exam simulations found in your history. Why not start one?"
        
        report = "Your Recent Simulation Results:\n"
        for s in sessions:
            date_str = s.start_time.strftime("%Y-%m-%d")
            score_info = f"{s.score}%" if s.score is not None else "Incomplete"
            report += f"- {date_str}: {score_info}\n"
        return report

    def grade_essay(self, content: str, criteria: str) -> str:
        """Grades an IELTS essay, Scholarship SOP, or academic writing."""
        result = AIEngine.grade_essay_or_sop_sync(content, criteria)
        return json.dumps(result, indent=2)

    def run_interview_coach(self, scenario: str, user_text: str) -> str:
        """Provides expert feedback on an interview response."""
        result = AIEngine.simulate_interview_sync(scenario, user_text)
        return json.dumps(result, indent=2)

    def generate_new_content(self, exam_name: str, topic: str, difficulty: str, count: int = 5) -> str:
        """
        Generates new practice questions and stores them in the local database.
        Use this when a user wants to practice a topic that 'get_adaptive_v2' says is empty.
        """
        # 1. Verify exam exist
        exam = self.db.query(Exam).filter(Exam.name.ilike(exam_name)).first()
        if not exam:
            return f"Error: Exam '{exam_name}' not found. Please create it first."

        # 2. Find or Create Subject for this Exam
        subject_name = topic.split()[0]
        subject = self.db.query(Subject).filter(
            Subject.name.ilike(subject_name), 
            Subject.exam_id == exam.id
        ).first()
        
        if not subject:
            subject = exam.subjects[0] if exam.subjects else Subject(name=subject_name, exam_id=exam.id)
            if not subject.id:
                self.db.add(subject)
                self.db.commit()
                self.db.refresh(subject)

        # 3. Generate via AI
        questions_data = AIEngine.generate_questions_sync(exam_name, topic, difficulty, count)
        
        # 4. Save to DB
        added_count = 0
        for q_data in questions_data:
            new_q = Question(
                subject_id=subject.id,
                text=q_data['text'],
                topic=topic,
                difficulty=DifficultyLevel(difficulty.lower()) if difficulty.lower() in [d.value for d in DifficultyLevel] else DifficultyLevel.MEDIUM,
                explanation=q_data.get('explanation'),
                is_ai_generated=True
            )
            self.db.add(new_q)
            self.db.flush()
            
            for choice_data in q_data.get('choices', []):
                choice = Choice(
                    question_id=new_q.id,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )
                self.db.add(choice)
            added_count += 1
        
        self.db.commit()
        return f"Successfully generated and stored {added_count} new questions for {exam_name} - {topic}."

    async def chat(self, user_id: int, message: str, history: List[Dict] = []) -> str:
        # Define tools for OpenAI
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_available_exams",
                    "description": "Lists all supported exams and certifications in the local database.",
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weak_topics",
                    "description": "Analyzes user performance and returns a string breakdown of accuracy per topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"}
                        },
                        "required": ["user_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_adaptive_v2",
                    "description": "Fetches a question specifically tailored to the user's current weakness level.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "exam_name": {"type": "string"}
                        },
                        "required": ["user_id", "exam_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "log_answer",
                    "description": "Records a user attempt in the database to track learning progress.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "question_id": {"type": "integer"},
                            "is_correct": {"type": "boolean"}
                        },
                        "required": ["user_id", "question_id", "is_correct"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grade_essay",
                    "description": "Grades an IELTS essay, Scholarship SOP, or academic writing.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "criteria": {"type": "string"}
                        },
                        "required": ["content", "criteria"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_interview_coach",
                    "description": "Provides expert feedback on an interview response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scenario": {"type": "string"},
                            "user_text": {"type": "string"}
                        },
                        "required": ["scenario", "user_text"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_new_content",
                    "description": "Generates new practice questions and stores them in the local database.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "exam_name": {"type": "string"},
                            "topic": {"type": "string"},
                            "difficulty": {"type": "string"},
                            "count": {"type": "integer", "default": 5}
                        },
                        "required": ["exam_name", "topic", "difficulty"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_practice_batch",
                    "description": "Fetches a batch of tailored questions for a practice session.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "exam_name": {"type": "string"},
                            "count": {"type": "integer", "default": 5}
                        },
                        "required": ["user_id", "exam_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_session_summary",
                    "description": "Analyzes the last N logged answers and provides a score.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "last_n": {"type": "integer"}
                        },
                        "required": ["user_id", "last_n"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_simulation_history",
                    "description": "Retrieves and analyzes the user's past full exam simulation scores.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"}
                        },
                        "required": ["user_id"],
                    },
                },
            }
        ]

        messages = [
            {"role": "system", "content": (
                f"You are the 'Reharz Exam Architect', an expert AI Agent managing local exam systems. "
                f"You are currently assisting User ID: {user_id}. "
                f"Protocol: "
                f"1. When a user wants to practice a specific number of questions, use 'get_practice_batch'. "
                f"2. When they want a REAL EXAM simulation, tell them to click the 'Practice' button on any exam card in the dashboard. "
                f"3. Ask questions ONE BY ONE for simple practice. "
                f"4. After each response, use 'log_answer'. "
                f"5. Use 'get_simulation_history' to see how they've performed in full proctored exams."
            )}
        ]
        
        for h in history:
            role = "assistant" if h["role"] == "model" else h["role"]
            messages.append({"role": role, "content": h["text"]})
        
        messages.append({"role": "user", "content": message})

        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the corresponding method
                method = getattr(self, function_name)
                # Ensure the result is a string
                result = method(**function_args)
                function_response = json.dumps(result) if not isinstance(result, str) else result
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            
            second_response = await async_client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
            )
            return second_response.choices[0].message.content
        
        return response_message.content
