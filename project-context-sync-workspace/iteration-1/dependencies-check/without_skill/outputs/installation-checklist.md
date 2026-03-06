# 依赖安装检查清单

## 系统要求

- [ ] macOS 12+ / Ubuntu 20.04+ / Windows 10+
- [ ] 至少 4GB RAM
- [ ] 至少 10GB 可用磁盘空间
- [ ] 稳定的网络连接

---

## 第一步: 系统级依赖安装

### macOS

```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖
brew install python@3.10 node ffmpeg

# 验证安装
python3 --version  # 应显示 3.10.x 或更高
node --version     # 应显示 v18.x 或更高
npm --version      # 应显示 9.x 或更高
ffmpeg -version    # 应显示 6.x 或更高
```

- [ ] Python 3.10+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] npm 9+ 已安装
- [ ] FFmpeg 6+ 已安装

### Ubuntu/Debian

```bash
# 更新包列表
sudo apt update

# 安装依赖
sudo apt install -y python3.10 python3-pip python3-venv nodejs npm ffmpeg

# 安装最新版 Node.js（如果系统版本过低）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
python3 --version
node --version
npm --version
ffmpeg -version
```

- [ ] Python 3.10+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] npm 9+ 已安装
- [ ] FFmpeg 已安装

### Windows

```powershell
# 使用 Chocolatey 安装（推荐）
# 先安装 Chocolatey: https://chocolatey.org/install

choco install python310 nodejs ffmpeg -y

# 验证安装
python --version
node --version
npm --version
ffmpeg -version
```

- [ ] Python 3.10+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] npm 9+ 已安装
- [ ] FFmpeg 已安装

---

## 第二步: 项目克隆

```bash
# 克隆项目（假设项目已在GitHub）
git clone https://github.com/your-org/xiaohongshu-content-factory.git
cd xiaohongshu-content-factory

# 或者如果是本地项目
cd /path/to/githubrepo
```

- [ ] 项目已克隆到本地
- [ ] 已进入项目根目录

---

## 第三步: 后端依赖安装

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install

# 验证安装
python -c "import fastapi; print(fastapi.__version__)"
python -c "import playwright; print('Playwright installed')"
```

- [ ] Python虚拟环境已创建
- [ ] 虚拟环境已激活
- [ ] requirements.txt 依赖已安装
- [ ] Playwright浏览器已安装
- [ ] 无安装错误

### 常见问题

**问题**: `pip install` 速度慢
**解决**: 使用国内镜像源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**问题**: `playwright install` 失败
**解决**: 手动指定浏览器
```bash
playwright install chromium
```

---

## 第四步: 前端依赖安装

```bash
# 进入前端目录
cd ../frontend

# 安装依赖
npm install

# 或使用 pnpm（更快）
npm install -g pnpm
pnpm install

# 验证安装
npm list next
npm list react
```

- [ ] package.json 依赖已安装
- [ ] node_modules 目录已创建
- [ ] 无安装错误或警告

### 常见问题

**问题**: `npm install` 速度慢
**解决**: 使用国内镜像源
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

**问题**: 依赖版本冲突
**解决**: 清理缓存重新安装
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 第五步: 环境变量配置

```bash
# 返回项目根目录
cd ..

# 创建 .env 文件
cp .env.example .env  # 如果有模板
# 或
touch .env

# 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

- [ ] .env 文件已创建
- [ ] DEEPSEEK_API_KEY 已配置
- [ ] REPLICATE_API_TOKEN 已配置
- [ ] DATABASE_URL 已配置
- [ ] SECRET_KEY 已生成并配置
- [ ] MEDIA_ROOT 已配置
- [ ] CORS_ORIGINS 已配置

参考: [环境变量配置指南](./env-config-guide.md)

---

## 第六步: 数据库初始化

```bash
# 进入后端目录
cd backend

# 激活虚拟环境（如果未激活）
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 创建数据库表
python -m app.database init

# 或运行迁移脚本（如果有）
alembic upgrade head
```

- [ ] 数据库文件已创建（SQLite）或连接成功（PostgreSQL）
- [ ] 数据表已创建
- [ ] 无数据库错误

---

## 第七步: 启动服务测试

### 启动后端

```bash
# 在 backend 目录下
cd backend
source venv/bin/activate

# 开发模式启动
uvicorn app.main:app --reload --port 8000

# 或使用脚本（如果有）
python run.py
```

- [ ] 后端服务启动成功
- [ ] 访问 http://localhost:8000/docs 可以看到API文档
- [ ] 无启动错误

### 启动前端

```bash
# 新开一个终端，进入 frontend 目录
cd frontend

# 开发模式启动
npm run dev

# 或使用 pnpm
pnpm dev
```

- [ ] 前端服务启动成功
- [ ] 访问 http://localhost:3000 可以看到界面
- [ ] 无启动错误

---

## 第八步: 功能测试

### 测试API连接

1. 访问 http://localhost:3000/settings
2. 进入"API配置"标签
3. 点击"测试连接"按钮

- [ ] DeepSeek API 连接成功
- [ ] Replicate API 连接成功

### 测试热点抓取

1. 访问 http://localhost:3000/trends
2. 添加关键词（如"美妆"）
3. 点击"立即抓取"

- [ ] 热点抓取成功
- [ ] 可以看到热点列表

### 测试内容生成

1. 选择一个热点话题
2. 点击"生成内容"
3. 等待AI生成完成

- [ ] 文案生成成功
- [ ] 封面图生成成功
- [ ] 视频生成成功（如果启用）

---

## 第九步: 开发工具配置（可选）

### VS Code 扩展

```bash
# 安装推荐扩展
code --install-extension ms-python.python
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension bradlc.vscode-tailwindcss
```

- [ ] Python 扩展已安装
- [ ] ESLint 扩展已安装
- [ ] Prettier 扩展已安装
- [ ] Tailwind CSS 扩展已安装

### Git 配置

```bash
# 配置 Git 用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 配置 .gitignore
cat >> .gitignore << EOF
.env
.env.local
*.db
media/
logs/
__pycache__/
node_modules/
.next/
venv/
EOF
```

- [ ] Git 用户信息已配置
- [ ] .gitignore 已配置

---

## 第十步: 性能优化（可选）

### 后端优化

```bash
# 安装性能监控工具
pip install uvicorn[standard]  # 使用高性能服务器
pip install gunicorn  # 生产环境使用

# 配置日志轮转
pip install python-json-logger
```

- [ ] 高性能服务器已安装
- [ ] 日志工具已配置

### 前端优化

```bash
# 安装构建优化工具
npm install -D @next/bundle-analyzer

# 配置环境变量
echo "ANALYZE=true" >> .env.local
```

- [ ] 构建分析工具已安装

---

## 完成检查

### 最终验证清单

- [ ] 所有系统依赖已安装
- [ ] 后端依赖已安装且无错误
- [ ] 前端依赖已安装且无错误
- [ ] 环境变量已正确配置
- [ ] 数据库已初始化
- [ ] 后端服务可以正常启动
- [ ] 前端服务可以正常启动
- [ ] API连接测试通过
- [ ] 基本功能测试通过
- [ ] 开发工具已配置（可选）

### 下一步

1. 阅读 [PRD.md](../PRD.md) 了解产品功能
2. 查看 [API文档](http://localhost:8000/docs) 了解接口
3. 开始开发或使用系统

---

## 故障排查

### 后端启动失败

**检查项**:
1. Python版本是否正确: `python3 --version`
2. 虚拟环境是否激活: `which python`
3. 依赖是否完整安装: `pip list`
4. 环境变量是否配置: `cat .env`
5. 端口是否被占用: `lsof -i :8000`

### 前端启动失败

**检查项**:
1. Node.js版本是否正确: `node --version`
2. 依赖是否完整安装: `npm list`
3. 端口是否被占用: `lsof -i :3000`
4. 环境变量是否配置: `cat .env.local`

### API调用失败

**检查项**:
1. API Key是否正确配置
2. 网络连接是否正常
3. API余额是否充足
4. 后端日志中的错误信息: `tail -f logs/app.log`

### 视频生成失败

**检查项**:
1. FFmpeg是否正确安装: `ffmpeg -version`
2. 媒体文件路径是否存在: `ls -la media/`
3. 磁盘空间是否充足: `df -h`
4. 文件权限是否正确: `ls -la media/`

---

## 获取帮助

如果遇到问题:

1. 查看项目文档: [README.md](../README.md)
2. 查看API文档: http://localhost:8000/docs
3. 查看日志文件: `logs/app.log`
4. 提交Issue: [GitHub Issues](https://github.com/your-org/xiaohongshu-content-factory/issues)

---

## 更新依赖

### 后端依赖更新

```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 前端依赖更新

```bash
cd frontend
npm update
# 或
pnpm update
```

建议每月检查一次依赖更新。
