from agent_core.database import SessionLocal, engine
from agent_core.models import main_models
from sqlalchemy import text

db = SessionLocal()
try:
    # 1. Check raw categories in DB
    with engine.connect() as conn:
        res = conn.execute(text("SELECT DISTINCT category FROM exams")).fetchall()
        print(f"Raw categories in DB: {[repr(r[0]) for r in res]}")
    
    # 2. Check Enum values
    print(f"Enum members: {[(m.name, m.value) for m in main_models.ExamCategory]}")

    # 3. Attempt query
    exams = db.query(main_models.Exam).all()
    print(f"Successfully fetched {len(exams)} exams")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
