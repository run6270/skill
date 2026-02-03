# web-to-doc Skill 优化方案

## 1. 工具选择优化

### 当前问题
- Playwright 需要独立浏览器实例，无法使用已登录状态
- 需要启动 Agent，消耗大量 token

### 优化方案：默认使用 Chrome DevTools

**优点**：
1. ✅ 直接连接已登录的 Chrome 浏览器
2. ✅ 不需要 Agent（节省 50%+ token）
3. ✅ 更快速（无需启动新浏览器）
4. ✅ 用户体验更好（利用现有浏览器状态）

**实施步骤**：
```python
# 1. 检查 Chrome DevTools 是否可用
if chrome_devtools_available():
    use_chrome_devtools()
else:
    # 降级到 Playwright
    use_playwright()
```

## 2. Token 消耗优化

### 问题根源
- 浏览器 snapshot 返回大量 DOM 数据（每次 3-5k tokens）
- Agent 执行过程返回所有中间步骤
- 多次重复操作

### 优化方案

#### 方案 A：精简数据提取（推荐）
```python
# 不要获取完整 snapshot，只提取需要的数据
def extract_twitter_thread_data():
    """直接用 JavaScript 提取数据，不返回 DOM"""
    script = """
    () => {
        const tweets = [];
        const articles = document.querySelectorAll('article');

        articles.forEach((article, index) => {
            const text = article.querySelector('[data-testid="tweetText"]')?.innerText || '';
            const images = Array.from(article.querySelectorAll('img[src*="pbs.twimg.com"]'))
                .map(img => img.src);
            const author = article.querySelector('[data-testid="User-Name"]')?.innerText || '';

            tweets.push({
                index: index + 1,
                text: text,
                author: author,
                images: images
            });
        });

        return tweets;
    }
    """

    # 只返回 JSON 数据，不返回整个 DOM
    return browser.evaluate(script)
```

**节省效果**：从 ~5k tokens/次 降到 ~500 tokens/次

#### 方案 B：批量操作
```python
# 一次性下载所有图片
def download_all_images(image_urls):
    """并行下载，不逐个执行"""
    import asyncio
    import aiohttp

    async def download(session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                f.write(await response.read())

    async def download_all():
        async with aiohttp.ClientSession() as session:
            tasks = [download(session, url, f'img_{i}.jpg')
                    for i, url in enumerate(image_urls)]
            await asyncio.gather(*tasks)

    asyncio.run(download_all())
```

**节省效果**：从 N 次浏览器操作降到 1 次提取 + 批量下载

#### 方案 C：避免使用 Agent
```python
# 直接在主会话中使用 Chrome DevTools
# 不要启动 playwright-test-planner agent

# 当前方式（消耗大）：
Task(subagent_type="playwright-test-planner", prompt="...")

# 优化后（直接操作）：
chrome_devtools.navigate(url)
data = chrome_devtools.evaluate(extract_script)
```

**节省效果**：节省 ~50k tokens（Agent overhead）

## 3. 具体优化实施

### 优化后的完整流程

```python
def web_to_pdf_optimized(url, output_format='pdf'):
    """优化后的 web-to-doc 流程"""

    # Step 1: 使用 Chrome DevTools 提取数据（< 2k tokens）
    data = chrome_devtools.evaluate("""
        () => {
            // 提取所有推文数据
            const tweets = extractTweetData();  // 自定义函数
            const images = extractImageUrls();   // 自定义函数
            return { tweets, images };
        }
    """)

    # Step 2: 批量下载图片（< 1k tokens）
    download_images_batch(data.images)

    # Step 3: 生成 PDF（< 1k tokens）
    generate_pdf(data.tweets, images_dir)

    # 总 token 消耗：~4k tokens（节省 95%）
```

### Token 消耗对比

| 操作 | 当前方式 | 优化后 | 节省 |
|------|---------|--------|------|
| 启动 Agent | 2k | 0 | 100% |
| 浏览器操作 | 20k | 2k | 90% |
| 数据提取 | 15k | 1k | 93% |
| 图片下载 | 5k | 1k | 80% |
| PDF 生成 | 1k | 1k | 0% |
| **总计** | **43k** | **5k** | **88%** |

## 4. 实施优先级

### 高优先级（立即实施）
1. ✅ 默认使用 Chrome DevTools 而非 Playwright
2. ✅ 用 JavaScript 直接提取数据，避免返回大量 DOM
3. ✅ 批量下载图片，避免逐个操作

### 中优先级（下个版本）
1. ⏰ 缓存机制：已访问的 URL 不重复抓取
2. ⏰ 增量更新：只下载新图片
3. ⏰ 压缩图片：减少 PDF 大小

### 低优先级（未来考虑）
1. 📋 支持视频下载
2. 📋 支持评论区抓取
3. 📋 支持多线程并行处理

## 5. 用户体验优化

### 进度提示
```python
# 添加清晰的进度提示
print("🔍 正在连接浏览器...")
print("📝 正在提取推文数据...")
print(f"📥 正在下载图片 (1/7)...")
print("📄 正在生成 PDF...")
print("✅ 完成！")
```

### 错误处理
```python
# 更好的错误提示
try:
    data = extract_tweets()
except LoginRequired:
    print("⚠️ 需要登录 X 账户")
    print("💡 请在 Chrome 浏览器中登录 x.com，然后重试")
except NetworkError:
    print("⚠️ 网络连接失败")
    print("💡 请检查网络连接或 VPN 设置")
```

## 6. 兼容性考虑

### 浏览器选择逻辑
```python
def select_browser_tool():
    """智能选择浏览器工具"""

    # 1. 优先使用 Chrome DevTools（如果可用）
    if is_chrome_devtools_available():
        return 'chrome-devtools'

    # 2. 降级到 Playwright（如果 Chrome 未运行）
    elif is_playwright_available():
        return 'playwright'

    # 3. 报错并提示用户
    else:
        raise BrowserNotAvailable(
            "请先打开 Chrome 浏览器，或安装 Playwright"
        )
```

## 7. 测试计划

### 性能测试
- [ ] 测试不同长度的推特串（5条、10条、20条）
- [ ] 测试包含大量图片的场景（10+图片）
- [ ] 测试无图片的纯文本推文
- [ ] 测试 token 消耗是否在预期范围（< 10k）

### 功能测试
- [ ] 测试中文显示是否正常
- [ ] 测试图片是否完整下载
- [ ] 测试 PDF 排版是否美观
- [ ] 测试错误处理是否友好

## 8. 文档更新

需要更新以下文档：
1. `README.md` - 更新使用说明
2. `skill.md` - 更新工作原理
3. 添加性能优化章节
4. 添加故障排除指南

## 总结

通过以上优化，预计可以：
- **减少 88% 的 token 消耗**（从 43k 降到 5k）
- **提升 3-5 倍的执行速度**
- **改善用户体验**（利用已登录浏览器）
- **提高稳定性**（减少 Agent 调用）
