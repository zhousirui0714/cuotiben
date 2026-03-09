import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def create_user(email: str, username: str, password_hash: str):
    try:
        data = {
            "email": email,
            "username": username,
            "password_hash": password_hash
        }
        result = supabase.table('users').insert(data).execute()
        print(f"✅ 用户创建成功: {username}")
        return result.data[0]
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return None

def get_all_users():
    try:
        result = supabase.table('users').select("*").execute()
        print(f"📋 获取到 {len(result.data)} 个用户")
        return result.data
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return []

def create_post(title: str, content: str, user_id: str):
    try:
        data = {
            "title": title,
            "content": content,
            "user_id": user_id
        }
        result = supabase.table('posts').insert(data).execute()
        print(f"✅ 文章创建成功: {title}")
        return result.data[0]
    except Exception as e:
        print(f"❌ 创建文章失败: {e}")
        return None

def get_all_posts():
    try:
        result = supabase.table('posts').select("*").execute()
        print(f"📋 获取到 {len(result.data)} 篇文章")
        return result.data
    except Exception as e:
        print(f"❌ 获取文章失败: {e}")
        return []

def create_comment(content: str, post_id: str, user_id: str):
    try:
        data = {
            "content": content,
            "post_id": post_id,
            "user_id": user_id
        }
        result = supabase.table('comments').insert(data).execute()
        print(f"✅ 评论创建成功")
        return result.data[0]
    except Exception as e:
        print(f"❌ 创建评论失败: {e}")
        return None

def get_posts_with_comments():
    try:
        result = supabase.table('posts').select("*, comments(*)").execute()
        print(f"📋 获取到 {len(result.data)} 篇文章及其评论")
        return result.data
    except Exception as e:
        print(f"❌ 获取文章和评论失败: {e}")
        return []

if __name__ == "__main__":
    print("Supabase 数据库操作示例")
    print("=" * 50)
    
    # 测试连接
    try:
        users = get_all_users()
        if users:
            print("\n🎉 数据库连接成功！表已创建。")
            print("\n当前用户列表:")
            for user in users:
                print(f"  - {user['username']} ({user['email']})")
            
            # 示例操作
            print("\n" + "=" * 50)
            print("示例操作:")
            print("=" * 50)
            
            # 创建新用户
            print("\n1. 创建新用户:")
            new_user = create_user(
                email="demo@example.com",
                username="demouser",
                password_hash="demo123"
            )
            
            if new_user:
                # 创建文章
                print("\n2. 创建文章:")
                new_post = create_post(
                    title="我的第一篇文章",
                    content="这是文章的内容...",
                    user_id=new_user['id']
                )
                
                if new_post:
                    # 创建评论
                    print("\n3. 创建评论:")
                    create_comment(
                        content="很好的文章！",
                        post_id=new_post['id'],
                        user_id=new_user['id']
                    )
                    
                    # 获取所有文章
                    print("\n4. 获取所有文章:")
                    posts = get_all_posts()
                    for post in posts:
                        print(f"  - {post['title']}")
                    
                    # 获取文章和评论
                    print("\n5. 获取文章及其评论:")
                    posts_with_comments = get_posts_with_comments()
                    for post in posts_with_comments:
                        print(f"  文章: {post['title']}")
                        if 'comments' in post:
                            for comment in post['comments']:
                                print(f"    评论: {comment['content']}")
        else:
            print("\n⚠️  数据库表尚未创建")
            print("请先在 Supabase 控制台执行 create_tables.sql 文件中的 SQL 语句")
            print("访问: https://suprozkxuccgvktyklodo.supabase.co/sql")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请确保:")
        print("1. 已在 Supabase 控制台创建了数据库表")
        print("2. .env 文件配置正确")
        print("3. 网络连接正常")