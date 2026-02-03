# 输出模板参考

## HTML模板

**模板位置**：`/Users/mac/Documents/GitHub/CFX-DWF行情/templates/cfx_briefing_template.html`

### 主要占位符

| 占位符 | 数据 | 示例 |
|--------|------|------|
| `{{DATE}}` | 日期 | 2026-01-02 |
| `{{DATETIME}}` | 日期时间 | 2026-01-03 14:30:45 |
| `{{CURRENT_PRICE}}` | 当前价格 | 0.0754 |
| `{{CHANGE_24H}}` | 24小时涨跌 | +6.02 |
| `{{CHANGE_DIRECTION}}` | 涨跌方向 | up / down |
| `{{CHANGE_ICON}}` | 涨跌图标 | ▲ / ▼ |
| `{{COST_GAP}}` | 距成本差距% | 71.0 |
| `{{BREAKEVEN_GAIN}}` | 回本涨幅% | 244.8 |

### 订单簿占位符

| 占位符 | 数据 |
|--------|------|
| `{{BINANCE_SPOT}}` | 币安现货价 |
| `{{BINANCE_FUTURES}}` | 币安合约价 |
| `{{BINANCE_BID}}` | 币安Bid深度 |
| `{{BINANCE_ASK}}` | 币安Ask深度 |
| `{{BINANCE_RATIO}}` | 币安Bid/Ask比 |
| `{{OKX_*}}` | OKX相关 |
| `{{GATE_*}}` | Gate相关 |
| `{{HTX_*}}` | HTX相关 |
| `{{CROSS_SPREAD}}` | 跨所价差% |
| `{{FUNDING_RATE}}` | 资金费率% |
| `{{TOTAL_BID}}` | 四所合计Bid |
| `{{TOTAL_ASK}}` | 四所合计Ask |

### 链上数据占位符

| 占位符 | 数据 |
|--------|------|
| `{{TVL}}` | Conflux TVL |
| `{{CORE_ACCOUNTS}}` | Core Space总账户数 |
| `{{CORE_DAILY}}` | Core Space今日新增 |
| `{{CORE_WEEKLY}}` | Core Space 7日新增 |
| `{{ESPACE_ACCOUNTS}}` | eSpace总账户数 |
| `{{ESPACE_DAILY}}` | eSpace今日新增 |
| `{{ESPACE_WEEKLY}}` | eSpace 7日新增 |

### 推文占位符

| 占位符 | 数据 |
|--------|------|
| `{{BULLISH_TWEETS}}` | 利好推文HTML |
| `{{BEARISH_TWEETS}}` | 利空推文HTML |
| `{{NEUTRAL_TWEETS}}` | 中性推文HTML |
| `{{NEWS_ITEMS}}` | 消息面列表 |
| `{{PREDICTION_ITEMS}}` | 预测列表 |
| `{{RISK_ITEMS}}` | 风险列表 |

### 推文HTML模板

```html
<div class="tweet">
    <div class="tweet__header">
        <div class="tweet__avatar">C</div>
        <div>
            <div class="tweet__author">账号名称</div>
            <div class="tweet__handle">@handle</div>
        </div>
    </div>
    <div class="tweet__content">推文内容...</div>
    <a href="链接" class="tweet__link" target="_blank">查看原文 →</a>
</div>
```

---

## Markdown输出格式

### 推文分类格式

```markdown
### 一、利好信号 🟢

**账号** @forgivenever（元杰/CSO）
- **时间**：[日期]
- **内容**：[推文内容摘要]
- **链接**：https://x.com/forgivenever/status/xxx
- **影响评估**：🟢 **重大利好** - [分析说明]

### 二、利空/警示信号 🔴

**账号** @账号名（身份）
- **时间**：[日期]
- **内容**：[推文内容摘要]
- **链接**：链接
- **影响评估**：🔴 **警示** - [分析说明]

### 三、中性动态 ⚪

**账号** @Conflux_Network（官方）
- **时间**：[日期]
- **内容**：[推文内容摘要]
- **链接**：链接
- **影响评估**：⚪ **中性** - [分析说明]

### 四、沉默账号警示 ⚠️

| 账号 | 身份 | 最后推文 | 沉默天数 | 风险 |
|------|------|----------|----------|------|
| @FanLong16 | CEO | Feb 14 | 300+天 | ⚠️⚠️⚠️ |
```

### 审计表格格式

```markdown
## 附录：推文阅读审计

| 账号 | 阅读条数 | 最新推文 | 状态 | 活跃度 |
|------|----------|----------|------|--------|
| @Conflux_Network | 10+ | 2025-12-19 | ✅ | ⭐⭐⭐⭐⭐ |
| @FanLong16 | 全部(51) | 2025-02-14 | ✅ | ⚠️沉默 |
```

---

## 保存路径

| 格式 | 路径 |
|------|------|
| HTML | `/Users/mac/Documents/GitHub/CFX-DWF行情/简报/CFX简报_YYYY-MM-DD.html` |
| Markdown | `/Users/mac/Documents/GitHub/CFX-DWF行情/简报历史/CFX简报_YYYY-MM-DD_HHMM.md` |
