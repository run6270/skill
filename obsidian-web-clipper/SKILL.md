---
name: obsidian-web-clipper
description: Save a web page into an Obsidian vault. Use when user says “保存到 Obsidian/Obsidian 笔记/剪藏网页/clip to Obsidian/Obsidian web clipper”, or asks to save a URL into a specified Obsidian notebook/folder.
---

# Obsidian Web Clipper

Save a URL into Obsidian as a full Markdown note.

## Default behavior

- Default vault: `/Users/mac/Documents/obsidian-demo`
- Default notebook: `AI笔记`
- If the user only gives a URL and says “保存到 Obsidian / AI笔记 下面”, do not ask for path confirmation.
- Only ask follow-up questions if:
  - the user explicitly asks to save somewhere else
  - the default vault is missing or unreadable
  - the write fails

## Routing rules

1. If the URL is `x.com` or `twitter.com`, do not start with `curl`.
2. Route X links through Playwright first.
3. If local X cookies exist, reuse them automatically.
4. Prefer extracting the article body from the rendered X page, including status pages that expand Article content inline.
5. Save the rendered X cover image as a local Obsidian asset when available.
6. For non-X pages, use the generic HTML -> Markdown flow.

## Notebook rules

- Reuse `AI笔记` by default.
- Normalize whitespace before comparing notebook names. Reuse an existing folder like `AI笔记` instead of creating `AI 笔记`.
- Create the notebook folder only if no normalized match already exists.

## Filename rules

- Default filename: page title.
- If title is empty, use `untitled`.
- If a file already exists, append ` (1)`, ` (2)` and so on.
- If the user asks to keep the original title, do not rename it.

## Images

- For generic pages, download remote images into `_assets/<note-name>/` and rewrite Markdown image paths to local relative paths.
- For X pages, save the rendered cover image locally via Playwright when available.

## Script

Use this script:

- `scripts/clip_url_to_obsidian.sh <url> [vault_abs_path] [notebook_rel_path]`

Notes:

- `vault_abs_path` is optional. If omitted, use `/Users/mac/Documents/obsidian-demo`.
- `notebook_rel_path` is optional. If omitted, use `AI笔记`.
- The script auto-routes X links to the Playwright workflow.
