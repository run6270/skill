# ConfluxHub 链上治理投票章节 HTML 模板

> **数据源**: https://confluxhub.io/governance/vote/onchain-dao-voting
> **获取方式**: Chrome DevTools MCP 浏览器自动化

## 有进行中投票时

```html
<section id="governance" class="governance-section">
  <h2>🗳️ ConfluxHub 链上治理投票</h2>

  <div class="governance-alert warning">
    <h3>⚠️ Round [轮次] 投票进行中</h3>
    <p><strong>投票期</strong>: [开始日期] ~ [结束日期]</p>
    <p><strong>生效时间</strong>: [日期]（如果通过）</p>
    <p><strong>最低投票权</strong>: [X] 票</p>
  </div>

  <table class="governance-table">
    <thead>
      <tr>
        <th>参数</th>
        <th>当前值</th>
        <th>即将生效</th>
        <th>投票中</th>
        <th>变化</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>PoW 区块奖励</td>
        <td>[X] CFX/Block</td>
        <td>[X] CFX/Block</td>
        <td class="[success/warning/danger]"><strong>[X] CFX/Block</strong></td>
        <td>[⬆️ 上调 / ⬇️ 减半 / ➡️ 不变]</td>
      </tr>
      <tr>
        <td>质押利率</td>
        <td>[X]%</td>
        <td>[X]%</td>
        <td>[X]%</td>
        <td>[⬆️ / ⬇️ / ➡️]</td>
      </tr>
      <tr>
        <td>存储点比例</td>
        <td>[X]%</td>
        <td>[X]%</td>
        <td class="[success/warning]"><strong>[X]%</strong></td>
        <td>[⬆️ / ⬇️ / ➡️]</td>
      </tr>
      <tr>
        <td>基础费用分享</td>
        <td>[X]%</td>
        <td>[X]%</td>
        <td>[X]%</td>
        <td>[⬆️ / ⬇️ / ➡️]</td>
      </tr>
    </tbody>
  </table>

  <div class="impact-analysis">
    <h4>📊 影响分析</h4>
    <ul>
      <li><strong>PoW奖励变化</strong>: [具体数据，如：年产出从 8.4M CFX → 4.2M CFX] - [🟢 利好 / 🔴 利空 / 🟡 中性]</li>
      <li><strong>存储点比例变化</strong>: [具体数据，如：从 63% → 78%] - [影响说明]</li>
      <li><strong>对回本的影响</strong>: [具体分析]</li>
    </ul>
  </div>

  <div class="action-items">
    <h4>🎯 建议行动</h4>
    <ul>
      <li>[具体行动1]</li>
      <li>[具体行动2]</li>
      <li>[具体行动3]</li>
    </ul>
  </div>
</section>
```

## 无进行中投票时

```html
<section id="governance" class="governance-section">
  <h2>🗳️ ConfluxHub 链上治理投票</h2>

  <div class="governance-alert success">
    <h3>✅ 当前无进行中的治理投票</h3>
    <p>最近一轮治理投票已结束，下一轮投票尚未开始。</p>
  </div>

  <div class="governance-history">
    <h4>📜 最近治理历史</h4>
    <table class="governance-table">
      <thead>
        <tr>
          <th>轮次</th>
          <th>时间</th>
          <th>PoW奖励</th>
          <th>利率</th>
          <th>存储点</th>
          <th>结果</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Round 20</td>
          <td>2025-12 ~ 2026-02</td>
          <td>0.80 → 0.40 CFX/Block</td>
          <td>3.26%</td>
          <td>63% → 78%</td>
          <td>⏳ 投票中</td>
        </tr>
        <tr>
          <td>Round 16</td>
          <td>2025-06</td>
          <td>1.60 → 0.80 CFX/Block</td>
          <td>-</td>
          <td>-</td>
          <td>✅ 通过</td>
        </tr>
        <tr>
          <td>Round 14</td>
          <td>2025-02</td>
          <td>1.00 → 1.60 CFX/Block</td>
          <td>-</td>
          <td>-</td>
          <td>✅ 通过</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="governance-info">
    <h4>ℹ️ 治理投票说明</h4>
    <p>Conflux 治理投票每 60 天一轮，用户可通过质押 CFX 获得投票权。主要投票参数包括：</p>
    <ul>
      <li><strong>PoW 区块奖励</strong>: 影响通胀率和矿工卖压</li>
      <li><strong>质押利率</strong>: 影响质押收益</li>
      <li><strong>存储点比例</strong>: 影响存储成本</li>
      <li><strong>基础费用分享比例</strong>: 影响交易成本分配</li>
    </ul>
  </div>
</section>
```

## CSS 样式

```css
.governance-section {
  margin: 20px 0;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.governance-alert {
  padding: 15px;
  margin: 15px 0;
  border-radius: 6px;
  border-left: 4px solid;
}

.governance-alert.warning {
  background: #fff3cd;
  border-color: #ffc107;
  color: #856404;
}

.governance-alert.success {
  background: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.governance-table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
}

.governance-table th,
.governance-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.governance-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.governance-table .danger {
  color: #dc3545;
  font-weight: bold;
}

.governance-table .warning {
  color: #ffc107;
  font-weight: bold;
}

.governance-table .success {
  color: #28a745;
  font-weight: bold;
}

.impact-analysis,
.action-items,
.governance-info {
  margin: 20px 0;
  padding: 15px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.impact-analysis h4,
.action-items h4,
.governance-info h4 {
  margin-top: 0;
  color: #333;
}

.impact-analysis ul,
.action-items ul,
.governance-info ul {
  margin: 10px 0;
  padding-left: 20px;
}

.impact-analysis li,
.action-items li,
.governance-info li {
  margin: 8px 0;
  line-height: 1.6;
}
```
