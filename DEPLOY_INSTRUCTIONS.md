# 工科数学分析错题本 - 部署说明

## 🎯 项目概述

这是一个专为工科大一下学生设计的数学分析错题本网站，包含以下功能：
- ✅ 拍照/上传图片录入错题
- ✅ 按知识点和题型分类管理
- ✅ 错题进度追踪与统计
- ✅ 复习记录和易错点提醒

## 📁 项目文件结构

```
cuotiben/
├── app.py                      # Flask 后端主程序
├── requirements.txt            # Python 依赖
├── Procfile                    # 部署配置文件
├── .env                        # 环境变量（包含 Supabase 配置）
├── create_tables.sql           # 数据库表结构
├── templates/                  # HTML 模板
│   ├── base.html              # 基础模板
│   ├── index.html             # 首页
│   ├── add_mistake.html       # 录入错题
│   ├── list_mistakes.html     # 错题列表
│   ├── review.html            # 错题详情/复习
│   └── stats.html             # 统计页面
├── static/                     # 静态文件
│   ├── css/                   # CSS 文件
│   ├── js/                    # JavaScript 文件
│   └── uploads/               # 上传的图片
└── ... 其他文档文件
```

## 🚀 部署步骤

### 第一步：在 Supabase 创建数据库表

1. 访问 Supabase 控制台: https://swrozkxuccgvktyklodo.supabase.co
2. 进入 SQL Editor
3. 执行 `create_tables.sql` 文件中的所有 SQL 语句
4. 这会创建以下表：
   - `knowledge_points` - 知识点表
   - `question_types` - 题型表
   - `mistakes` - 错题表
   - `review_logs` - 复习记录表

### 第二步：部署到 EdgeOne Pages

#### 方法1: 通过 Git 仓库部署（推荐）

1. **确保代码已推送到 GitHub**
   ```bash
   git push origin master
   ```

2. **在 EdgeOne 控制台配置**
   - 访问: https://console.cloud.tencent.com/edgeone/pages/project/pages-ddw9ahjai7r6/index
   - 进入"构建部署"页面
   - 确保已连接 GitHub 仓库: `zhousirui0714/cuotiben`
   - 配置构建设置：
     - 构建命令: `pip install -r requirements.txt`
     - 启动命令: `python app.py` 或 `gunicorn app:app`
   - 点击"重新部署"

#### 方法2: 手动上传（如果 EdgeOne 支持）

1. 打包项目文件
2. 在 EdgeOne 控制台上传
3. 配置环境变量

### 第三步：配置环境变量

在 EdgeOne 控制台设置以下环境变量：

```
SUPABASE_URL=https://swrozkxuccgvktyklodo.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cm96a3h1Y2Nndmt0eWtsb2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5Njc1MDQsImV4cCI6MjA4ODU0MzUwNH0.RAdooU-rqBDrkCRMCI_FHC7LAAanBhS5F-H-PdJuRlQ
```

### 第四步：验证部署

1. 访问 EdgeOne 提供的 URL
2. 测试以下功能：
   - 录入 3 道高数错题
   - 按知识点分类查看
   - 查看统计页面
   - 添加复习记录

## 🧪 测试数据

成功标准：录入 3 道高数错题并完成分类标记

### 示例错题1：极限计算
- **标题**: 极限计算错误 - 洛必达法则应用
- **知识点**: 函数极限
- **题型**: 计算题
- **错误原因**: 忘记检查洛必达法则的前提条件，直接求导导致错误

### 示例错题2：导数定义
- **标题**: 导数定义理解错误
- **知识点**: 导数定义
- **题型**: 概念题
- **错误原因**: 混淆了导数的几种等价定义形式

### 示例错题3：定积分计算
- **标题**: 定积分换元法错误
- **知识点**: 定积分
- **题型**: 计算题
- **错误原因**: 换元时忘记改变积分上下限

## 📊 数据库表结构

### 知识点表 (knowledge_points)
预置了工科数学分析的主要知识点：
- 极限与连续（函数极限、数列极限、连续性）
- 导数与微分（导数定义、求导法则、微分中值定理）
- 积分学（不定积分、定积分、重积分）
- 级数（级数收敛、幂级数、傅里叶级数）

### 题型表 (question_types)
- 计算题、证明题、概念题
- 应用题、选择题、填空题

### 错题表 (mistakes)
- 题目内容和图片
- 解答过程和图片
- 错误原因分析
- 知识点和题型关联
- 掌握程度（未掌握/复习中/已掌握）
- 复习次数和最后复习时间

## 🔧 技术栈

- **后端**: Flask + Python 3
- **数据库**: Supabase (PostgreSQL)
- **前端**: HTML + CSS + JavaScript
- **部署**: EdgeOne Pages / 腾讯云

## 📝 注意事项

1. **图片上传**: 支持拍照上传和文件上传，图片保存在 `static/uploads/` 目录
2. **数据持久化**: 所有数据通过 Supabase API 存储，确保数据不会丢失
3. **响应式设计**: 支持手机、平板、电脑访问
4. **环境变量**: 确保 `SUPABASE_URL` 和 `SUPABASE_KEY` 正确配置

## 🐛 常见问题

### Q1: 部署后无法访问？
A: 检查 EdgeOne 控制台日志，确认 Flask 应用正常启动

### Q2: 数据库连接失败？
A: 检查环境变量是否正确设置，Supabase 表是否已创建

### Q3: 图片上传失败？
A: 检查 `static/uploads/` 目录是否有写入权限

### Q4: 如何更新网站？
A: 修改代码后推送到 GitHub，EdgeOne 会自动重新部署

## 📞 技术支持

- Supabase 文档: https://supabase.com/docs
- EdgeOne 文档: https://cloud.tencent.com/document/product/1552
- Flask 文档: https://flask.palletsprojects.com/

---

**项目状态**: 已完成开发，等待部署
**最后更新**: 2026-03-09