# 价格分析模块

## 职责范围
- 获取 CFX 实时价格数据
- 计算浮亏/回本涨幅
- 分析 4 个交易所盘口
- 监控巨鲸持仓变化

## 工作流序列

### 1. 价格数据获取
**数据源优先级**: CoinGecko → DefiLlama → 交易所直连

```bash
# 主数据源
curl -s "https://api.coingecko.com/api/v3/coins/conflux-token?localization=false&tickers=false"

# 备用数据源
curl -s "https://coins.llama.fi/prices/current/coingecko:conflux-token"
```

**提取字段**:
- price (当前价格)
- change_24h (24小时涨跌%)
- change_7d (7天涨跌%)
- market_cap (市值)
- volume_24h (24小时成交量)
- circulating_supply (流通量)

### 2. 成本计算
**用户成本**: $0.26

```python
浮亏% = (current_price - 0.26) / 0.26 * 100
回本涨幅% = (0.26 - current_price) / current_price * 100
```

### 3. 交易所盘口数据
**并行请求 4 个交易所** (任何失败标记"接口受限",不停止):

| 交易所 | API Endpoint |
|--------|--------------|
| Binance | `https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT` |
| OKX | `https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT` |
| Gate | `https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT` |
| MEXC | `https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT` |

**提取字段**:
- name (交易所名称)
- price (价格)
- change_24h (24小时涨跌%)
- volume (24小时成交量)
- status ("ok" 或 "接口受限")

### 4. 巨鲸持仓分析
**数据源**: CoinCarp Rich List

```bash
WebFetch https://www.coincarp.com/currencies/confluxtoken/richlist/
```

**提取数据**:
- Top 10/20/50/100 持仓占比
- 重点监控地址变化:
  - `0xe2fc31f816a9b94326492132018c3aecc4a93ae1` (Binance提币钱包 #22)
  - `0x83da47ab9d850e2352edc200f172dbab39f66d84` (休眠冷存储 #27)

**解读规则**:
- Binance提币钱包减持 = 用户提币到自托管 (看涨信号)
- 冷存储增持 = 聪明钱看好 (看涨信号)
- ⚠️ 对于休眠地址,必须交叉验证链上数据,不可直接引用 CoinCarp 7d Change

## 输出格式

### 价格概览章节
```html
<section class="price-overview">
  <h2>💰 价格概览</h2>
  <div class="metrics">
    <div class="metric">
      <span class="label">当前价格</span>
      <span class="value">${price}</span>
    </div>
    <div class="metric">
      <span class="label">成本价</span>
      <span class="value">$0.26</span>
    </div>
    <div class="metric loss">
      <span class="label">浮亏</span>
      <span class="value">{浮亏%}%</span>
    </div>
    <div class="metric">
      <span class="label">回本涨幅</span>
      <span class="value">{回本涨幅%}%</span>
    </div>
  </div>
</section>
```

### 交易所盘口章节
```html
<section class="exchange-data">
  <h2>📊 交易所盘口</h2>
  <table>
    <thead>
      <tr>
        <th>交易所</th>
        <th>价格</th>
        <th>24H涨跌</th>
        <th>成交量</th>
      </tr>
    </thead>
    <tbody>
      <!-- 对于失败的交易所 -->
      <tr>
        <td>Binance</td>
        <td colspan="3"><span class="tag tag-red">接口受限</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

### 巨鲸持仓章节
```html
<section class="whale-holdings">
  <h2>🐋 巨鲸持仓</h2>
  <div class="distribution">
    <p>Top 10: {占比}% | Top 20: {占比}% | Top 50: {占比}% | Top 100: {占比}%</p>
  </div>
  <div class="tracked-addresses">
    <h3>📌 已识别地址</h3>
    <ul>
      <li>0xe2fc...93ae1 (Binance提币钱包): {变动描述} → {信号解读}</li>
      <li>0x83da...66d84 (休眠冷存储): 持有 4,409,772 bCFX,自 2022-09 起无交易 (⚠️ CoinCarp 7d 变动数据不可靠,以链上记录为准)</li>
    </ul>
  </div>
</section>
```

## 行为规则

### 数据缺失处理
- API 失败 → 标记"接口受限",继续其他数据源
- 巨鲸数据失败 → 显示"⚠️ 数据暂不可用"
- 不暂停,不询问用户

### 数据验证
- 价格异常 (>$1 或 <$0.01) → 标记"数据异常,请人工核实"
- 交易所价差 >5% → 标注"存在套利空间"

### 内存写入
完成分析后,追加到 `memory/cfx_metrics.jsonl`:
```jsonl
{"timestamp": "2026-03-02T12:00:00Z", "price": 0.12, "change_24h": -2.3, "change_7d": 5.1, "market_cap": 450000000, "volume_24h": 12000000, "circulating_supply": 3750000000, "exchange_data": [{"exchange": "Binance", "price": 0.1201, "volume": 5000000, "status": "ok"}]}
```

## 依赖模块
- VOICE.md (写作风格)
- memory/cfx_metrics.jsonl (历史数据)
- memory/cfx_preferences.jsonl (用户偏好)
