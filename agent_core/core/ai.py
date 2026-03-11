from openai import OpenAI, AsyncOpenAI
import json
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
async_client = AsyncOpenAI(api_key=api_key)
MODEL_ID = "gpt-4o"

class AIEngine:
    @staticmethod
    def grade_essay_or_sop_sync(content: str, criteria: str) -> Dict:
        """Sync version of grading."""
        rubric_instructions = ""
        if "IELTS" in criteria.upper():
            rubric_instructions = "Use the IELTS Writing Task 2 descriptors: Task Response (0-9), Coherence and Cohesion (0-9), Lexical Resource (0-9), Grammatical Range and Accuracy (0-9)"
        elif "SOP" in criteria.upper() or "SCHOLARSHIP" in criteria.upper():
            rubric_instructions = "Evaluate based on scholarship standards: Clarity of Goals, Argument and Evidence, Personal Voice and Tone, Structural Flow"

        prompt = f"Act as an expert examiner for {criteria}. {rubric_instructions}\nSubmission:\n{content}"
        
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def grade_essay_or_sop(content: str, criteria: str) -> Dict:
        """
        Grades an essay or SOP using OpenAI with specific rubrics.
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
        
        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

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
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
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
        
        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("questions", [])

    @staticmethod
    def simulate_interview_sync(question: str, user_answer: str) -> Dict:
        """Sync version of interview evaluation."""
        prompt = f"Act as an interviewer. Question: {question}\nAnswer: {user_answer}\nEvaluate and return ONLY JSON."
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def simulate_interview(question: str, user_answer: str) -> Dict:
        """
        Simulates an interview response evaluation using OpenAI.
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
        
        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    @staticmethod
    async def analyze_syllabus(subject_name: str, questions: List[Dict], extra_content: str = "") -> Dict:
        """
        Analyzes a set of questions and additional material to generate a 'Scheme of Work'.
        """
        # Limit questions to avoid token overflow
        sample_questions = questions[:15]
        
        prompt = f"""
        Act as a Senior Educational Curriculum Designer and Subject Matter Expert for {subject_name}.
        
        I will provide you with a sample of past questions and some raw data from the syllabus/scheme of work.
        Based on this, I want you to "learn" and "describe" the DNAS of this course for a student simulation.
        
        Input Data:
        - Sample Questions: {json.dumps(sample_questions)}
        - Extra Content: {extra_content[:2000]}
        
        Generate a JSON object with:
        1. "subject_name": "{subject_name}"
        2. "scheme_of_work": [A list of key topics identified, e.g., ["Algebra", "Geometry"]]
        3. "structure_analysis": "A detailed explanation of how questions are structured in this subject (e.g., 'Heavy on calculations', 'Conceptual multiple choice')"
        4. "learning_path": [Recommended sequence of topics to master]
        5. "ai_proctor_persona": "A brief description of how the AI should act as a proctor for this specific subject (e.g., 'A patient but rigorous Mathematics Mentor')"
        6. "mastery_tips": ["Tip 1", "Tip 2"]
        
        Return ONLY valid JSON.
        """
        
        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def analyze_syllabus_sync(subject_name: str, questions: List[Dict], extra_content: str = "") -> Dict:
        """Sync version of syllabus analysis."""
        sample_questions = questions[:15]
        prompt = f"""
        Act as a Senior Educational Curriculum Designer and Subject Matter Expert for {subject_name}.
        Input Data:
        - Sample Questions: {json.dumps(sample_questions)}
        - Extra Content: {extra_content[:2000]}
        
        Generate a JSON object with:
        1. "subject_name": "{subject_name}"
        2. "scheme_of_work": [List of topics]
        3. "structure_analysis": "Explanation of structure"
        4. "learning_path": [Recommended sequence]
        5. "ai_proctor_persona": "Persona"
        6. "mastery_tips": ["Tips"]
        
        Return ONLY valid JSON.
        """
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def analyze_exam_result(results: Dict) -> Dict:
        """
        Analyzes the results of a CBT simulation to provide strategic feedback.
        """
        prompt = f"""
        Act as a Senior Educational Consultant and Exam Strategist.
        I have a set of exam results for a user. Analyze them and provide a detailed breakdown and improvement strategy.
        
        Results Data:
        {json.dumps(results)}
        
        Generate a JSON object with:
        1. "overall_assessment": "Short motivational summary of performance"
        2. "strong_topics": [List of topics they mastered]
        3. "critical_gaps": [List of topics they failed or underperformed in]
        4. "action_plan": [Specific steps to improve, e.g., 'Review Newton's Laws', 'Practice 20 objective questions on calculus']
        5. "encouragement": "A supportive closing statement"
        
        Return ONLY valid JSON.
        """
        
        response = await async_client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
