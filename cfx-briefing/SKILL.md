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
3. **如果不存在**：将当前工作目录追加到 `~/.claude/CLAUDE.md`：
   ```
   - cfx-briefing skill 的项目目录在：<当前工作目录>
   ```

**路径引用规则：**
- 脚本路径：`$CFX_PROJECT_DIR/scripts/fetch_orderbook.py`
- 输出路径：`$CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html`
- 环境变量：`$CFX_PROJECT_DIR/.env`

## ⚠️ 核心规则：零确认执行

**本 Skill 的所有操作必须全自动执行，严禁在任何环节暂停等待用户确认。**

具体要求：
1. **Task Agent 必须使用 `mode: "bypassPermissions"`** — 所有并行 Agent 自动执行所有工具
2. **不询问"是否继续"** — 数据获取、HTML 生成、文件打开全部自动
3. **不展示中间结果等确认** — 拿到数据直接进入下一步
4. **API 失败自动降级** — 不问用户"要不要试备用方案"，直接试
5. **数据缺失自动标注** — 写"⚠️ 数据暂不可用"，不停下来问

**错误示范（禁止）：**
- "我已获取到价格数据，是否继续获取订单簿？" ❌
- "OKX API 返回 403，要尝试备用方案吗？" ❌
- "以下是 7 个 Agent 的数据，确认后我开始生成 HTML" ❌
- "HTML 已生成，要打开吗？" ❌

**正确做法：** 从头到尾一气呵成，用户只看到最终结果。

## 执行流程（全自动 3 步）

### Step 1: 并行获取 7 类数据

**同时启动 7 个 Task Agent（全部 `mode: "bypassPermissions"`），不等一个完成再启动下一个：**

先读取 `$CFX_PROJECT_DIR/.env` 获取 `XAI_API_KEY`，然后并行派发：

#### Agent 1: 价格数据
```bash
curl -s "https://api.coingecko.com/api/v3/coins/conflux-token?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
# 提取: current_price.usd, price_change_percentage_24h, price_change_percentage_7d, market_cap, total_volume
# 备用: curl -s "https://coins.llama.fi/prices/current/coingecko:conflux-token"
```

#### Agent 2: 订单簿（4 交易所，自动跳过失败的）
```bash
# 全部并行请求，任何一个 403/超时 → 标记"接口受限"，不停
curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT"
curl -s "https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT"
curl -s "https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT"
curl -s "https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT"
```

#### Agent 3: 推特舆情（Grok Agent Tools API）
```bash
# ⚠️ 必须用新 API: POST https://api.x.ai/v1/responses
# Model: grok-4-1-fast-reasoning
# 工具: x_search（每批最多 10 个账号）
# 分 2 批：
#   批次1: Conflux_Network, Conflux_Intern, CamillaCaban, CikeinWeb3, SwappiDEX, OfficialNucleon, dForcenet, BitUnion_Card, Joyzinweb3, forgivenever
#   批次2: estherinweb3, FanLong16, GuangYang_9, AnchorX_Ltd, HexbitApp, bxiaokang
# 输出: 每个账号的 sentiment (BULLISH/NEUTRAL/SILENT) + 摘要
```

#### Agent 4: 链上数据
```bash
# TVL
curl -s "https://api.llama.fi/v2/chains" | python3 -c "import sys,json; data=json.load(sys.stdin); cfx=[c for c in data if c.get('name')=='Conflux']; print(json.dumps({'tvl': cfx[0]['tvl'] if cfx else 'N/A'}))"

# Core Space 账户
curl -s "https://api.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"

# eSpace 账户
curl -s "https://evmapi.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"

# AxCNH（如果脚本存在就跑，不存在就跳过）
python3 $CFX_PROJECT_DIR/scripts/fetch_axcnh_data.py 2>/dev/null || echo '{"success":false}'
```

#### Agent 5: 治理投票（Chrome DevTools）
```
mcp__chrome-devtools__navigate_page → https://confluxhub.io/governance/vote/onchain-dao-voting
mcp__chrome-devtools__take_snapshot
# 解析: Round 轮次、投票期、4 个参数的当前值/即将生效/投票中
# 如果页面加载失败 → WebSearch "Conflux governance Round voting 2026" 作为备用
# 如果都失败 → 返回 "当前无进行中的治理投票"
```

#### Agent 6: 巨鲸持仓
```
WebFetch → https://www.coincarp.com/currencies/confluxtoken/richlist/
# 提取: Top10/20/50/100 占比、近期大户异动
# 如果失败 → WebSearch "Conflux CFX whale holdings top holders 2026"
```

#### Agent 7: 新闻消息面
```
WebSearch → "Conflux CFX news February 2026"
# 提取: 交易所上线、技术升级、合作伙伴、牌照进展
```

### Step 2: 生成 HTML（一次性写入）

**所有 Agent 返回后，立即组装 HTML，不展示中间数据等确认。**

缺失数据处理（自动，不问）：
- API 失败的交易所 → 表格中标注 `<span class="tag tag-red">接口受限</span>`
- 推特账号无发言 → 归入"沉默"分类
- AxCNH 数据失败 → 显示 `⚠️ 数据暂不可用`
- 治理投票无数据 → 显示 `✅ 当前无进行中的治理投票`

```bash
Write → $CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html
```

### Step 3: 打开简报

```bash
open $CFX_PROJECT_DIR/CFX简报_YYYY-MM-DD.html
```

**Step 2 和 Step 3 之间不暂停，写完直接打开。**

## HTML 9 章节

1. **价格概览**: 当前价、成本 $0.26、浮亏%、回本涨幅%、24H/7D 涨跌
2. **交易所盘口**: 4 交易所价格+涨跌+成交量（失败的标注"接口受限"）
3. **治理投票**: Round 轮次、参数变更、投票进度、影响分析
4. **巨鲸持仓**: Top10/20/50/100 占比 + 大户异动
5. **链上数据**: TVL、Core/eSpace 账户数、AxCNH
6. **推特舆情**: BULLISH/NEUTRAL/SILENT 三栏 + 每账号摘要
7. **重大新闻**: 交易所上线、技术升级、合作、牌照
8. **综合评估**: 利好因素 / 风险因素 / 操作建议 三栏
9. **数据来源**: 列出所有 API 来源

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

## 重点监控地址（2026-02-13更新）

生成简报时，Agent 6（巨鲸持仓）应特别关注以下已识别地址的变动：

### 地址 1: Binance Withdrawals 7（交易所提币热钱包）

| 项目 | 详情 |
|------|------|
| **地址** | `0xe2fc31f816a9b94326492132018c3aecc4a93ae1` |
| **身份** | Binance: Withdrawals 7（官方提币热钱包） |
| **CoinCarp排名** | #22 |
| **标签来源** | Etherscan 官方标签 |
| **多链资产** | $191M（跨9条链） |
| **BSC资产** | $3.87M BNB + $12.15M 代币 |
| **BSC交易数** | 45.5M 笔 |
| **资金来源** | Binance 51（内部调拨） |
| **BSC持有bCFX** | 7,057,649 bCFX（$362,571） |

**分析要点**：
- 该地址的CFX减持 ≠ 鲸鱼抛售，而是用户从Binance提币（看涨信号）
- 大量提币说明用户将CFX转入自托管钱包，减少交易所抛压
- 监控此地址的7日变化可判断Binance用户的提币/充值趋势

### 地址 2: cryptomoonwalker.bnb（冷存储积累者）

| 项目 | 详情 |
|------|------|
| **地址** | `0x83da47ab9d850e2352edc200f172dbab39f66d84` |
| **身份** | cryptomoonwalker.bnb 控制的冷存储钱包 |
| **CoinCarp排名** | #27 |
| **行为特征** | 纯积累，零卖出 |
| **BSC持仓** | 2021-2022年购入的多种代币（SHIB、DOGE等） |
| **Conflux持仓** | 新近积累，持续增持CFX |
| **资金流向** | 单向：cryptomoonwalker.bnb → 此地址 |

**分析要点**：
- 典型的长期持有者行为，所有资金只进不出
- BSC上的持仓模式显示该用户偏好在低位积累并长期持有
- 持续增持CFX说明对项目有长期信心
- 监控此地址的增持速度可判断聪明钱的态度

### 简报输出要求

在巨鲸持仓章节中，如果上述地址出现在7日变动排行中，应特别标注：

```
📌 已识别地址异动：
- 0xe2fc...93ae1 (Binance提币钱包): [变动量] → [看涨/看跌解读]
- 0x83da...66d84 (冷存储积累者): [变动量] → [持续积累/异常卖出]
```

## 用户背景

- 成本: $0.26
- 止盈: $0.15-0.18 卖 30%，$0.22-0.26 卖 40%，$0.30+ 卖剩余

