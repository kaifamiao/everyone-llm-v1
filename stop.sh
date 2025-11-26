#!/bin/bash

echo "🛑 Everyone-LLM 停止脚本"
echo "================================"
echo ""

# 从文件读取 PID
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "停止后端服务 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm .backend.pid
        echo "✅ 后端服务已停止"
    else
        echo "⚠️  后端服务进程不存在"
        rm .backend.pid
    fi
else
    # 尝试通过端口查找进程
    BACKEND_PID=$(lsof -ti:8000)
    if [ ! -z "$BACKEND_PID" ]; then
        echo "通过端口找到后端进程 (PID: $BACKEND_PID)，正在停止..."
        kill $BACKEND_PID
        echo "✅ 后端服务已停止"
    else
        echo "⚠️  未找到运行中的后端服务"
    fi
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "停止前端服务 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm .frontend.pid
        echo "✅ 前端服务已停止"
    else
        echo "⚠️  前端服务进程不存在"
        rm .frontend.pid
    fi
else
    # 尝试通过端口查找进程
    FRONTEND_PID=$(lsof -ti:3000)
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "通过端口找到前端进程 (PID: $FRONTEND_PID)，正在停止..."
        kill $FRONTEND_PID
        echo "✅ 前端服务已停止"
    else
        echo "⚠️  未找到运行中的前端服务"
    fi
fi

echo ""
echo "✅ 所有服务已停止"

