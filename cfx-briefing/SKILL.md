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

## 初始化（首次运行自动执行）

> 每次执行简报前，先检查 `~/.claude/CLAUDE.md` 中是否已记录项目目录。

**检查逻辑：**
1. 读取 `~/.claude/CLAUDE.md`，查找是否包含 `cfx-briefing skill 的项目目录在：`
2. **如果已存在**：直接使用记录的路径作为 `$CFX_PROJECT_DIR`，跳到执行流程
3. **如果不存在**：执行以下初始化步骤

**初始化步骤：**
1. 将当前工作目录写入 `~/.claude/CLAUDE.md`，追加一行：
   ```
   - cfx-briefing skill 的项目目录在：<当前工作目录>
   ```
2. 后续新会话无需再询问目录位置，所有路径基于 `$CFX_PROJECT_DIR` 解析

**路径引用规则：**
- 脚本路径：`$CFX_PROJECT_DIR/scripts/fetch_orderbook.py`
- 模板路径：`$CFX_PROJECT_DIR/templates/cfx_briefing_template.html`
- 输出路径：`$CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html`
- 环境变量：`$CFX_PROJECT_DIR/.env`

## 自动执行权限（全部已配置，无需手动确认）

settings.local.json 已配置以下自动执行规则：
- `WebSearch` / `WebFetch` - 所有网络访问
- `Bash(curl:*)` / `Bash(python3:*)` / `Bash(timeout:*)` - 所有命令
- `mcp__chrome-devtools__*` - 所有浏览器自动化
- `Bash(open:*)` / `Bash(git:*)` - 文件和版本控制

## 执行流程（全自动，零确认）

### Step 1: 并行获取7类数据

**使用 Task 工具并行派发7个 Agent，每个负责一类数据：**

#### Agent 1: 价格数据
```bash
# CoinGecko API（已验证 2026-02-10）
curl -s "https://api.coingecko.com/api/v3/coins/conflux-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
# 提取: current_price, price_change_percentage_24h, price_change_percentage_7d, market_cap, total_volume, circulating_supply
# 写入: /tmp/cfx-price.json
```

#### Agent 2: 订单簿数据（4交易所）
```python
# Python urllib 获取 Binance/OKX/Gate/MEXC ticker + orderbook
# Binance: https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT
#          https://api.binance.com/api/v3/depth?symbol=CFXUSDT&limit=100
# OKX:     https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT
# Gate:    https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT
# MEXC:    https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT
# 写入: /tmp/cfx-orderbook.json
```

#### Agent 3: 推特动态（Grok Agent Tools API）
```bash
# ⚠️ 新API（2026-02-05更新）- 旧 Live Search API 已弃用
# Endpoint: https://api.x.ai/v1/responses
# Model: grok-4-1-fast
# 工具: x_search（最多10个账号/批次，需分2批）

# 批次1（10个）：官方+核心
curl -s -X POST 'https://api.x.ai/v1/responses' \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "获取以下账号过去7天推文，分析利好/利空/中性"}],
    "tools": [{"type": "x_search", "allowed_x_handles": [
      "Conflux_Network","Conflux_Intern","CamillaCaban","CikeinWeb3",
      "SwappiDEX","OfficialNucleon","dForcenet","BitUnion_Card",
      "Joyzinweb3","forgivenever"
    ]}]
  }'

# 批次2（6个）：生态+KOL
# allowed_x_handles: ["estherinweb3","FanLong16","GuangYang_9","AnchorX_Ltd","HexbitApp","bxiaokang"]
# 写入: /tmp/cfx-twitter.json
```

#### Agent 4: 链上数据（ConfluxScan API）
```bash
# Core Space 账户增长（已验证）
curl -s "https://api.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"

# eSpace 账户增长（已验证）
curl -s "https://evmapi.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"

# AxCNH 供应量（RPC查询）
python3 scripts/fetch_axcnh_data.py
# 写入: /tmp/cfx-onchain.json
```

#### Agent 5: 治理投票（Chrome DevTools MCP）
```
mcp__chrome-devtools__navigate_page → https://confluxhub.io/governance/vote/onchain-dao-voting
mcp__chrome-devtools__take_snapshot
# 解析: Round轮次、投票期、4个参数(PoW/利率/存储点/费用分享)的当前值/即将生效/投票中
# 写入: output/governance_data.json
```

#### Agent 6: 持仓分布
```
WebFetch → https://www.coincarp.com/currencies/confluxtoken/richlist/
# 提取: Top10/20/50/100占比、大户异动
```

#### Agent 7: 新闻消息面
```
WebSearch → "Conflux CFX news February 2026"
# 提取: 官方公告、牌照进展、生态活动
```

### Step 2: 组装HTML简报

使用 Python 脚本读取所有数据文件，替换 HTML 模板中的 `{{PLACEHOLDER}}` 变量：

```bash
python3 << 'EOF'
# 读取模板: templates/cfx_briefing_template.html
# 读取数据: /tmp/cfx-price.json, /tmp/cfx-twitter.json, etc.
# 替换所有 {{PLACEHOLDER}}
# 添加治理投票章节（模板中无此章节，需动态插入）
# 写入: output/cfx_briefing_YYYY-MM-DD.html
EOF
```

### Step 3: 打开简报
```bash
open output/cfx_briefing_YYYY-MM-DD.html
```

## HTML 9章节

1. **价格概览**: 当前价、成本$0.26、浮亏%、回本涨幅%
2. **订单簿**: 4交易所(Binance/OKX/Gate/HTX)价格+深度+可视化
3. **持仓分布**: Top10/20/50/100占比 + 大户动向
4. **链上数据**: Core Space + eSpace账户数 + AxCNH供应量
5. **治理投票**: Round轮次、4参数投票状态、影响分析
6. **推特动态**: 利好/利空/中性三栏分类
7. **消息面**: 官方公告、牌照、生态活动
8. **风险警告**: 数据风险提示
9. **汇总统计**: 四所Bid/Ask总深度、TVL、eSpace账户

## 计算公式

```
浮亏% = (price - 0.26) / 0.26 * 100
回本涨幅% = (0.26 - price) / price * 100
Bid/Ask比 = bid_depth / ask_depth
深度条百分比 = bid / (bid + ask) * 100
```

## 禁止

- ❌ 询问确认（所有操作自动执行）
- ❌ 跳过任何章节
- ❌ 用占位符或"暂无数据"
- ❌ 默认输出Markdown（除非 `--md`）
- ❌ 使用旧的 Grok API（`/v1/chat/completions` 已弃用）

## 用户背景

- 成本: $0.26
- 止盈: $0.15-0.18卖30%，$0.22-0.26卖40%，$0.30+卖剩余
