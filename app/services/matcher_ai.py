import google.generativeai as genai
import json
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def ai_match_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an ATS system.

Compare the resume and job description below.

Resume:
{resume_text}

Job Description:
{job_description}

Respond ONLY in valid JSON with this format:

{{
  "match_score": number (0-100),
  "strengths": [string],
  "missing_skills": [string],
  "recommendation": string
}}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        # Fallback (never crash API)
        return {
            "match_score": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendation": "AI parsing failed."
        }
