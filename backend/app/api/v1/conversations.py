"""
对话相关 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.credit import CreditDeduction
from app.schemas.conversation import (
    ConversationCreate, ConversationUpdate, ConversationResponse,
    MessageCreate, MessageResponse, ConversationDetailResponse,
    CreditDeductRequest, CreditDeductResponse
)

router = APIRouter()

@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取对话列表"""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.status == "active"
    ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()
    return conversations

@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取对话详情"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建对话"""
    conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title or "新对话",
        model=conversation_data.model,
        mode=conversation_data.mode
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新对话"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation_data.title is not None:
        conversation.title = conversation_data.title
    
    db.commit()
    db.refresh(conversation)
    return conversation

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除对话"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    db.delete(conversation)
    db.commit()
    return None

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取消息列表"""
    # 验证对话属于当前用户
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    
    return messages

@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存消息"""
    # 验证对话属于当前用户
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    message = Message(
        conversation_id=conversation_id,
        role=message_data.role,
        content=message_data.content,
        token_count=message_data.token_count
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/search", response_model=List[ConversationResponse])
async def search_conversations(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """搜索对话"""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.status == "active",
        Conversation.title.ilike(f"%{q}%")
    ).order_by(Conversation.updated_at.desc()).limit(50).all()
    return conversations

