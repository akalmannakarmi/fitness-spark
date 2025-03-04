from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    expires_at: Optional[float] = None

class UserOut(BaseModel):
    username: str
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str
    expires_at: Optional[float] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: float
