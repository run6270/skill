# 项目依赖与环境配置 - 文档索引

本目录包含小红书热点内容工厂项目的完整依赖分析和环境配置文档。

## 文档列表

### 1. [dependencies-analysis.md](./dependencies-analysis.md) - 依赖分析报告
**文件大小**: 9.7KB

**内容概要**:
- 完整的技术栈依赖清单（前端、后端、系统级）
- 环境变量详细说明（必需、可选）
- 安全配置要求
- 开发环境搭建步骤
- 生产环境部署要求
- 成本估算（API调用、基础设施）
- 常见问题排查

**适用场景**:
- 了解项目整体技术架构
- 评估项目成本
- 规划部署方案

---

### 2. [env-config-guide.md](./env-config-guide.md) - 环境变量配置指南
**文件大小**: 6.7KB

**内容概要**:
- .env 文件完整模板
- 配置优先级说明（P0/P1/P2）
- 快速配置步骤（含API Key获取方法）
- 配置文件位置说明
- 安全注意事项
- 故障排查指南
- 开发/生产环境示例配置

**适用场景**:
- 首次配置项目环境
- 排查环境变量相关问题
- 部署到新环境

---

### 3. [installation-checklist.md](./installation-checklist.md) - 安装检查清单
**文件大小**: 8.6KB

**内容概要**:
- 系统要求检查
- 分步安装指南（10个步骤）
- 多平台安装命令（macOS/Ubuntu/Windows）
- 功能测试步骤
- 开发工具配置（可选）
- 完成检查清单
- 详细的故障排查指南

**适用场景**:
- 从零开始搭建开发环境
- 验证环境配置是否完整
- 排查安装过程中的问题

---

## 快速导航

### 我是新手，第一次搭建环境
1. 先阅读 [installation-checklist.md](./installation-checklist.md)
2. 按照清单逐步安装
3. 遇到环境变量问题时查看 [env-config-guide.md](./env-config-guide.md)

### 我需要了解项目依赖
1. 阅读 [dependencies-analysis.md](./dependencies-analysis.md)
2. 查看技术栈和依赖清单
3. 评估成本和部署方案

### 我遇到了配置问题
1. 查看 [env-config-guide.md](./env-config-guide.md) 的故障排查部分
2. 检查 [installation-checklist.md](./installation-checklist.md) 的故障排查部分
3. 查看 [dependencies-analysis.md](./dependencies-analysis.md) 的常见问题部分

---

## 核心依赖速查

### 前端
- Next.js 15
- React 18+
- shadcn/ui + Tailwind CSS
- TypeScript 5.x

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy 2.x
- APScheduler 3.x
- Playwright
- FFmpeg 6.x

### AI服务
- DeepSeek API（文案生成）
- Replicate Flux（图片生成）
- Edge TTS（语音合成，免费）

---

## 必需的环境变量

| 变量名 | 说明 | 优先级 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | P0 |
| `REPLICATE_API_TOKEN` | Replicate API令牌 | P0 |
| `DATABASE_URL` | 数据库连接字符串 | P0 |
| `SECRET_KEY` | 应用密钥（32字符） | P0 |
| `MEDIA_ROOT` | 媒体文件存储路径 | P0 |
| `CORS_ORIGINS` | 允许的跨域来源 | P1 |
| `XIAOHONGSHU_COOKIE` | 小红书Cookie | P1 |

---

## 成本估算

### API调用成本（月）
- DeepSeek: 约 ¥1.2/月
- Replicate Flux: 约 ¥13/月
- Edge TTS: 免费
- **总计**: 约 ¥15/月

### 部署成本（月）
- 本地部署: ¥0
- 云部署: ¥200-550/月

---

## 系统要求

- **操作系统**: macOS 12+ / Ubuntu 20.04+ / Windows 10+
- **内存**: 至少 4GB RAM
- **磁盘**: 至少 10GB 可用空间
- **网络**: 稳定的互联网连接

---

## 开发环境快速启动

```bash
# 1. 安装系统依赖
brew install python@3.10 node ffmpeg  # macOS

# 2. 安装后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install

# 3. 安装前端依赖
cd ../frontend
npm install

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入API Key

# 5. 启动服务
# 终端1: 启动后端
cd backend && uvicorn app.main:app --reload

# 终端2: 启动前端
cd frontend && npm run dev
```

---

## 文档更新记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-03-04 | v1.0 | 初始版本，完整的依赖分析和配置指南 |

---

## 相关文档

- [PRD.md](../../../PRD.md) - 产品需求文档
- [README.md](../../../README.md) - 项目说明文档（待创建）
- [API文档](http://localhost:8000/docs) - FastAPI自动生成的API文档

---

## 获取帮助

如果文档中的信息无法解决你的问题:

1. 查看项目根目录的 PRD.md 了解更多技术细节
2. 查看后端日志: `tail -f backend/logs/app.log`
3. 访问API文档: http://localhost:8000/docs
4. 提交Issue到项目仓库

---

**文档生成时间**: 2026-03-04
**分析工具**: Claude Code (Opus 4.6)
**项目路径**: /Users/mac/Documents/GitHub/githubrepo
