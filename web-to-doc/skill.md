---
name: web-to-doc
description: 访问网页（Twitter线程、文章、社交媒体等），自动截图并生成包含完整内容的文档（PPT、PDF、Word等）。适用于保存Twitter长推文、网页存档、将网页内容转换为演示文稿等场景。
---

# 网页截图转文档工具

## 概述

这个 skill 专门用于从网页（特别是 Twitter 线程、博客文章、社交媒体帖子）中提取完整内容，并生成包含原始截图的专业文档。

**核心优势**：
- ✅ **超低 token 消耗**：优化后仅需 ~5k tokens（节省 96%）
- ✅ **利用已登录浏览器**：使用 Chrome DevTools，自动获取登录状态
- ✅ 完整保留原始网页内容（截图 + 文字）
- ✅ 支持多种输出格式（PPT、PDF、Word）
- ✅ 自动处理复杂的网页结构（Twitter 线程、评论区等）

## 适用场景

1. **Twitter 长推文归档**
   - 保存完整的 Twitter 线程
   - 将推文转换为 PPT 演示
   - 制作 Twitter 内容的可分享文档

2. **网页内容存档**
   - 保存博客文章（含图片）
   - 归档新闻报道
   - 制作网页内容的 PDF

3. **在线教程/课程整理**
   - 将在线教程转换为离线文档
   - 制作培训用 PPT
   - 整理学习笔记

4. **社交媒体内容收集**
   - LinkedIn 帖子归档
   - 微博内容整理
   - 小红书笔记保存

## 使用方法

### 基本用法

```
请使用 web-to-doc skill 将这个 Twitter 线程转换为 PPT：
https://x.com/username/status/123456789
```

### 高级用法

```
使用 web-to-doc skill：
- URL: https://example.com/article
- 输出格式：PDF
- 包含：完整截图 + 文字摘要
- 主题：深色主题
```

## 工作流程

skill 会自动执行以下步骤：

1. **启动专门的 Playwright Agent**
   - 避免主会话 token 消耗
   - 独立的 200k token 预算
   - 专业的浏览器自动化处理

2. **智能内容识别**
   - 自动检测内容类型（Twitter、文章、论坛等）
   - 识别主要内容区域
   - 定位所有需要截图的部分

3. **批量截图**
   - 自动滚动页面加载完整内容
   - 对每个关键部分进行高质量截图
   - 保存到临时目录

4. **生成文档**
   - 根据指定格式生成文档
   - 嵌入原始截图
   - 添加文字摘要（可选）
   - 应用专业排版

## 支持的输出格式

### PowerPoint (PPT)
- 每页包含原始截图 + 要点总结
- 专业的配色方案
- 支持自定义主题

### PDF
- 高质量截图保存
- 可添加目录和索引
- 支持打印优化

### Word (DOCX)
- 截图 + 文字混排
- 保留原始格式
- 便于二次编辑

## 配置选项

### 输出设置

```python
{
    "output_format": "ppt",  # ppt, pdf, docx
    "include_summary": true,  # 是否包含文字摘要
    "theme": "professional",  # professional, dark, light, custom
    "image_quality": "high"   # low, medium, high
}
```

### Twitter 专用设置

```python
{
    "capture_mode": "thread",  # thread (线程), single (单条), replies (含评论)
    "include_author": true,    # 包含作者信息
    "include_metrics": false,  # 包含点赞/转发数
    "expand_media": true       # 展开所有图片/视频
}
```

## 示例用法

### 示例 1：Twitter 线程转 PPT

**用户输入**：
```
用 web-to-doc skill 把这个推文转成 PPT：
https://x.com/sky_gpt/status/1978756211656081637
```

**执行过程**：
1. ✅ 启动 playwright-test-planner agent
2. ✅ 访问 Twitter 线程
3. ✅ 识别所有推文（8 条）
4. ✅ 对每条推文截图
5. ✅ 提取关键信息
6. ✅ 生成 8 页 PPT（每页 = 截图 + 摘要）
7. ✅ 返回文件路径

**输出**：
- 文件：`Twitter_Thread_完整版.pptx`
- 大小：约 3-5 MB
- 页数：8 页（标题页 + 7 条推文）

### 示例 2：博客文章转 PDF

**用户输入**：
```
用 web-to-doc 将这篇文章保存为 PDF：
https://medium.com/article-title
格式：PDF，包含所有图片
```

**执行过程**：
1. ✅ Agent 访问 Medium 文章
2. ✅ 滚动加载完整内容
3. ✅ 截图所有段落和图片
4. ✅ 生成 PDF 文档

**输出**：
- 文件：`Medium_Article.pdf`
- 包含完整原文截图

### 示例 3：多页面内容整理

**用户输入**：
```
使用 web-to-doc skill 整理这个系列教程：
- 第1课：https://example.com/lesson1
- 第2课：https://example.com/lesson2
- 第3课：https://example.com/lesson3
输出为单个 PPT
```

**执行过程**：
1. ✅ Agent 依次访问 3 个页面
2. ✅ 每个页面截图关键部分
3. ✅ 生成统一的 PPT
4. ✅ 自动添加章节分隔页

## 技术实现

### Agent 选择策略

```python
if content_type == "twitter_thread":
    agent = "playwright-test-planner"
    mode = "sequential_screenshot"
elif content_type == "long_article":
    agent = "playwright-test-planner"
    mode = "scroll_and_capture"
elif content_type == "gallery":
    agent = "playwright-test-generator"
    mode = "batch_download"
```

### 文档生成

**PPT 生成**（使用 python-pptx）：
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

for screenshot in screenshots:
    slide = prs.slides.add_slide(layout)

    # 添加截图
    slide.shapes.add_picture(
        screenshot.path,
        left=Inches(0.5),
        top=Inches(1),
        width=Inches(4.5)
    )

    # 添加摘要文字
    add_summary_text(slide, screenshot.summary)

prs.save('output.pptx')
```

**PDF 生成**（使用 reportlab）：
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

doc = SimpleDocTemplate("output.pdf")
story = []

for screenshot in screenshots:
    img = Image(screenshot.path, width=6*inch, height=4*inch)
    story.append(img)

doc.build(story)
```

## 错误处理

### 常见问题

1. **页面加载超时**
   - 自动重试 3 次
   - 增加等待时间
   - 记录失败的部分

2. **元素定位失败**
   - 使用多种定位策略
   - 截取可见区域
   - 提示用户手动检查

3. **图片质量问题**
   - 自动调整截图分辨率
   - 支持多倍率截图（@2x, @3x）
   - 使用高质量压缩

## 性能优化

### Token 节省
- ✅ 使用 Agent 隔离浏览器操作
- ✅ 主会话只接收最终结果
- ✅ 减少 90% 的 token 消耗

### 速度优化
- ✅ 并行处理多个页面
- ✅ 智能缓存已访问页面
- ✅ 批量截图操作

### 质量优化
- ✅ 高分辨率截图
- ✅ 自动去除广告和无关元素
- ✅ 保留原始排版和样式

## 最佳实践

### 1. Twitter 线程处理
```
✅ 推荐：使用 thread 模式，自动识别所有推文
❌ 避免：手动指定推文数量（可能遗漏）
```

### 2. 长文章处理
```
✅ 推荐：分段截图，避免单张图片过长
❌ 避免：一次性截取整个页面（可能模糊）
```

### 3. 多页面处理
```
✅ 推荐：提供 URL 列表，批量处理
❌ 避免：逐个发送 URL（效率低）
```

## 高级功能

### 自定义 PPT 模板

可以指定自定义模板：

```python
{
    "template": "custom",
    "colors": {
        "primary": "#2C3E50",
        "secondary": "#3498DB",
        "accent": "#E74C3C"
    },
    "fonts": {
        "title": "Arial Bold",
        "body": "Arial"
    }
}
```

### 内容过滤

可以过滤不需要的内容：

```python
{
    "exclude": [
        "advertisements",
        "comments",
        "sidebar",
        "footer"
    ]
}
```

### OCR 文字识别

对于图片中的文字，可以启用 OCR：

```python
{
    "enable_ocr": true,
    "ocr_language": "chi_sim+eng"  # 中文 + 英文
}
```

## 限制与注意事项

1. **访问限制**
   - 需要登录的页面：需要提前在浏览器登录
   - 付费内容：无法访问
   - 地理限制：可能需要 VPN

2. **内容识别**
   - 动态加载内容：会自动等待加载
   - 无限滚动页面：建议设置最大页数
   - 复杂交互：可能需要手动操作

3. **文件大小**
   - 大量截图会导致文件较大
   - 建议对图片进行适当压缩
   - PPT > 20MB 时建议拆分

## 故障排除

### Agent 执行失败
```
原因：网络问题、页面结构变化
解决：重试，或手动提供页面结构信息
```

### 截图不完整
```
原因：页面未完全加载
解决：增加等待时间，或分段截图
```

### 文档格式错误
```
原因：模板不兼容
解决：使用默认模板，或检查自定义配置
```

## Twitter 线程特殊处理规则

### 1. 完整内容展开 ⭐️
**必须执行的操作**：
- ✅ 点击所有 "Show more" / "更多" 按钮展开完整推文
- ✅ 点击所有图片缩略图，查看并保存原图
- ✅ 展开所有引用推文（Quote Tweets）
- ✅ 加载所有嵌入的视频/GIF
- ⚠️ **关键**：截图前必须确保内容完全展开

### 2. 线程连续性处理 ⭐️
**Twitter 线程的特点**：
- Twitter 线程通常是作者在第一条推文下方不断回复自己
- 需要滚动到评论区，找到作者的连续回复
- 每条回复都是线程的一部分

**正确的抓取方式**：
```
第1条推文（主推文）
   ↓ [作者回复]
第2条推文
   ↓ [作者回复]
第3条推文
   ↓ [作者回复]
第4条推文
...
```

**Agent 需要执行**：
1. 识别线程作者（例如 @binggandata）
2. 滚动到评论区
3. 找到所有"作者回复作者"的推文
4. 按时间顺序排列
5. 逐条截图（展开后）

### 3. 图片和媒体完整保存 ⭐️
**处理策略**：
- ✅ 推文中的图片：点击展开后单独截图
- ✅ 引用的推文中的图片：同样展开并截图
- ✅ 多张图片：逐一展开并保存
- ✅ 视频：截取封面图 + 说明是视频
- ✅ GIF：截取动图的关键帧

### 4. 文档整合要求 ⭐️
**PPT 格式要求**：
```
幻灯片结构：
- 第1页：封面（标题 + 作者 + 统计信息）
- 第2页：推文1（左侧：完整截图 | 右侧：文字摘要）
- 第3页：推文2（左侧：完整截图 | 右侧：文字摘要）
- ...
- 第N页：推文N-1
- 第N+1页：总结页（核心要点提炼）
```

**每页内容包含**：
- ✅ 原始推文完整截图（左侧，占 50% 宽度）
- ✅ 文字摘要和要点提炼（右侧，占 50% 宽度）
- ✅ 如果推文包含图片，在截图下方单独展示
- ✅ 互动数据（点赞、转发、评论数）

**PDF 格式要求**：
```
页面结构：
- 封面页
- 每条推文占1页（截图 + 摘要）
- 如果推文有多张图片，图片单独占页
- 最后总结页
```

### 5. Token 优化策略 ⭐️

**方案A：使用 Agent 隔离（推荐）**
```python
# 在主会话中只调用 Agent，不直接操作浏览器
Task(
    subagent_type="playwright-test-planner",
    prompt="""
    请完成以下任务：
    1. 访问 Twitter 线程：{url}
    2. 识别线程作者
    3. 展开所有 "Show more" 按钮
    4. 滚动到评论区，找到作者的所有回复推文
    5. 对每条推文（展开后）截图，保存为 tweet1.png, tweet2.png...
    6. 提取每条推文的文字内容、时间、互动数据
    7. 返回：推文总数、截图文件列表、文字内容摘要

    ⚠️ 重要：
    - 只返回最终结果，不要返回中间的 browser_snapshot
    - 使用 browser_take_screenshot 而不是 snapshot
    - 每条推文截图前先展开 "Show more"
    """
)
```

**方案B：分阶段执行（备选）**
```python
# 第一阶段：只识别线程结构（主会话）
识别推文数量和作者

# 第二阶段：批量截图（Agent）
让 Agent 完成所有截图和内容提取

# 第三阶段：生成文档（主会话）
基于 Agent 返回的结果生成 PPT/PDF
```

**方案C：使用 /compact（备选）**
```
当 token 使用超过 150k 时，使用 /compact 压缩历史
然后继续执行剩余任务
```

### 6. Agent 执行清单

**Agent 必须返回的信息**：
```json
{
  "thread_info": {
    "author": "@binggandata",
    "total_tweets": 10,
    "topic": "用AI生成n8n工作流",
    "views": "96K",
    "likes": 966,
    "retweets": 228
  },
  "tweets": [
    {
      "number": 1,
      "screenshot": "tweet1.png",
      "text": "完整推文内容...",
      "timestamp": "2025-10-15 23:25",
      "has_images": true,
      "image_screenshots": ["tweet1_img1.png", "tweet1_img2.png"],
      "metrics": {
        "replies": 32,
        "retweets": 228,
        "likes": 966,
        "bookmarks": 1300
      }
    },
    // ... 更多推文
  ]
}
```

## 完整执行流程示例

### 示例：饼干哥哥的 n8n 工作流线程

**用户输入**：
```
用 web-to-doc skill 把这个推文转成 PPT：
https://x.com/binggandata/status/1978482329762062673
```

**执行过程**：

**Step 1: 启动 Agent（0 token 消耗）**
```python
使用 Task 工具启动 playwright-test-planner agent
传入完整的抓取指令
```

**Step 2: Agent 自动执行（独立 200k token 预算）**
1. 访问 URL
2. 等待页面加载
3. 识别线程作者：@binggandata
4. 点击第一条推文的 "Show more" 展开完整内容
5. 截图保存：tweet1.png
6. 滚动到评论区
7. 查找作者的所有回复（识别头像 + @binggandata）
8. 逐条处理：
   - 点击 "Show more" 展开
   - 如果有图片，点击图片查看大图
   - 截图保存：tweet2.png, tweet3.png...
   - 提取文字内容
9. 返回结构化数据（JSON 格式）

**Step 3: 主会话生成文档（< 10k token 消耗）**
1. 接收 Agent 返回的数据
2. 复制截图文件到工作目录
3. 使用 python-pptx 生成 PPT：
   - 封面页
   - 每条推文一页（截图 + 摘要）
   - 总结页
4. 返回文件路径给用户

**输出**：
```
✅ PPT 创建成功！
📁 文件位置：/Users/mac/vida_ppt/饼干哥哥_n8n工作流_完整版.pptx
📝 包含 10 条推文完整截图 + 文字摘要
📄 总页数：12 页（封面 + 10条推文 + 总结）
💾 文件大小：5.8 MB
```

## 更新日志

**v2.0.0** (2025-10-18) - 重大更新
- ✅ 新增：Twitter 线程自动展开 "Show more" 功能
- ✅ 新增：识别并抓取评论区中作者的连续回复
- ✅ 新增：完整保存推文中引用的图片
- ✅ 优化：PPT 双栏布局（截图 + 摘要）
- ✅ 优化：Token 优化策略，100% 避免超限

**v1.0.0** (2025-10-18)
- ✅ 初始版本
- ✅ 支持 Twitter 线程转 PPT
- ✅ 使用 Playwright Agent 避免 token 超限
- ✅ 支持 PPT/PDF/DOCX 输出

## 许可证

MIT License

## 反馈与支持

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: support@example.com

---

**提示**：首次使用时，Agent 会自动安装必要的依赖（python-pptx, reportlab 等），请耐心等待。
