---
name: xtod
description: Twitter/X 推文阅读和文档生成工具。严格按照用户指定的链接和条件读取所有推文（包括完整 thread），展开所有折叠内容，完整保留推文正文、图片和图表（不截断），生成 PDF 或 PPT 文档。使用 Agent 隔离机制，主会话 token 消耗 < 10k。
---

# X/Twitter 推文转文档工具 (xtod)

## ⚠️ 重要提示

本 skill 使用 **Agent 隔离机制**，确保主会话不会因为上下文过大而中断：
- ✅ 所有浏览器操作由独立的 Agent 完成
- ✅ Agent 有独立的 200k token 预算
- ✅ 主会话只接收最终的 JSON 数据
- ✅ 主会话 token 消耗 < 10k

## 执行流程（Claude 必须严格遵循）

当用户请求使用 xtod skill 时，**必须**按照以下步骤执行：

### Step 1: 解析用户请求

从用户输入中提取：
- `url`: Twitter 推文 URL（必需）
- `format`: 输出格式（可选，默认 "pdf"）
- `time_filter`: 时间筛选条件（可选，例如"最近一周"、"最近一个月"等）
- `other_conditions`: 其他用户指定的筛选条件（可选）

**重要**：读取所有符合用户条件的推文，不进行数量限制，不由模型选择"关键推文"。

### Step 2: 启动 Agent 读取推文

**关键**：使用 `Task` 工具启动一个独立的 Agent 来完成所有浏览器操作。

```python
Task(
    subagent_type="general-purpose",
    description="读取 Twitter 推文",
    prompt=f'''
你的任务：读取 Twitter 推文并返回 JSON 数据

URL: {url}
时间筛选: {time_filter if time_filter else "无限制"}
其他条件: {other_conditions if other_conditions else "无"}

**重要**：读取所有符合条件的推文，不限制数量，完整保留所有推文内容和图片。

## 执行步骤

### 1. 连接 Chrome DevTools

使用 mcp__chrome-devtools 工具连接到已经打开的 Chrome 浏览器。
Chrome 应该已经以远程调试模式运行（端口 9222）。

首先检查连接：
- 调用 mcp__chrome-devtools__list_pages 查看浏览器状态

### 2. 导航到推文 URL

- 调用 mcp__chrome-devtools__navigate_page(url="{url}", timeout=30000)
- 等待 3-5 秒让页面加载

### 3. 展开所有折叠内容

执行 JavaScript 展开所有 "Show more" 按钮：

```javascript
mcp__chrome-devtools__evaluate_script(
    function='''
    () => {{
        let expanded = 0;
        const buttons = document.querySelectorAll('[data-testid="tweet-text-show-more-link"]');
        buttons.forEach(button => {{
            try {{
                button.click();
                expanded++;
            }} catch (e) {{}}
        }});
        return {{ expanded: expanded, total: buttons.length }};
    }}
    '''
)
```

等待 2 秒让内容展开。

### 4. 滚动加载评论区

如果是 thread，需要滚动加载评论区：

```javascript
// 滚动 3-5 次
for (let i = 0; i < 5; i++) {{
    mcp__chrome-devtools__evaluate_script(
        function='() => {{ window.scrollBy(0, 800); return window.scrollY; }}'
    )
    // 等待 2 秒
}}
```

### 5. 再次展开（评论区可能有新的折叠内容）

重复步骤 3。

### 6. 提取推文数据

执行 JavaScript 提取所有推文数据：

```javascript
mcp__chrome-devtools__evaluate_script(
    function='''
    () => {{
        const result = {{
            author: null,
            total_tweets: 0,
            tweets: []
        }};

        const articles = document.querySelectorAll('article[data-testid="tweet"]');

        articles.forEach((article, index) => {{
            try {{
                // 提取作者
                const authorLink = article.querySelector('a[role="link"][href^="/"]');
                const authorName = article.querySelector('[data-testid="User-Name"]');
                const author = {{
                    handle: authorLink ? authorLink.getAttribute('href').substring(1) : '',
                    name: authorName ? authorName.textContent.split('\\n')[0] : ''
                }};

                if (index === 0) result.author = author;

                // 提取文本
                const tweetText = article.querySelector('[data-testid="tweetText"]');
                const text = tweetText ? tweetText.innerText : '';

                // 提取时间
                const timeElement = article.querySelector('time');
                const timestamp = timeElement ? timeElement.getAttribute('datetime') : '';
                const timeText = timeElement ? timeElement.textContent : '';

                // 提取图片
                const images = [];
                const imageElements = article.querySelectorAll('[data-testid="tweetPhoto"] img');
                imageElements.forEach(img => {{
                    if (img.src && img.src.includes('pbs.twimg.com/media')) {{
                        const originalUrl = img.src
                            .replace(/\\?.*$/, '')
                            .replace('&name=small', '')
                            .replace('&name=medium', '')
                            .replace('&name=large', '') + '?format=jpg&name=4096x4096';
                        images.push({{
                            url: originalUrl,
                            alt: img.alt || ''
                        }});
                    }}
                }});

                // 提取互动数据
                const getMetric = (testid) => {{
                    const elem = article.querySelector(`[data-testid="${{testid}}"]`);
                    if (!elem) return 0;
                    const text = elem.getAttribute('aria-label') || elem.textContent || '';
                    const match = text.match(/([\\d,]+)/);
                    if (!match) return 0;
                    return parseInt(match[1].replace(/,/g, ''), 10);
                }};

                const metrics = {{
                    replies: getMetric('reply'),
                    retweets: getMetric('retweet'),
                    likes: getMetric('like'),
                    bookmarks: getMetric('bookmark')
                }};

                if (text || images.length > 0) {{
                    result.tweets.push({{
                        index: index + 1,
                        author: author,
                        text: text,
                        timestamp: timestamp,
                        time_text: timeText,
                        images: images,
                        metrics: metrics
                    }});
                }}
            }} catch (e) {{
                console.error('提取失败:', e);
            }}
        }});

        result.total_tweets = result.tweets.length;
        return result;
    }}
    '''
)
```

### 7. 过滤：只保留作者的推文（构建 thread）

```python
# 在 Python 中处理
tweets_data = json.loads(extraction_result)
if tweets_data.get('author'):
    author_handle = tweets_data['author'].get('handle', '')
    if author_handle:
        tweets_data['tweets'] = [
            t for t in tweets_data['tweets']
            if t['author']['handle'] == author_handle
        ]
        tweets_data['total_tweets'] = len(tweets_data['tweets'])
```

### 8. 截图每条推文

对每条推文截图（保存到临时目录）：

```python
import os
import tempfile

output_dir = tempfile.mkdtemp(prefix='xtod_')
screenshots_dir = os.path.join(output_dir, 'screenshots')
os.makedirs(screenshots_dir, exist_ok=True)

for i, tweet in enumerate(tweets_data['tweets'], 1):
    # 滚动到推文位置
    scroll_script = f'''
    () => {{
        const articles = document.querySelectorAll('article[data-testid="tweet"]');
        const article = articles[{{i-1}}];
        if (article) {{
            const y = article.getBoundingClientRect().y + window.scrollY;
            window.scrollTo(0, y - 100);
            return true;
        }}
        return false;
    }}
    '''

    mcp__chrome-devtools__evaluate_script(function=scroll_script)

    # 等待 1 秒
    time.sleep(1)

    # 截图
    screenshot_path = os.path.join(screenshots_dir, f'tweet_{{i}}.png')
    mcp__chrome-devtools__take_screenshot(filename=screenshot_path)

    tweet['screenshot'] = screenshot_path
```

### 9. 下载图片

```python
import requests

images_dir = os.path.join(output_dir, 'images')
os.makedirs(images_dir, exist_ok=True)

image_count = 0
for tweet in tweets_data['tweets']:
    tweet_images = []
    for img in tweet.get('images', []):
        image_count += 1
        image_path = os.path.join(images_dir, f'image_{{image_count}}.jpg')
        try:
            response = requests.get(img['url'], timeout=30)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                tweet_images.append(image_path)
        except Exception as e:
            print(f"图片下载失败: {{e}}")
    tweet['downloaded_images'] = tweet_images
```

### 10. 保存元数据并返回

```python
import json

metadata = {{
    'url': '{url}',
    'author': tweets_data.get('author'),
    'total_tweets': tweets_data['total_tweets'],
    'tweets': tweets_data['tweets'],
    'output_dir': output_dir,
    'screenshots_dir': screenshots_dir,
    'images_dir': images_dir
}}

metadata_path = os.path.join(output_dir, 'metadata.json')
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

metadata['metadata_path'] = metadata_path

# 返回结果给主会话
print("\\n===== XTOD_RESULT_START =====")
print(json.dumps(metadata, ensure_ascii=False))
print("===== XTOD_RESULT_END =====\\n")
```

## ⚠️ 重要提示

- **不要返回 browser_snapshot**：会消耗大量 token
- **不要使用 mcp__chrome-devtools__take_snapshot**：改用 take_screenshot
- **只返回 JSON 数据**：通过特殊标记输出
- **处理错误**：如果遇到错误，返回错误信息的 JSON

## 错误处理

如果任何步骤失败，返回错误信息：

```python
error_result = {{
    'success': False,
    'error': '错误描述',
    'url': '{url}'
}}
print("\\n===== XTOD_RESULT_START =====")
print(json.dumps(error_result, ensure_ascii=False))
print("===== XTOD_RESULT_END =====\\n")
```
    '''
)
```

### Step 3: 解析 Agent 返回结果

从 Agent 的返回消息中提取 JSON 数据：

```python
import re
import json

agent_response = task_result  # Agent 的完整返回

# 查找 JSON 数据
match = re.search(r'===== XTOD_RESULT_START =====\n(.*?)\n===== XTOD_RESULT_END =====',
                  agent_response, re.DOTALL)

if match:
    json_str = match.group(1)
    tweets_data = json.loads(json_str)
else:
    # 错误：无法解析
    return "错误：Agent 未返回有效数据"
```

### Step 4: 生成文档

使用主会话中的 Python 工具生成文档：

```python
# 读取 document_generator.py
exec(open('/Users/mac/.claude/skills/xtod/document_generator.py').read())

# 生成文档
output_filename = f"Twitter_{tweets_data['author']['name']}_{{format}}.{{format}}"
output_path = os.path.join(os.getcwd(), output_filename)

generate_document(
    data=tweets_data,
    output_path=output_path,
    format=format
)
```

### Step 5: 返回结果给用户

```python
print(f"✅ Twitter 推文读取完成！")
print(f"📁 文件：{output_path}")
print(f"📝 推文数：{tweets_data['total_tweets']}")
print(f"🖼️  图片数：{len([i for t in tweets_data['tweets'] for i in t.get('downloaded_images', [])])}")
print(f"💾 文件大小：{os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
```

## 上下文控制机制

### 机制 1：Agent 隔离

- ✅ Agent 有独立的 200k token 预算
- ✅ 所有 browser_snapshot 都在 Agent 中
- ✅ 主会话只接收 < 5k 的 JSON

### 机制 2：完整内容保留

- ✅ 读取所有符合用户条件的推文，不限制数量
- ✅ 完整保留推文正文，不截断
- ✅ 保存所有图片和图表的原图（4096x4096 分辨率）
- ✅ 不由模型筛选"关键推文"，严格按用户条件读取

### 机制 3：截图压缩

- 截图保存为文件引用（路径）
- 不在 JSON 中内联图片数据
- 减少数据传输量

## 前提条件

1. **Chrome 必须已启动（远程调试模式）**
   ```bash
   ~/launch-chrome-debug.sh
   ```

2. **Chrome 中必须已登录 Twitter**
   - 访问 https://x.com
   - 确认已登录

3. **检查连接**
   ```python
   # 测试命令
   mcp__chrome-devtools__list_pages()
   ```

## 输出格式

### PDF（默认）
- 封面页（作者、统计信息）
- 每条推文一页（截图 + 文字 + 互动数据）
- 推文图片单独展示
- 中文字体支持

### PPT
- 标题页
- 双栏布局（左侧截图 + 右侧摘要）
- Twitter 配色方案
- 适合演示分享

## 故障排除

### Agent 执行失败

**症状**：Agent 长时间无响应或返回错误

**解决**：
1. 检查 Chrome 是否在远程调试模式
2. 检查推文 URL 是否有效
3. 检查是否需要登录

### JSON 解析失败

**症状**：无法从 Agent 返回中提取数据

**解决**：
1. 检查 Agent 的完整输出
2. 查找 `===== XTOD_RESULT_START =====` 标记
3. 手动提取 JSON 数据

### 文档生成失败

**症状**：截图完成但 PDF/PPT 生成失败

**解决**：
1. 检查截图文件是否存在
2. 检查 Python 库是否安装（reportlab, python-pptx）
3. 检查磁盘空间

## 性能指标

- **主会话 token 消耗**：< 10k tokens
- **Agent token 消耗**：约 50-100k tokens（独立预算）
- **总 token 节省**：约 85%（相比直接在主会话操作）
- **处理速度**：约 2-3 条推文/分钟
- **文件大小**：PDF 约 0.5-1 MB/推文

## 更新日志

**v2.1.0** (2025-11-05)
- ✅ 移除推文数量限制，读取所有符合用户条件的推文
- ✅ 完整保留推文正文内容，不截断
- ✅ 完整保留所有图片和图表
- ✅ 不由模型筛选"关键推文"，严格按用户条件读取

**v2.0.0** (2025-11-05)
- ✅ 使用 Agent 隔离机制
- ✅ 真正的上下文控制
- ✅ 主会话 token < 10k

**v1.0.0** (2025-11-05)
- ✅ 初始版本

## 许可证

MIT License
