import json
import re
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def extract_json(text: str) -> dict:
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in AI response")
        return json.loads(match.group())
    except Exception as e:
        raise ValueError(f"Failed to parse AI JSON: {e}")


def run_resume_match(resume_text: str, job_description: str) -> dict:
    prompt = (
        "You are an AI recruiter assistant.\n"
        "Analyze the resume against the job description and return ONLY valid JSON.\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        "Return JSON with this exact structure:\n"
        '{"match_score": number between 0 and 100, '
        '"strengths": [list of strings], '
        '"missing_skills": [list of strings], '
        '"recommendation": "string"}'
    )

    try:
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("Empty response from Gemini")
        ai_output = extract_json(response.text)
        return {
            "match_score": int(ai_output.get("match_score", 0)),
            "strengths": ai_output.get("strengths", []),
            "missing_skills": ai_output.get("missing_skills", []),
            "recommendation": ai_output.get("recommendation", ""),
        }
    except Exception as e:
        error_msg = str(e)
        print(f"AI service error: {type(e).__name__}: {error_msg}")
        return {
            "match_score": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendation": f"AI error: {error_msg}",
        }
