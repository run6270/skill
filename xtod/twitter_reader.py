#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter 推文阅读和文档生成工具
专门设计用于复用 Chrome 登录状态，完整读取 Twitter thread
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class TwitterThreadReader:
    """Twitter Thread 读取器 - 使用 Chrome DevTools"""

    # 提取推文数据的 JavaScript
    EXTRACT_TWEETS_SCRIPT = """
    () => {
        const result = {
            author: null,
            total_tweets: 0,
            tweets: [],
            extracted_at: new Date().toISOString()
        };

        // 获取所有 article 元素（每个推文一个）
        const articles = document.querySelectorAll('article[data-testid="tweet"]');

        articles.forEach((article, index) => {
            try {
                // 提取作者信息
                const authorLink = article.querySelector('a[role="link"][href^="/"]');
                const authorName = article.querySelector('[data-testid="User-Name"]');
                const author = {
                    handle: authorLink ? authorLink.getAttribute('href').substring(1) : '',
                    name: authorName ? authorName.textContent.split('\\n')[0] : ''
                };

                // 第一条推文的作者作为线程作者
                if (index === 0) {
                    result.author = author;
                }

                // 提取推文文本
                const tweetText = article.querySelector('[data-testid="tweetText"]');
                const text = tweetText ? tweetText.innerText : '';

                // 提取时间
                const timeElement = article.querySelector('time');
                const timestamp = timeElement ? timeElement.getAttribute('datetime') : '';
                const timeText = timeElement ? timeElement.textContent : '';

                // 提取图片
                const images = [];
                const imageElements = article.querySelectorAll('[data-testid="tweetPhoto"] img');
                imageElements.forEach(img => {
                    if (img.src && img.src.includes('pbs.twimg.com/media')) {
                        // 获取原图 URL
                        const originalUrl = img.src
                            .replace(/\\?.*$/, '')
                            .replace('&name=small', '')
                            .replace('&name=medium', '')
                            .replace('&name=large', '') + '?format=jpg&name=4096x4096';
                        images.push({
                            url: originalUrl,
                            alt: img.alt || ''
                        });
                    }
                });

                // 提取互动数据
                const getMetric = (testid) => {
                    const elem = article.querySelector(`[data-testid="${testid}"]`);
                    if (!elem) return 0;
                    const text = elem.getAttribute('aria-label') || elem.textContent || '';
                    const match = text.match(/([\\d,]+)/);
                    if (!match) return 0;
                    return parseInt(match[1].replace(/,/g, ''), 10);
                };

                const metrics = {
                    replies: getMetric('reply'),
                    retweets: getMetric('retweet'),
                    likes: getMetric('like'),
                    bookmarks: getMetric('bookmark')
                };

                // 检查是否有 "Show more" 按钮
                const showMoreButton = article.querySelector('[data-testid="tweet-text-show-more-link"]');
                const isTruncated = showMoreButton !== null;

                if (text || images.length > 0) {
                    result.tweets.push({
                        index: index + 1,
                        author: author,
                        text: text,
                        is_truncated: isTruncated,
                        timestamp: timestamp,
                        time_text: timeText,
                        images: images,
                        metrics: metrics
                    });
                }
            } catch (e) {
                console.error('提取推文失败:', e);
            }
        });

        result.total_tweets = result.tweets.length;
        return result;
    }
    """

    # 展开 "Show more" 的 JavaScript
    EXPAND_TWEETS_SCRIPT = """
    () => {
        let expanded = 0;
        const buttons = document.querySelectorAll('[data-testid="tweet-text-show-more-link"]');

        buttons.forEach(button => {
            try {
                button.click();
                expanded++;
            } catch (e) {
                console.error('展开失败:', e);
            }
        });

        return {
            total_buttons: buttons.length,
            expanded: expanded,
            message: `展开了 ${expanded} 个折叠的推文`
        };
    }
    """

    # 滚动加载评论区
    SCROLL_TO_LOAD_SCRIPT = """
    (distance) => {
        window.scrollBy(0, distance || 500);
        return {
            scrollY: window.scrollY,
            scrollHeight: document.documentElement.scrollHeight
        };
    }
    """

    def __init__(self, chrome_devtools):
        """
        初始化 Twitter 读取器

        Args:
            chrome_devtools: Chrome DevTools MCP 实例
        """
        self.chrome = chrome_devtools

    def navigate_to_tweet(self, url: str):
        """导航到推文 URL"""
        print(f"🌐 正在访问: {url}")
        self.chrome.navigate_page(url=url, timeout=30000)

    def wait_for_load(self, seconds: int = 3):
        """等待页面加载"""
        import time
        print(f"⏳ 等待页面加载 {seconds} 秒...")
        time.sleep(seconds)

    def expand_all_tweets(self):
        """展开所有折叠的推文"""
        print("📖 正在展开所有折叠的推文...")
        result = self.chrome.evaluate_script(
            function=self.EXPAND_TWEETS_SCRIPT
        )

        result_data = json.loads(result) if isinstance(result, str) else result
        print(f"  ✅ {result_data.get('message', '展开完成')}")
        return result_data

    def scroll_and_load_replies(self, max_scrolls: int = 5):
        """滚动页面加载评论区"""
        print(f"📜 正在滚动加载评论区（最多 {max_scrolls} 次）...")

        for i in range(max_scrolls):
            result = self.chrome.evaluate_script(
                function=self.SCROLL_TO_LOAD_SCRIPT,
                args=[]
            )
            self.wait_for_load(2)
            print(f"  第 {i+1}/{max_scrolls} 次滚动完成")

    def extract_tweets_data(self) -> Dict:
        """提取推文数据"""
        print("📝 正在提取推文数据...")

        result = self.chrome.evaluate_script(
            function=self.EXTRACT_TWEETS_SCRIPT
        )

        data = json.loads(result) if isinstance(result, str) else result
        print(f"✅ 提取完成：共 {data.get('total_tweets', 0)} 条推文")

        return data

    def screenshot_tweet(self, tweet_index: int, output_path: str):
        """截图指定的推文"""
        # 使用 CSS 选择器定位推文
        selector_script = f"""
        () => {{
            const articles = document.querySelectorAll('article[data-testid="tweet"]');
            const article = articles[{tweet_index - 1}];
            if (!article) return null;

            return {{
                x: article.getBoundingClientRect().x,
                y: article.getBoundingClientRect().y + window.scrollY,
                width: article.offsetWidth,
                height: article.offsetHeight
            }};
        }}
        """

        # 获取推文位置
        result = self.chrome.evaluate_script(function=selector_script)
        bounds = json.loads(result) if isinstance(result, str) else result

        if not bounds:
            print(f"  ⚠️ 推文 #{tweet_index} 未找到")
            return False

        # 滚动到推文位置
        scroll_script = f"() => {{ window.scrollTo(0, {bounds['y'] - 100}); }}"
        self.chrome.evaluate_script(function=scroll_script)
        self.wait_for_load(1)

        # 截图
        self.chrome.take_screenshot(filename=output_path)
        print(f"  ✅ 推文 #{tweet_index} 截图完成")
        return True

    def download_image(self, image_url: str, output_path: str):
        """下载图片"""
        try:
            import requests
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"  ⚠️ 图片下载失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ 图片下载错误: {e}")
            return False

    def read_full_thread(
        self,
        url: str,
        output_dir: str,
        expand_replies: bool = True
    ) -> Dict:
        """
        完整读取 Twitter thread

        Args:
            url: Twitter 推文 URL
            output_dir: 输出目录
            expand_replies: 是否展开并读取评论区的作者回复

        Returns:
            包含所有推文数据的字典
        """
        os.makedirs(output_dir, exist_ok=True)
        screenshots_dir = os.path.join(output_dir, 'screenshots')
        images_dir = os.path.join(output_dir, 'images')
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        # 1. 访问 URL
        self.navigate_to_tweet(url)
        self.wait_for_load(3)

        # 2. 展开所有 "Show more"
        self.expand_all_tweets()
        self.wait_for_load(2)

        # 3. 提取主推文数据
        tweets_data = self.extract_tweets_data()

        # 4. 如果需要，滚动加载评论区
        if expand_replies:
            self.scroll_and_load_replies(max_scrolls=5)
            self.wait_for_load(2)

            # 再次展开（评论区可能有新的折叠内容）
            self.expand_all_tweets()
            self.wait_for_load(2)

            # 重新提取（包括评论区的推文）
            tweets_data = self.extract_tweets_data()

        # 5. 过滤：只保留作者的推文（构建 thread）
        if tweets_data.get('author'):
            author_handle = tweets_data['author'].get('handle', '')
            if author_handle:
                original_count = len(tweets_data['tweets'])
                tweets_data['tweets'] = [
                    t for t in tweets_data['tweets']
                    if t['author']['handle'] == author_handle
                ]
                tweets_data['total_tweets'] = len(tweets_data['tweets'])
                filtered_count = original_count - tweets_data['total_tweets']
                if filtered_count > 0:
                    print(f"🔍 过滤后：保留 {tweets_data['total_tweets']} 条作者推文（过滤掉 {filtered_count} 条其他人的推文）")

        # 6. 截图每条推文
        print(f"📸 正在截图 {tweets_data['total_tweets']} 条推文...")
        for i, tweet in enumerate(tweets_data['tweets'], 1):
            screenshot_path = os.path.join(screenshots_dir, f'tweet_{i}.png')
            if self.screenshot_tweet(i, screenshot_path):
                tweet['screenshot'] = screenshot_path

        # 7. 下载所有图片
        print("📥 正在下载推文中的图片...")
        image_count = 0
        for tweet in tweets_data['tweets']:
            tweet_images = []
            for img in tweet.get('images', []):
                image_count += 1
                image_path = os.path.join(images_dir, f'image_{image_count}.jpg')
                if self.download_image(img['url'], image_path):
                    tweet_images.append(image_path)
                    print(f"  ✅ 图片 {image_count} 下载完成")
            tweet['downloaded_images'] = tweet_images

        # 8. 保存元数据
        metadata_path = os.path.join(output_dir, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(tweets_data, f, ensure_ascii=False, indent=2)
        print(f"💾 元数据已保存: {metadata_path}")

        # 9. 返回结果
        result = {
            'url': url,
            'author': tweets_data.get('author'),
            'total_tweets': tweets_data['total_tweets'],
            'tweets': tweets_data['tweets'],
            'output_dir': output_dir,
            'screenshots_dir': screenshots_dir,
            'images_dir': images_dir,
            'metadata_path': metadata_path
        }

        print("\n" + "="*60)
        print("✅ Twitter Thread 读取完成！")
        print(f"📝 推文数：{result['total_tweets']}")
        print(f"🖼️  图片数：{image_count}")
        print(f"📁 输出目录：{output_dir}")
        print("="*60 + "\n")

        return result


def read_twitter_thread(url: str, chrome_devtools, output_dir: Optional[str] = None) -> Dict:
    """
    简化的接口：读取 Twitter thread

    Args:
        url: Twitter 推文 URL
        chrome_devtools: Chrome DevTools MCP 实例
        output_dir: 输出目录（可选，默认当前目录）

    Returns:
        包含推文数据和文件路径的字典
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), 'twitter_output')

    reader = TwitterThreadReader(chrome_devtools)
    return reader.read_full_thread(url, output_dir)
