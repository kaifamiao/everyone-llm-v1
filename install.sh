#!/bin/bash

echo "📦 Everyone-LLM 安装脚本"
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
    echo "   安装方法："
    echo "   - macOS: brew install postgresql"
    echo "   - Ubuntu: sudo apt-get install postgresql"
    echo "   - CentOS: sudo yum install postgresql-server"
fi

echo "✅ 环境检查完成"
echo ""

# ============================================
# 后端安装
# ============================================
echo "📦 安装后端依赖..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装 Python 依赖包..."
pip install -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "创建 .env 配置文件..."
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
    echo "✅ .env 文件已创建"
    echo "⚠️  请根据实际情况修改 .env 文件中的数据库连接信息！"
else
    echo "✅ .env 文件已存在，跳过创建"
fi

# 初始化数据库
echo ""
echo "初始化数据库..."
python init_db.py

cd ..

# ============================================
# 前端安装
# ============================================
echo ""
echo "📦 安装前端依赖..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装 Node.js 依赖包..."
    npm install
    echo "✅ 前端依赖安装完成"
else
    echo "✅ node_modules 已存在，跳过安装"
    echo "   如需重新安装，请删除 node_modules 目录后再次运行此脚本"
fi

cd ..

# ============================================
# 完成
# ============================================
echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 下一步："
echo "   1. 检查并修改 backend/.env 文件中的数据库连接信息"
echo "   2. 确保 PostgreSQL 数据库已创建："
echo "      psql -U postgres -c 'CREATE DATABASE everyone_llm;'"
echo "   3. 运行启动脚本：./start.sh"
echo "   或手动启动："
echo "      - 后端：cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "      - 前端：cd frontend && npm run dev"
echo ""

