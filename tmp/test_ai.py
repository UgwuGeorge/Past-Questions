import asyncio
import os
import sys
sys.path.append(os.getcwd())
from agent_core.core.agent import ExamAgent
from agent_core.database import SessionLocal

async def test_chat():
    db = SessionLocal()
    agent = ExamAgent(db=db)
    try:
        print("Testing AI Chat...")
        response = await agent.chat(user_id=1, message="Hi, what exams are available?")
        print(f"AI Response: {response}")
    except Exception as e:
        print(f"FAILED: {str(e)}")
    finally:
        agent.close()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_chat())
