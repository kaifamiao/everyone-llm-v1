"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/everyone_llm"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API 配置
    API_BASE_URL: str = "https://api.kfm.plus/v1"
    
    # CORS 配置（支持逗号分隔的字符串）
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # 积分配置
    INITIAL_CREDITS: int = 100000
    CREDIT_DEDUCTION_RATE: float = 1.0  # 1 Token = 1 积分
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

