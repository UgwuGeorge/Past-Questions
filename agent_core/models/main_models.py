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
    category = Column(String)  # e.g., "Professional", "International", "Scholarship"
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

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    text = Column(String, nullable=False)
    explanation = Column(String)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    topic = Column(String, index=True)
    year = Column(Integer)
    is_ai_generated = Column(Boolean, default=False)
    
    subject = relationship("Subject", back_populates="questions")
    choices = relationship("Choice", back_populates="question")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(String, nullable=False)
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
