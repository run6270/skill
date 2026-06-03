# 技术更新模块

## 职责范围
- 获取链上数据 (TVL、账户数、AxCNH)
- 获取治理投票数据
- 搜索重大新闻和技术更新
- 分析技术进展对价格的影响

## 工作流序列

### 1. 链上数据获取

#### 1.1 TVL (Total Value Locked)
```bash
curl -s "https://api.llama.fi/v2/chains"
```
提取 `name=="Conflux"` 的 `tvl` 值

#### 1.2 Core Space 账户数
```bash
curl -s "https://api.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
```
提取:
- 最新总账户数
- 日增量

#### 1.3 eSpace 账户数
```bash
curl -s "https://evmapi.confluxscan.io/statistics/account/growth?duration=day&intervalType=day"
```
提取:
- 最新总账户数
- 日增量

#### 1.4 AxCNH 供应量
```bash
WebFetch https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e
```
提取:
- 总供应量
- 持有人数
- 转移次数

### 2. 治理投票数据

**方法 1 (优先): Chrome DevTools MCP**
```javascript
1. mcp__chrome-devtools__navigate_page → https://confluxhub.io/governance/vote/onchain-dao-voting
2. mcp__chrome-devtools__wait_for "Round" (timeout 15000)
3. mcp__chrome-devtools__take_snapshot
4. 解析快照中的投票数据
```

**方法 2 (备用): WebSearch**
```bash
WebSearch "site:confluxhub.io governance vote onchain-dao-voting 2026"
```

**方法 3 (最终备用): 无数据**
```json
{"status": "no_data", "message": "当前无进行中的治理投票"}
```

**提取数据格式**:
```json
{
  "round": 轮次数字,
  "voting_period": {
    "start": "日期",
    "end": "日期"
  },
  "effective_date": "日期",
  "min_votes": 数字,
  "params": [
    {
      "name": "PoW区块奖励",
      "current": "X CFX/Block",
      "pending": "X CFX/Block",
      "voting": "X CFX/Block",
      "change": "减半/不变/上调"
    },
    {
      "name": "质押利率",
      "current": "X%",
      "pending": "X%",
      "voting": "X%",
      "change": "..."
    },
    {
      "name": "存储点比例",
      "current": "X%",
      "pending": "X%",
      "voting": "X%",
      "change": "..."
    },
    {
      "name": "基础费用分享",
      "current": "X%",
      "pending": "X%",
      "voting": "X%",
      "change": "..."
    }
  ]
}
```

### 3. 新闻消息面

**搜索策略**:
```bash
# 搜索 1: 最新新闻
WebSearch "Conflux CFX news {当前月份} {当前年份}"

# 搜索 2: 官方公告
WebSearch "Conflux Network announcement {当前月份} {当前年份}"

# 搜索 3: 合作伙伴
WebSearch "CFX token listing partnership {当前年份}"
```

**分类提取**:
- 交易所上线 (Exchange Listing)
- 技术升级 (Tech Upgrade)
- 合作伙伴 (Partnership)
- 牌照进展 (License Progress) - 尤其香港稳定币牌照
- 生态活动 (Ecosystem Event)

**输出格式**:
```json
[
  {
    "category": "交易所上线",
    "title": "标题",
    "summary": "摘要",
    "date": "日期",
    "source": "来源",
    "impact": "HIGH|MEDIUM|LOW"
  }
]
```

## 输出格式

### 链上数据章节
```html
<section class="onchain-data">
  <h2>⛓️ 链上数据</h2>
  <div class="metrics">
    <div class="metric">
      <span class="label">TVL</span>
      <span class="value">${tvl}M</span>
    </div>
    <div class="metric">
      <span class="label">Core Space 账户</span>
      <span class="value">{total_accounts} (+{daily_new})</span>
    </div>
    <div class="metric">
      <span class="label">eSpace 账户</span>
      <span class="value">{total_accounts} (+{daily_new})</span>
    </div>
    <div class="metric">
      <span class="label">AxCNH 供应量</span>
      <span class="value">{supply} ({holders} 持有人)</span>
    </div>
  </div>
</section>
```

### 治理投票章节
```html
<section class="governance">
  <h2>🗳️ 治理投票</h2>

  <!-- 有投票时 -->
  <div class="voting-info">
    <h3>Round {round} 投票进行中</h3>
    <p>投票期: {start} - {end} | 生效日期: {effective_date}</p>
    <p>最低票数: {min_votes}</p>

    <table>
      <thead>
        <tr>
          <th>参数</th>
          <th>当前值</th>
          <th>待生效</th>
          <th>投票中</th>
          <th>变化</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>PoW区块奖励</td>
          <td>{current}</td>
          <td>{pending}</td>
          <td>{voting}</td>
          <td><span class="tag tag-{color}">{change}</span></td>
        </tr>
      </tbody>
    </table>

    <div class="impact-analysis">
      <h4>影响分析</h4>
      <ul>
        <li>PoW奖励减半 → 通胀率下降 → 长期利好</li>
        <li>质押利率上调 → 吸引更多质押 → 流通量减少</li>
      </ul>
    </div>
  </div>

  <!-- 无投票时 -->
  <p>✅ 当前无进行中的治理投票</p>
</section>
```

### 重大新闻章节
```html
<section class="news">
  <h2>📰 重大新闻</h2>

  <div class="news-category">
    <h3>🏦 交易所上线</h3>
    <ul>
      <li>
        <strong>{title}</strong>
        <p>{summary}</p>
        <span class="date">{date}</span>
        <span class="tag tag-green">HIGH IMPACT</span>
      </li>
    </ul>
  </div>

  <div class="news-category">
    <h3>🔧 技术升级</h3>
    <ul>
      <li>
        <strong>{title}</strong>
        <p>{summary}</p>
        <span class="date">{date}</span>
        <span class="tag tag-blue">MEDIUM IMPACT</span>
      </li>
    </ul>
  </div>

  <div class="news-category">
    <h3>🤝 合作伙伴</h3>
    <ul>
      <li>
        <strong>{title}</strong>
        <p>{summary}</p>
        <span class="date">{date}</span>
      </li>
    </ul>
  </div>

  <div class="news-category">
    <h3>📜 牌照进展</h3>
    <ul>
      <li>
        <strong>{title}</strong>
        <p>{summary}</p>
        <span class="date">{date}</span>
        <span class="tag tag-purple">REGULATORY</span>
      </li>
    </ul>
  </div>
</section>
```

## 行为规则

### 数据缺失处理
- TVL API 失败 → 显示"⚠️ TVL 数据暂不可用"
- 账户数 API 失败 → 显示"⚠️ 账户数据暂不可用"
- AxCNH 数据失败 → 显示"⚠️ AxCNH 数据暂不可用"
- 治理投票无数据 → 显示"✅ 当前无进行中的治理投票"
- 新闻搜索失败 → 显示"⚠️ 新闻数据暂不可用"

### 数据验证
- TVL 异常 (<$10M 或 >$1B) → 标记"数据异常,请人工核实"
- 账户数负增长 → 标注"异常:账户数减少,可能是数据问题"
- AxCNH 供应量异常变化 (>10%) → 标注"供应量大幅变化,需关注"

### 影响分析规则

**治理投票影响**:
- PoW奖励减半 → 通胀率下降 → 长期利好
- 质押利率上调 → 吸引质押 → 流通量减少 → 短期利好
- 存储点比例上调 → 开发者成本增加 → 中性偏空
- 基础费用分享上调 → 质押者收益增加 → 利好

**新闻影响**:
- 交易所上线 → HIGH IMPACT (流动性增加)
- 技术升级 → MEDIUM IMPACT (长期利好)
- 合作伙伴 → MEDIUM IMPACT (生态扩展)
- 牌照进展 → HIGH IMPACT (合规突破)
- 生态活动 → LOW IMPACT (短期关注)

### 内存写入
完成分析后,追加到 `memory/cfx_metrics.jsonl`:
```jsonl
{"timestamp": "2026-03-02T12:00:00Z", "tvl": 450000000, "core_accounts": 1234567, "espace_accounts": 234567, "axcnh_supply": "12345678", "governance_round": 15, "news_count": 3}
```

## 依赖模块
- VOICE.md (写作风格)
- memory/cfx_metrics.jsonl (历史数据)
- memory/cfx_preferences.jsonl (用户偏好)

## 注意事项
- 治理投票数据可能需要多次尝试才能获取
- 新闻搜索结果需要去重和时效性过滤
- 对于模糊信号,标注"需进一步验证"
- 避免过度解读技术更新的短期影响
