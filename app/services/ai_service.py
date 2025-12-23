import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def run_resume_match(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an ATS and hiring expert.

Compare the RESUME and JOB DESCRIPTION.

Return ONLY valid JSON in this exact format:

{{
  "match_score": number (0-100),
  "strengths": [string],
  "missing_skills": [string],
  "recommendation": string
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return json.loads(response.choices[0].message.content)
