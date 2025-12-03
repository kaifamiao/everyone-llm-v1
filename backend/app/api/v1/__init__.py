"""
API v1 路由
"""
from fastapi import APIRouter
from app.api.v1 import auth, user, conversations, chat

api_router = APIRouter()

# 注册子路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(chat.router, tags=["chat"])
