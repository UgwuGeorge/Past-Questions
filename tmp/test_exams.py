from agent_core.main import get_exams
from agent_core.database import SessionLocal
import json

db = SessionLocal()
try:
    exams = get_exams(db)
    with open('tmp/test_exams.json', 'w') as f:
        json.dump([e for e in exams], f)
except Exception as e:
    with open('tmp/test_exams.json', 'w') as f:
        f.write(str(e))
finally:
    db.close()
