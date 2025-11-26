"""
对话相关 Schema
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ConversationCreate(BaseModel):
    title: Optional[str] = "新对话"
    model: str
    mode: str  # AI, DOC, KB, DB, WEB, IMG, MCP

class ConversationUpdate(BaseModel):
    title: Optional[str] = None

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    model: Optional[str]
    mode: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    role: str  # user, assistant, system
    content: str
    token_count: int = 0

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    token_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []

class CreditDeductRequest(BaseModel):
    conversation_id: int
    message_id: int
    token_count: int
    mode: str

class CreditDeductResponse(BaseModel):
    success: bool
    remaining_credits: int
    deduction_id: int

