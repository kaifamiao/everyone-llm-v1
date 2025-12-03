"""
数据库初始化脚本
创建所有表结构并创建测试用户

使用方法：
1. 使用 Python 脚本：python init_db.py
2. 使用 SQL 文件：psql -U postgres -d everyone_llm -f database/init.sql
"""
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.core.config import settings
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
    
    # 创建测试用户
    db = SessionLocal()
    try:
        # 检查测试用户是否已存在
        existing_user = db.query(User).filter(User.username == "test").first()
        if not existing_user:
            print("\nCreating test user...")
            test_user = User(
                username="test",
                email="test@example.com",
                password_hash=get_password_hash("test123"),
                status="active"
            )
            db.add(test_user)
            db.flush()
            
            # 创建用户积分记录
            user_credit = UserCredit(
                user_id=test_user.id,
                credits=settings.INITIAL_CREDITS
            )
            db.add(user_credit)
            db.commit()
            
            print(f"Test user created successfully!")
            print(f"  Username: test")
            print(f"  Password: test123")
            print(f"  Email: test@example.com")
            print(f"  Initial Credits: {settings.INITIAL_CREDITS}")
        else:
            print("\nTest user already exists.")
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n提示：也可以使用 SQL 文件初始化：")
    print("  psql -U postgres -d everyone_llm -f database/init.sql")

if __name__ == "__main__":
    init_db()

