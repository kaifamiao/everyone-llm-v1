"""
对话和消息相关模型
"""
from sqlalchemy import Column, BigInteger, String, Text, Integer, TIMESTAMP, ForeignKey, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Conversation(Base):
    """对话表"""
    __tablename__ = "cp_conversation"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255))
    model = Column(String(50))
    mode = Column(String(10))  # AI, DOC, KB, DB, WEB, IMG, MCP
    status = Column(String(10), default="active", server_default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("mode IN ('AI','DOC','KB','DB','WEB','IMG','MCP')", name="check_conversation_mode"),
        CheckConstraint("status IN ('active','archived')", name="check_conversation_status"),
        Index("idx_conversation_updated_at", "updated_at"),
    )
    
    # 关系
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    files = relationship("File", back_populates="conversation")
    credit_deductions = relationship("CreditDeduction", back_populates="conversation")

class Message(Base):
    """消息表"""
    __tablename__ = "cp_message"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(BigInteger, ForeignKey("cp_conversation.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20))  # user, assistant, system
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0, server_default="0")
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        CheckConstraint("role IN ('user','assistant','system')", name="check_message_role"),
    )
    
    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    credit_deductions = relationship("CreditDeduction", back_populates="message")

class File(Base):
    """文件上传表"""
    __tablename__ = "cp_file"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(BigInteger, ForeignKey("cp_conversation.id", ondelete="SET NULL"), index=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(BigInteger)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500))
    upload_type = Column(String(20))  # document, image
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("upload_type IN ('document','image')", name="check_upload_type"),
        Index("idx_file_upload_type", "upload_type"),
    )
    
    # 关系
    conversation = relationship("Conversation", back_populates="files")

