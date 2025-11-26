"""
角色权限相关模型
"""
from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Role(Base):
    """角色表"""
    __tablename__ = "cp_role"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    role_code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Permission(Base):
    """权限表"""
    __tablename__ = "cp_permission"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    permission_name = Column(String(100), unique=True, nullable=False)
    permission_code = Column(String(100), unique=True, nullable=False)
    resource = Column(String(100))
    action = Column(String(50))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class UserRole(Base):
    """用户角色关联表"""
    __tablename__ = "cp_user_role"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("cp_user.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(BigInteger, ForeignKey("cp_role.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )

class RolePermission(Base):
    """角色权限关联表"""
    __tablename__ = "cp_role_permission"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, ForeignKey("cp_role.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(BigInteger, ForeignKey("cp_permission.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )

