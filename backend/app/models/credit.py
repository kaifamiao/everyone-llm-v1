"""
积分扣除相关模型
"""
from sqlalchemy import Column, BigInteger, Integer, Numeric, String, TIMESTAMP, ForeignKey, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CreditDeduction(Base):
    """积分扣除记录表"""
    __tablename__ = "cp_credit_deduction"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(BigInteger, ForeignKey("cp_conversation.id", ondelete="CASCADE"), nullable=False, index=True)
    message_id = Column(BigInteger, ForeignKey("cp_message.id", ondelete="SET NULL"))
    mode = Column(String(10))  # AI, DOC, KB, DB, WEB, IMG, MCP
    token_count = Column(Integer, nullable=False)
    deduction_amount = Column(BigInteger, nullable=False)
    deduction_rate = Column(Numeric(10, 4), default=1.0, server_default="1.0")
    remaining_credits = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        CheckConstraint("mode IN ('AI','DOC','KB','DB','WEB','IMG','MCP')", name="check_deduction_mode"),
        Index("idx_credit_deduction_created_at", "created_at"),
        Index("idx_credit_deduction_mode", "mode"),
        Index("idx_credit_deduction_user_mode", "user_id", "mode"),
    )
    
    # 关系
    user = relationship("User", foreign_keys=[user_id], overlaps="deductions")
    conversation = relationship("Conversation", back_populates="credit_deductions")
    message = relationship("Message", back_populates="credit_deductions")

