"""
用户相关模型
"""
from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, ForeignKey, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    """用户基础表"""
    __tablename__ = "cp_user"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(30), unique=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="active", server_default="active")
    last_login_ip = Column(String(45))
    last_login_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('active','disabled','locked')", name="check_user_status"),
    )
    
    # 关系
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    credit = relationship("UserCredit", back_populates="user", uselist=False)
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    """用户资料表"""
    __tablename__ = "cp_user_profile"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), unique=True, nullable=False)
    nickname = Column(String(100))
    avatar_url = Column(String(500))
    bio = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="profile")

class UserCredit(Base):
    """用户积分表"""
    __tablename__ = "cp_user_credit"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), unique=True, nullable=False)
    credits = Column(BigInteger, default=100000, nullable=False, server_default="100000")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="credit")
    deductions = relationship("CreditDeduction", back_populates="user", foreign_keys="CreditDeduction.user_id")

class UserSession(Base):
    """用户会话表"""
    __tablename__ = "cp_user_session"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True, nullable=False)
    device_info = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    expires_at = Column(TIMESTAMP, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_activity_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="sessions")

class LoginLog(Base):
    """登录日志表"""
    __tablename__ = "cp_login_log"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, index=True)
    username = Column(String(50))
    login_type = Column(String(20))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    status = Column(String(20))
    failure_reason = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        CheckConstraint("login_type IN ('username','email','phone')", name="check_login_type"),
        CheckConstraint("status IN ('success','failed','blocked')", name="check_login_status"),
        Index("idx_login_log_created_at", "created_at"),
        Index("idx_login_log_status", "status"),
    )

class VerifyCode(Base):
    """验证码表"""
    __tablename__ = "cp_verify_code"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    receiver = Column(String(100), nullable=False, index=True)
    code = Column(String(20), nullable=False, index=True)
    code_type = Column(String(20))
    channel = Column(String(20))
    status = Column(String(20), default="pending", server_default="pending")
    ip_address = Column(String(45))
    expires_at = Column(TIMESTAMP, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("code_type IN ('register','login','reset_password','bind','unbind')", name="check_code_type"),
        CheckConstraint("channel IN ('email','sms')", name="check_channel"),
        CheckConstraint("status IN ('pending','used','expired')", name="check_code_status"),
    )

