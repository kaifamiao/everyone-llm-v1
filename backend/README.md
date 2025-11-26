# Everyone-LLM Backend

FastAPI 后端服务

## 环境要求

- Python 3.11+
- PostgreSQL 数据库

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 修改 `.env` 中的数据库连接信息和其他配置

## 初始化数据库

```bash
python init_db.py
```

## 运行

```bash
uvicorn main:app --reload
```

服务将在 `http://localhost:8000` 启动

## API 文档

启动服务后，访问 `http://localhost:8000/docs` 查看 Swagger API 文档

## 主要功能

- ✅ 用户注册、登录、JWT 认证
- ✅ 对话管理（创建、查询、更新、删除）
- ✅ 消息管理（保存、查询）
- ✅ 积分系统（查询、扣除）
- ✅ 积分扣除记录

