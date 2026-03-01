from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class ExamType(enum.Enum):
    CBT = "cbt"
    APTITUDE = "aptitude"
    ESSAY = "essay"
    INTERVIEW = "interview"

class DifficultyLevel(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class ExamCategory(enum.Enum):
    ACADEMICS = "Academics"
    PROFESSIONAL = "Professional"
    SCHOLARSHIPS = "scholarships"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("ExamSession", back_populates="user")
    ai_feedback = relationship("AIFeedback", back_populates="user")

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # e.g., "JAMB", "ICAN", "IELTS"
    category = Column(SQLEnum(ExamCategory), nullable=False)
    sub_category = Column(String) # e.g., "Medical", "Secondary"
    description = Column(String)
    
    subjects = relationship("Subject", back_populates="exam")
    sessions = relationship("ExamSession", back_populates="exam")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    
    exam = relationship("Exam", back_populates="subjects")
    questions = relationship("Question", back_populates="subject")
    papers = relationship("QuestionPaper", back_populates="subject")

class QuestionPaper(Base):
    """Represents a specific year's paper (e.g., 2022 Mathematics Paper 1)."""
    __tablename__ = "question_papers"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    year = Column(Integer)
    term = Column(String) # e.g., "June/July", "Nov/Dec"
    paper_number = Column(String) # e.g., "Paper 1", "Paper 2", "Obj"
    duration_minutes = Column(Integer)
    instructions = Column(String)
    
    subject = relationship("Subject", back_populates="papers")
    questions = relationship("Question", back_populates="paper")

class QuestionContext(Base):
    """Comprehension passages, common diagrams, or shared instructions."""
    __tablename__ = "question_contexts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String) # Passage text
    image_url = Column(String) # Shared diagram image
    
    questions = relationship("Question", back_populates="context")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    paper_id = Column(Integer, ForeignKey("question_papers.id"), nullable=True)
    context_id = Column(Integer, ForeignKey("question_contexts.id"), nullable=True)
    question_num = Column(Integer) # Question 1, 2, 3...
    section = Column(String) # e.g., "Section A"
    text = Column(String, nullable=False)
    image_url = Column(String) # For diagram questions
    explanation = Column(String)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    topic = Column(String, index=True)
    year = Column(Integer)
    is_ai_generated = Column(Boolean, default=False)
    
    subject = relationship("Subject", back_populates="questions")
    paper = relationship("QuestionPaper", back_populates="questions")
    context = relationship("QuestionContext", back_populates="questions")
    choices = relationship("Choice", back_populates="question")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    label = Column(String) # "A", "B", "C", "D"
    text = Column(String, nullable=False)
    image_url = Column(String) # Some choices are images
    is_correct = Column(Boolean, default=False)
    
    question = relationship("Question", back_populates="choices")

class ExamSession(Base):
    __tablename__ = "exam_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    score = Column(Float)
    results_json = Column(JSON)  # Detailed breakdown per topic
    
    user = relationship("User", back_populates="sessions")
    exam = relationship("Exam", back_populates="sessions")

class AIFeedback(Base):
    __tablename__ = "ai_feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_type = Column(String)  # "essay", "sop", "interview"
    input_text = Column(String)    # User submission
    feedback_json = Column(JSON)   # AI breakdown
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="ai_feedback")

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    topic = Column(String, index=True)
    difficulty = Column(SQLEnum(DifficultyLevel))
    is_correct = Column(Boolean)
    attempt_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    question = relationship("Question")
