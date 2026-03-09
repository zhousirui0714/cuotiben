-- Supabase 数据库建表脚本
-- 请在 Supabase 控制台的 SQL 编辑器中执行此脚本
-- 访问: https://suprozkxuccgvktyklodo.supabase.co/sql

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建文章表
CREATE TABLE IF NOT EXISTS posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建评论表
CREATE TABLE IF NOT EXISTS comments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    content TEXT NOT NULL,
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);

-- 启用行级安全性 (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- 创建 RLS 策略
-- 用户表策略
CREATE POLICY "用户可以查看所有用户" ON users FOR SELECT USING (true);
CREATE POLICY "用户可以插入自己的记录" ON users FOR INSERT WITH CHECK (true);
CREATE POLICY "用户可以更新自己的记录" ON users FOR UPDATE USING (true);

-- 文章表策略
CREATE POLICY "所有人可以查看文章" ON posts FOR SELECT USING (true);
CREATE POLICY "认证用户可以创建文章" ON posts FOR INSERT WITH CHECK (true);
CREATE POLICY "用户可以更新自己的文章" ON posts FOR UPDATE USING (true);
CREATE POLICY "用户可以删除自己的文章" ON posts FOR DELETE USING (true);

-- 评论表策略
CREATE POLICY "所有人可以查看评论" ON comments FOR SELECT USING (true);
CREATE POLICY "认证用户可以创建评论" ON comments FOR INSERT WITH CHECK (true);
CREATE POLICY "用户可以删除自己的评论" ON comments FOR DELETE USING (true);

-- 创建更新时间戳的函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为表创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入测试数据
INSERT INTO users (email, username, password_hash) VALUES
('test@example.com', 'testuser', 'hashed_password_123')
ON CONFLICT (email) DO NOTHING;

-- 查询创建的表
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name IN ('users', 'posts', 'comments')
ORDER BY table_name, ordinal_position;