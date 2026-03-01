import asyncio
import os
import sys
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
load_dotenv(os.path.join(project_root, ".env"))

from agent_core.core.agent import ExamAgent

async def test_session():
    agent = ExamAgent()
    print("Testing session capabilities...")
    # User asks for 2 questions
    message = "I want to do a quick 2-question quiz on WAEC Mathematics."
    response = await agent.chat(user_id=1, message=message)
    print(f"Agent Response (Start): {response}")
    
    # Simulate user answering the first question (assuming the agent asks it)
    # We'll just print the output to see if it initiated the session correctly.

if __name__ == "__main__":
    asyncio.run(test_session())
