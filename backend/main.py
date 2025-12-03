"""
Everyone-LLM Backend
FastAPI 主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, conversations, user, chat

# 创建数据库表
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理（如果需要）

app = FastAPI(
    title="Everyone-LLM API",
    description="多用户算力平台 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(',')]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["对话"])
app.include_router(user.router, prefix="/api/v1/user", tags=["用户"])
app.include_router(chat.router, prefix="/api/v1", tags=["聊天"])

@app.get("/")
async def root():
    return {"message": "Everyone-LLM API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

