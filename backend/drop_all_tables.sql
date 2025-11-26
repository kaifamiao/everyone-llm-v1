-- Everyone-LLM 数据库清理脚本
-- 警告：此脚本将删除所有表和数据，请谨慎使用！
-- PostgreSQL 数据库

-- ============================================
-- 删除所有触发器
-- ============================================

DROP TRIGGER IF EXISTS update_user_updated_at ON cp_user;
DROP TRIGGER IF EXISTS update_user_profile_updated_at ON cp_user_profile;
DROP TRIGGER IF EXISTS update_user_credit_updated_at ON cp_user_credit;
DROP TRIGGER IF EXISTS update_conversation_updated_at ON cp_conversation;
DROP TRIGGER IF EXISTS update_role_updated_at ON cp_role;

-- ============================================
-- 删除所有表（按依赖关系顺序）
-- ============================================

-- 删除关联表（先删除外键依赖的表）
DROP TABLE IF EXISTS cp_credit_deduction CASCADE;
DROP TABLE IF EXISTS cp_file CASCADE;
DROP TABLE IF EXISTS cp_message CASCADE;
DROP TABLE IF EXISTS cp_conversation CASCADE;
DROP TABLE IF EXISTS cp_user_session CASCADE;
DROP TABLE IF EXISTS cp_login_log CASCADE;
DROP TABLE IF EXISTS cp_verify_code CASCADE;
DROP TABLE IF EXISTS cp_user_role CASCADE;
DROP TABLE IF EXISTS cp_role_permission CASCADE;
DROP TABLE IF EXISTS cp_user_profile CASCADE;
DROP TABLE IF EXISTS cp_user_credit CASCADE;

-- 删除基础表
DROP TABLE IF EXISTS cp_permission CASCADE;
DROP TABLE IF EXISTS cp_role CASCADE;
DROP TABLE IF EXISTS cp_user CASCADE;

-- ============================================
-- 删除函数
-- ============================================

DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- ============================================
-- 完成
-- ============================================

-- 验证所有表已删除
SELECT 
    schemaname,
    tablename
FROM 
    pg_tables
WHERE 
    schemaname = 'public' 
    AND tablename LIKE 'cp_%';

-- 如果没有返回任何结果，说明所有表已成功删除

