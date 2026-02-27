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
    from server.routes.ai import generate_questions, QuestionGenRequest
    
    request_data = QuestionGenRequest(
        subject_id=1,
        topic="Geography",
        difficulty="EASY",
        count=1
    )
    
    with patch("server.core.ai.model.generate_content") as mock_generate:
        mock_generate.return_value = mock_response
        
        # 4. Call the endpoint function
        result = await generate_questions(request_data, mock_db)
        
        # 5. Assertions
        print(f"Result message: {result['message']}")
        assert "Successfully generated and saved 1 questions" in result['message']
        assert len(result['questions']) == 1
        
        # Check DB calls
        # We expect at least one add for the question and 4 for the choices
        assert mock_db.add.called
        assert mock_db.commit.called
        print("Database persistence logic verified.")
        
    print("Verification successful!")

if __name__ == "__main__":
    try:
        asyncio.run(test_ai_generation_logic())
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
