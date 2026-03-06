# CFX-DWF行情 项目分析报告

## 项目概览

**项目名称**: CFX-DWF行情 (CFX Investment Briefing System)
**项目类型**: 自动化投资研究与交易工具
**主要功能**: 生成 Conflux (CFX) 代币的每日投资简报，并提供智能交易和套利功能
**项目路径**: `/Users/mac/Documents/GitHub/CFX-DWF行情`

---

## 核心技术栈

### 编程语言
- **Python 3.14**: 核心交易脚本和数据处理
- **Bash**: 自动化部署和执行脚本
- **JavaScript**: 数据处理和报告生成辅助脚本

### 框架与工具
- **Claude Code**: AI 驱动的自动化工作流
- **Agent Teams**: 并行数据采集架构
- **MCP Servers**:
  - Chrome DevTools MCP (浏览器自动化)
  - Grok Agent Tools API (推特舆情分析)

### 数据源集成
- **价格数据**: CoinGecko API, DefiLlama
- **交易所**: Binance, OKX, Gate.io, MEXC
- **链上数据**: ConfluxScan API (Core Space + eSpace)
- **社交媒体**: xAI Grok API (16个关键推特账号)
- **治理数据**: ConfluxHub (Chrome DevTools 自动化)
- **巨鲸数据**: CoinCarp Rich List

### 依赖库
```python
requests          # HTTP 请求
python-dotenv     # 环境变量管理
```

---

## 项目架构

### 1. CFX 投资简报生成器 (核心功能)

**入口**: `.claude/skills/cfx-briefing/SKILL.md`

**执行模式**: Agent Teams 并行架构
- 7个独立 Agent 并行执行数据采集
- 零确认自动化流程
- 输出格式: HTML (默认) 或 Markdown

**工作流程**:
```
用户输入 CFX
    ↓
TeamCreate (创建团队)
    ↓
并行启动 7 个 Agent
    ├─ Agent 1: 价格数据 (CoinGecko)
    ├─ Agent 2: 交易所盘口 (4个交易所)
    ├─ Agent 3: 推特舆情 (Grok API)
    ├─ Agent 4: 链上数据 (ConfluxScan)
    ├─ Agent 5: 治理投票 (ConfluxHub)
    ├─ Agent 6: 巨鲸持仓 (CoinCarp)
    └─ Agent 7: 新闻消息面 (WebSearch)
    ↓
TaskOutput 收集结果
    ↓
生成 HTML 简报 (9个章节)
    ↓
自动打开文件
    ↓
TeamDelete (清理资源)
```

**简报内容 (9个章节)**:
1. 价格概览 - 当前价、浮亏、回本涨幅
2. 交易所盘口 - 4交易所价格对比
3. 治理投票 - ConfluxHub DAO 参数变更
4. 巨鲸持仓 - Top10/20/50/100 占比
5. 链上数据 - TVL、账户数、AxCNH
6. 推特舆情 - 16账号情绪分析
7. 重大新闻 - 交易所、合作、牌照
8. 综合评估 - 利好/风险/操作建议
9. 数据来源 - API 来源列表

### 2. CFX 智能交易 Agent

**文件**: `cfx_trading_agent.py`

**功能**: 自动监控 CFX 价格并执行止盈策略

**止盈策略**:
- $0.15-$0.18: 卖出 30% (第一批止盈)
- $0.22-$0.26: 卖出 40% (第二批止盈，回本)
- $0.30+: 卖出剩余 30% (第三批止盈)

**特性**:
- 实时价格监控 (CoinGecko API)
- 模拟交易模式 (默认)
- 交易记录保存 (`executed_trades.json`)
- OKX DEX API 集成 (待完成)

**使用方式**:
```bash
# 执行一次检查
python cfx_trading_agent.py --once

# 持续监控 (每60秒)
python cfx_trading_agent.py
```

### 3. CFX 套利 Agent

**文件**: `cfx_arbitrage_agent.py`

**功能**: CEX/DEX 价差监控与自动套利

**监控交易所**:
- Binance
- OKX
- Gate.io

**套利逻辑**:
1. 获取所有 CEX 价格
2. 计算最大价差
3. 扣除手续费 (提币费、交易费、Gas费)
4. 判断净利润是否达到阈值
5. 执行套利 (模拟/实盘)

**配置文件**: `cfx-arbitrage-config.json`
```json
{
  "min_spread_percent": 1.5,
  "max_amount_per_trade": 10000,
  "check_interval": 60,
  "dry_run": true
}
```

---

## 项目文件结构

```
CFX-DWF行情/
├── .claude/
│   ├── skills/
│   │   ├── cfx-briefing/          # 简报生成 Skill
│   │   │   ├── SKILL.md           # 主执行逻辑
│   │   │   ├── modules/           # 模块化组件
│   │   │   │   ├── PRICE_ANALYSIS.md
│   │   │   │   ├── SENTIMENT.md
│   │   │   │   ├── TECH_UPDATE.md
│   │   │   │   └── VOICE.md       # 写作风格指南
│   │   │   └── governance_template.md
│   │   ├── cfx-trading-agent/     # 交易 Agent Skill
│   │   └── cfx-arbitrage-agent/   # 套利 Agent Skill
│   └── settings.json              # Claude Code 配置
│
├── scripts/                       # 辅助脚本
│   ├── fetch_orderbook.py
│   └── fetch_axcnh_data.py
│
├── output/                        # 数据输出目录
│   ├── price_data.json
│   ├── twitter_data.json
│   ├── governance_data.json
│   └── ...
│
├── 简报历史/                      # 历史简报存档
│   └── CFX简报_*.md
│
├── cfx_trading_agent.py          # 智能交易脚本
├── cfx_arbitrage_agent.py        # 套利监控脚本
├── cfx-trading-config.json       # 交易配置
├── cfx-arbitrage-config.json     # 套利配置
│
├── deploy-to-openclaw.sh         # 云端部署脚本
├── .env                          # API 密钥 (XAI_API_KEY)
├── CLAUDE.md                     # 项目配置文档
├── CFX-TRADING-AGENT-README.md   # 交易 Agent 文档
├── README-DEPLOY.md              # 部署指南
└── CFX简报_*.html                # 生成的简报文件
```

---

## 关键技术特性

### 1. Agent Teams 并行架构

**优势**:
- 7个 Agent 同时执行，大幅缩短生成时间
- 单个 Agent 失败不影响其他 Agent
- 自动降级处理 (API 失败时使用备用方案)

**实现方式**:
```markdown
Task:
  name: "price-agent"
  subagent_type: "general-purpose"
  team_name: "cfx-briefing"
  mode: "bypassPermissions"  # 零确认自动执行
  prompt: |
    执行价格分析模块...
```

### 2. 零确认自动化

**设计原则**:
- 全程自动，严禁暂停等待用户确认
- API 失败时自动尝试备用方案
- 缺失数据自动标注，不中断流程

**禁止行为**:
- ❌ "是否继续?"
- ❌ "确认后我开始生成"
- ❌ "要试备用方案吗?"

### 3. 模块化设计

**价格分析模块** (`modules/PRICE_ANALYSIS.md`):
- CoinGecko → DefiLlama 降级
- 4个交易所并行查询
- 浮亏/回本涨幅计算

**社区情绪模块** (`modules/SENTIMENT.md`):
- Grok Agent Tools API
- 16个推特账号分2批查询
- BULLISH/NEUTRAL/SILENT 分类

**技术更新模块** (`modules/TECH_UPDATE.md`):
- 链上数据 (TVL、账户数)
- 治理投票 (ConfluxHub)
- 新闻搜索 (交易所、合作、牌照)

**写作风格模块** (`modules/VOICE.md`):
- 统一的语气和风格
- 专业但易懂的表达
- 数据驱动的分析

---

## API 配置

### Grok API (xAI) - 推特舆情分析

**当前版本**: Agent Tools API (2026-02-05)

**Endpoint**: `POST https://api.x.ai/v1/responses`

**请求示例**:
```bash
curl -X POST 'https://api.x.ai/v1/responses' \
  -H 'Authorization: Bearer $XAI_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "grok-4-1-fast-reasoning",
    "input": [{"role": "user", "content": "查询内容"}],
    "tools": [{"type": "x_search", "allowed_x_handles": ["账号1", "账号2"]}]
  }'
```

**限制**:
- `allowed_x_handles` 最多 10 个账号/请求
- 需分 2 批请求获取全部 16 个监控账号

**已弃用**:
- ~~`/v1/chat/completions`~~ (2026-01-12 停用)
- ~~`grok-3-latest`~~ 模型

### 其他 API

**价格数据**:
- CoinGecko: `https://api.coingecko.com/api/v3/coins/conflux-token`
- DefiLlama: `https://defillama.com/chain/Conflux`

**交易所**:
- Binance: `https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT`
- OKX: `https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT`
- Gate.io: `https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT`
- MEXC: `https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT`

**链上数据**:
- Core Space: `https://www.confluxscan.org/`
- eSpace: `https://evm.confluxscan.net/`
- ConfluxScan API: `https://api.confluxscan.io/`

---

## 投资背景

### 用户持仓信息
- **成本价**: $0.26
- **当前状态**: 浮亏
- **投资目标**: 回本并盈利

### 关键催化剂 (按重要性排序)

1. **⭐⭐⭐ 香港稳定币牌照** - 预计 2026年3月首批发放
2. **⭐⭐⭐ Hexbit × Conflux 合作** - 支付产品、RWA、AxCNH 打通
3. **⭐⭐ ConfluxHub 治理投票** - Round 21 (PoW温和减产-8.75%、利率翻倍6.52%)
4. **⭐ 山寨季启动** - 比特币周期驱动
5. **⭐ DWF Labs 做市** - 链上动向监控

### Conflux 双空间架构

| 特性 | Core Space | eSpace |
|------|------------|--------|
| **浏览器** | confluxscan.org | evm.confluxscan.net |
| **地址格式** | `cfx:` 开头 | `0x` 开头 (EVM 兼容) |
| **总账户** | ~2500万 | ~111万 (2026-02) |
| **日增账户** | 25-75 | 25-100 |
| **DeFi 生态** | 少 | 主要集中地 |

---

## 部署方式

### 本地运行

```bash
# 生成 HTML 简报
CFX

# 生成 Markdown 简报
CFX --md

# 运行交易 Agent (模拟模式)
python cfx_trading_agent.py --once

# 运行套利 Agent (模拟模式)
python cfx_arbitrage_agent.py --once
```

### 云端部署 (OpenClaw)

```bash
# 一键部署到云端服务器
./deploy-to-openclaw.sh user@your-cloud-server.com

# 在云端运行
ssh user@your-cloud-server.com 'cd ~/cfx-briefing && ./run-cfx-briefing.sh'

# 设置定时任务 (每天早上9点)
0 9 * * * cd ~/cfx-briefing && ./run-cfx-briefing.sh >> ~/cfx-briefing/cron.log 2>&1
```

---

## 安全机制

### 交易安全
1. ✅ **模拟模式**: 默认不执行真实交易
2. ✅ **价格确认**: 使用 CoinGecko API 获取实时价格
3. ✅ **交易记录**: 所有操作记录到 JSON 文件
4. ✅ **错误处理**: API 失败自动跳过本次检查

### API 密钥管理
- 存储在 `.env` 文件 (不提交到 Git)
- 云端服务器访问控制
- 定期轮换 API 密钥

---

## 项目特色

### 1. 高度自动化
- 零确认执行流程
- 自动降级处理
- 智能错误恢复

### 2. 并行架构
- 7个 Agent 同时执行
- 大幅缩短生成时间
- 单点失败不影响整体

### 3. 模块化设计
- 价格分析、情绪分析、技术更新独立模块
- 易于维护和扩展
- 统一的写作风格

### 4. 多功能集成
- 投资简报生成
- 智能交易执行
- 套利机会监控

### 5. 云端部署支持
- 一键部署脚本
- 定时任务配置
- 远程执行能力

---

## 技术亮点

### Agent Teams 架构
- 使用 Claude Code 的 Agent Teams 功能
- 并行执行 7 个独立任务
- 自动资源管理和清理

### 零确认自动化
- 全程无需用户干预
- 智能降级和错误处理
- 自动生成并打开报告

### 模块化组件
- 独立的分析模块
- 统一的写作风格
- 易于扩展和维护

### 多数据源集成
- 价格、交易所、链上、社交媒体
- 自动降级和备用方案
- 数据验证和清洗

---

## 总结

CFX-DWF行情 是一个功能完整的加密货币投资研究与交易系统，具有以下特点:

**技术栈**: Python + Bash + Claude Code + Agent Teams + MCP Servers

**核心功能**:
1. 自动化投资简报生成 (9个章节，HTML/Markdown)
2. 智能交易执行 (止盈策略，模拟/实盘)
3. 套利机会监控 (CEX价差，自动套利)

**架构特色**:
- Agent Teams 并行架构 (7个独立 Agent)
- 零确认自动化流程
- 模块化设计 (易于维护和扩展)
- 云端部署支持 (OpenClaw)

**数据源**: CoinGecko, Binance, OKX, Gate.io, ConfluxScan, Grok API, ConfluxHub, CoinCarp

**安全机制**: 模拟模式、交易记录、错误处理、API 密钥管理

这是一个设计精良、功能完整、高度自动化的加密货币投资工具，适合需要每日监控 CFX 代币的投资者使用。
