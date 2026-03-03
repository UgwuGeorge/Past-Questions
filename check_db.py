from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agent_core.models.main_models import Exam, Subject

engine = create_engine("sqlite:///./past_questions_v2.db")
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

exams = db.query(Exam).all()
print(f"Found {len(exams)} exams.")
for e in exams:
    print(f"- {e.name} ({e.category.value})")
    for s in e.subjects:
        print(f"  * {s.name}")
db.close()
