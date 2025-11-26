#!/bin/bash

echo "🚀 Everyone-LLM 启动脚本"
echo "================================"
echo ""

# 检查是否已安装
if [ ! -d "backend/venv" ]; then
    echo "❌ 未检测到后端虚拟环境，请先运行安装脚本："
    echo "   ./install.sh"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "❌ 未检测到前端依赖，请先运行安装脚本："
    echo "   ./install.sh"
    exit 1
fi

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "❌ 未找到 backend/.env 文件，请先运行安装脚本："
    echo "   ./install.sh"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 检查端口是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 8000 已被占用，后端服务可能已在运行"
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 3000 已被占用，前端服务可能已在运行"
fi

# 启动后端
echo "📦 启动后端服务..."
cd backend

# 激活虚拟环境
source venv/bin/activate

# 启动后端（后台运行）
echo "启动后端服务 (http://localhost:8000)..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

# 检查后端是否启动成功
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  后端服务可能启动失败，请查看 backend.log"
else
    echo "✅ 后端服务启动成功"
fi

# 启动前端
echo ""
echo "📦 启动前端服务..."
cd frontend

# 启动前端（后台运行）
echo "启动前端服务 (http://localhost:3000)..."
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端 PID: $FRONTEND_PID"

cd ..

# 保存 PID 到文件
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📝 服务信息："
echo "   - 后端 API: http://localhost:8000"
echo "   - API 文档: http://localhost:8000/docs"
echo "   - 前端应用: http://localhost:3000"
echo ""
echo "📋 日志文件："
echo "   - 后端日志: backend.log (tail -f backend.log)"
echo "   - 前端日志: frontend.log (tail -f frontend.log)"
echo ""
echo "🛑 停止服务："
echo "   ./stop.sh"
echo "   或手动停止：kill $BACKEND_PID $FRONTEND_PID"
echo ""

