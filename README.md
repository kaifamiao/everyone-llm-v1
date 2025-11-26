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
│   ├── main.py          # 应用入口
│   ├── init_db.py       # 数据库初始化
│   └── requirements.txt  # Python 依赖
├── frontend/            # Nuxt4 前端
│   ├── components/      # Vue 组件
│   ├── pages/           # 页面
│   ├── stores/          # Pinia Stores
│   ├── services/        # API 服务
│   └── assets/          # 静态资源
├── README.md            # 项目说明
└── 设计说明书V0.01.md   # 设计文档
```

## 📋 前置要求

- **Python 3.11+**
- **Node.js 18+** 和 npm
- **PostgreSQL 数据库**（已安装并运行）

## 🚀 快速开始

### 第一步：启动 PostgreSQL 数据库

确保 PostgreSQL 服务正在运行：

```bash
# macOS (使用 Homebrew)
brew services start postgresql

# Linux (使用 systemd)
sudo systemctl start postgresql

# Windows
# 通过服务管理器启动 PostgreSQL 服务
```

### 第二步：创建数据库

连接到 PostgreSQL 并创建数据库：

```bash
# 连接到 PostgreSQL
psql -U postgres

# 在 psql 中执行
CREATE DATABASE everyone_llm;
\q
```

### 第三步：配置并启动后端

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
# 创建 .env 文件
cat > .env << EOF
DATABASE_URL=postgresql://postgres:password@localhost:5432/everyone_llm
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_BASE_URL=https://api.kfm.plus/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
INITIAL_CREDITS=100000
CREDIT_DEDUCTION_RATE=1.0
EOF

# 注意：请根据实际情况修改 DATABASE_URL 中的用户名和密码

# 5. 初始化数据库表
# 方式1：使用 SQL 文件（推荐）
psql -U postgres -d everyone_llm -f init.sql

# 方式2：使用 Python 脚本
python init_db.py

# 6. 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 启动

**验证后端是否运行：**
- 访问 `http://localhost:8000/docs` 查看 Swagger API 文档
- 访问 `http://localhost:8000/health` 应该返回 `{"status": "ok"}`

### 第四步：配置并启动前端

打开**新的终端窗口**：

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

前端将在 `http://localhost:3000` 启动

**验证前端是否运行：**
- 浏览器访问 `http://localhost:3000`
- 应该能看到 Everyone-LLM 界面

## 🔧 详细配置说明

### 后端环境变量配置

编辑 `backend/.env` 文件：

```env
# 数据库连接（根据实际情况修改）
DATABASE_URL=postgresql://用户名:密码@localhost:5432/everyone_llm

# JWT 密钥（生产环境请使用强随机密钥）
JWT_SECRET_KEY=your-secret-key-here

# CORS 允许的源（前端地址）
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# 积分配置
INITIAL_CREDITS=100000
CREDIT_DEDUCTION_RATE=1.0

# API 配置
API_BASE_URL=https://api.kfm.plus/v1
```

### 前端 API 配置

前端默认 API 地址在 `frontend/nuxt.config.ts` 中配置：

```typescript
runtimeConfig: {
  public: {
    apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
  }
}
```

如需修改，可以：
1. 设置环境变量：`export API_BASE_URL=http://your-api-url`
2. 或直接修改 `nuxt.config.ts` 中的默认值

## 📝 测试运行

### 测试后端 API

1. **访问 API 文档**：`http://localhost:8000/docs`
2. **测试健康检查**：
   ```bash
   curl http://localhost:8000/health
   ```
   应该返回：`{"status": "ok"}`

3. **测试用户注册**（在 Swagger UI 中）：
   - 找到 `/api/v1/auth/register` 接口
   - 点击 "Try it out"
   - 输入测试数据：
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "test123456"
     }
     ```
   - 点击 "Execute"

### 测试前端

1. 打开浏览器访问 `http://localhost:3000`
2. 应该能看到：
   - 左侧边栏（Logo、新建对话按钮、对话列表）
   - 右侧主聊天区域
   - 底部输入框

## ⚠️ 常见问题

### 1. 数据库连接失败

**错误信息**：`could not connect to server`

**解决方法**：
- 检查 PostgreSQL 是否运行：`psql -U postgres -c "SELECT version();"`
- 检查 `.env` 中的 `DATABASE_URL` 是否正确
- 确认数据库 `everyone_llm` 已创建

### 2. 端口被占用

**错误信息**：`Address already in use`

**解决方法**：
- 后端：修改 `uvicorn` 命令中的端口：`--port 8001`
- 前端：修改 `nuxt.config.ts` 中的端口配置，或使用：`npm run dev -- --port 3001`

### 3. Python 依赖安装失败

**解决方法**：
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像（可选）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. Node.js 依赖安装失败

**解决方法**：
```bash
# 清除缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install
```

### 5. CORS 错误

**错误信息**：`Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**解决方法**：
- 检查后端 `.env` 中的 `CORS_ORIGINS` 是否包含前端地址
- 重启后端服务

### 6. 前端无法连接后端

**解决方法**：
- 确认后端服务正在运行
- 检查浏览器控制台的网络请求
- 确认 `nuxt.config.ts` 中的 API 地址正确

## ✨ 功能特性

### 已实现功能

✅ **后端**
- 用户注册、登录、JWT 认证
- 对话管理（创建、查询、更新、删除）
- 消息管理（保存、查询）
- 积分系统（查询、扣除）
- 积分扣除记录
- PostgreSQL 数据库存储

✅ **前端**
- 响应式布局（PC 和移动端）
- 对话管理（创建、选择、删除、搜索）
- 7种对话模式（AI、文档、知识库、数据库、Web、图片、MCP）
- SSE 流式响应（基础实现）
- Markdown 渲染
- 积分显示
- 设置面板（主题、API 配置、AI 参数）
- Pinia 状态管理

### 待完善功能

⚠️ **需要进一步完善**
- 完整的 SSE 流式响应处理
- 文件上传功能（文档、图片）
- 知识库和数据库选择界面
- Web 搜索和 MCP 配置界面
- 对话标题自动生成（AI 生成）
- 用户登录/注册页面
- Token 刷新机制
- 错误处理和提示优化

## 🎯 使用指南

项目成功运行后，你可以：

1. **注册用户账号**：通过 API 文档或前端界面注册
2. **创建对话**：点击"新建对话"按钮
3. **选择对话模式**：在输入框上方选择 7 种对话模式之一
4. **选择 AI 模型**：选择 GPT-4o、Claude 等模型
5. **发送消息**：在输入框中输入消息并发送
6. **查看积分**：在侧边栏查看当前积分（初始 100,000 分）
7. **配置设置**：点击设置按钮配置 API Key 等参数
8. **导出对话**：点击导出按钮导出对话记录（JSON 格式）

## 💡 开发提示

1. **后端热重载**：使用 `--reload` 参数，代码修改后自动重启
2. **前端热重载**：Nuxt 默认支持，修改代码后自动刷新
3. **查看日志**：后端日志在终端输出，前端日志在浏览器控制台
4. **调试工具**：
   - 后端：使用 Swagger UI 测试 API (`http://localhost:8000/docs`)
   - 前端：使用 Vue DevTools 调试 Pinia 状态
5. **数据库迁移**：建议使用 Alembic 进行数据库迁移管理
6. **代码规范**：遵循 Python PEP 8 和 JavaScript ESLint 规范

## 📚 API 文档

启动后端服务后，访问以下地址查看 API 文档：

- **Swagger UI**：`http://localhost:8000/docs`
- **ReDoc**：`http://localhost:8000/redoc`

## 🔐 安全注意事项

1. **生产环境配置**：
   - 修改 `JWT_SECRET_KEY` 为强随机密钥
   - 使用 HTTPS
   - 配置正确的 CORS 源
   - 设置数据库访问权限

2. **密码安全**：
   - 使用强密码策略
   - 密码使用 bcrypt 加密存储

3. **API 安全**：
   - 所有 API 请求需要 JWT 认证（除注册/登录外）
   - 实现请求限流
   - 验证输入数据

## 📄 相关文档

- **设计说明书**：`设计说明书V0.01.md`
- **后端 README**：`backend/README.md`
- **前端 README**：`frontend/README.md`
- **SQL 文件说明**：`backend/README_SQL.md`

## 📊 数据库 SQL 文件

项目提供了完整的 SQL 初始化脚本：

- **`backend/init.sql`** - 完整的数据库初始化脚本（推荐使用）
- **`backend/drop_all_tables.sql`** - 数据库清理脚本（谨慎使用）

**使用 SQL 文件初始化数据库：**

```bash
# 连接到数据库并执行 SQL 文件
psql -U postgres -d everyone_llm -f backend/init.sql
```

详细说明请参考 `backend/README_SQL.md`

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目基于 NextChat 开源项目改造

## 🙏 致谢

- [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) - 原始项目
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Nuxt](https://nuxt.com/) - 前端框架

---

如有问题或建议，请提交 Issue 或 Pull Request。
