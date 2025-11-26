# 数据库 SQL 文件说明

## 文件说明

### 1. `init.sql` - 数据库初始化脚本

完整的数据库初始化 SQL 脚本，包含：
- 所有表结构定义
- 索引创建
- 触发器创建
- 外键约束

**使用方法：**

```bash
# 方法1：使用 psql 命令行
psql -U postgres -d everyone_llm -f init.sql

# 方法2：在 psql 中执行
psql -U postgres -d everyone_llm
\i init.sql
```

### 2. `drop_all_tables.sql` - 数据库清理脚本

删除所有表、触发器和函数的清理脚本。

**警告：此脚本会删除所有数据，请谨慎使用！**

**使用方法：**

```bash
psql -U postgres -d everyone_llm -f drop_all_tables.sql
```

## 表结构说明

### 用户相关表
- `cp_user` - 用户基础表
- `cp_user_profile` - 用户资料表
- `cp_user_credit` - 用户积分表

### 角色权限表
- `cp_role` - 角色表
- `cp_permission` - 权限表
- `cp_user_role` - 用户角色关联表
- `cp_role_permission` - 角色权限关联表

### 会话管理表
- `cp_user_session` - 用户会话表
- `cp_login_log` - 登录日志表
- `cp_verify_code` - 验证码表

### 对话相关表
- `cp_conversation` - 对话表
- `cp_message` - 消息表
- `cp_file` - 文件上传表

### 积分相关表
- `cp_credit_deduction` - 积分扣除记录表

## 初始化方式对比

### 方式1：使用 SQL 文件（推荐）

**优点：**
- 更直观，可以看到完整的 SQL 语句
- 便于版本控制和迁移
- 可以手动调整和优化

**使用方法：**
```bash
psql -U postgres -d everyone_llm -f init.sql
```

### 方式2：使用 Python 脚本

**优点：**
- 自动处理，无需手动执行 SQL
- 与代码模型保持一致

**使用方法：**
```bash
python init_db.py
```

## 注意事项

1. **执行顺序**：SQL 文件已经按照正确的依赖顺序组织，可以直接执行
2. **IF NOT EXISTS**：所有 CREATE TABLE 语句都使用了 `IF NOT EXISTS`，可以安全地重复执行
3. **触发器**：`updated_at` 字段的自动更新通过触发器实现
4. **索引**：所有索引都使用了 `IF NOT EXISTS`，避免重复创建错误

## 数据库迁移建议

对于生产环境，建议使用 Alembic 进行数据库迁移管理：

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

## 验证数据库结构

执行初始化后，可以验证表是否创建成功：

```sql
-- 查看所有表
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename LIKE 'cp_%'
ORDER BY tablename;

-- 查看表结构
\d cp_user
\d cp_conversation
\d cp_message
```

