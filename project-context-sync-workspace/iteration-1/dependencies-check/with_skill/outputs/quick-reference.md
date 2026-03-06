# 依赖清单速查表

> 快速参考版本,完整文档见 dependencies-analysis.md

## 前端依赖

### package.json (预计)
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "tailwindcss": "^3.0.0",
    "@radix-ui/react-dialog": "latest",
    "@radix-ui/react-dropdown-menu": "latest",
    "@radix-ui/react-select": "latest",
    "@radix-ui/react-toast": "latest",
    "lucide-react": "latest",
    "class-variance-authority": "latest",
    "clsx": "latest",
    "tailwind-merge": "latest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^15.0.0",
    "prettier": "^3.0.0"
  }
}
```

## 后端依赖

### requirements.txt (预计)
```txt
# Web 框架
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
python-multipart>=0.0.6

# 数据库
sqlalchemy>=2.0.0
alembic>=1.12.0

# 数据验证
pydantic>=2.0.0
pydantic-settings>=2.0.0

# 定时任务
apscheduler>=3.10.0

# 视频处理
moviepy>=1.0.3
pillow>=10.0.0

# AI 服务
edge-tts>=6.0.0
replicate>=0.15.0
openai>=1.0.0  # 用于 DeepSeek API

# 浏览器自动化
playwright>=1.40.0

# HTTP 客户端
httpx>=0.24.0
requests>=2.31.0

# 工具库
python-dotenv>=1.0.0
pydantic-settings>=2.0.0
```

## 系统依赖

```bash
# FFmpeg (必需)
brew install ffmpeg  # macOS
apt-get install ffmpeg  # Ubuntu
choco install ffmpeg  # Windows

# Playwright 浏览器 (Phase 4)
playwright install chromium
```

## 环境变量 (必需)

```bash
# AI 服务
DEEPSEEK_API_KEY=sk-xxxxx
REPLICATE_API_TOKEN=r8_xxxxx

# 应用配置
APP_ENV=development
SECRET_KEY=your-secret-key-32-chars-min
CORS_ORIGINS=http://localhost:3000

# 数据库
DATABASE_URL=sqlite:///./app.db  # 开发环境
# DATABASE_URL=postgresql://user:pass@host:5432/db  # 生产环境
```

## 快速启动

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 验证安装

```bash
# 检查 FFmpeg
ffmpeg -version

# 检查 Python 依赖
pip list

# 检查 Node 依赖
npm list --depth=0

# 测试 API 连接
curl http://localhost:8000/health
```

## 预计依赖数量

| 类型 | 数量 |
|------|------|
| 前端生产依赖 | ~15-20 |
| 前端开发依赖 | ~10-15 |
| 后端依赖 | ~15-20 |
| 系统依赖 | 2 (FFmpeg, Playwright) |

## 关键依赖版本要求

| 依赖 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Node.js | 18.x | 20.x LTS |
| Python | 3.9 | 3.11+ |
| FFmpeg | 4.x | 6.x |
| PostgreSQL | 13.x | 15.x |

## 注意事项

1. **FFmpeg**: 必须先安装,否则视频生成会失败
2. **API Keys**: DeepSeek 和 Replicate 必须配置
3. **Playwright**: 首次安装需下载 ~200MB 浏览器文件
4. **数据库**: 开发用 SQLite,生产建议 PostgreSQL
5. **Python 版本**: 建议 3.11+,moviepy 在 3.12 可能有兼容性问题
