"""
数据库初始化脚本
创建所有表结构

使用方法：
1. 使用 Python 脚本：python init_db.py
2. 使用 SQL 文件：psql -U postgres -d everyone_llm -f database/init.sql
"""
from app.core.database import engine, Base
from app.models import (
    User, UserProfile, UserCredit, UserSession, LoginLog, VerifyCode,
    Conversation, Message, File,
    CreditDeduction,
    Role, Permission, UserRole, RolePermission
)

def init_db():
    """初始化数据库表（使用 SQLAlchemy ORM）"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("\n提示：也可以使用 SQL 文件初始化：")
    print("  psql -U postgres -d everyone_llm -f database/init.sql")

if __name__ == "__main__":
    init_db()

