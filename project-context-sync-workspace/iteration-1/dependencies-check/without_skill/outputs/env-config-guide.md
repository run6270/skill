# 环境变量快速配置指南

## .env 文件模板

```bash
# ============================================
# AI服务配置（必需）
# ============================================

# DeepSeek API Key - 用于AI文案生成
# 获取地址: https://platform.deepseek.com/api_keys
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here

# Replicate API Token - 用于AI封面图生成
# 获取地址: https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN=r8_your-replicate-token-here


# ============================================
# 数据库配置（必需）
# ============================================

# 开发环境使用SQLite（无需额外配置）
DATABASE_URL=sqlite:///./xiaohongshu_factory.db

# 生产环境使用PostgreSQL（推荐）
# DATABASE_URL=postgresql://username:password@localhost:5432/xiaohongshu_factory


# ============================================
# 系统配置（必需）
# ============================================

# 应用密钥 - 用于数据加密（请生成随机32字符字符串）
# 生成方式: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-secret-key-32-characters-long

# 媒体文件存储路径
MEDIA_ROOT=./media

# 允许的跨域来源（前端地址）
CORS_ORIGINS=http://localhost:3000,http://localhost:8000


# ============================================
# 小红书配置（可选，用于热点抓取）
# ============================================

# 小红书登录Cookie
# 获取方式:
# 1. 浏览器登录小红书
# 2. 打开开发者工具 -> Network
# 3. 刷新页面，找到任意请求
# 4. 复制Cookie请求头的值
XIAOHONGSHU_COOKIE=web_session=your-cookie-here


# ============================================
# 日志配置（可选）
# ============================================

# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO


# ============================================
# 业务配置（可选）
# ============================================

# 热点抓取间隔（小时）
CRAWLER_INTERVAL_HOURS=2

# 视频默认时长（秒）
VIDEO_DURATION_SECONDS=45

# AI调用失败重试次数
MAX_RETRY_ATTEMPTS=3

# 数据库备份配置
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
```

## 配置优先级说明

### P0 - 必须配置（应用无法启动）

1. `DEEPSEEK_API_KEY` - AI文案生成核心功能
2. `REPLICATE_API_TOKEN` - AI图片生成核心功能
3. `DATABASE_URL` - 数据存储
4. `SECRET_KEY` - 数据加密
5. `MEDIA_ROOT` - 媒体文件存储

### P1 - 强烈推荐（影响核心功能）

1. `XIAOHONGSHU_COOKIE` - 热点抓取功能需要
2. `CORS_ORIGINS` - 前后端通信需要

### P2 - 可选配置（使用默认值）

1. `LOG_LEVEL` - 默认INFO
2. `CRAWLER_INTERVAL_HOURS` - 默认2小时
3. `VIDEO_DURATION_SECONDS` - 默认45秒
4. `MAX_RETRY_ATTEMPTS` - 默认3次
5. `BACKUP_ENABLED` - 默认true
6. `BACKUP_RETENTION_DAYS` - 默认30天

## 快速配置步骤

### 1. 创建 .env 文件

```bash
cd /path/to/project
cp .env.example .env  # 如果有模板文件
# 或
touch .env
```

### 2. 生成 SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

将输出的字符串填入 `SECRET_KEY`

### 3. 获取 DeepSeek API Key

1. 访问: https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的API Key
5. 复制并填入 `DEEPSEEK_API_KEY`

### 4. 获取 Replicate API Token

1. 访问: https://replicate.com/
2. 注册/登录账号
3. 进入 Account -> API Tokens
4. 复制API Token
5. 填入 `REPLICATE_API_TOKEN`

### 5. 获取小红书Cookie（可选）

1. 浏览器打开 https://www.xiaohongshu.com/
2. 登录账号
3. 按F12打开开发者工具
4. 切换到 Network 标签
5. 刷新页面
6. 点击任意请求
7. 找到 Request Headers 中的 Cookie
8. 复制完整Cookie值
9. 填入 `XIAOHONGSHU_COOKIE`

### 6. 验证配置

```bash
# 启动后端
cd backend
source venv/bin/activate
python -m app.main

# 访问API文档测试
open http://localhost:8000/docs

# 测试API Key连接
# 在系统设置页面点击"测试连接"按钮
```

## 配置文件位置

| 环境 | 配置文件路径 | 说明 |
|------|-------------|------|
| 开发环境 | `.env` | 本地开发使用 |
| 生产环境 | `/etc/xiaohongshu-factory/.env` | 服务器部署使用 |
| Docker | `docker-compose.yml` 中的 `environment` | 容器化部署 |

## 安全注意事项

1. **不要提交 .env 文件到Git**
   ```bash
   # 确保 .gitignore 包含
   .env
   .env.local
   .env.*.local
   ```

2. **定期轮换API Key**
   - 建议每3个月更换一次
   - 发现泄露立即更换

3. **限制文件权限**
   ```bash
   chmod 600 .env  # 仅所有者可读写
   ```

4. **使用环境变量管理工具**
   - 开发: `python-dotenv`
   - 生产: AWS Secrets Manager / HashiCorp Vault

## 故障排查

### 问题1: API Key无效

**错误信息**: `Authentication failed` 或 `Invalid API key`

**解决方案**:
1. 检查API Key是否正确复制（无多余空格）
2. 确认API Key未过期
3. 检查账户余额是否充足
4. 使用系统设置页面的"测试连接"功能

### 问题2: 数据库连接失败

**错误信息**: `Could not connect to database`

**解决方案**:
1. 检查 `DATABASE_URL` 格式是否正确
2. 确认数据库服务已启动
3. 验证数据库用户名和密码
4. 检查数据库是否已创建

### 问题3: Cookie失效

**错误信息**: `Unauthorized` 或 `Cookie expired`

**解决方案**:
1. 重新登录小红书获取新Cookie
2. 检查Cookie是否完整复制
3. 确认Cookie未包含换行符

### 问题4: 跨域错误

**错误信息**: `CORS policy blocked`

**解决方案**:
1. 检查 `CORS_ORIGINS` 是否包含前端地址
2. 确认前端地址格式正确（包含协议和端口）
3. 重启后端服务使配置生效

## 环境变量加载顺序

1. 系统环境变量（最高优先级）
2. `.env.local` 文件（本地覆盖）
3. `.env` 文件（默认配置）
4. 代码中的默认值（最低优先级）

## 示例配置（开发环境）

```bash
# 最小化配置 - 仅包含必需项
DEEPSEEK_API_KEY=sk-abc123def456
REPLICATE_API_TOKEN=r8_xyz789
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=random-32-char-string-here
MEDIA_ROOT=./media
CORS_ORIGINS=http://localhost:3000
```

## 示例配置（生产环境）

```bash
# 完整配置 - 包含所有优化项
DEEPSEEK_API_KEY=sk-prod-key-here
REPLICATE_API_TOKEN=r8_prod-token-here
DATABASE_URL=postgresql://user:pass@db.example.com:5432/xiaohongshu_prod
SECRET_KEY=production-secret-key-32-chars
MEDIA_ROOT=/var/www/xiaohongshu-factory/media
CORS_ORIGINS=https://app.example.com
LOG_LEVEL=WARNING
CRAWLER_INTERVAL_HOURS=1
VIDEO_DURATION_SECONDS=60
MAX_RETRY_ATTEMPTS=5
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=90
XIAOHONGSHU_COOKIE=prod-cookie-here
```
