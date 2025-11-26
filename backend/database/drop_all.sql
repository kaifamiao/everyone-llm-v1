-- Everyone-LLM 数据库删除脚本
-- 警告：此脚本将删除所有表和数据，请谨慎使用！
-- 使用说明：psql -U postgres -d everyone_llm -f drop_all.sql

-- ============================================
-- 删除所有触发器
-- ============================================

DROP TRIGGER IF EXISTS update_conversation_updated_at ON cp_conversation;
DROP TRIGGER IF EXISTS update_user_updated_at ON cp_user;
DROP TRIGGER IF EXISTS update_user_profile_updated_at ON cp_user_profile;
DROP TRIGGER IF EXISTS update_user_credit_updated_at ON cp_user_credit;
DROP TRIGGER IF EXISTS update_role_updated_at ON cp_role;

-- ============================================
-- 删除触发器函数
-- ============================================

DROP FUNCTION IF EXISTS update_updated_at_column();

-- ============================================
-- 删除所有表（按依赖关系顺序）
-- ============================================

-- 删除积分扣除记录表
DROP TABLE IF EXISTS cp_credit_deduction CASCADE;

-- 删除文件表
DROP TABLE IF EXISTS cp_file CASCADE;

-- 删除消息表
DROP TABLE IF EXISTS cp_message CASCADE;

-- 删除对话表
DROP TABLE IF EXISTS cp_conversation CASCADE;

-- 删除验证码表
DROP TABLE IF EXISTS cp_verify_code CASCADE;

-- 删除登录日志表
DROP TABLE IF EXISTS cp_login_log CASCADE;

-- 删除用户会话表
DROP TABLE IF EXISTS cp_user_session CASCADE;

-- 删除角色权限关联表
DROP TABLE IF EXISTS cp_role_permission CASCADE;

-- 删除用户角色关联表
DROP TABLE IF EXISTS cp_user_role CASCADE;

-- 删除权限表
DROP TABLE IF EXISTS cp_permission CASCADE;

-- 删除角色表
DROP TABLE IF EXISTS cp_role CASCADE;

-- 删除用户积分表
DROP TABLE IF EXISTS cp_user_credit CASCADE;

-- 删除用户资料表
DROP TABLE IF EXISTS cp_user_profile CASCADE;

-- 删除用户基础表（最后删除，因为其他表依赖它）
DROP TABLE IF EXISTS cp_user CASCADE;

-- ============================================
-- 完成
-- ============================================

SELECT 'All tables dropped successfully!' AS message;

