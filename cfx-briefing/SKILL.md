---
name: cfx-briefing
description: CFX投资简报生成器。输入"CFX"或"CFX --api"生成HTML简报。
context: fork
base_dir_key: cfx-briefing
---

# CFX 投资简报生成器

## 命令

| 命令 | 输出 |
|------|------|
| `CFX` / `CFX --api` | HTML |
| `CFX --md` | Markdown |

## 初始化

1. 读取 `~/.claude/CLAUDE.md`，查找 `cfx-briefing skill 的项目目录在：`
2. **已存在** → 使用该路径作为 `$CFX_PROJECT_DIR`
3. **不存在** → 追加 `- cfx-briefing skill 的项目目录在：<当前工作目录>` 到 `~/.claude/CLAUDE.md`

路径约定：
- 输出：`$CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html`
- 环境变量：`$CFX_PROJECT_DIR/.env`（含 `XAI_API_KEY`）

## 核心规则：零确认 + Agent Teams

**全程自动，严禁暂停等待用户确认。**

禁止：
- "是否继续？" / "确认后我开始生成" / "要试备用方案吗？" / "要打开吗？"

正确做法：一气呵成，用户只看到最终 HTML。

---

## 执行流程（3 步）

### Step 0: 读取环境变量

```
读取 $CFX_PROJECT_DIR/.env → 获取 XAI_API_KEY
```

### Step 1: 创建 Agent Team + 并行派发 7 个 Teammate

**使用 TeamCreate 创建团队，然后用 TaskCreate 创建 7 个任务，最后用 Task 工具并行启动 7 个 Teammate。**

#### 1.1 创建团队

```
TeamCreate:
  team_name: "cfx-briefing"
  description: "CFX 每日投资简报数据采集团队"
```

#### 1.2 创建 7 个任务

用 TaskCreate 一次性创建以下 7 个任务（全部 pending 状态）：

| Task ID | subject | activeForm |
|---------|---------|------------|
| 1 | 获取 CFX 价格数据 | Fetching price data |
| 2 | 获取 4 交易所盘口数据 | Fetching exchange data |
| 3 | 获取推特舆情数据 | Fetching Twitter sentiment |
| 4 | 获取链上数据 | Fetching on-chain data |
| 5 | 获取治理投票数据 | Fetching governance data |
| 6 | 获取巨鲸持仓数据 | Fetching whale holdings |
| 7 | 获取新闻消息面 | Fetching news |

#### 1.3 并行启动 7 个 Teammate

**在一条消息中同时发出 7 个 Task 调用**（不是顺序发，是并行发）：

---

**Teammate 1: price-agent**
```
Task:
  name: "price-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报价格数据采集 Agent。

    任务：获取 CFX 当前价格数据，写入 /tmp/cfx-price.json

    步骤：
    1. curl -s "https://api.coingecko.com/api/v3/coins/conflux-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
    2. 如果 CoinGecko 失败，备用：curl -s "https://coins.llama.fi/prices/current/coingecko:conflux-token"
    3. 提取并写入 /tmp/cfx-price.json：
       {
         "price": 当前价格,
         "change_24h": 24小时涨跌%,
         "change_7d": 7天涨跌%,
         "market_cap": 市值,
         "volume_24h": 24小时成交量,
         "circulating_supply": 流通量
       }

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 2: exchange-agent**
```
Task:
  name: "exchange-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报交易所数据采集 Agent。

    任务：获取 4 个交易所的 CFX/USDT 行情，写入 /tmp/cfx-exchange.json

    并行请求（任何一个失败就标记 "接口受限"，不停）：
    1. Binance: curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT"
    2. OKX: curl -s "https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT"
    3. Gate: curl -s "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT"
    4. MEXC: curl -s "https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT"

    每个交易所提取：{ name, price, change_24h, volume, status: "ok"/"接口受限" }
    写入 /tmp/cfx-exchange.json（数组格式）

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 3: twitter-agent**
```
Task:
  name: "twitter-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报推特舆情采集 Agent。

    任务：用 Grok Agent Tools API 获取 16 个账号最近 7 天推文，写入 /tmp/cfx-twitter.json

    先读取环境变量：读取 $CFX_PROJECT_DIR/.env 获取 XAI_API_KEY（注意：$CFX_PROJECT_DIR 的值从 ~/.claude/CLAUDE.md 中获取）

    ⚠️ 必须使用新 API（旧 /v1/chat/completions 已弃用）：
    - Endpoint: POST https://api.x.ai/v1/responses
    - Model: grok-4-1-fast
    - 工具: x_search（每批最多 10 个账号，必须分 2 批）

    批次 1（10 个）：
    curl -s -X POST 'https://api.x.ai/v1/responses' \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "grok-4-1-fast",
        "input": [{"role": "user", "content": "获取以下Twitter账号过去7天的推文动态，对每个账号分析其内容是利好(BULLISH)、中性(NEUTRAL)还是沉默(SILENT，无发言)，给出每个账号的摘要"}],
        "tools": [{"type": "x_search", "allowed_x_handles": [
          "Conflux_Network","Conflux_Intern","CamillaCaban","CikeinWeb3",
          "SwappiDEX","OfficialNucleon","dForcenet","BitUnion_Card",
          "Joyzinweb3","forgivenever"
        ]}]
      }'

    批次 2（6 个）：
    curl -s -X POST 'https://api.x.ai/v1/responses' \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "grok-4-1-fast",
        "input": [{"role": "user", "content": "获取以下Twitter账号过去7天的推文动态，对每个账号分析其内容是利好(BULLISH)、中性(NEUTRAL)还是沉默(SILENT，无发言)，给出每个账号的摘要"}],
        "tools": [{"type": "x_search", "allowed_x_handles": [
          "estherinweb3","FanLong16","GuangYang_9","AnchorX_Ltd","HexbitApp","bxiaokang"
        ]}]
      }'

    解析两批响应中的 output[].content[].text，合并为：
    [{ "account": "@xxx", "sentiment": "BULLISH/NEUTRAL/SILENT", "summary": "摘要" }, ...]
    写入 /tmp/cfx-twitter.json

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 4: onchain-agent**
```
Task:
  name: "onchain-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报链上数据采集 Agent。

    任务：获取 TVL + 双空间账户数 + AxCNH 供应量，写入 /tmp/cfx-onchain.json

    1. TVL:
       curl -s "https://api.llama.fi/v2/chains"
       提取 name=="Conflux" 的 tvl 值

    2. Core Space 账户:
       curl -s "https://api.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
       提取最新总账户数和日增量

    3. eSpace 账户:
       curl -s "https://evmapi.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
       提取最新总账户数和日增量

    4. AxCNH 供应量:
       WebFetch https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e
       提取: 总供应量、持有人数、转移次数

    写入 /tmp/cfx-onchain.json：
    {
      "tvl": 数值,
      "core_space": { "total_accounts": X, "daily_new": X },
      "espace": { "total_accounts": X, "daily_new": X },
      "axcnh": { "supply": "X", "holders": X, "transfers": X }
    }

    任何 API 失败 → 对应字段写 null，不停。

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 5: governance-agent**
```
Task:
  name: "governance-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报治理投票数据采集 Agent。

    任务：获取 ConfluxHub 链上投票数据，写入 /tmp/cfx-governance.json

    方法 1（优先）：Chrome DevTools MCP
    1. mcp__chrome-devtools__navigate_page → https://confluxhub.io/governance/vote/onchain-dao-voting
    2. mcp__chrome-devtools__wait_for "Round" (timeout 15000)
    3. mcp__chrome-devtools__take_snapshot
    4. 解析快照中的投票数据

    方法 2（备用）：如果方法 1 失败
    WebSearch "site:confluxhub.io governance vote onchain-dao-voting 2026"

    方法 3（最终备用）：如果方法 1 和 2 都失败
    返回 { "status": "no_data", "message": "当前无进行中的治理投票" }

    提取数据格式：
    {
      "round": 轮次数字,
      "voting_period": { "start": "日期", "end": "日期" },
      "effective_date": "日期",
      "min_votes": 数字,
      "params": [
        { "name": "PoW区块奖励", "current": "X CFX/Block", "pending": "X CFX/Block", "voting": "X CFX/Block", "change": "减半/不变/上调" },
        { "name": "质押利率", "current": "X%", "pending": "X%", "voting": "X%", "change": "..." },
        { "name": "存储点比例", "current": "X%", "pending": "X%", "voting": "X%", "change": "..." },
        { "name": "基础费用分享", "current": "X%", "pending": "X%", "voting": "X%", "change": "..." }
      ]
    }

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 6: whale-agent**
```
Task:
  name: "whale-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报巨鲸持仓数据采集 Agent。

    任务：获取 CFX 持仓分布和大户动向，写入 /tmp/cfx-whale.json

    1. WebFetch https://www.coincarp.com/currencies/confluxtoken/richlist/
       提取: Top10/20/50/100 占比

    2. 如果 CoinCarp 失败 → WebSearch "Conflux CFX whale holdings top holders 2026"

    3. 特别关注已识别地址：
       - 0xe2fc31f816a9b94326492132018c3aecc4a93ae1 (Binance提币钱包 #22)
         减持 = 用户提币到自托管（看涨信号）
       - 0x83da47ab9d850e2352edc200f172dbab39f66d84 (冷存储积累者 #27)
         纯积累零卖出，增持 = 聪明钱看好

    写入 /tmp/cfx-whale.json：
    {
      "distribution": { "top10": "X%", "top20": "X%", "top50": "X%", "top100": "X%" },
      "tracked_addresses": [
        { "address": "0xe2fc...", "label": "Binance提币钱包", "change_7d": "描述", "signal": "看涨/看跌/中性" },
        { "address": "0x83da...", "label": "冷存储积累者", "change_7d": "描述", "signal": "看涨/看跌/中性" }
      ]
    }

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

---

**Teammate 7: news-agent**
```
Task:
  name: "news-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"
  prompt: |
    你是 CFX 简报新闻消息面采集 Agent。

    任务：搜索 Conflux/CFX 最新新闻，写入 /tmp/cfx-news.json

    1. WebSearch "Conflux CFX news {当前月份} {当前年份}"
    2. WebSearch "Conflux Network announcement {当前月份} {当前年份}"
    3. WebSearch "CFX token listing partnership {当前年份}"

    分类提取：
    - 交易所上线
    - 技术升级
    - 合作伙伴
    - 牌照进展（尤其香港稳定币牌照）
    - 生态活动

    写入 /tmp/cfx-news.json：
    [{ "category": "分类", "title": "标题", "summary": "摘要", "date": "日期", "source": "来源" }, ...]

    完成后用 TaskUpdate 将任务标记为 completed，并用 SendMessage 将 JSON 结果发送给 team lead。
```

### Step 2: 汇总 + 生成 HTML

**所有 7 个 Teammate 完成后（通过 TaskList 确认全部 completed），Team Lead 立即执行：**

1. 读取 7 个 `/tmp/cfx-*.json` 文件
2. 用 Python 或直接在内存中组装完整的 HTML 简报
3. Write → `$CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html`

**缺失数据自动处理（不问）：**
- API 失败的交易所 → `<span class="tag tag-red">接口受限</span>`
- 推特账号无发言 → 归入 SILENT 分类
- AxCNH 数据失败 → `⚠️ 数据暂不可用`
- 治理投票无数据 → `✅ 当前无进行中的治理投票`

### Step 3: 打开 + 清理团队

```bash
open $CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html
```

然后依次：
1. 向所有 Teammate 发送 `shutdown_request`
2. 等待所有 Teammate 确认 shutdown
3. `TeamDelete` 清理团队资源

**Step 2 → Step 3 之间不暂停。**

---

## HTML 9 章节

1. **价格概览**: 当前价、成本 $0.26、浮亏%、回本涨幅%、24H/7D 涨跌
2. **交易所盘口**: 4 交易所价格+涨跌+成交量（失败的标注"接口受限"）
3. **治理投票**: Round 轮次、参数变更、投票进度、影响分析
4. **巨鲸持仓**: Top10/20/50/100 占比 + 大户异动 + 已识别地址标注
5. **链上数据**: TVL、Core/eSpace 账户数、AxCNH
6. **推特舆情**: BULLISH/NEUTRAL/SILENT 三栏 + 每账号摘要
7. **重大新闻**: 交易所上线、技术升级、合作、牌照
8. **综合评估**: 利好因素 / 风险因素 / 操作建议 三栏
9. **数据来源**: 列出所有 API 来源 + Agent 执行状态

## 计算公式

```
浮亏% = (price - 0.26) / 0.26 * 100
回本涨幅% = (0.26 - price) / price * 100
```

## 禁止

- ❌ 在任何步骤暂停等待用户确认
- ❌ 展示中间数据问"是否继续"
- ❌ API 失败时问"要试备用方案吗"（直接试）
- ❌ 跳过任何章节
- ❌ 用占位符
- ❌ 使用旧 Grok API（`/v1/chat/completions` 已弃用，必须用 `/v1/responses`）
- ❌ 顺序启动 Agent（必须在一条消息中并行启动全部 7 个）

## 重点监控地址（2026-02-13更新）

### 地址 1: Binance Withdrawals 7（交易所提币热钱包）

| 项目 | 详情 |
|------|------|
| **地址** | `0xe2fc31f816a9b94326492132018c3aecc4a93ae1` |
| **身份** | Binance: Withdrawals 7（官方提币热钱包） |
| **CoinCarp排名** | #22 |
| **解读** | 减持 = 用户提币到自托管（看涨信号） |

### 地址 2: cryptomoonwalker.bnb（冷存储积累者）

| 项目 | 详情 |
|------|------|
| **地址** | `0x83da47ab9d850e2352edc200f172dbab39f66d84` |
| **身份** | cryptomoonwalker.bnb 控制的冷存储钱包 |
| **CoinCarp排名** | #27 |
| **解读** | 纯积累零卖出，增持 = 聪明钱看好 |

### 简报输出要求

在巨鲸持仓章节中标注：
```
📌 已识别地址异动：
- 0xe2fc...93ae1 (Binance提币钱包): [变动量] → [看涨/看跌解读]
- 0x83da...66d84 (冷存储积累者): [变动量] → [持续积累/异常卖出]
```

## 用户背景

- 成本: $0.26
- 止盈: $0.15-0.18 卖 30%，$0.22-0.26 卖 40%，$0.30+ 卖剩余
