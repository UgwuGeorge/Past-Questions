import asyncio
import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Add project root to path
sys.path.insert(0, os.getcwd())

# Set dummy key for client initialization
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"

async def test_ai_generation_logic():
    print("Starting verification of AI question generation logic...")
    
    # 1. Mock Gemini Response
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "questions": [
            {
                "text": "What is the capital of Nigeria?",
                "choices": [
                    {"text": "Abuja", "is_correct": True},
                    {"text": "Lagos", "is_correct": False},
                    {"text": "Kano", "is_correct": False},
                    {"text": "Ibadan", "is_correct": False}
                ],
                "explanation": "Abuja became the capital in 1991."
            }
        ]
    })
    
    # 2. Mock DB Session and Subject
    mock_db = MagicMock()
    mock_subject = MagicMock()
    mock_subject.id = 1
    mock_subject.exam.name = "UTME"
    
    mock_db.query().filter().first.return_value = mock_subject
    
    # 3. Import and patch components
    from agent_core.core.ai import AIEngine
    
    with patch("agent_core.core.ai.model.generate_content_async") as mock_generate:
        mock_generate.return_value = mock_response
        
        # 4. Call the engine function
        result = await AIEngine.generate_questions("UTME", "Geography", "EASY", 1)
        
        # 5. Assertions
        print(f"Generated {len(result)} questions")
        assert len(result) == 1
        assert result[0]['text'] == "What is the capital of Nigeria?"
        
    print("AI Content Logic verified.")
        
    print("Verification successful!")

if __name__ == "__main__":
    try:
        asyncio.run(test_ai_generation_logic())
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
