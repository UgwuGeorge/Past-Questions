import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent_core.main import get_exams, get_exam_subjects
from agent_core.database import SessionLocal
import json

db = SessionLocal()
try:
    exams = db.query(get_exams.__annotations__['db'].__args__[0].__args__[0]).all() # wait, just query Exam directly
    from agent_core.models import main_models
    exams = db.query(main_models.Exam).all()
    for e in exams:
        try:
            subjects = db.query(main_models.Subject).filter(main_models.Subject.exam_id == e.id).all()
        except Exception as ex:
            print(f"Failed for exam {e.id}: {ex}")
    print("Checked all subjects successfully.")
except Exception as e:
    print(e)
finally:
    db.close()
