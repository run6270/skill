# X/Twitter 推文转文档工具 (xtod)

## 快速开始

### 1. 确保 Chrome 远程调试模式已启动

```bash
~/launch-chrome-debug.sh
```

### 2. 在 Chrome 中登录 Twitter

打开 Chrome 浏览器，访问 https://x.com 并登录你的账号。

### 3. 使用 Skill

在 Claude Code 中：

```
使用 xtod skill 读取这条推文：
https://x.com/username/status/1234567890
```

或指定输出格式：

```
用 xtod 把这个推文转成 PPT：
https://x.com/sama/status/1234567890
```

## 功能特点

- ✅ 复用 Chrome 登录状态
- ✅ 自动识别完整 Thread
- ✅ 展开所有折叠内容
- ✅ 保存所有图片（原图）
- ✅ 生成 PDF 或 PPT 文档
- ✅ 上下文优化（< 10k tokens）

## 输出格式

### PDF（默认）
- 封面页
- 每条推文一页
- 包含截图和文字
- 互动数据

### PPT
- 标题页
- 左侧截图 + 右侧摘要
- 适合演示

## 依赖安装

第一次使用时会自动安装：
- reportlab (PDF 生成)
- python-pptx (PPT 生成)
- requests (图片下载)

## 故障排除

### 无法连接 Chrome

确保 Chrome 以远程调试模式运行：
```bash
ps aux | grep "remote-debugging-port=9222"
```

如果没有，重新运行：
```bash
~/launch-chrome-debug.sh
```

### 推文需要登录

在 Chrome 中访问 https://x.com 并确认已登录。

## 示例

### 读取单条推文
```
skill xtod
URL: https://x.com/elonmusk/status/123
```

### 读取 Thread 生成 PPT
```
用 xtod 把这个 thread 转成 PPT：
https://x.com/sama/status/456
```

## 目录结构

```
~/.claude/skills/xtod/
├── skill.md                  # Skill 定义
├── twitter_reader.py         # 推文读取器
├── document_generator.py     # 文档生成器
└── README.md                 # 本文件
```

## 技术细节

### 上下文控制

主会话只接收最终的 JSON 数据，所有浏览器操作都在 Python 脚本中完成，避免超出 token 限制。

### Thread 识别

自动识别作者的所有回复，构建完整的 Thread 顺序。

### 图片处理

自动下载原图（4096x4096 分辨率），嵌入到文档中。

## 限制

- 推文数量：无限制，读取所有符合用户条件的推文
- 视频：只截取封面
- 私密账号：需要有访问权限
- Rate Limiting：建议每次间隔 30 秒

## 更新日志

**v2.1.0** (2025-11-05)
- ✅ 移除推文数量限制
- ✅ 完整保留推文正文，不截断
- ✅ 完整保留所有图片和图表
- ✅ 按用户条件读取，不由模型筛选

**v1.0.0** (2025-11-05)
- 初始版本
- 支持 PDF 和 PPT 格式
- 完整 Thread 识别
- 上下文优化

## 许可证

MIT License
