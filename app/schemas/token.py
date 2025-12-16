from pydantic import BaseModel
from typing import Optional

# Response model for login endpoint
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Data extracted from JWT for dependency
class TokenData(BaseModel):
    email: Optional[str] = None
