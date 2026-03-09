# EdgeOne Pages 部署指南

## 🎯 项目信息
- **EdgeOne 项目**: https://console.cloud.tencent.com/edgeone/pages/project/pages-ddw9ahjai7r6/index
- **项目 ID**: pages-ddw9ahjai7r6
- **部署类型**: 静态网站

## 📋 部署步骤

### 方法1: 通过 EdgeOne 控制台部署（推荐）

#### 步骤1: 访问 EdgeOne Pages 项目
1. 打开浏览器，访问: https://console.cloud.tencent.com/edgeone/pages/project/pages-ddw9ahjai7r6/index
2. 登录你的腾讯云账号

#### 步骤2: 上传文件
1. 在项目页面中，找到"文件管理"或"上传文件"选项
2. 点击上传按钮
3. 选择以下文件进行上传：
   - `index.html` (主页面)
   - `setup_guide.html` (设置指南页面)

#### 步骤3: 配置部署设置
1. 设置默认首页为 `index.html`
2. 配置域名（如果需要）
3. 启用 HTTPS
4. 保存配置

#### 步骤4: 部署
1. 点击"部署"或"发布"按钮
2. 等待部署完成
3. 获取访问链接

### 方法2: 通过 Git 仓库部署

#### 步骤1: 连接 GitHub 仓库
1. 在 EdgeOne Pages 项目中，选择"连接 Git 仓库"
2. 授权 EdgeOne 访问你的 GitHub
3. 选择仓库: `zhousirui0714/cuotiben`

#### 步骤2: 配置构建设置
1. 设置构建命令: 无需构建（静态网站）
2. 设置输出目录: 根目录
3. 设置默认首页: `index.html`

#### 步骤3: 部署
1. 点击"部署"按钮
2. EdgeOne 会自动从 GitHub 拉取代码并部署
3. 部署完成后获取访问链接

## 📁 需要部署的文件

| 文件名 | 用途 | 必需 |
|--------|------|------|
| index.html | 主页面 | ✅ 是 |
| setup_guide.html | 设置指南 | ⚪ 可选 |
| README.md | 项目说明 | ⚪ 可选 |

## 🔧 部署配置建议

### 基础配置
- **默认首页**: index.html
- **错误页面**: index.html
- **目录索引**: 启用

### 性能优化
- **压缩**: 启用 Gzip 压缩
- **缓存**: 静态文件缓存 1 小时
- **CDN**: 启用全球加速

### 安全配置
- **HTTPS**: 启用
- **WAF**: 启用 Web 应用防火墙
- **访问控制**: 按需配置

## ✅ 部署验证

部署完成后，验证以下内容：

1. **访问测试**
   - 访问你的域名或 EdgeOne 提供的链接
   - 检查页面是否正常显示
   - 测试所有链接和功能

2. **性能测试**
   - 检查页面加载速度
   - 测试移动端显示
   - 验证 CDN 加速效果

3. **安全测试**
   - 检查 HTTPS 是否正常
   - 验证 WAF 防护是否生效
   - 测试访问控制规则

## 🚀 快速部署命令

如果使用 EdgeOne CLI（需要 Node.js）:

```bash
# 安装 EdgeOne CLI
npm install -g edgeone

# 登录 EdgeOne
edgeone login

# 部署到项目
edgeone pages deploy -n pages-ddw9ahjai7r6
```

## 📊 部署状态检查

部署完成后，可以通过以下方式检查状态：

1. **EdgeOne 控制台**: 查看部署日志和状态
2. **访问测试**: 直接访问部署的 URL
3. **监控工具**: 使用 EdgeOne 提供的监控功能

## 🔍 常见问题

### Q1: 部署失败怎么办？
A: 检查文件格式、网络连接和权限设置，查看部署日志获取详细错误信息。

### Q2: 如何更新网站？
A: 修改文件后，重新上传或在 Git 仓库中提交，EdgeOne 会自动重新部署。

### Q3: 如何绑定自定义域名？
A: 在 EdgeOne 控制台的域名设置中添加你的域名，并配置 DNS 解析。

### Q4: 如何查看访问统计？
A: 在 EdgeOne 控制台的统计分析中查看访问量、流量等数据。

## 📞 技术支持

如遇到问题，可以：
- 查看 EdgeOne 官方文档
- 联系腾讯云技术支持
- 在社区论坛寻求帮助

---

**部署完成后，你的网站将通过 EdgeOne 的全球 CDN 加速，为用户提供快速、安全的访问体验！**