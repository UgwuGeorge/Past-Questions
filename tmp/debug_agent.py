import asyncio
import os
import json
from agent_core.core.agent import ExamAgent

async def test():
    agent = ExamAgent()
    response = await agent.chat(user_id=1, message="Take me to the grading section", history=[], subject_context="Biology")
    print(response)

if __name__ == "__main__":
    asyncio.run(test())
