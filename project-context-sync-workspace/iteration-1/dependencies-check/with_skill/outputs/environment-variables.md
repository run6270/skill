# 环境变量配置文档

> 项目: 小红书热点内容工厂
> 文档版本: v1.0
> 更新时间: 2026-03-04

## 环境变量清单

### 1. AI 服务配置 (必需)

#### DeepSeek API
```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```
- **用途**: AI 文案生成服务
- **获取方式**: https://platform.deepseek.com/
- **费用**: 按 token 计费
- **验证**: 调用 API 测试连通性

#### Replicate API
```bash
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx
```
- **用途**: Flux 模型封面图生成
- **获取方式**: https://replicate.com/account/api-tokens
- **费用**: 按次计费
- **验证**: 调用 Flux 模型测试

### 2. 数据库配置

#### 开发环境 (SQLite)
```bash
DATABASE_URL=sqlite:///./app.db
```
- **说明**: 本地开发使用 SQLite,无需额外配置
- **文件位置**: 项目根目录 `app.db`

#### 生产环境 (PostgreSQL)
```bash
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
```
- **格式**: `postgresql://[user]:[password]@[host]:[port]/[database]`
- **示例**: `postgresql://admin:secret123@localhost:5432/xiaohongshu_prod`
- **注意**: 密码中的特殊字符需要 URL 编码

### 3. 应用基础配置 (必需)

```bash
# 运行环境
APP_ENV=development
# 可选值: development, staging, production

# 应用密钥 (用于 JWT 签名等)
SECRET_KEY=your-random-secret-key-min-32-chars
# 生成方式: openssl rand -hex 32

# CORS 跨域配置
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
# 多个域名用逗号分隔

# API 服务端口
API_PORT=8000
# 默认 8000,可根据需要修改

# 前端服务端口
FRONTEND_PORT=3000
# 默认 3000,可根据需要修改
```

### 4. 文件存储配置

#### 本地存储 (开发环境)
```bash
STORAGE_TYPE=local

# 媒体文件根目录
MEDIA_ROOT=./media

# 子目录配置
VIDEO_OUTPUT_DIR=./media/videos
IMAGE_OUTPUT_DIR=./media/images
AUDIO_OUTPUT_DIR=./media/audio
MUSIC_LIBRARY_DIR=./media/music
```

#### 对象存储 (生产环境)
```bash
STORAGE_TYPE=oss

# OSS 配置 (阿里云/腾讯云/AWS S3)
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY=LTAI5txxxxxxxxxxxxx
OSS_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
OSS_BUCKET=xiaohongshu-content-prod
OSS_REGION=cn-hangzhou

# CDN 加速域名 (可选)
CDN_DOMAIN=https://cdn.example.com
```

### 5. 小红书账号配置 (Phase 4 自动发布)

```bash
# 小红书账号凭证
XHS_USERNAME=your_phone_or_email
XHS_PASSWORD=your_password

# 或使用 Cookie (推荐)
XHS_COOKIE=web_session=xxxxx; xsec_token=xxxxx

# 发布配置
XHS_AUTO_PUBLISH=false
# 设为 true 启用全自动发布 (Phase 4)
```

**安全提示**:
- 生产环境建议使用 Cookie 方式,避免明文密码
- Cookie 有效期约 30 天,需定期更新
- 不要将凭证提交到 Git 仓库

### 6. 日志配置

```bash
# 日志级别
LOG_LEVEL=INFO
# 可选值: DEBUG, INFO, WARNING, ERROR, CRITICAL

# 日志文件路径
LOG_FILE_PATH=./logs/app.log

# 日志文件大小限制 (MB)
LOG_MAX_SIZE=100

# 日志文件保留数量
LOG_BACKUP_COUNT=10

# 是否输出到控制台
LOG_TO_CONSOLE=true
```

### 7. 定时任务配置

```bash
# 时区设置
SCHEDULER_TIMEZONE=Asia/Shanghai

# 热点抓取间隔 (分钟)
CRAWLER_INTERVAL_MINUTES=30

# 发布任务检查间隔 (分钟)
PUBLISH_CHECK_INTERVAL_MINUTES=5

# 数据清理任务 (每天凌晨 3 点)
DATA_CLEANUP_CRON=0 3 * * *
```

### 8. 性能与限制配置

```bash
# 并发任务数
MAX_WORKERS=4
# 建议: CPU 核心数 * 2

# 视频生成超时 (秒)
VIDEO_GENERATION_TIMEOUT=300

# 图片生成超时 (秒)
IMAGE_GENERATION_TIMEOUT=60

# API 请求超时 (秒)
API_REQUEST_TIMEOUT=30

# 最大上传文件大小 (MB)
MAX_UPLOAD_SIZE=100

# 视频文件大小限制 (MB)
MAX_VIDEO_SIZE=50
# 小红书限制 50MB
```

### 9. 缓存配置 (可选)

```bash
# Redis 配置 (用于任务队列和缓存)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password

# 缓存过期时间 (秒)
CACHE_TTL=3600
```

### 10. 监控与告警 (可选)

```bash
# Sentry 错误追踪
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# 钉钉/企业微信 Webhook (告警通知)
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxxxx
WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx
```

## 环境变量文件示例

### .env.example (开发环境模板)
```bash
# ==================== AI 服务 ====================
DEEPSEEK_API_KEY=sk-your-key-here
REPLICATE_API_TOKEN=r8_your-token-here

# ==================== 数据库 ====================
DATABASE_URL=sqlite:///./app.db

# ==================== 应用配置 ====================
APP_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000
API_PORT=8000
FRONTEND_PORT=3000

# ==================== 文件存储 ====================
STORAGE_TYPE=local
MEDIA_ROOT=./media
VIDEO_OUTPUT_DIR=./media/videos
IMAGE_OUTPUT_DIR=./media/images
AUDIO_OUTPUT_DIR=./media/audio
MUSIC_LIBRARY_DIR=./media/music

# ==================== 小红书账号 (Phase 4) ====================
XHS_USERNAME=
XHS_PASSWORD=
XHS_AUTO_PUBLISH=false

# ==================== 日志配置 ====================
LOG_LEVEL=DEBUG
LOG_FILE_PATH=./logs/app.log
LOG_TO_CONSOLE=true

# ==================== 定时任务 ====================
SCHEDULER_TIMEZONE=Asia/Shanghai
CRAWLER_INTERVAL_MINUTES=30
PUBLISH_CHECK_INTERVAL_MINUTES=5

# ==================== 性能配置 ====================
MAX_WORKERS=4
VIDEO_GENERATION_TIMEOUT=300
IMAGE_GENERATION_TIMEOUT=60
API_REQUEST_TIMEOUT=30
MAX_VIDEO_SIZE=50
```

### .env.production (生产环境示例)
```bash
# ==================== AI 服务 ====================
DEEPSEEK_API_KEY=sk-prod-xxxxxxxxxxxxx
REPLICATE_API_TOKEN=r8_prod-xxxxxxxxxxxxx

# ==================== 数据库 ====================
DATABASE_URL=postgresql://admin:SecurePass123@db.example.com:5432/xiaohongshu_prod

# ==================== 应用配置 ====================
APP_ENV=production
SECRET_KEY=prod-random-32-char-secret-key-here
CORS_ORIGINS=https://app.example.com
API_PORT=8000
FRONTEND_PORT=3000

# ==================== 文件存储 ====================
STORAGE_TYPE=oss
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY=LTAI5txxxxxxxxxxxxx
OSS_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
OSS_BUCKET=xiaohongshu-content-prod
OSS_REGION=cn-hangzhou
CDN_DOMAIN=https://cdn.example.com

# ==================== 小红书账号 ====================
XHS_COOKIE=web_session=xxxxx; xsec_token=xxxxx
XHS_AUTO_PUBLISH=true

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE_PATH=/var/log/xiaohongshu/app.log
LOG_TO_CONSOLE=false

# ==================== 定时任务 ====================
SCHEDULER_TIMEZONE=Asia/Shanghai
CRAWLER_INTERVAL_MINUTES=15
PUBLISH_CHECK_INTERVAL_MINUTES=2

# ==================== 性能配置 ====================
MAX_WORKERS=8
VIDEO_GENERATION_TIMEOUT=300
IMAGE_GENERATION_TIMEOUT=60
API_REQUEST_TIMEOUT=30

# ==================== 缓存 ====================
REDIS_URL=redis://redis.example.com:6379/0
REDIS_PASSWORD=redis_secure_password
CACHE_TTL=3600

# ==================== 监控 ====================
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxxxx
```

## 配置步骤

### 1. 复制环境变量模板
```bash
cp .env.example .env
```

### 2. 编辑 .env 文件
```bash
# 使用你喜欢的编辑器
vim .env
# 或
nano .env
# 或
code .env
```

### 3. 填写必需的 API Keys
- 访问 DeepSeek 官网获取 API Key
- 访问 Replicate 官网获取 API Token
- 生成随机 SECRET_KEY: `openssl rand -hex 32`

### 4. 验证配置
```bash
# 后端验证
cd backend
python -c "from app.config import settings; print(settings.dict())"

# 前端验证
cd frontend
npm run build
```

## 安全最佳实践

### 1. 不要提交 .env 文件到 Git
```bash
# .gitignore 中添加
.env
.env.local
.env.production
.env.*.local
```

### 2. 使用环境变量管理工具
- **开发环境**: direnv, dotenv
- **生产环境**: Docker secrets, Kubernetes secrets, AWS Secrets Manager

### 3. 定期轮换密钥
- API Keys: 每 3-6 个月轮换
- 数据库密码: 每 6-12 个月轮换
- SECRET_KEY: 每年轮换

### 4. 最小权限原则
- 数据库账号只授予必要的权限
- OSS 账号使用子账号,限制 Bucket 访问范围
- API Keys 设置 IP 白名单 (如果支持)

### 5. 监控异常访问
- 启用 API 访问日志
- 监控异常流量和错误率
- 设置告警阈值

## 常见问题

### Q1: 如何生成安全的 SECRET_KEY?
```bash
# 方法 1: OpenSSL
openssl rand -hex 32

# 方法 2: Python
python -c "import secrets; print(secrets.token_hex(32))"

# 方法 3: Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Q2: DATABASE_URL 中密码包含特殊字符怎么办?
```python
from urllib.parse import quote_plus
password = "p@ssw0rd!"
encoded = quote_plus(password)
# 结果: p%40ssw0rd%21
```

### Q3: 如何在 Docker 中使用环境变量?
```yaml
# docker-compose.yml
services:
  backend:
    env_file:
      - .env
    environment:
      - DATABASE_URL=${DATABASE_URL}
```

### Q4: 前端如何访问环境变量?
```javascript
// Next.js 中,以 NEXT_PUBLIC_ 开头的变量会暴露给浏览器
// .env
NEXT_PUBLIC_API_URL=http://localhost:8000

// 代码中访问
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

### Q5: 如何在不同环境使用不同配置?
```bash
# 创建多个环境文件
.env.development
.env.staging
.env.production

# 启动时指定
APP_ENV=production python main.py
```

## 配置检查清单

部署前检查:
- [ ] 所有必需的环境变量已配置
- [ ] API Keys 有效且有足够额度
- [ ] 数据库连接正常
- [ ] 文件存储路径存在且有写权限
- [ ] 日志目录存在且有写权限
- [ ] SECRET_KEY 已更换为生产密钥
- [ ] CORS_ORIGINS 配置正确
- [ ] 定时任务时区设置正确
- [ ] 性能参数根据服务器配置调整
- [ ] .env 文件已添加到 .gitignore

## 总结

本文档列出了小红书热点内容工厂项目所需的所有环境变量配置。

**关键配置**:
- **必需**: DEEPSEEK_API_KEY, REPLICATE_API_TOKEN, SECRET_KEY
- **开发环境**: 使用 SQLite + 本地存储
- **生产环境**: 使用 PostgreSQL + OSS + Redis

**安全提示**:
- 不要将 .env 文件提交到 Git
- 定期轮换密钥
- 使用最小权限原则
- 启用监控和告警

建议在项目初始化时,先创建 `.env.example` 模板,团队成员复制后填入自己的配置。
