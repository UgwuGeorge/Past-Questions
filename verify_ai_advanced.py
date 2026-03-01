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
    from agent_core.core.agent import ExamAgent
    
    agent = ExamAgent()
    
    # Test Essay Grading
    with patch("agent_core.core.ai.model.generate_content") as mock_generate:
        mock_generate.return_value = mock_essay_response
        result_json = await agent.grade_essay("I think technology is good.", "IELTS")
        result = json.loads(result_json)
        print(f"Essay grading result: {result['overall_score']}")
        assert result['overall_score'] == "7.5"
        print("Essay grading logic verified.")

    # Test Interview Simulation
    with patch("agent_core.core.ai.model.generate_content") as mock_generate:
        mock_generate.return_value = mock_intv_response
        result_json = await agent.run_interview_coach("Tell me about yourself", "I am a developer.")
        result = json.loads(result_json)
        print(f"Interview simulation result: {result['confidence_rating']}")
        assert result['confidence_rating'] == 8
        print("Interview simulation logic verified.")
        
    print("Verification successful!")

if __name__ == "__main__":
    try:
        asyncio.run(test_essay_and_interview_logic())
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
