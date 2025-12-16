from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Request schemas (what users send to API)
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response schemas (what API returns to users)
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows creating from ORM models

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None