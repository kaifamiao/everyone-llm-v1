# Everyone-LLM

基于 NextChat 开源项目改造的多用户算力平台

## 📖 项目简介

Everyone-LLM 是一个多用户 AI 对话平台，采用前后端分离架构，支持多种对话模式、流式响应、积分系统等功能。

## 🛠️ 技术栈

### 前端
- **Vue3 + Nuxt4** - 前端框架
- **Pinia** - 状态管理
- **Tailwind CSS** - 样式框架
- **Lucide Vue Next** - 图标库
- **Marked** - Markdown 渲染
- **Highlight.js** - 代码高亮

### 后端
- **Python 3.11 + FastAPI** - 后端框架
- **PostgreSQL** - 数据库
- **SQLAlchemy** - ORM
- **JWT + Refresh Token** - 认证机制
- **Pydantic** - 数据验证

## 📁 项目结构

```
code/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/      # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── models/       # 数据库模型
│   │   └── schemas/      # Pydantic Schema
│   ├── database/         # SQL 脚本
│   ├── main.py          # 应用入口
│   └── requirements.txt  # Python 依赖
├── frontend/            # Nuxt4 前端
│   ├── components/      # Vue 组件
│   ├── pages/           # 页面
│   ├── stores/          # Pinia Stores
│   └── services/        # API 服务
├── install.sh           # 安装脚本
├── start.sh             # 启动脚本
├── stop.sh              # 停止脚本
└── README.md            # 项目说明
```

## 📋 前置要求

- **Python 3.11+**
- **Node.js 18+** 和 npm
- **PostgreSQL 数据库**（已安装并运行）

## 🚀 快速开始

### 第一步：启动 PostgreSQL 数据库

```bash
# macOS (使用 Homebrew)
brew services start postgresql

# Linux (使用 systemd)
sudo systemctl start postgresql
```

### 第二步：创建数据库

```bash
psql -U postgres -c "CREATE DATABASE everyone_llm;"
```

### 第三步：安装和启动

**方式一：使用脚本（推荐）**

```bash
# 安装
./install.sh

# 启动
./start.sh

# 停止
./stop.sh
```

**方式二：手动安装**

```bash
# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload

# 前端（新终端）
cd frontend
npm install
npm run dev
```

## 🔧 配置说明

### 后端环境变量

编辑 `backend/.env` 文件：

```env
DATABASE_URL=postgresql://用户名:密码@localhost:5432/everyone_llm
JWT_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 前端 API 配置

前端默认 API 地址在 `frontend/nuxt.config.ts` 中配置。

## ✨ 功能特性

✅ **后端**
- 用户注册、登录、JWT 认证
- 对话管理（创建、查询、更新、删除）
- 消息管理（保存、查询）
- 积分系统（查询、扣除）
- PostgreSQL 数据库存储

✅ **前端**
- 响应式布局（PC 和移动端）
- 对话管理（创建、选择、删除、搜索）
- 7种对话模式（AI、文档、知识库、数据库、Web、图片、MCP）
- SSE 流式响应
- Markdown 渲染
- 积分显示
- 设置面板

## 📝 测试运行

- **后端 API 文档**：`http://localhost:8000/docs`
- **前端应用**：`http://localhost:3000`
- **健康检查**：`http://localhost:8000/health`

## ⚠️ 常见问题

### 数据库连接失败
检查 PostgreSQL 是否运行，确认 `.env` 中的 `DATABASE_URL` 正确。

### 端口被占用
修改端口或停止占用端口的进程。

### CORS 错误
检查后端 `.env` 中的 `CORS_ORIGINS` 是否包含前端地址。

## 📚 相关文档

- **设计说明书**：`设计说明书V0.01.md`
- **运行指南**：`运行指南.md`
- **项目启动指南**：`项目启动指南.md`
- **后端 README**：`backend/README.md`
- **前端 README**：`frontend/README.md`

## 📄 许可证

本项目基于 NextChat 开源项目改造

## 🙏 致谢

- [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) - 原始项目
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Nuxt](https://nuxt.com/) - 前端框架
