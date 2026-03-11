import asyncio
import os
import sys

# Ensure agent_core is in path
sys.path.append(os.getcwd())

from agent_core.core.agent import ExamAgent

async def test():
    agent = ExamAgent()
    print("Testing 'start a jamb english exam for me'...")
    resp = await agent.chat(1, "start a jamb english exam for me")
    print(f"RESPONSE:\n{resp}")
    print("-" * 20)
    
    print("Testing 'take me to the grading section'...")
    resp = await agent.chat(1, "take me to the grading section")
    print(f"RESPONSE:\n{resp}")

if __name__ == "__main__":
    asyncio.run(test())
