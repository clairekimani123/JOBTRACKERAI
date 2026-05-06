# app/services/ai_service.py

import json
import re
import google.generativeai as genai
from app.core.config import settings

# -----------------------------------
# Configure Gemini
# -----------------------------------
genai.configure(api_key=settings.GEMINI_API_KEY)


MODEL_NAME = "models/gemini-1.5-flash"

model = genai.GenerativeModel(MODEL_NAME)


# -----------------------------------
# Helper: safely extract JSON
# -----------------------------------
def extract_json(text: str) -> dict:
    """
    Gemini sometimes returns text before/after JSON.
    This safely extracts the first JSON object found.
    """
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in AI response")
        return json.loads(match.group())
    except Exception as e:
        raise ValueError(f"Failed to parse AI JSON: {e}")


# -----------------------------------
# AI Resume Matching
# -----------------------------------
def run_resume_match(resume_text: str, job_description: str) -> dict:
    """
    Uses Gemini to match a resume against a job description.
    Returns structured match results.
    """

    prompt = f"""
You are an AI recruiter assistant.

Analyze the resume against the job description and return ONLY valid JSON.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"

Return JSON with this exact structure:
{{
  "match_score": number (0-100),
  "strengths": [string],
  "missing_skills": [string],
  "recommendation": string
}}
"""

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
        print(f"⚠️ AI service error: {type(e).__name__}: {e}")
    return {
        "match_score": 0,
        "strengths": [],
        "missing_skills": [],
        "recommendation": f"AI error: {str(e)}"
    }
