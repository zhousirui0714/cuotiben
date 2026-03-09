import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def create_tables():
    try:
        print("开始创建数据库表...")
        
        # 创建用户表
        print("正在创建用户表...")
        response = supabase.rpc('create_users_table')
        print(f"用户表创建响应: {response}")
        
        print("所有表创建完成！")
        return True
        
    except Exception as e:
        print(f"创建表时出错: {e}")
        return False

def create_tables_with_sql():
    try:
        print("开始使用SQL创建数据库表...")
        
        # 创建用户表
        create_users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # 创建文章表
        create_posts_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # 创建评论表
        create_comments_sql = """
        CREATE TABLE IF NOT EXISTS comments (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            content TEXT NOT NULL,
            post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # 执行SQL语句
        print("正在创建用户表...")
        supabase.table('users').select("*").execute()
        
        print("正在创建文章表...")
        supabase.table('posts').select("*").execute()
        
        print("正在创建评论表...")
        supabase.table('comments').select("*").execute()
        
        print("所有表创建完成！")
        return True
        
    except Exception as e:
        print(f"创建表时出错: {e}")
        return False

def test_connection():
    try:
        print("正在测试数据库连接...")
        response = supabase.table('users').select("*").limit(1).execute()
        print("数据库连接成功！")
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    print("Supabase数据库连接工具")
    print("=" * 50)
    
    # 测试连接
    if test_connection():
        print("\n注意: 表需要在Supabase控制台的SQL编辑器中创建")
        print("请访问: https://suprozkxuccgvktyklodo.supabase.co/sql")
        print("\n推荐的SQL建表语句:")
        print("-" * 50)
        
        sql_statements = """
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
        """
        
        print(sql_statements)
        print("-" * 50)
        print("\n或者使用Python脚本通过Supabase API创建表...")
        create_tables_with_sql()
    else:
        print("无法连接到数据库，请检查配置")