from google import genai
import json
import os
from typing import List, Dict

# Configure Gemini via the new unified SDK
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.0-flash"

class AIEngine:
    @staticmethod
    def generate_questions_sync(exam_type: str, topic: str, difficulty: str, count: int = 5) -> List[Dict]:
        """Sync version of question generation."""
        prompt = f"""
        Generate {count} multiple choice questions for {exam_type} on the topic: {topic}.
        Difficulty level: {difficulty}.
        
        Format:
        {{
            "questions": [
                {{
                    "text": "Question content",
                    "choices": [
                        {{"text": "Option A", "is_correct": false}},
                        {{"text": "Option B", "is_correct": true}},
                        {{"text": "Option C", "is_correct": false}},
                        {{"text": "Option D", "is_correct": false}}
                    ],
                    "explanation": "Brief explanation"
                }}
            ]
        }}
        Return ONLY valid JSON.
        """
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        return data.get("questions", [])

    @staticmethod
    async def generate_questions(exam_type: str, topic: str, difficulty: str, count: int = 5) -> List[Dict]:
        prompt = f"""
        Generate {count} multiple choice questions for {exam_type} on the topic: {topic}.
        Difficulty level: {difficulty}.
        Ensure these are not common duplicate questions found on the web.
        
        Format:
        {{
            "questions": [
                {{
                    "text": "Question content",
                    "choices": [
                        {{"text": "Option A", "is_correct": false}},
                        {{"text": "Option B", "is_correct": true}},
                        {{"text": "Option C", "is_correct": false}},
                        {{"text": "Option D", "is_correct": false}}
                    ],
                    "explanation": "Why the correct answer is right"
                }}
            ]
        }}
        
        Return ONLY valid JSON.
        """
        
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        return data.get("questions", [])

        data = json.loads(response.text)
        return data.get("questions", [])
