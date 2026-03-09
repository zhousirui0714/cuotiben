# EdgeOne 部署配置

## 📋 项目信息
- **项目名称**: Supabase 数据库设置指南
- **部署类型**: 静态网站
- **主要文件**: `setup_guide.html`

## 🔧 EdgeOne 部署步骤

### 1. 准备部署文件
- **主页面**: `setup_guide.html`
- **资源文件**: 所有静态资源已内联在HTML中
- **配置文件**: 无需特殊配置

### 2. 部署到 EdgeOne

#### 方法1: 使用 EdgeOne 控制台
1. 登录 [EdgeOne 控制台](https://console.cloud.tencent.com/edgeone)
2. 选择 "站点管理" → "添加站点"
3. 输入你的域名
4. 完成域名解析配置
5. 在 "规则引擎" 中配置静态网站托管
6. 上传 `setup_guide.html` 文件

#### 方法2: 使用 EdgeOne API
```bash
# 示例命令
tcc edgeone site create --domain your-domain.com
tcc edgeone origin add --site-id xxx --origin your-github-repo
```

### 3. 配置规则

**推荐规则配置**:
- **缓存规则**: 静态文件缓存 1 小时
- **安全规则**: 启用 WAF 防护
- **HTTPS**: 启用 HTTPS 并配置证书
- **CDN**: 启用全球加速

## 📁 项目结构

```
cuotiben/
├── setup_guide.html        # 主页面
├── README.md              # 项目说明
├── create_tables.sql      # SQL 建表脚本
├── example_usage.py       # 使用示例
├── setup_database.py      # 数据库连接脚本
└── .gitignore             # Git 忽略文件
```

## 🌐 访问方式

部署完成后，通过以下方式访问：
- **主页面**: `https://your-domain.com/setup_guide.html`
- **直接访问**: `https://your-domain.com` (如果设置为默认首页)

## 📝 注意事项

1. **文件路径**: 确保 `setup_guide.html` 位于根目录
2. **资源引用**: 所有CSS和JS已内联，无需额外文件
3. **域名配置**: 确保域名已正确解析到 EdgeOne
4. **HTTPS**: 建议启用 HTTPS 以提高安全性
5. **缓存策略**: 合理配置缓存以提高访问速度

## 🚀 快速部署

如果使用 GitHub Pages 作为源站：
1. 确保项目已推送到 GitHub
2. 在 EdgeOne 中配置源站为 GitHub Pages URL
3. 启用 CDN 加速

## 🔍 验证部署

部署完成后，验证：
- 网站是否正常访问
- 图片和样式是否显示正确
- 响应速度是否流畅
- 安全性配置是否生效