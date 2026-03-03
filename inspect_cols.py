from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv(".env")
db_url = os.getenv("DATABASE_URL")
print(f"Checking DB: {db_url}")
engine = create_engine(db_url)
inspector = inspect(engine)
columns = inspector.get_columns("exams")
for c in columns:
    print(f"Column: {c['name']}")
