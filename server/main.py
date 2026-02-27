from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import main_models
from .schemas import main_schemas
from .core import auth
import os

from .routes import exams, questions, cbt, ai

# Create tables
main_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Exam Platform API")

# Include routers
app.include_router(exams.router)
app.include_router(questions.router)
app.include_router(cbt.router)
app.include_router(ai.router)

@app.post("/token", response_model=main_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(main_models.User).filter(main_models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Scalable AI Exam Platform API"}
