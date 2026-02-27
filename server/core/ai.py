import google.generativeai as genai
import json
import os
from typing import List, Dict

# Configure Gemini
genai.configure(api_key=os.getenv("OPENAI_API_KEY")) # Using the existing variable name for compatibility
model = genai.GenerativeModel("gemini-1.5-flash")

class AIEngine:
    @staticmethod
    async def grade_essay_or_sop(content: str, criteria: str) -> Dict:
        """
        Grades an essay or SOP using Gemini with specific rubrics.
        """
        rubric_instructions = ""
        if "IELTS" in criteria.upper():
            rubric_instructions = """
            Use the IELTS Writing Task 2 descriptors:
            - Task Response (0-9)
            - Coherence and Cohesion (0-9)
            - Lexical Resource (0-9)
            - Grammatical Range and Accuracy (0-9)
            """
        elif "SOP" in criteria.upper() or "SCHOLARSHIP" in criteria.upper():
            rubric_instructions = """
            Evaluate based on scholarship/admission standards:
            - Clarity of Goals
            - Argument and Evidence
            - Personal Voice and Tone
            - Structural Flow
            """

        prompt = f"""
        Act as an expert examiner for {criteria}. 
        {rubric_instructions}
        
        Grade the following submission. Break it down into a JSON object with:
        1. "overall_score": (Float or string band)
        2. "breakdown": {{ "criterion_name": score }}
        3. "strengths": [List of strings]
        4. "weaknesses": [List of strings]
        5. "corrections": [List of {{"original": "...", "suggestion": "...", "reason": "..."}}]
        6. "improvement_plan": "Summary of next steps"
        
        Submission:
        {content}
        
        Return ONLY valid JSON.
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)

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
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        data = json.loads(response.text)
        return data.get("questions", [])

    @staticmethod
    async def simulate_interview(question: str, user_answer: str) -> Dict:
        """
        Simulates an interview response evaluation using Gemini.
        """
        prompt = f"""
        Act as a professional interviewer for a high-stakes scholarship or professional role.
        
        Question Asked: {question}
        User's Response: {user_answer}
        
        Evaluate the response based on:
        1. Confidence and Articulation
        2. Content Relevance and Depth
        3. Structural Clarity
        
        Return a JSON object with:
        - "confidence_rating": (1-10)
        - "content_rating": (1-10)
        - "positive_aspects": [List of strings]
        - "areas_for_improvement": [List of strings]
        - "model_response": "A better version of how the user could have answered"
        - "overall_feedback": "Summary advice"
        
        Return ONLY valid JSON.
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
