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



**Achievements So Far**

✔ Fully functional backend API
✔ Secure authentication system
✔ Resume upload and parsing
✔ Job application tracking
✔ AI pipeline wired end-to-end
✔ Production-ready architecture

The backend is 90% complete, with only AI model selection remaining.