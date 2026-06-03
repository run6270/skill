# 数据源和API参考

## 价格数据

### 优先级

| 优先级 | 方法 | 可靠性 |
|--------|------|--------|
| 1 | **WebSearch** | ⭐⭐⭐⭐⭐ |
| 2 | DefiLlama API | ⭐⭐⭐⭐⭐ |
| 3 | CoinCarp | ⭐⭐⭐⭐ |
| 4 | CoinMarketCap | ⭐⭐⭐ |
| 5 | CoinGecko | ⭐⭐ (常403) |

---

## 链上数据

### Core Space API

**账户增长API**：
```bash
curl -s "https://api.confluxscan.org/statistics/account/growth"
```

**返回格式**：
```json
{
  "code": 0,
  "data": {
    "total": 1895,
    "list": [
      {"statTime": "2026-01-04", "count": 0},
      {"statTime": "2026-01-03", "count": 22}
    ]
  }
}
```

> **注意**：`data.total`是数据条数，不是累计账户总数！

### eSpace数据

> **优化**：优先尝试API，MCP作为最后手段

**API端点**（优先使用）：
```bash
# 统计信息
curl -s "https://evm.confluxscan.net/api?module=stats&action=ethsupply"

# 账户列表
curl -s "https://evm.confluxscan.net/api?module=account&action=listaccounts"
```

**MCP回退**（仅API失败时）：
- 首页：https://evm.confluxscan.net/
- Charts页：https://evm.confluxscan.net/charts

---

## TVL数据

### DefiLlama API（推荐）

```bash
curl -s "https://api.llama.fi/v2/chains" | jq '.[] | select(.name=="Conflux")'
```

---

## 订单簿数据

### 交易所列表（2026-02-07更新）

| 交易所 | 状态 | 数据获取方式 |
|--------|------|--------------|
| Binance | ✅ 主导 | API |
| **Kraken** | 🆕 新上市 | MCP/WebFetch |
| Gate.io | ✅ | API |
| MEXC | ✅ | API |
| OKX | ✅ | API |

### Kraken CFX数据获取（2026-02-07新增）

> **重要**：Kraken 于 2026-02-03 上市 CFX，必须单独获取数据

**方案A（优先）：MCP浏览器**
```
mcp__chrome-devtools__navigate_page → https://www.kraken.com/zh-cn/prices/conflux
mcp__chrome-devtools__take_snapshot
```

**提取字段**：
- 24h成交量（如 $23,133,567）
- 买卖比例（如 68% 买入 / 32% 卖出）
- 今日购买量（如 454,445,870 CFX）

**方案B（备用）：WebFetch**
```
WebFetch → https://www.kraken.com/prices/conflux
提示词: "Extract CFX 24h trading volume, buy/sell ratio, price"
```

### Python脚本获取四交易所数据

```python
import requests
from concurrent.futures import ThreadPoolExecutor

def get_binance():
    try:
        spot = requests.get("https://api.binance.com/api/v3/depth?symbol=CFXUSDT&limit=500", timeout=10).json()
        price = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=CFXUSDT", timeout=10).json()["price"])
        futures = requests.get("https://fapi.binance.com/fapi/v1/depth?symbol=CFXUSDT&limit=500", timeout=10).json()
        funding = float(requests.get("https://fapi.binance.com/fapi/v1/fundingRate?symbol=CFXUSDT&limit=1", timeout=10).json()[0]["fundingRate"])
        return {"exchange": "binance", "spot_price": price, "spot_ob": spot, "futures_ob": futures, "funding_rate": funding}
    except: return None

def get_okx():
    try:
        spot = requests.get("https://www.okx.com/api/v5/market/books?instId=CFX-USDT&sz=400", timeout=10).json()
        price = float(requests.get("https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT", timeout=10).json()["data"][0]["last"])
        return {"exchange": "okx", "spot_price": price, "spot_ob": spot["data"][0] if spot.get("data") else None}
    except: return None

def get_gate():
    try:
        ob = requests.get("https://api.gateio.ws/api/v4/spot/order_book?currency_pair=CFX_USDT&limit=100", timeout=10).json()
        price = (float(ob["bids"][0][0]) + float(ob["asks"][0][0])) / 2 if ob.get("bids") else None
        return {"exchange": "gate", "spot_price": price, "spot_ob": ob}
    except: return None

def get_htx():
    try:
        resp = requests.get("https://api.huobi.pro/market/depth?symbol=cfxusdt&type=step0", timeout=10).json()
        tick = resp.get("tick", {})
        price = float(tick.get("bids", [[0]])[0][0])
        return {"exchange": "htx", "spot_price": price, "spot_ob": {"bids": tick.get("bids", []), "asks": tick.get("asks", [])}}
    except: return None

# 并行获取
with ThreadPoolExecutor(max_workers=4) as ex:
    results = list(filter(None, ex.map(lambda f: f(), [get_binance, get_okx, get_gate, get_htx])))
```

### 深度计算

```python
def calculate_depth(orderbook, current_price, depth_percent=10):
    if not orderbook or not current_price: return None, None
    price_range = current_price * depth_percent / 100
    min_p, max_p = current_price - price_range, current_price + price_range
    bid_depth = sum(float(b[0])*float(b[1]) for b in orderbook.get("bids", []) if float(b[0]) >= min_p)
    ask_depth = sum(float(a[0])*float(a[1]) for a in orderbook.get("asks", []) if float(a[0]) <= max_p)
    return bid_depth, ask_depth
```

---

## Grok API调用（2026-02-05更新 - Agent Tools API）

> ⚠️ 旧的 Live Search API (`/v1/chat/completions`) 已于 2026年1月12日弃用

### 配置

| 配置项 | 值 |
|--------|-----|
| **API Key位置** | `.env` 文件中的 `XAI_API_KEY` |
| **Endpoint** | `https://api.x.ai/v1/responses` |
| **模型** | `grok-4-1-fast-reasoning` |
| **搜索工具** | `tools: [{"type": "x_search"}]` |
| **代理** | macOS 系统代理若为 `127.0.0.1:7890`，curl 显式使用 `-x http://127.0.0.1:7890` |

### 调用命令（自动执行）

```bash
# 只加载 API Key，不打印 .env
set -a
. /Users/mac/Documents/GitHub/CFX-DWF行情/.env
set +a

# 预检：先确认 key、模型和网络通路
curl -x http://127.0.0.1:7890 -sS \
  -H "Authorization: Bearer $XAI_API_KEY" \
  https://api.x.ai/v1/models

# 新API调用（分批，每批最多10个账号）
curl -x http://127.0.0.1:7890 -sS -X POST 'https://api.x.ai/v1/responses' \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-4-1-fast-reasoning","input":[{"role":"user","content":"Use x_search once with this exact query: (from:账号1 OR from:账号2) since:YYYY-MM-DD until:YYYY-MM-DD. Classify only these handles and return compact JSON."}],"tools":[{"type":"x_search","allowed_x_handles":["账号1","账号2"]}]}'
```

### 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `allowed_x_handles` | 最多10个 | 超过需分批请求 |
| `from:... OR from:...` | 必填 | 防止 Grok 扩展到非监控账号 |
| 响应字段 | `output[].content[].text` | 文本内容 |
| 注释字段 | `annotations` | 引用来源 |
| Prompt语言 | **英文** | 中文会返回过时数据！ |

---

## AxCNH供应量

> **优化策略**：API优先，MCP延迟加载（基于 Tool Search 思想）

### 优先级1: eSpace API（推荐）

```bash
# Token信息API
curl -s "https://evm.confluxscan.net/api?module=token&action=getToken&contractaddress=0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e"

# Token供应量API
curl -s "https://evm.confluxscan.net/api?module=stats&action=tokensupply&contractaddress=0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e"
```

### 优先级2: MCP延迟加载（仅API失败时）

```
# [DEFERRED_MCP] 仅当上述API均失败时才加载
mcp__chrome-devtools__navigate_page → https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e
mcp__chrome-devtools__take_snapshot
```

**提取字段**：总供应量、持有人数、转移次数

---

## 持仓分布

**CoinCarp Rich List**：
```
https://www.coincarp.com/currencies/confluxtoken/richlist/
```

提取：Top 10/20/50/100 占比

### 重点监控地址（2026-02-13更新）

#### 0xe2fc...93ae1 — Binance Withdrawals 7

| 项目 | 详情 |
|------|------|
| **完整地址** | `0xe2fc31f816a9b94326492132018c3aecc4a93ae1` |
| **身份** | Binance 官方提币热钱包（Etherscan标签: Binance: Withdrawals 7） |
| **CoinCarp排名** | #22 |
| **多链总资产** | ~$191M（跨9条链） |
| **BSC资产** | $3.87M BNB + $12.15M 代币（含 7,057,649 bCFX） |
| **BSC交易数** | 45.5M 笔 |
| **资金来源** | Binance 51（内部调拨钱包） |
| **查询链接** | Etherscan / BSCScan / Blockscan |

**解读规则**：
- 此地址减持CFX = Binance用户提币（看涨：用户转入自托管）
- 此地址增持CFX = 用户充值到Binance（看跌：可能准备卖出）
- 大额变动反映交易所资金流向，是重要的市场情绪指标

#### 0x83da...66d84 — cryptomoonwalker.bnb 冷存储

| 项目 | 详情 |
|------|------|
| **完整地址** | `0x83da47ab9d850e2352edc200f172dbab39f66d84` |
| **身份** | cryptomoonwalker.bnb 控制的冷存储钱包 |
| **CoinCarp排名** | #27 |
| **行为特征** | 纯积累，零卖出，所有资金单向流入 |
| **BSC持仓** | 2021-2022年购入多种代币（长期持有风格） |
| **资金来源** | cryptomoonwalker.bnb 单一来源 |

**解读规则**：
- 持续增持 = 聪明钱看好CFX长期价值
- 首次卖出 = 重大信号，需立即关注
- 增持速度加快 = 可能预期短期利好
