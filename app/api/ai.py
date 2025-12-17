from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import Application, Resume
from app.models.ai_match import AIMatch
from app.schemas.ai import AIMatchCreate, AIMatchOut
from app.services.matcher_ai import ai_match_resume

router = APIRouter(prefix="/api/ai", tags=["AI"])
