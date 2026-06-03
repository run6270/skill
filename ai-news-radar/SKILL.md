---
name: ai-news-radar
description: "Use when working on the locally installed AI News Radar / 伯乐Skill project: running the 24h AI news radar, adding or evaluating RSS/OPML/GitHub/newsletter sources, checking source health, maintaining the static web UI, or preparing GitHub Pages/Actions deployment."
---

# AI News Radar Local Skill

The local project is installed at:

```text
/Users/mac/Documents/GitHub/githubrepo/ai-news-radar
```

Start there before acting:

```bash
cd /Users/mac/Documents/GitHub/githubrepo/ai-news-radar
source .venv/bin/activate
```

Read the project skill first:

```text
/Users/mac/Documents/GitHub/githubrepo/ai-news-radar/skills/ai-news-radar/SKILL.md
```

Default safe local run:

```bash
python scripts/update_news.py --output-dir data --window-hours 24 --archive-days 21 --rss-opml feeds/follow.opml --rss-max-feeds 10
python -m http.server 8080 --bind 127.0.0.1
```

Safety:

- Do not commit `feeds/follow.opml`, private OPML files, secrets, tokens, cookies, or inbox details.
- Keep AgentMail and X API disabled unless the user explicitly provides environment variables or GitHub Secrets.
- Prefer RSS/Atom/OPML and stable public generated feeds before custom scraping.
