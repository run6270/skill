---
name: cfx-briefing
description: >
  Use this skill when the user wants a CFX/Conflux investment briefing, market
  report,行情分析,投资简报, or multi-source report covering price, exchange data,
  on-chain data, governance, Twitter/X sentiment, whale holdings, and news.
  Trigger on "CFX", "cfx", "CFX --api", "CFX --md", "生成CFX简报",
  "Conflux简报", "今日CFX", and similar requests. This is the Codex-native
  version. Never call Claude Code or /Users/mac/.local/bin/claude.
base_dir_key: cfx-briefing
---

# CFX 投资简报生成器 (Codex 原生版)

## 硬规则

- 不调用 Claude Code CLI。
- 不调用 `/Users/mac/.local/bin/claude`。
- 不使用 Claude-only 的 `TeamCreate`、`TaskCreate`、`TaskOutput`、`TaskUpdate`。
- 全程自动执行；API 失败直接降级，不问用户是否继续。
- 不输出 `.env` 或任何 API Key。
- 生成 HTML 时保留 10 个章节，缺失数据必须明确标注原因。
- 每次日报都必须先做自我质量对标，不等用户提供其它模型报告才发现改进空间。
- 默认质量下限是最近一份已验证合格日报；2026-05-16 起，`reports/daily/CFX简报_2026-05-16.html` 的完整度作为新的最低基线。
- 最终日报不得低于该基线：10 个主章节、独立生态项目章节、16 个 X 账号逐账号表、数据来源状态、benchmark 证据文件、浏览器渲染截图都必须齐全。

## 项目目录定位

优先级：
1. 当前工作目录如果包含 `PROJECT_CONTEXT.md`、`TRACKING.md` 或 `.claude/skills/cfx-briefing`，直接作为 `$CFX_PROJECT_DIR`。
2. 否则读取 `~/.codex/AGENTS.md`，查找 `cfx-briefing skill 的项目目录在：`。
3. 仍找不到时，使用当前工作目录，并在最终报告中说明路径是假定值。

本项目默认目录：

```text
/Users/mac/Documents/GitHub/CFX-DWF行情
```

## 必读文件

按需读取，避免一次性加载全部历史简报：

- `$CFX_PROJECT_DIR/PROJECT_CONTEXT.md`
- `$CFX_PROJECT_DIR/TRACKING.md`
- `$CFX_PROJECT_DIR/.claude/skills/cfx-briefing/modules/VOICE.md`
- `$CFX_PROJECT_DIR/.claude/skills/cfx-briefing/modules/PRICE_ANALYSIS.md`
- `$CFX_PROJECT_DIR/.claude/skills/cfx-briefing/modules/SENTIMENT.md`
- `$CFX_PROJECT_DIR/.claude/skills/cfx-briefing/modules/TECH_UPDATE.md`
- `$CFX_PROJECT_DIR/TRACKING.md` 中的生态激励、AxCNH、BSIM、Hexbit/Conflux 合作跟踪。
- `reference/ecosystem_projects.md`（若在 skill 目录存在）中的生态项目清单。

## 执行流程

### Step 0: 状态热身

在项目目录运行：

```bash
git log --oneline -10
git status --short
date '+%Y-%m-%d %H:%M:%S %Z'
```

只汇报必要状态，不要暴露 `.env`。

### Step 0.5: 质量基线与自我对标

生成前必须读取以下本地基线，不要跳过：

- `/Users/mac/.codex/automations/cfx/memory.md` 的最近 3 条 CFX 日报记录。
- `reports/daily/` 中日期最近、通过验证的 `CFX简报_YYYY-MM-DD.html`。
- 如果存在，读取 `reports/daily/CFX简报_2026-05-16.html` 和 `reports/benchmarks/cfx_briefing_data_2026-05-16.json`，把它们作为最低质量基线。

对标检查必须在心里或临时笔记中覆盖：

- 最新基线是否包含 10 个准确 H2 主章节。
- 是否有独立的「生态项目」章节，而不是把生态内容塞进新闻。
- 是否有 16 个监控账号逐账号表格，而不是三张超时卡片。
- 是否有 ConfluxHub 浏览器渲染快照、原始数据 benchmark、HTML 渲染截图。
- 是否明确区分实时数据、缓存数据、历史基准和接口失败。

如果当天新稿缺少基线中已有的结构、字段或证据文件，先修复再进入最终回复。

### Step 1: 并行采集数据

在 Codex 中用可用工具并行采集独立数据源。能用 `multi_tool_use.parallel` 时优先并行读取 shell/API 输出；需要最新外部消息时必须联网检索并引用来源。

价格：

```bash
curl -s "https://api.coingecko.com/api/v3/coins/conflux-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
curl -s "https://coins.llama.fi/prices/current/coingecko:conflux-token"
```

提取：
- `current_price.usd`
- `price_change_percentage_24h`
- `price_change_percentage_7d`
- `price_change_percentage_30d`
- `market_cap.usd`
- `total_volume.usd`
- `circulating_supply`
- `market_cap_rank`

交易所盘口：

```bash
curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT"
curl -s "https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT"
curl -s "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT"
curl -s "https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT"
python3 "$CFX_PROJECT_DIR/scripts/fetch_orderbook.py"
```

链上：

```bash
curl -s "https://api.llama.fi/v2/chains"
curl -s "https://api.llama.fi/v2/historicalChainTvl/Conflux"
curl -s "https://api.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
curl -s "https://evmapi.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
python3 "$CFX_PROJECT_DIR/scripts/fetch_axcnh_data.py"
```

治理：
- 用 Chrome DevTools / browser-use 打开 `https://confluxhub.io/vote/chain-params/`。
- 等页面渲染完成后取 snapshot。
- 提取 Round、最低投票权、截止时间、PoW Base Reward、Interest Rate、Storage Point Prop、Base Fee Sharing Prop 的 Current / Coming Effective / In voting。
- 如果页面只显示 placeholder，等待 5-10 秒后重试 snapshot。
- 如果仍失败，标注 `治理页面渲染失败`，不要编造。

巨鲸：

```bash
python3 "$CFX_PROJECT_DIR/scripts/fetch_whale_data.py"
```

如果 CoinCarp 解析失败但脚本返回历史缓存，必须在简报中写明 `使用历史基准数据`，不要把缓存当作实时异动。

推特/X 舆情：
- 读取 `$CFX_PROJECT_DIR/.env` 只用于加载 `XAI_API_KEY`，不要打印内容。
- 必须使用 `POST https://api.x.ai/v1/responses`。
- 模型优先 `grok-4-1-fast-reasoning`；如官方模型列表变化，先用 `/v1/models` 确认，再回退到文档示例的 `grok-4.20-reasoning` 或列表中的具体版本名。
- 工具为 `x_search`。
- `allowed_x_handles` 每批最多 10 个账号。
- 本机 shell/curl 可能被失效代理环境影响。优先用 Python/urllib 或 Node fetch 安全解析 `.env` 中的 `XAI_API_KEY`，并在请求 xAI 前清理 `http_proxy`、`https_proxy`、`all_proxy`、`no_proxy`；如果 Python/Node `/v1/models` 返回 200，不要因为 curl 失败把 xAI 误判为不可用。
- macOS 中 `curl` 不一定继承系统代理。调用 xAI 前先执行 `scutil --proxy`；如果 HTTPS/SOCKS 代理指向 `127.0.0.1:7890`，curl 必须显式增加 `-x http://127.0.0.1:7890`。如果直连 `/v1/models` 超时而代理请求成功，不要判定为额度不足。
- 先跑 `/v1/models` 预检：返回 `200` 才继续 `x_search`；如果返回 `401/402/429`，按鉴权/余额/限流处理；如果是 `HTTP_STATUS:000`、`Connection reset`、`Timeout`，优先检查 DNS/代理。
- Prompt 必须要求使用精确查询：`(from:账号1 OR from:账号2 ...) since:YYYY-MM-DD until:YYYY-MM-DD`，并且只输出监控账号，避免 Grok 扩展到非监控账号。
- 两批账号：
  - `Conflux_Network`, `Conflux_Intern`, `CamillaCaban`, `CikeinWeb3`, `SwappiDEX`, `OfficialNucleon`, `dForcenet`, `BitUnion_Card`, `Joyzinweb3`, `forgivenever`
  - `estherinweb3`, `FanLong16`, `GuangYang_9`, `AnchorX_Ltd`, `HexbitApp`, `bxiaokang`
- 如果代理预检和精确查询后 Grok 仍超时或无输出，写 `获取超时`，不要使用旧推文填充。
- 即使 xAI 或 X 页面失败，推特舆情章节也必须保留 16 个监控账号的逐账号表格（账号、分类、最近动态/采集结果、来源状态），不能只输出三张 `获取超时` 汇总卡片。

新闻：
- 联网检索最新 Conflux / CFX 新闻、官方博客、GitHub release。
- 优先官方来源、GitHub release、可信媒体。
- 输出必须带来源链接或在数据来源章节列明。

### Step 2: 生成简报

输出路径：

```text
$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.html
```

可用 Python/TypeScript 组装 HTML，因为这是动态报告产物。不要用 Claude skill 中的 Bash heredoc 分段写入规则；那是 Claude 工具限制，不适用于 Codex。

同时尽量保存结构化证据文件，命名按日期落到 `reports/benchmarks/`：

- `cfx_live_collect_YYYY-MM-DD.json`：可获取的实时 API/网页数据汇总。
- `cfx_briefing_data_YYYY-MM-DD.json`：最终进入报告的规范化数据快照。
- `confluxhub_snapshot_YYYY-MM-DD.txt`：治理页面浏览器渲染快照。
- `xai_twitter_refresh_YYYY-MM-DD.json`：xAI/X 舆情原始响应或失败预检。
- `orderbook_top5_YYYY-MM-DD.json`、`whale_YYYY-MM-DD.json`、`axcnh_YYYY-MM-DD.json`：本地脚本结果。

生成 HTML 后必须用浏览器打开本地文件并保存：

```text
$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.png
$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.snapshot.txt
```

如果截图或 snapshot 工具不可用，必须在最终报告和数据来源章节说明原因；不能把“HTML 已写入”当作完整完成。

Markdown 请求 (`CFX --md`) 时输出：

```text
$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.md
```

## HTML 10 个章节

1. 价格概览：当前价、成本 `$0.26`、浮亏、回本涨幅、24H/7D/30D 涨跌、市值、成交量。
2. 交易所盘口：Binance、OKX、Gate.io、MEXC，失败标注 `接口受限`。
3. 治理投票：Round、截止时间、最低投票权、4 参数 Current / Coming Effective / In voting。
4. 巨鲸持仓：Top10/20/50/100，占比来源，缓存或实时状态说明，重点地址解释。
5. 链上数据：TVL、历史 TVL、Core/eSpace 账户增长、AxCNH。
6. 推特舆情：BULLISH / NEUTRAL / SILENT 汇总，以及 16 个监控账号逐账号分类/状态；接口失败时逐账号标注 `获取超时` 或降级原因。
7. 生态项目：AxCNH、XAUt0、USDT0/Unitus、Swappi、Nucleon、dForce、BitUnion、Hexbit、BSIM 的当前状态、催化强度和风险。
8. 重大新闻：交易所、技术升级、合作、牌照、GitHub release、官方月报。
9. 综合评估：利好因素、风险因素、操作建议。
10. 数据来源：所有 API、网页、脚本、失败/降级状态。

## 计算公式

```text
浮亏% = (price - 0.26) / 0.26 * 100
回本涨幅% = (0.26 - price) / price * 100
```

## 写作风格

遵守 `modules/VOICE.md`：
- 客观、专业、不过度营销。
- 不使用「稳赚不赔」「百分百」「保证」「必然」「绝对」「肯定会」「一定」「确保」「无风险」等保证性词语。
- 价格保留 4-6 位，百分比保留 1 位，大数使用 M/B 或千分位。
- 明确区分实时数据、缓存数据、推断、失败降级。

## 验证

生成后必须运行：

```bash
test -f "$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.html"
rg -n "价格概览|交易所盘口|治理投票|巨鲸|链上数据|推特|生态项目|重大新闻|综合评估|数据来源" "$CFX_PROJECT_DIR/reports/daily/CFX简报_YYYY-MM-DD.html"
```

必须执行质量闸门，任一失败先修 HTML 再重跑：

- H2 主章节必须恰好覆盖 10 节：价格概览、交易所盘口、治理投票、巨鲸持仓、链上数据、推特舆情、生态项目、重大新闻、综合评估、数据来源。
- 价格公式必须按成本 `$0.26` 重新计算：`(price - 0.26) / 0.26` 和 `(0.26 - price) / price`。
- 禁用词扫描必须通过：`稳赚不赔|百分百|保证|必然|绝对|肯定会|一定|确保|无风险`。
- Secret 扫描必须通过：不要出现 `Bearer`、真实 key、`sk-...`、`.env` 内容或 API key 变量值。
- 16 个 X 账号必须全部出现，并带账号、分类、动态/采集结果、来源状态。
- 「生态项目」必须是独立章节，并覆盖 AxCNH、XAUt0、USDT0/Unitus、Swappi、Nucleon、dForce、BitUnion、Hexbit、BSIM。
- 数据来源章节必须列出成功、降级、缓存、历史基准和失败状态，不能只列成功源。
- 本地浏览器渲染、PNG 截图和 snapshot 必须成功；失败时必须写明工具/环境原因。
- `reports/benchmarks/cfx_briefing_data_YYYY-MM-DD.json` 必须存在，并能回溯关键数字。
- 如果今天有任何部分低于最近合格日报或 2026-05-16 基线，先修复，不要直接汇报完成。

如果项目依赖可用，运行：

```bash
npm run test:evaluator
```

运行 evaluator 前先预检 `node_modules/.bin/tsx`、`@anthropic-ai/sdk`、`test-evaluator.ts`、`agents/cfx-briefing-evaluator.ts` 或对应 `.js`。如果评估器失败，先读失败原因；能修就修，不能修就在最终报告中说明。

## 最终报告

最终回复包含：
- 生成的文件路径。
- PNG 截图路径和关键 benchmark 路径。
- 关键数据摘要。
- 降级项和失败项。
- 已运行的验证。
- 明确说明是否达到最近合格日报 / 2026-05-16 基线。
- 不要说调用了 Claude Code；本 skill 禁止调用 Claude Code。
