import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    print("Verifying imports...")
    import google.generativeai as genai
    import sqlalchemy
    from agent_core.database import engine, Base
    from agent_core.models import main_models
    from agent_core.core.agent import ExamAgent
    from agent_core.core.ai import AIEngine
    print("✅ All imports successful!")

    print("Verifying database connection and schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables verified/created!")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
