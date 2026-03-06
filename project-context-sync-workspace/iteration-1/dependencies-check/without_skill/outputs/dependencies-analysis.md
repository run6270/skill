# 小红书热点内容工厂 - 依赖与环境配置分析

## 项目概述

**项目名称**: 小红书热点内容工厂（XiaoHongShu Content Factory）
**项目类型**: AI驱动的内容生产工具
**架构**: 前后端分离（Next.js + FastAPI）

---

## 技术栈依赖

### 前端依赖

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 15 | 前端框架，支持SSR/SSG、App Router |
| React | 18+ | UI库 |
| shadcn/ui | latest | UI组件库 |
| Tailwind CSS | 3.x | CSS框架 |
| TypeScript | 5.x | 类型系统 |

**预计的 package.json 依赖**:
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@radix-ui/react-*": "latest",
    "tailwindcss": "^3.0.0",
    "class-variance-authority": "latest",
    "clsx": "latest",
    "tailwind-merge": "latest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "latest",
    "@types/react": "latest",
    "eslint": "latest",
    "prettier": "latest"
  }
}
```

### 后端依赖

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 后端语言 |
| FastAPI | latest | Web框架 |
| SQLAlchemy | 2.x | ORM |
| Pydantic | 2.x | 数据校验 |
| APScheduler | 3.x | 定时任务调度 |
| Playwright | latest | 浏览器自动化 |
| FFmpeg | 6.x | 视频处理 |
| moviepy | 1.x | Python视频处理封装 |

**预计的 requirements.txt 依赖**:
```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
apscheduler>=3.10.0
playwright>=1.40.0
moviepy>=1.0.3
pillow>=10.0.0
requests>=2.31.0
httpx>=0.24.0
python-multipart>=0.0.6
aiofiles>=23.0.0
cryptography>=41.0.0
python-dotenv>=1.0.0
```

### 系统级依赖

| 工具 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| FFmpeg | 6.x | 视频/音频处理 | `brew install ffmpeg` (macOS) |
| Node.js | 18+ | 前端运行环境 | `brew install node` |
| Python | 3.10+ | 后端运行环境 | `brew install python@3.10` |
| Playwright Browsers | latest | 浏览器自动化 | `playwright install` |

---

## 环境变量配置

### 必需的环境变量

#### AI服务相关

| 变量名 | 说明 | 示例值 | 优先级 |
|--------|------|--------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（文案生成） | `sk-xxxxx` | P0 |
| `REPLICATE_API_TOKEN` | Replicate API令牌（封面图生成） | `r8_xxxxx` | P0 |

#### 数据库配置

| 变量名 | 说明 | 示例值 | 优先级 |
|--------|------|--------|--------|
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///./data.db` 或 `postgresql://user:pass@host/db` | P0 |

#### 小红书相关

| 变量名 | 说明 | 示例值 | 优先级 |
|--------|------|--------|--------|
| `XIAOHONGSHU_COOKIE` | 小红书登录Cookie（加密存储） | `web_session=xxxxx` | P1 |

#### 系统配置

| 变量名 | 说明 | 示例值 | 优先级 |
|--------|------|--------|--------|
| `SECRET_KEY` | 应用密钥（用于加密） | 随机生成的32字符字符串 | P0 |
| `MEDIA_ROOT` | 媒体文件存储路径 | `./media` | P0 |
| `LOG_LEVEL` | 日志级别 | `INFO` | P2 |
| `CORS_ORIGINS` | 允许的跨域来源 | `http://localhost:3000` | P1 |

### 可选的环境变量

| 变量名 | 说明 | 默认值 | 优先级 |
|--------|------|--------|--------|
| `CRAWLER_INTERVAL_HOURS` | 热点抓取间隔（小时） | `2` | P2 |
| `VIDEO_DURATION_SECONDS` | 视频时长（秒） | `45` | P2 |
| `MAX_RETRY_ATTEMPTS` | AI调用失败重试次数 | `3` | P2 |
| `BACKUP_ENABLED` | 是否启用数据库备份 | `true` | P2 |
| `BACKUP_RETENTION_DAYS` | 备份保留天数 | `30` | P2 |

### 环境变量文件示例

创建 `.env` 文件：

```bash
# AI服务配置
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
REPLICATE_API_TOKEN=r8_your-replicate-token-here

# 数据库配置
DATABASE_URL=sqlite:///./xiaohongshu_factory.db

# 小红书配置
XIAOHONGSHU_COOKIE=web_session=your-cookie-here

# 系统配置
SECRET_KEY=your-secret-key-32-characters-long
MEDIA_ROOT=./media
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# 可选配置
CRAWLER_INTERVAL_HOURS=2
VIDEO_DURATION_SECONDS=45
MAX_RETRY_ATTEMPTS=3
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
```

---

## 安全配置要求

### API Key 存储安全

1. **加密存储**: 所有API Key使用AES-256加密后存储在数据库
2. **界面显示**: 仅显示后4位字符（如：`****xxxx`）
3. **日志脱敏**: 日志中不记录完整的API Key
4. **连接测试**: 支持验证Key有效性和余额检查

### Cookie 安全

1. **加密存储**: 小红书Cookie加密存储
2. **定期检查**: 自动检查Cookie有效性
3. **过期告警**: Cookie失效时发送告警通知

### 数据传输安全

| 安全措施 | 说明 |
|----------|------|
| HTTPS | 上云后强制使用HTTPS |
| 输入校验 | XSS过滤和长度限制 |
| 用户认证 | 本地部署使用密码保护，上云后接入OAuth 2.0 |

---

## 开发环境搭建步骤

### 1. 安装系统依赖

```bash
# macOS
brew install python@3.10 node ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip nodejs npm ffmpeg

# 验证安装
python3 --version  # 应显示 3.10+
node --version     # 应显示 18+
ffmpeg -version    # 应显示 6.x
```

### 2. 克隆项目并安装依赖

```bash
# 后端
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install  # 安装浏览器

# 前端
cd frontend
npm install
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际的API Key
nano .env
```

### 4. 初始化数据库

```bash
cd backend
python -m app.database init  # 创建数据库表
```

### 5. 启动服务

```bash
# 启动后端（开发模式）
cd backend
uvicorn app.main:app --reload --port 8000

# 启动前端（开发模式）
cd frontend
npm run dev
```

### 6. 访问应用

- 前端: http://localhost:3000
- 后端API文档: http://localhost:8000/docs

---

## 生产环境部署要求

### 数据库迁移

从SQLite迁移到PostgreSQL：

```bash
# 安装PostgreSQL
brew install postgresql  # macOS
sudo apt install postgresql  # Ubuntu

# 修改环境变量
DATABASE_URL=postgresql://user:password@localhost:5432/xiaohongshu_factory

# 运行迁移脚本
python -m app.database migrate
```

### 性能优化配置

| 配置项 | 开发环境 | 生产环境 |
|--------|----------|----------|
| 数据库 | SQLite | PostgreSQL |
| 文件存储 | 本地文件系统 | OSS/S3 |
| 日志级别 | DEBUG | INFO/WARNING |
| 工作进程数 | 1 | CPU核心数 |
| 缓存 | 无 | Redis |

---

## 依赖版本兼容性

### Python版本要求

- **最低版本**: Python 3.10
- **推荐版本**: Python 3.11
- **原因**: 使用了类型提示新特性和性能优化

### Node.js版本要求

- **最低版本**: Node.js 18
- **推荐版本**: Node.js 20 LTS
- **原因**: Next.js 15需要Node.js 18+

### FFmpeg版本要求

- **最低版本**: FFmpeg 5.0
- **推荐版本**: FFmpeg 6.x
- **原因**: 需要最新的编码器和滤镜支持

---

## 常见问题排查

### 1. API Key无效

**症状**: 文案生成或图片生成失败
**解决方案**:
- 检查 `.env` 文件中的API Key是否正确
- 使用系统设置页面的"测试连接"功能验证
- 检查API余额是否充足

### 2. 视频生成失败

**症状**: 视频合成任务失败
**解决方案**:
- 确认FFmpeg已正确安装: `ffmpeg -version`
- 检查媒体文件路径权限
- 查看后端日志: `tail -f logs/app.log`

### 3. 浏览器自动化失败

**症状**: 热点抓取失败
**解决方案**:
- 重新安装Playwright浏览器: `playwright install`
- 检查小红书Cookie是否过期
- 确认网络连接正常

### 4. 数据库连接失败

**症状**: 应用启动失败
**解决方案**:
- 检查 `DATABASE_URL` 配置
- 确认数据库服务已启动
- 验证数据库用户权限

---

## 监控与维护

### 日志文件位置

| 日志类型 | 路径 | 保留期限 |
|----------|------|----------|
| 应用日志 | `logs/app.log` | 30天 |
| 错误日志 | `logs/error.log` | 90天 |
| 任务日志 | `logs/scheduler.log` | 30天 |
| 访问日志 | `logs/access.log` | 7天 |

### 定期维护任务

1. **每日**: 数据库自动备份
2. **每周**: 清理过期媒体文件
3. **每月**: 检查API Key余额和有效性
4. **每季度**: 更新依赖包版本

---

## 成本估算

### API调用成本（按月）

| 服务 | 用量 | 单价 | 月成本 |
|------|------|------|--------|
| DeepSeek API | 600条文案 × 2000 tokens | ¥0.001/1K tokens | ¥1.2 |
| Replicate (Flux) | 600张图片 | $0.003/张 | $1.8 (¥13) |
| Edge TTS | 免费 | - | ¥0 |
| **总计** | - | - | **约¥15/月** |

### 基础设施成本

| 项目 | 本地部署 | 云部署（阿里云） |
|------|----------|------------------|
| 服务器 | ¥0（自有设备） | ¥100-300/月 |
| 存储 | ¥0（本地硬盘） | ¥50-100/月 |
| 带宽 | ¥0（家庭网络） | ¥50-150/月 |
| **总计** | **¥0** | **¥200-550/月** |

---

## 总结

本项目是一个完整的AI内容生产系统，主要依赖：

1. **前端**: Next.js 15 + shadcn/ui + Tailwind CSS
2. **后端**: Python FastAPI + SQLAlchemy + APScheduler
3. **AI服务**: DeepSeek（文案）+ Replicate Flux（图片）+ Edge TTS（语音）
4. **视频处理**: FFmpeg + moviepy
5. **浏览器自动化**: Playwright

**关键环境变量**:
- `DEEPSEEK_API_KEY`: 必需，用于AI文案生成
- `REPLICATE_API_TOKEN`: 必需，用于AI图片生成
- `DATABASE_URL`: 必需，数据库连接
- `SECRET_KEY`: 必需，数据加密
- `XIAOHONGSHU_COOKIE`: 可选，用于热点抓取

**开发成本**: 约¥15/月（仅API调用）
**部署方式**: 支持本地部署（零成本）或云部署（¥200-550/月）
