# Supabase 数据库设置指南

## 📋 项目信息
- **项目URL**: https://swrozkxuccgvktyklodo.supabase.co
- **数据库状态**: 已连接，但需要创建表

## 🔧 创建数据库表

由于使用的是 anon key，需要在 Supabase 控制台手动创建表。请按照以下步骤操作：

### 方法1: 使用 SQL 编辑器（推荐）

1. 访问 Supabase 控制台: https://suprozkxuccgvktyklodo.supabase.co
2. 点击左侧菜单的 "SQL Editor"
3. 点击 "New query"
4. 复制并执行 [create_tables.sql](file:///d:/zhousirui/新建文件夹%20(2)/cuotiben/create_tables.sql) 文件中的所有 SQL 语句

### 方法2: 使用 Table Editor

1. 访问 Supabase 控制台
2. 点击左侧菜单的 "Table Editor"
3. 点击 "Create a new table"
4. 手动创建以下表：
   - **users**: 用户表
   - **posts**: 文章表  
   - **comments**: 评论表

## 📊 数据库表结构

### users 表
- `id` (UUID, 主键)
- `email` (VARCHAR, 唯一)
- `username` (VARCHAR, 唯一)
- `password_hash` (VARCHAR)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### posts 表
- `id` (UUID, 主键)
- `title` (VARCHAR)
- `content` (TEXT)
- `user_id` (UUID, 外键)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### comments 表
- `id` (UUID, 主键)
- `content` (TEXT)
- `post_id` (UUID, 外键)
- `user_id` (UUID, 外键)
- `created_at` (TIMESTAMP)

## ✅ 验证设置

创建表后，运行以下命令验证连接：

```bash
python setup_database.py
```

如果看到 "数据库连接成功！" 的消息，说明设置完成。

## 📝 使用示例

```python
from supabase import create_client

# 连接到数据库
supabase = create_client(
    "https://swrozkxuccgvktyklodo.supabase.co",
    "your-anon-key"
)

# 插入数据
data = {"email": "test@example.com", "username": "testuser", "password_hash": "123"}
result = supabase.table('users').insert(data).execute()

# 查询数据
users = supabase.table('users').select("*").execute()
```

## 🔐 安全提示

- 当前使用的是 anon key，适合公开访问
- 对于管理员操作，建议使用 service_role key
- 已启用行级安全性 (RLS) 保护数据

## 📚 相关文件

- [.env](file:///d:/zhousirui/新建文件夹%20(2)/cuotiben/.env) - 环境配置
- [setup_database.py](file:///d:/zhousirui/新建文件夹%20(2)/cuotiben/setup_database.py) - 数据库连接脚本
- [create_tables.sql](file:///d:/zhousirui/新建文件夹%20(2)/cuotiben/create_tables.sql) - SQL 建表脚本