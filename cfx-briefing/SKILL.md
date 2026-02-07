---
name: cfx-briefing
description: CFX投资简报生成器。输入"CFX"或"CFX --api"生成HTML简报。
context: fork
---

# CFX 投资简报生成器

## 命令

| 命令 | 输出 |
|------|------|
| `CFX` / `CFX --api` | HTML |
| `CFX --md` | Markdown |

## 执行流程（3步，全自动）

> **已验证的API端点** (2026-01-16测试通过)

### Step 1: 并行获取数据（6个请求同时发）⭐ 新增治理投票

**直接执行，不询问确认：**

```bash
# 1. 价格（DefiLlama优先✅，CoinGecko备用✅）
curl -s "https://coins.llama.fi/prices/current/coingecko:conflux-token" || \
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=conflux-token&vs_currencies=usd&include_24hr_change=true"

# 2. TVL（从chains API提取✅）
curl -s "https://api.llama.fi/v2/chains" | python3 -c "import sys,json; data=json.load(sys.stdin); cfx=[c for c in data if c.get('name')=='Conflux']; print(cfx[0]['tvl'] if cfx else 'N/A')"

# 3. 订单簿（含Kraken）
python3 /Users/mac/Documents/GitHub/CFX-DWF行情/scripts/fetch_orderbook.py

# 3b. Kraken CFX数据（新上市交易所）⭐ 2026-02-07新增
# 方案A：MCP浏览器获取
mcp__chrome-devtools__navigate_page → https://www.kraken.com/zh-cn/prices/conflux
mcp__chrome-devtools__take_snapshot
# 提取：24h成交量、买卖比例

# 方案B：WebFetch备用
WebFetch → https://www.kraken.com/prices/conflux
提示词: "Extract CFX 24h trading volume, buy/sell ratio"

# 4. Grok推特（16账号）- 先读取.env获取API Key
cat /Users/mac/Documents/GitHub/CFX-DWF行情/.env  # 获取 XAI_API_KEY
curl -s --http1.1 --max-time 90 "https://api.x.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{"model":"grok-3-latest","search_parameters":{"mode":"on","sources":[{"type":"x"}]},"messages":[{"role":"user","content":"Search Twitter for latest posts (past 7 days) from these 16 Conflux accounts: @Conflux_Network @Conflux_Intern @AnchorX_Ltd @SwappiDEX @dForceNet @OfficialNucleon @ABCpospool @forgivenever @estherinweb3 @FanLong16 @GuangYang_9 @CamillaCaban @CikeinWeb3 @Joyzinweb3 @bxiaokang @David6LIANG8\n\nFor each: date, summary (1 line), sentiment (BULLISH/NEUTRAL/SILENT). Return JSON array."}]}'

# 5. 巨鲸持仓（WebFetch）
WebFetch → https://www.coincarp.com/currencies/confluxtoken/richlist/

# 6. DAO 治理投票 ⭐ 新增
# 方案A（优先）：WebSearch 搜索最新治理提案
WebSearch → "Conflux CFX governance proposal Round voting status 2026"

# 方案B（备用）：Grok 搜索 Twitter 治理讨论
curl -s --http1.1 --max-time 60 "https://api.x.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{"model":"grok-3-latest","search_parameters":{"mode":"on","sources":[{"type":"x"}]},"messages":[{"role":"user","content":"Search Twitter for latest Conflux governance voting proposals and status. Keywords: Conflux governance, CFX voting, DAO proposal, Round 20, PoW reward. Return: proposal content, voting status, deadline, sentiment."}]}'

# 方案C（备用）：WebFetch Conflux Forum
WebFetch → https://forum.conflux.fun/search?q=governance%20voting
```

**治理投票数据提取目标：**
- ✅ 提案轮次（如 Round 20）
- ✅ 提案内容（如 PoW 奖励调整）
- ✅ 投票状态（赞成/反对/中立比例）
- ✅ 投票截止日期
- ✅ 生效日期（如果通过）
- ⚠️ 如无进行中提案，返回"当前无进行中的治理投票"

### Step 2: 获取AxCNH数据（多重备用方案）

> ✅ **新方案：直接RPC查询链上数据（2026-01-19更新）**

**方案A（优先）：RPC直接查询 - 总供应量**
```bash
# 使用Conflux eSpace RPC获取实时总供应量
python3 /Users/mac/Documents/GitHub/CFX-DWF行情/scripts/fetch_axcnh_data.py
# 返回JSON: {"success": true, "total_supply": 36128445.4, "total_supply_formatted": "36,128,445", ...}
```

**方案B（备用）：MCP Chrome DevTools - 持有人数和转移次数**
```
mcp__chrome-devtools__navigate_page → https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e
mcp__chrome-devtools__take_snapshot
# 提取: Holders count, Transfers count
```

**方案C（备用）：WebFetch**
```
WebFetch → https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e
提示词: "Extract: Holders count, Transfers count for AxCNH token"
```

**方案D（降级）：部分数据展示**
- 总供应量：✅ 始终可用（通过RPC）
- 持有人数/转移次数：如果B和C都失败，显示"暂时不可用"
- **不再使用历史数据**，确保总供应量始终是最新的

**提取目标**：
- ✅ 总供应量（必有，通过RPC）
- ⚠️ 持有人数（尽力获取）
- ⚠️ 转移次数（尽力获取）

### Step 3: 生成HTML并打开

**写入前检查：**
- ✅ 16个推特账号都有状态
- ✅ Top10/20/50/100持仓占比
- ✅ 至少3个交易所订单簿
- ✅ 价格+24h变化
- ✅ DAO治理投票状态（必须有，即使是"无进行中提案"）⭐ 新增
- ⚠️ AxCNH数据（可选，失败则标注"暂时不可用"）

**缺失处理规则：**
- 核心数据（价格/订单簿/推特/巨鲸/治理投票）缺失 → 重试对应Step
- DAO治理投票：如搜索无结果，显示"✅ 当前无进行中的治理投票"
- AxCNH数据缺失 → 使用降级文案，不阻塞生成
- 不使用占位符

```bash
Write → /Users/mac/Documents/GitHub/CFX-DWF行情/CFX简报_YYYY-MM-DD.html
open /Users/mac/Documents/GitHub/CFX-DWF行情/CFX简报_YYYY-MM-DD.html
```

## HTML 9章节（⭐ 新增 DAO 治理投票）

1. **价格概览**: 当前价、成本$0.26、浮亏%、回本涨幅%
2. **DAO 治理投票** ⭐ 新增必须章节
   - 当前进行中的治理提案（如 Round 20）
   - 提案内容（如 PoW 奖励调整：0.80 → 1.60 CFX/Block）
   - 投票状态（赞成/反对/中立比例）
   - 投票截止日期和生效日期
   - 对价格的影响分析（利好🟢/利空🔴/中性🟡）
   - 行动建议（投票、发声、仓位调整）
   - 如无进行中提案，显示"当前无进行中的治理投票"
3. **订单簿**: 5交易所数据（Binance、Kraken🆕、Gate、MEXC、OKX）
   - **Kraken**：2026-02-03新上市，必须单独获取数据
   - 展示：价格、24h涨跌、24h成交量、买卖比例
4. **巨鲸持仓**: Top10/20/50/100 + 7日异动
5. **链上数据**: TVL、AxCNH（含降级处理）、账户数
   - AxCNH数据不可用时显示：`⚠️ AxCNH数据暂时不可用（eSpace浏览器访问受限）`
   - 保留章节结构，不影响其他数据展示
6. **推特动态**: 利好/中性/沉默分类
7. **生态激励**: 当前活动
8. **风险警告**: 数据风险提示
9. **操作建议**: 止盈目标

## 计算

```
浮亏% = (price - 0.26) / 0.26 * 100
回本涨幅% = (0.26 - price) / price * 100
```

## 禁止

- ❌ 询问确认
- ❌ 分多次写HTML
- ❌ 跳过推特/巨鲸/治理投票 ⭐ 新增
- ❌ 用占位符
- ❌ 治理投票章节留空（必须显示状态或"无进行中提案"）

## 用户背景

- 成本: $0.26
- 止盈: $0.15-0.18卖30%，$0.22-0.26卖40%，$0.30+卖剩余
