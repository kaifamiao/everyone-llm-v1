"""
用户相关 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User, UserCredit
from app.models.conversation import Conversation
from app.models.credit import CreditDeduction
from app.schemas.conversation import CreditDeductRequest, CreditDeductResponse
from app.core.config import settings

router = APIRouter()

@router.get("/credits")
async def get_credits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户积分"""
    user_credit = db.query(UserCredit).filter(
        UserCredit.user_id == current_user.id
    ).first()
    
    if not user_credit:
        # 如果不存在，创建积分记录
        user_credit = UserCredit(
            user_id=current_user.id,
            credits=settings.INITIAL_CREDITS
        )
        db.add(user_credit)
        db.commit()
        db.refresh(user_credit)
    
    return {
        "credits": user_credit.credits,
        "updated_at": user_credit.updated_at
    }

@router.post("/credits/deduct", response_model=CreditDeductResponse)
async def deduct_credits(
    deduct_data: CreditDeductRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """扣除积分"""
    # 获取用户积分
    user_credit = db.query(UserCredit).filter(
        UserCredit.user_id == current_user.id
    ).first()
    
    if not user_credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User credit record not found"
        )
    
    # 验证对话属于当前用户
    conversation = db.query(Conversation).filter(
        Conversation.id == deduct_data.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # 计算扣除金额
    deduction_amount = int(deduct_data.token_count * settings.CREDIT_DEDUCTION_RATE)
    
    # 检查积分是否充足
    if user_credit.credits < deduction_amount:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Insufficient credits"
        )
    
    # 使用事务扣除积分
    try:
        # 更新积分
        user_credit.credits -= deduction_amount
        remaining_credits = user_credit.credits
        
        # 创建扣除记录
        deduction = CreditDeduction(
            user_id=current_user.id,
            conversation_id=deduct_data.conversation_id,
            message_id=deduct_data.message_id,
            mode=deduct_data.mode,
            token_count=deduct_data.token_count,
            deduction_amount=deduction_amount,
            deduction_rate=settings.CREDIT_DEDUCTION_RATE,
            remaining_credits=remaining_credits
        )
        db.add(deduction)
        db.commit()
        db.refresh(deduction)
        
        return {
            "success": True,
            "remaining_credits": remaining_credits,
            "deduction_id": deduction.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deduct credits: {str(e)}"
        )

