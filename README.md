## JobTrackAI Backend Documentation
## Overview

JobTrackAI is an AI-powered job application tracking backend built with FastAPI, PostgreSQL, and JWT authentication.

***.The system allows users to.***:

-Register and authenticate securely

-Track job applications

-Upload and manage resumes (PDF)

-Extract resume text for analysis

-Match resumes against job descriptions using AI

***This backend is designed as a RESTful API and is intended to be consumed by a frontend web application.***

## Tech Stack

-Backend Framework: FastAPI

-Database: PostgreSQL

-ORM: SQLAlchemy

-Migrations: Alembic

-Authentication: JWT (Bearer tokens)

-AI Integration: Google Gemini API

-File Handling: Local file storage

-PDF Text Extraction: pdfplumber

## Project Structure
app/
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── applications.py
│   ├── resumes.py
│   └── ai.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── deps.py
│
├── models/
│   ├── user.py
│   ├── application.py
│   ├── resume.py
│   └── ai_match.py
│
├── schemas/
│   ├── user.py
│   ├── application.py
│   ├── resume.py
│   └── ai_match.py
│
├── services/
│   ├── pdf_extractor.py
│   └── ai_service.py
│
├── main.py
└── alembic/

## Authentication System

***Features***

-User registration

-User login

-JWT-based authentication

-Protected routes using dependency injection

-Security

-Passwords are hashed before storage

-JWT tokens are required for all protected endpoints

-Tokens are validated on every request

***Applications ModulePurpose***

-Allows users to track job applications they have submitted.

-Stored Data

-Company name

-Position title

-Job description

-Application status

-Dates (applied, follow-up)

-Notes and metadata

-Each application is owned by a user and cannot be accessed by others.

***Resume Module Features***

-PDF resume upload

-File storage on disk

-Resume metadata stored in database

-Automatic text extraction

-Important Behavior

-Only text-based PDFs can be extracted successfully

-Scanned/image-based PDFs will result in empty text

-Resume text is stored in extracted_text

-This behavior is expected and aligns with real-world resume parsing systems.

## AI Resume Matching Module
***Endpoint***
POST /api/ai/match

***Functionality***

-Matches a user’s resume against a job description

-Uses extracted resume text

**Generates:**

-Match score

-Strengths

-Missing skills

-AI recommendation

-Validation Rules

-Resume must belong to the authenticated user

-Resume must contain sufficient extracted text

-Job description must exist

-Current Status

-API route is fully functional

-Database operations are correct

-Authentication and authorization are enforced

-AI integration is connected but pending model selection

-AI Integration (Current State)

-The backend integrates with Google Gemini API

-AI prompts are generated dynamically using resume text and job descriptions

-The system currently fails due to model availability mismatch

-Model selection will be finalized after listing available models for the API key

-This is the only remaining backend blocker.

-Error Handling & Logging

-SQLAlchemy query logging enabled

-Clear HTTP error responses (400, 401, 404)

-Internal server errors are logged with full stack traces

-Transaction rollbacks occur safely on failure

## Job Application Management

***Users can:***

-Create job applications

-Store job descriptions, company name, role, status, notes

-Link resumes to applications

- AI Resume Matching

**Endpoint**
-POST /api/ai/match

```
Request Body
{
  "application_id": 1,
  "resume_id": 3
}
200 
Response body 
{
    "id": 7,

    "application_id": 1,

    "resume_id": 3,

    "match_score": 5,

    "strengths": [ "Demonstrated intent to acquire skills in Artificial Intelligence, showing a commitment to future professional development." ],

    "missing_skills": [ "Current Artificial Intelligence skills (as the course completion date is in the future)", "Specific technical or practical skills relevant to bringing ideas into reality", "Evidence of past projects, experience, or achievements demonstrating the ability to 'amend ideas into a reality world'", "Any specific skills (technical, soft, or domain-specific) are missing, as the job description provides no context" ],

    "recommendation": "The candidate should update their resume after the Artificial Intelligence course is completed in December 2025 to reflect acquired skills and knowledge. To better align with the job description's broad requirement to 'amend ideas into a reality world,' the candidate needs to provide concrete examples of past projects, experiences, or achievements that demonstrate initiative, problem-solving abilities, and the successful execution of ideas. Given the extreme vagueness of the job description, it is also recommended to seek clarification on specific skills or experiences required for the role.", 

    "created_at": "2026-01-07T09:22:21.280964+03:00"
}
```

***AI Analysis Includes:***

-Match score (0–100)

-Candidate strengths

-Missing or weak skills

-Actionable hiring recommendation

-Reliability

-Graceful fallback when AI is unavailable

-Always returns valid JSON

-Results stored in the database for history tracking

**AI Model Used**

-Model: models/gemini-2.5 flash

***Reason:***

-Fast

-Stable

-Supports generateContent

-Ideal for text analysis and structured output

## Validation & Error Handling

-Strong request validation using Pydantic

-Response validation enforced

-User-friendly fallback messages

-No frontend-breaking null values


**Achievements So Far**

✔ Fully functional backend API
✔ Secure authentication system
✔ Resume upload and parsing
✔ Job application tracking
✔ AI pipeline wired end-to-end
✔ Production-ready architecture

The backend is 90% complete, with only AI model selection remaining.