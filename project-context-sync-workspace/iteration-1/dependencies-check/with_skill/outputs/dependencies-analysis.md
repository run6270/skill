# 项目依赖分析报告

> 项目路径: /Users/mac/Documents/GitHub/githubrepo
> 分析时间: 2026-03-04
> 项目名称: 小红书热点内容工厂 (XiaoHongShu Content Factory)

## 项目概述

这是一个 AI 驱动的小红书内容生产工具,提供从热点抓取、内容生成、视频制作到发布管理的一站式解决方案。

## 项目状态

**当前状态**: 规划阶段 (PRD 文档已完成)
- 项目目录仅包含 PRD.md 文档和少量测试数据
- 尚未开始实际开发
- 无代码文件、依赖配置文件

## 技术栈 (根据 PRD 规划)

### 前端技术栈

| 技术 | 版本/说明 | 用途 |
|------|----------|------|
| **Next.js** | 15 | 前端框架,支持 SSR/SSG、App Router |
| **React** | - | UI 库 (Next.js 依赖) |
| **shadcn/ui** | - | UI 组件库 |
| **Tailwind CSS** | - | CSS 框架 |
| **TypeScript** | - | 类型系统 |

### 后端技术栈

| 技术 | 版本/说明 | 用途 |
|------|----------|------|
| **Python** | 3.x | 后端语言 |
| **FastAPI** | - | 后端框架,异步支持 |
| **SQLAlchemy** | - | ORM 框架 |
| **Pydantic** | - | 数据校验 |
| **APScheduler** | - | 定时任务调度 |

### AI 服务

| 服务 | 用途 |
|------|------|
| **DeepSeek V3** | AI 文案生成 |
| **Flux (Replicate)** | AI 封面图生成 |
| **Edge TTS** | 语音合成 (免费) |

### 视频处理

| 技术 | 用途 |
|------|------|
| **FFmpeg** | 视频处理核心 |
| **moviepy** | Python 视频处理库 |

### 数据库

| 技术 | 阶段 |
|------|------|
| **SQLite** | 本地开发 |
| **PostgreSQL** | 生产环境 (上云后) |

### 浏览器自动化

| 技术 | 用途 |
|------|------|
| **Playwright** | 浏览器自动化发布 (Phase 4) |

## 前端依赖 (预计)

### 生产依赖
```json
{
  "next": "^15.0.0",
  "react": "^18.0.0",
  "react-dom": "^18.0.0",
  "tailwindcss": "^3.0.0",
  "@radix-ui/react-*": "多个 shadcn/ui 依赖组件",
  "lucide-react": "图标库",
  "class-variance-authority": "样式工具",
  "clsx": "类名工具",
  "tailwind-merge": "Tailwind 工具"
}
```

### 开发依赖
```json
{
  "typescript": "^5.0.0",
  "@types/node": "^20.0.0",
  "@types/react": "^18.0.0",
  "@types/react-dom": "^18.0.0",
  "eslint": "^8.0.0",
  "eslint-config-next": "^15.0.0",
  "prettier": "^3.0.0"
}
```

## 后端依赖 (预计)

### Python 包 (requirements.txt)
```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
apscheduler>=3.10.0
moviepy>=1.0.3
playwright>=1.40.0
httpx>=0.24.0
python-multipart>=0.0.6
pillow>=10.0.0
edge-tts>=6.0.0
replicate>=0.15.0
deepseek-api  # 需确认实际包名
```

### 系统依赖
```bash
# FFmpeg (视频处理)
brew install ffmpeg  # macOS
apt-get install ffmpeg  # Ubuntu

# Playwright 浏览器
playwright install chromium
```

## 环境变量配置

### 必需环境变量

```bash
# AI 服务 API Keys
DEEPSEEK_API_KEY=sk-xxxxx          # DeepSeek V3 文案生成
REPLICATE_API_TOKEN=r8_xxxxx       # Flux 图片生成

# 数据库配置 (生产环境)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# 应用配置
APP_ENV=development                 # development / production
SECRET_KEY=your-secret-key-here    # FastAPI 密钥
CORS_ORIGINS=http://localhost:3000 # 前端地址

# 文件存储 (上云后)
OSS_ENDPOINT=https://oss.example.com
OSS_ACCESS_KEY=xxxxx
OSS_SECRET_KEY=xxxxx
OSS_BUCKET=xiaohongshu-content
```

### 可选环境变量

```bash
# 小红书账号 (Phase 4 自动发布)
XHS_USERNAME=your_username
XHS_PASSWORD=your_password

# 日志配置
LOG_LEVEL=INFO                     # DEBUG / INFO / WARNING / ERROR
LOG_FILE_PATH=./logs/app.log

# 视频生成配置
VIDEO_OUTPUT_DIR=./media/videos
IMAGE_OUTPUT_DIR=./media/images
AUDIO_OUTPUT_DIR=./media/audio

# 定时任务配置
SCHEDULER_TIMEZONE=Asia/Shanghai
CRAWLER_INTERVAL_MINUTES=30        # 热点抓取间隔

# 性能配置
MAX_WORKERS=4                      # 并发任务数
VIDEO_GENERATION_TIMEOUT=300       # 视频生成超时(秒)
```

## 项目结构 (规划)

```
xiaohongshu-content-factory/
├── frontend/                      # Next.js 前端
│   ├── app/                       # App Router
│   ├── components/                # React 组件
│   ├── lib/                       # 工具函数
│   ├── types/                     # TypeScript 类型
│   ├── package.json
│   └── tsconfig.json
├── backend/                       # FastAPI 后端
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/               # API 路由
│   │   ├── services/              # 业务逻辑
│   │   ├── models/                # 数据模型
│   │   └── schemas/               # Pydantic 模型
│   ├── media/                     # 媒体文件
│   │   ├── images/
│   │   ├── audio/
│   │   ├── music/
│   │   └── videos/
│   ├── requirements.txt
│   └── tests/
├── .env.example                   # 环境变量模板
├── docker-compose.yml             # Docker 配置
└── README.md
```

## 开发环境搭建 (预计步骤)

### 前端
```bash
cd frontend
npm install
# 或
pnpm install
# 或
yarn install

npm run dev  # 启动开发服务器 (http://localhost:3000)
```

### 后端
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 安装 FFmpeg
brew install ffmpeg  # macOS

# 安装 Playwright 浏览器
playwright install chromium

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

### 环境变量配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件,填入实际的 API Keys
vim .env
```

## 关键依赖说明

### 1. FFmpeg
- **用途**: 视频合成、音频处理
- **安装**: 系统级依赖,需单独安装
- **验证**: `ffmpeg -version`

### 2. DeepSeek V3 API
- **用途**: AI 文案生成
- **费用**: 按 token 计费
- **文档**: https://platform.deepseek.com/docs

### 3. Replicate (Flux)
- **用途**: AI 封面图生成
- **费用**: 按次计费
- **文档**: https://replicate.com/docs

### 4. Edge TTS
- **用途**: 语音合成
- **费用**: 免费
- **特点**: 微软 Edge 浏览器的 TTS 服务

### 5. Playwright
- **用途**: 浏览器自动化 (Phase 4)
- **特点**: 需下载浏览器二进制文件 (~200MB)

## 预计依赖数量

| 类型 | 数量 |
|------|------|
| 前端生产依赖 | ~15-20 个 |
| 前端开发依赖 | ~10-15 个 |
| 后端依赖 | ~15-20 个 |
| 系统依赖 | 2 个 (FFmpeg, Playwright) |

## 风险与注意事项

### 1. API 依赖风险
- DeepSeek/Replicate API 可能不稳定或变更
- 建议: 预留替换接口,支持多个 AI 服务商

### 2. FFmpeg 版本兼容性
- 不同系统的 FFmpeg 版本可能导致兼容性问题
- 建议: 在 README 中明确最低版本要求

### 3. Playwright 浏览器下载
- 首次安装需下载 ~200MB 浏览器文件
- 建议: 在 CI/CD 中缓存浏览器文件

### 4. 视频生成性能
- moviepy + FFmpeg 可能消耗大量 CPU/内存
- 建议: 限制并发任务数,监控系统资源

### 5. 数据库迁移
- SQLite → PostgreSQL 迁移需要数据导出/导入
- 建议: 使用 Alembic 管理数据库版本

## 下一步行动

1. **创建项目骨架**
   - 初始化 Next.js 前端项目
   - 初始化 FastAPI 后端项目
   - 配置 monorepo 结构 (可选)

2. **配置依赖管理**
   - 创建 `package.json` (前端)
   - 创建 `requirements.txt` (后端)
   - 创建 `.env.example` 模板

3. **搭建开发环境**
   - 安装系统依赖 (FFmpeg)
   - 配置 API Keys
   - 验证各服务连通性

4. **Phase 1 技术验证**
   - 验证 DeepSeek API 文案生成
   - 验证 Flux 图片生成
   - 验证 Edge TTS 语音合成
   - 验证 FFmpeg 视频合成

## 总结

该项目目前处于规划阶段,尚未开始实际开发。根据 PRD 文档,项目将采用 Next.js + FastAPI 的前后端分离架构,依赖多个 AI 服务和视频处理工具。

**关键依赖**:
- 前端: Next.js 15 + shadcn/ui + Tailwind CSS
- 后端: Python FastAPI + SQLAlchemy + APScheduler
- AI: DeepSeek V3 + Flux + Edge TTS
- 视频: FFmpeg + moviepy
- 自动化: Playwright

**环境变量**: 主要需要配置 DeepSeek 和 Replicate 的 API Keys,以及数据库连接信息。

建议在开始开发前,先进行 Phase 1 技术验证,确保所有关键依赖可用且性能满足需求。
