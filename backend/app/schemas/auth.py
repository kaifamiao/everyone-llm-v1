"""
认证相关 Schema
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

