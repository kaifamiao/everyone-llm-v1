"""
聊天 API 代理
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import httpx
from typing import AsyncGenerator

from app.core.database import get_db
from app.core.config import settings
from app.api.v1.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/chat/completions")
async def chat_completions(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    代理聊天完成请求到外部 API
    支持流式响应
    """
    # 获取请求体
    body = await request.json()
    
    # 构建外部 API URL
    url = f"{settings.API_BASE_URL}/chat/completions"
    
    # 准备请求头
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # 检查是否是流式请求
    is_stream = body.get("stream", False)
    
    async def generate_stream() -> AsyncGenerator[bytes, None]:
        """生成流式响应"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                url,
                json=body,
                headers=headers
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"External API error: {error_text.decode()}"
                    )
                
                async for chunk in response.aiter_bytes():
                    yield chunk
    
    if is_stream:
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )
    else:
        # 非流式请求
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=body,
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"External API error: {response.text}"
                )
            
            return response.json()
