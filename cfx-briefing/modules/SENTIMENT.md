# 社区情绪模块

## 职责范围
- 获取 16 个推特账号最近 7 天动态
- 分析情绪倾向 (BULLISH/NEUTRAL/SILENT)
- 提取关键信号和摘要
- 追踪推文历史

## 工作流序列

### 1. 环境准备
读取 `$CFX_PROJECT_DIR/.env` 获取 `XAI_API_KEY`
- 不要用 shell `source .env` / `. .env`。用 Python/Node 解析目标键，且不要打印值。
- 本机 curl 可能受失效代理影响；优先用 Python/urllib 或 Node fetch 清理 `http_proxy`、`https_proxy`、`all_proxy`、`no_proxy` 后访问 xAI。

### 2. Grok API 调用
**⚠️ 必须使用新 API** (旧 `/v1/chat/completions` 已弃用):
- Endpoint: `POST https://api.x.ai/v1/responses`
- Model: `grok-4-1-fast-reasoning`
- 工具: `x_search` (每批最多 10 个账号)
- 先用 `GET https://api.x.ai/v1/models` 预检 key、网络和模型列表。
- 如果 Python/Node `/v1/models` 返回 200，继续 `responses + x_search`；不要因为 curl 的代理/DNS/SSL 错误误判 xAI 不可用。
- 如果 macOS `scutil --proxy` 显示 `127.0.0.1:7890`，`curl` 必须显式加 `-x http://127.0.0.1:7890`；否则 shell 直连可能 DNS/路由超时。
- Prompt 必须包含精确查询 `(from:账号1 OR from:账号2 ...) since:YYYY-MM-DD until:YYYY-MM-DD`，并要求只输出监控账号，防止模型扩展到其他账号。

### 3. 账号分批
**批次 1 (10 个账号)**:
```json
{
  "model": "grok-4-1-fast-reasoning",
  "input": [{
    "role": "user",
    "content": "Use x_search once with this exact query: (from:Conflux_Network OR from:Conflux_Intern OR from:CamillaCaban OR from:CikeinWeb3 OR from:SwappiDEX OR from:OfficialNucleon OR from:dForcenet OR from:BitUnion_Card OR from:Joyzinweb3 OR from:forgivenever) since:YYYY-MM-DD until:YYYY-MM-DD. Classify only these handles as BULLISH/NEUTRAL/BEARISH/SILENT and return compact JSON."
  }],
  "tools": [{
    "type": "x_search",
    "allowed_x_handles": [
      "Conflux_Network",
      "Conflux_Intern",
      "CamillaCaban",
      "CikeinWeb3",
      "SwappiDEX",
      "OfficialNucleon",
      "dForcenet",
      "BitUnion_Card",
      "Joyzinweb3",
      "forgivenever"
    ]
  }]
}
```

**批次 2 (6 个账号)**:
```json
{
  "model": "grok-4-1-fast-reasoning",
  "input": [{
    "role": "user",
    "content": "Use x_search once with this exact query: (from:estherinweb3 OR from:FanLong16 OR from:GuangYang_9 OR from:AnchorX_Ltd OR from:HexbitApp OR from:bxiaokang) since:YYYY-MM-DD until:YYYY-MM-DD. Classify only these handles as BULLISH/NEUTRAL/BEARISH/SILENT and return compact JSON."
  }],
  "tools": [{
    "type": "x_search",
    "allowed_x_handles": [
      "estherinweb3",
      "FanLong16",
      "GuangYang_9",
      "AnchorX_Ltd",
      "HexbitApp",
      "bxiaokang"
    ]
  }]
}
```

### 4. 响应解析
从 `output[].content[].text` 和 `annotations` 提取:
- account (账号名)
- sentiment (BULLISH/NEUTRAL/SILENT)
- summary (摘要,50-100字)
- key_tweets (关键推文ID列表)

### 5. 情绪分类规则

**BULLISH (利好)**:
- 提及技术升级、合作伙伴、交易所上线
- 正面评价生态项目
- 展示增长数据 (TVL、用户数、交易量)
- 牌照进展 (尤其香港稳定币牌照)

**NEUTRAL (中性)**:
- 常规公告、活动预告
- 技术教程、科普内容
- 无明显情绪倾向的转发

**SILENT (沉默)**:
- 7 天内无推文
- 仅转发无评论

## 降级与完整性

- 推特舆情章节必须包含 16 个监控账号逐账号结果：账号、分类、最近动态/采集结果、来源状态。
- 如果 xAI 失败，继续尝试浏览器公共页、web 检索或最近成功缓存；仍失败也要逐账号标注失败原因。
- 不能只输出 BULLISH / NEUTRAL / SILENT 三张 `获取超时` 卡片。

## 输出格式

### 推特舆情章节
```html
<section class="twitter-sentiment">
  <h2>🐦 推特舆情</h2>
  <div class="sentiment-summary">
    <span class="tag tag-green">BULLISH: {数量}</span>
    <span class="tag tag-gray">NEUTRAL: {数量}</span>
    <span class="tag tag-red">SILENT: {数量}</span>
  </div>

  <div class="sentiment-group bullish">
    <h3>📈 利好账号</h3>
    <ul>
      <li>
        <strong>@Conflux_Network</strong>
        <p>{摘要}</p>
      </li>
    </ul>
  </div>

  <div class="sentiment-group neutral">
    <h3>➡️ 中性账号</h3>
    <ul>
      <li>
        <strong>@SwappiDEX</strong>
        <p>{摘要}</p>
      </li>
    </ul>
  </div>

  <div class="sentiment-group silent">
    <h3>🔇 沉默账号</h3>
    <ul>
      <li>@estherinweb3</li>
      <li>@FanLong16</li>
    </ul>
  </div>
</section>
```

## 行为规则

### API 失败处理
- 批次 1 失败 → 尝试批次 2
- 两批次都失败 → 显示"⚠️ 推特数据暂不可用,请稍后重试"
- 不暂停,不询问用户

### 数据质量检查
- 如果所有账号都是 SILENT → 标注"⚠️ 异常:所有账号无发言,可能是 API 问题"
- 如果摘要为空 → 使用"无明显动态"

### 内存写入
完成分析后,追加到 `memory/cfx_tweets.jsonl`:
```jsonl
{"tweet_id": "1234567890", "account": "@Conflux_Network", "timestamp": "2026-03-02T10:30:00Z", "content": "推文内容", "sentiment": "BULLISH", "summary": "宣布与某交易所合作", "engagement": {"likes": 120, "retweets": 45, "replies": 23}}
```

### 信号提取
从推文中提取关键信号:
- 交易所上线 → 标记为"重大利好"
- 技术升级 → 标记为"中期利好"
- 合作伙伴 → 标记为"生态扩展"
- 牌照进展 → 标记为"合规突破"

## 情绪评分算法

```python
bullish_score = (bullish_count * 2 + neutral_count * 1) / total_accounts * 100
```

- 80-100: 强烈看涨
- 60-79: 偏向看涨
- 40-59: 中性
- 20-39: 偏向看跌
- 0-19: 强烈看跌

## 依赖模块
- VOICE.md (写作风格)
- memory/cfx_tweets.jsonl (推文历史)
- memory/cfx_preferences.jsonl (用户偏好)

## 注意事项
- 推文内容可能包含多语言,优先提取中文和英文
- 避免过度解读,保持客观
- 对于模糊信号,标注"需进一步验证"
