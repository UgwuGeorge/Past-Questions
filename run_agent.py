import asyncio
import os
import sys
from dotenv import load_dotenv

# Add project root to path (parent of 'server' directory)
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, ".env"))

from agent_core.core.agent import ExamAgent

async def main():
    agent = ExamAgent()
    print("---------------------------------------------------------")
    print("Welcome to the Antigravity local AI Agent (Exam Assistant)")
    print("Type 'exit' or 'quit' to stop.")
    print("---------------------------------------------------------")
    
    view_history = []
    
    while True:
        try:
            user_input = input("\nUser > ")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            response = await agent.chat(user_id=1, message=user_input, history=view_history)
            
            print(f"\nAgent > {response}")
            
            # Simple history management
            view_history.append({"role": "user", "text": user_input})
            view_history.append({"role": "model", "text": response})
            if len(view_history) > 10:
                view_history = view_history[-10:]
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    asyncio.run(main())
