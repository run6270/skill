---
name: getmedia
description: Extracts video and audio download links (magnet, direct download, thunder, ed2k, m3u8, etc.) from URLs. This skill should be used when the user provides a URL and wants to find downloadable media links from that page, such as movie download sites, music sites, or video platforms.
---

# GetMedia

Extract video and audio download links from web pages, including magnet links, direct download URLs, thunder links, and other media formats.

## Supported Link Types

| Type | Pattern | Common Sources |
|------|---------|----------------|
| Magnet | `magnet:?xt=urn:btih:...` | 电影天堂, BT站点 |
| Direct Download | `.mp4`, `.mkv`, `.avi`, `.mp3`, `.flac` | 各类资源站 |
| Thunder/迅雷 | `thunder://...` | 国内资源站 |
| ED2K | `ed2k://...` | 电驴资源 |
| M3U8 Stream | `.m3u8` | 视频流媒体 |
| Baidu Pan | `pan.baidu.com/s/...` | 百度网盘分享 |
| Aliyun Pan | `aliyundrive.com/s/...` | 阿里云盘分享 |

## Workflow

1. Receive URL from user
2. Fetch the webpage using WebFetch with the extraction prompt
3. Parse and organize all found media links
4. Present links in a clean, organized format with usage instructions

## WebFetch Prompt

When fetching the URL, use this prompt:

```
查找页面中所有的下载链接，包括：
1. 磁力链接 (magnet:开头)
2. 直接下载链接 (.mp4, .mkv, .avi, .mp3, .flac, .wav, .aac等)
3. 迅雷链接 (thunder://开头)
4. ED2K链接 (ed2k://开头)
5. 百度网盘链接 (pan.baidu.com)
6. 阿里云盘链接 (aliyundrive.com)
7. M3U8流媒体链接 (.m3u8)
8. 其他下载链接

提取完整的链接地址，并说明每个链接对应的资源名称和格式。
```

## Output Format

Present extracted links as follows:

```markdown
**资源名称**: [从页面提取的标题]

| 类型 | 链接 |
|------|------|
| [链接类型] | `[完整链接]` |

**下载建议**: [根据链接类型给出下载工具建议]
```

## Download Tool Recommendations

| Link Type | Recommended Tools |
|-----------|-------------------|
| Magnet | qBittorrent, Transmission, BitComet |
| Thunder | 迅雷 |
| ED2K | eMule, 迅雷 |
| Direct | wget, curl, IDM, 浏览器 |
| M3U8 | ffmpeg, N_m3u8DL-RE |
| Baidu Pan | 百度网盘客户端 |
| Aliyun Pan | 阿里云盘客户端 |

## Error Handling

- **No links found**: Report "未找到下载链接" and suggest checking if the page requires login or has anti-scraping protection
- **Page inaccessible**: Report the error and suggest the user try again or provide an alternative URL
- **Multiple formats**: List all options and indicate the best quality version
