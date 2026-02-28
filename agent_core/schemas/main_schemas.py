from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ChoiceBase(BaseModel):
    text: str
    is_correct: bool

class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    explanation: Optional[str] = None
    difficulty: str
    topic: str
    year: Optional[int] = None
    subject_id: int

class QuestionCreate(QuestionBase):
    choices: List[ChoiceBase]

class Question(QuestionBase):
    id: int
    year: Optional[int] = None
    is_ai_generated: bool
    choices: List[Choice]

    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    exam_id: int

class Subject(SubjectBase):
    id: int
    
    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None

class Exam(ExamBase):
    id: int
    subjects: List[Subject]

    class Config:
        from_attributes = True
