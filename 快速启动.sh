#!/bin/bash

echo "🚀 Everyone-LLM 快速启动脚本"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.11+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

# 检查 PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  未找到 PostgreSQL，请确保已安装并运行"
fi

echo "✅ 环境检查完成"
echo ""

# 启动后端
echo "📦 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f ".deps_installed" ]; then
    echo "安装后端依赖..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，请先配置环境变量"
    echo "创建 .env 文件..."
    cat > .env << EOL
DATABASE_URL=postgresql://postgres:password@localhost:5432/everyone_llm
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_BASE_URL=https://api.kfm.plus/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
INITIAL_CREDITS=100000
CREDIT_DEDUCTION_RATE=1.0
EOL
    echo "✅ .env 文件已创建，请根据实际情况修改数据库连接信息"
fi

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 启动后端（后台运行）
echo "启动后端服务 (http://localhost:8000)..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

# 启动前端
echo ""
echo "📦 启动前端服务..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端（后台运行）
echo "启动前端服务 (http://localhost:3000)..."
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端 PID: $FRONTEND_PID"

cd ..

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📝 服务信息："
echo "   - 后端 API: http://localhost:8000"
echo "   - API 文档: http://localhost:8000/docs"
echo "   - 前端应用: http://localhost:3000"
echo ""
echo "📋 日志文件："
echo "   - 后端日志: backend.log"
echo "   - 前端日志: frontend.log"
echo ""
echo "🛑 停止服务："
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""


# chmod +x install.sh start.sh stop.sh 快速启动.sh