# 数据库脚本说明

本目录包含 Everyone-LLM 项目的数据库初始化和管理脚本。

## 文件说明

### init.sql
完整的数据库初始化脚本，包含：
- 所有表的创建语句
- 索引的创建
- 触发器的创建
- 触发器函数的定义

### drop_all.sql
删除所有数据库表和触发器的脚本（用于重置数据库）

## 使用方法

### 初始化数据库

1. **创建数据库**（如果还没有创建）：
```bash
psql -U postgres -c "CREATE DATABASE everyone_llm;"
```

2. **运行初始化脚本**：
```bash
psql -U postgres -d everyone_llm -f database/init.sql
```

或者使用 Python 脚本：
```bash
cd backend
python init_db.py
```

### 重置数据库

⚠️ **警告**：此操作将删除所有数据！

```bash
psql -U postgres -d everyone_llm -f database/drop_all.sql
psql -U postgres -d everyone_llm -f database/init.sql
```

## 表结构说明

### 用户相关表
- `cp_user` - 用户基础表
- `cp_user_profile` - 用户资料表
- `cp_user_credit` - 用户积分表
- `cp_user_session` - 用户会话表

### 认证相关表
- `cp_login_log` - 登录日志表
- `cp_verify_code` - 验证码表

### 角色权限表
- `cp_role` - 角色表
- `cp_permission` - 权限表
- `cp_user_role` - 用户角色关联表
- `cp_role_permission` - 角色权限关联表

### 对话相关表
- `cp_conversation` - 对话表
- `cp_message` - 消息表
- `cp_file` - 文件上传表

### 积分相关表
- `cp_credit_deduction` - 积分扣除记录表

## 注意事项

1. **PostgreSQL 语法**：所有脚本使用 PostgreSQL 语法
2. **外键约束**：表之间有外键约束，删除时需要注意顺序
3. **触发器**：`updated_at` 字段通过触发器自动更新
4. **索引**：已为常用查询字段创建索引，提升查询性能

## 备份和恢复

### 备份数据库
```bash
pg_dump -U postgres -d everyone_llm > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 恢复数据库
```bash
psql -U postgres -d everyone_llm < backup_20240101_120000.sql
```

## 查看表结构

```sql
-- 查看所有表
\dt

-- 查看表结构
\d cp_user

-- 查看所有表及其行数
SELECT 
    schemaname,
    tablename,
    (SELECT COUNT(*) FROM information_schema.tables t2 
     WHERE t2.table_schema = t.schemaname 
     AND t2.table_name = t.tablename) as row_count
FROM pg_tables t
WHERE schemaname = 'public' 
    AND tablename LIKE 'cp_%'
ORDER BY tablename;
```

