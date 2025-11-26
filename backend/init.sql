-- Everyone-LLM 数据库初始化脚本
-- PostgreSQL 数据库
-- 版本: 1.0.0

-- ============================================
-- 1. 创建 updated_at 更新触发器函数
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================
-- 2. 用户基础表
-- ============================================

-- 用户基础表
CREATE TABLE IF NOT EXISTS cp_user (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE,
  phone VARCHAR(30) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','disabled','locked')),
  last_login_ip VARCHAR(45),
  last_login_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_username ON cp_user(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON cp_user(email);

-- 用户资料表
CREATE TABLE IF NOT EXISTS cp_user_profile (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL UNIQUE,
  nickname VARCHAR(100),
  avatar_url VARCHAR(500),
  bio TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE
);

-- 用户积分表
CREATE TABLE IF NOT EXISTS cp_user_credit (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL UNIQUE,
  credits BIGINT DEFAULT 100000 NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE
);

-- ============================================
-- 3. 角色权限表
-- ============================================

-- 角色表
CREATE TABLE IF NOT EXISTS cp_role (
  id BIGSERIAL PRIMARY KEY,
  role_name VARCHAR(50) UNIQUE NOT NULL,
  role_code VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 权限表
CREATE TABLE IF NOT EXISTS cp_permission (
  id BIGSERIAL PRIMARY KEY,
  permission_name VARCHAR(100) UNIQUE NOT NULL,
  permission_code VARCHAR(100) UNIQUE NOT NULL,
  resource VARCHAR(100),
  action VARCHAR(50),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户角色关联表
CREATE TABLE IF NOT EXISTS cp_user_role (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  role_id BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES cp_role(id) ON DELETE CASCADE,
  UNIQUE(user_id, role_id)
);

CREATE INDEX IF NOT EXISTS idx_user_role_user_id ON cp_user_role(user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_role_id ON cp_user_role(role_id);

-- 角色权限关联表
CREATE TABLE IF NOT EXISTS cp_role_permission (
  id BIGSERIAL PRIMARY KEY,
  role_id BIGINT NOT NULL,
  permission_id BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES cp_role(id) ON DELETE CASCADE,
  FOREIGN KEY (permission_id) REFERENCES cp_permission(id) ON DELETE CASCADE,
  UNIQUE(role_id, permission_id)
);

CREATE INDEX IF NOT EXISTS idx_role_permission_role_id ON cp_role_permission(role_id);

-- ============================================
-- 4. 会话管理表
-- ============================================

-- 用户会话表
CREATE TABLE IF NOT EXISTS cp_user_session (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  session_token VARCHAR(255) UNIQUE NOT NULL,
  refresh_token VARCHAR(255) UNIQUE NOT NULL,
  device_info VARCHAR(255),
  ip_address VARCHAR(45),
  user_agent TEXT,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_session_user_id ON cp_user_session(user_id);
CREATE INDEX IF NOT EXISTS idx_session_token ON cp_user_session(session_token);
CREATE INDEX IF NOT EXISTS idx_session_expires_at ON cp_user_session(expires_at);

-- 登录日志表
CREATE TABLE IF NOT EXISTS cp_login_log (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT,
  username VARCHAR(50),
  login_type VARCHAR(20) CHECK (login_type IN ('username','email','phone')),
  ip_address VARCHAR(45),
  user_agent TEXT,
  status VARCHAR(20) CHECK (status IN ('success','failed','blocked')),
  failure_reason TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_login_log_user_id ON cp_login_log(user_id);
CREATE INDEX IF NOT EXISTS idx_login_log_created_at ON cp_login_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_login_log_status ON cp_login_log(status);

-- 验证码表
CREATE TABLE IF NOT EXISTS cp_verify_code (
  id BIGSERIAL PRIMARY KEY,
  receiver VARCHAR(100) NOT NULL,
  code VARCHAR(20) NOT NULL,
  code_type VARCHAR(20) CHECK (code_type IN ('register','login','reset_password','bind','unbind')),
  channel VARCHAR(20) CHECK (channel IN ('email','sms')),
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','used','expired')),
  ip_address VARCHAR(45),
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_verify_code_receiver ON cp_verify_code(receiver);
CREATE INDEX IF NOT EXISTS idx_verify_code_code ON cp_verify_code(code);
CREATE INDEX IF NOT EXISTS idx_verify_code_expires_at ON cp_verify_code(expires_at);

-- ============================================
-- 5. 对话及消息表
-- ============================================

-- 对话表
CREATE TABLE IF NOT EXISTS cp_conversation (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  title VARCHAR(255),
  model VARCHAR(50),
  mode VARCHAR(10) CHECK (mode IN ('AI','DOC','KB','DB','WEB','IMG','MCP')),
  status VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active','archived')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_conversation_user_id ON cp_conversation(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_updated_at ON cp_conversation(updated_at DESC);

-- 消息表
CREATE TABLE IF NOT EXISTS cp_message (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL,
  role VARCHAR(20) CHECK (role IN ('user','assistant','system')),
  content TEXT NOT NULL,
  token_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES cp_conversation(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_message_conversation_id ON cp_message(conversation_id);
CREATE INDEX IF NOT EXISTS idx_message_created_at ON cp_message(created_at);

-- 文件上传表（用于文档对话和图片对话）
CREATE TABLE IF NOT EXISTS cp_file (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  conversation_id BIGINT,
  file_name VARCHAR(255) NOT NULL,
  file_type VARCHAR(50),
  file_size BIGINT,
  file_path VARCHAR(500) NOT NULL,
  file_url VARCHAR(500),
  upload_type VARCHAR(20) CHECK (upload_type IN ('document','image')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE,
  FOREIGN KEY (conversation_id) REFERENCES cp_conversation(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_file_user_id ON cp_file(user_id);
CREATE INDEX IF NOT EXISTS idx_file_conversation_id ON cp_file(conversation_id);
CREATE INDEX IF NOT EXISTS idx_file_upload_type ON cp_file(upload_type);

-- ============================================
-- 6. 积分扣除记录表
-- ============================================

-- 积分扣除记录表（记录每次积分扣除的详细信息，关联用户、对话、对话方式）
CREATE TABLE IF NOT EXISTS cp_credit_deduction (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  conversation_id BIGINT NOT NULL,
  message_id BIGINT,
  mode VARCHAR(10) CHECK (mode IN ('AI','DOC','KB','DB','WEB','IMG','MCP')),
  token_count INT NOT NULL,
  deduction_amount BIGINT NOT NULL,
  deduction_rate DECIMAL(10,4) DEFAULT 1.0,
  remaining_credits BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES cp_user(id) ON DELETE CASCADE,
  FOREIGN KEY (conversation_id) REFERENCES cp_conversation(id) ON DELETE CASCADE,
  FOREIGN KEY (message_id) REFERENCES cp_message(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_credit_deduction_user_id ON cp_credit_deduction(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_deduction_conversation_id ON cp_credit_deduction(conversation_id);
CREATE INDEX IF NOT EXISTS idx_credit_deduction_created_at ON cp_credit_deduction(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_credit_deduction_mode ON cp_credit_deduction(mode);
CREATE INDEX IF NOT EXISTS idx_credit_deduction_user_mode ON cp_credit_deduction(user_id, mode);

-- ============================================
-- 7. 创建触发器（用于自动更新 updated_at 字段）
-- ============================================

-- 删除已存在的触发器（如果存在）
DROP TRIGGER IF EXISTS update_user_updated_at ON cp_user;
DROP TRIGGER IF EXISTS update_user_profile_updated_at ON cp_user_profile;
DROP TRIGGER IF EXISTS update_user_credit_updated_at ON cp_user_credit;
DROP TRIGGER IF EXISTS update_conversation_updated_at ON cp_conversation;
DROP TRIGGER IF EXISTS update_role_updated_at ON cp_role;

-- 创建触发器
CREATE TRIGGER update_user_updated_at 
    BEFORE UPDATE ON cp_user
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profile_updated_at 
    BEFORE UPDATE ON cp_user_profile
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_credit_updated_at 
    BEFORE UPDATE ON cp_user_credit
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversation_updated_at 
    BEFORE UPDATE ON cp_conversation
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_role_updated_at 
    BEFORE UPDATE ON cp_role
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 8. 初始化数据（可选）
-- ============================================

-- 可以在这里添加初始数据，例如：
-- INSERT INTO cp_role (role_name, role_code, description) VALUES 
--   ('管理员', 'admin', '系统管理员'),
--   ('普通用户', 'user', '普通用户');

-- ============================================
-- 完成
-- ============================================

-- 显示创建的表
SELECT 
    schemaname,
    tablename
FROM 
    pg_tables
WHERE 
    schemaname = 'public' 
    AND tablename LIKE 'cp_%'
ORDER BY 
    tablename;

