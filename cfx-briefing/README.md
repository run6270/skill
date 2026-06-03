# CFX Briefing Skill - Codex 原生版

本目录是从项目内 `.claude/skills/cfx-briefing/` 迁移出的 Codex skill。迁移后的入口是 `SKILL.md`，执行时走 Codex 工具链，不调用 Claude Code CLI。

## 目录结构

```text
cfx-briefing/
├── SKILL.md
├── modules/
│   ├── PRICE_ANALYSIS.md
│   ├── SENTIMENT.md
│   ├── TECH_UPDATE.md
│   ├── SCRAPLING_FETCHER.md
│   └── VOICE.md
├── memory/
│   ├── cfx_tweets.jsonl
│   ├── cfx_metrics.jsonl
│   ├── cfx_decisions.jsonl
│   ├── cfx_failures.jsonl
│   └── cfx_preferences.jsonl
└── governance_template.md
```

## 执行原则

- 输入 `CFX` / `生成CFX简报` 时触发 `cfx-briefing`。
- 使用 Codex 的 shell、browser/Chrome DevTools、web 检索和本地脚本采集数据。
- 不调用 `/Users/mac/.local/bin/claude`。
- 不使用 Claude-only 的 TeamCreate / TaskCreate / TaskOutput。
- API 失败时自动降级并在报告中标注。

## 数据流

1. 读取项目上下文：`PROJECT_CONTEXT.md`、`TRACKING.md`、`modules/VOICE.md`。
2. 采集价格、盘口、TVL、账户增长、AxCNH、治理、巨鲸、推特/X、新闻。
3. 生成 `reports/daily/CFX简报_YYYY-MM-DD.html` 或 `reports/daily/CFX简报_YYYY-MM-DD.md`。
4. 验证 10 个章节、公式、降级标记和数据来源。
5. 必要时写入 `reports/benchmarks/YYYY-MM-DD.json`。

## 输出章节

1. 价格概览
2. 交易所盘口
3. 治理投票
4. 巨鲸持仓
5. 链上数据
6. 推特舆情
7. 生态项目
8. 重大新闻
9. 综合评估
10. 数据来源

## 维护说明

原始 Claude skill 仍保留在项目 `.claude/skills/cfx-briefing/` 中作为历史参考。修改执行协议时，以本目录 `SKILL.md` 为准。
