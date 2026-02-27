import asyncio
import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Add project root to path
sys.path.insert(0, os.getcwd())

# Set dummy key for client initialization
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"

async def test_essay_and_interview_logic():
    print("Starting verification of AI Essay and Interview logic...")
    
    # 1. Mock Essay Response
    mock_essay_response = MagicMock()
    mock_essay_response.text = json.dumps({
        "overall_score": "7.5",
        "breakdown": {"Task Response": 8, "Coherence": 7},
        "strengths": ["Clear arguments"],
        "weaknesses": ["Minor grammar issues"],
        "corrections": [],
        "improvement_plan": "Practice more transitions."
    })
    
    # 2. Mock Interview Response
    mock_intv_response = MagicMock()
    mock_intv_response.text = json.dumps({
        "confidence_rating": 8,
        "content_rating": 7,
        "positive_aspects": ["Good eye contact (simulated)"],
        "areas_for_improvement": ["Be more concise"],
        "model_response": "...",
        "overall_feedback": "Well done."
    })
    
    # 3. Mock DB Session
    mock_db = MagicMock()
    
    # 4. Import components
    from server.routes.ai import grade_essay, EssaySubmission, simulate_interview, InterviewRequest
    
    # Test Essay Grading
    essay_req = EssaySubmission(content="I think technology is good.", criteria="IELTS")
    with patch("server.core.ai.model.generate_content") as mock_generate:
        mock_generate.return_value = mock_essay_response
        result = await grade_essay(essay_req, user_id=1, db=mock_db)
        print(f"Essay grading result: {result['overall_score']}")
        assert result['overall_score'] == "7.5"
        assert mock_db.add.called
        assert mock_db.commit.called
        print("Essay grading persistence verified.")

    # Test Interview Simulation
    mock_db.reset_mock()
    intv_req = InterviewRequest(user_id=1, question="Tell me about yourself", user_answer="I am a developer.")
    with patch("server.core.ai.model.generate_content") as mock_generate:
        mock_generate.return_value = mock_intv_response
        result = await simulate_interview(intv_req, db=mock_db)
        print(f"Interview simulation result: {result['confidence_rating']}")
        assert result['confidence_rating'] == 8
        assert mock_db.add.called
        assert mock_db.commit.called
        print("Interview simulation persistence verified.")
        
    print("Verification successful!")

if __name__ == "__main__":
    try:
        asyncio.run(test_essay_and_interview_logic())
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
