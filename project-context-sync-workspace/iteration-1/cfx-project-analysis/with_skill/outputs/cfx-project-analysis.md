# CFX-DWF行情 项目分析报告

## 项目概述

**项目名称**: CFX-DWF行情
**项目类型**: 加密货币投资研究与自动化交易工具
**主要功能**:
- 生成 Conflux (CFX) 代币的每日投资简报
- 自动化套利监控与执行
- 智能交易止盈策略

## 技术栈

### 核心技术
- **编程语言**: Python 3.14
- **脚本语言**: Bash
- **前端展示**: HTML
- **数据格式**: JSON, Markdown

### 关键依赖
- `requests` - HTTP 请求库
- `python-dotenv` - 环境变量管理
- Python 虚拟环境 (venv)

### 集成服务
- **MCP Servers**:
  - Grok API (xAI) - 推特舆情分析
  - Chrome DevTools - 浏览器自动化
- **数据源 API**:
  - CoinGecko API - 价格数据
  - Binance, OKX, Gate.io, MEXC - 交易所数据
  - ConfluxScan API - 链上数据
  - DefiLlama - DeFi 数据
  - CoinCarp - 巨鲸持仓数据

## 项目架构

### 1. CFX 投资简报生成器 (核心功能)

**位置**: `.claude/skills/cfx-briefing/`

**执行模式**: Agent Teams 并行架构
- 使用 7 个独立 Agent 并行采集数据
- 零确认全自动执行
- 输出格式: HTML (默认) 或 Markdown

**数据采集模块**:
1. **价格分析** - CoinGecko + DefiLlama
2. **交易所盘口** - 4 个交易所 API
3. **推特舆情** - Grok API (16 个关键账号)
4. **链上数据** - ConfluxScan (Core Space + eSpace)
5. **治理投票** - ConfluxHub (Chrome DevTools)
6. **巨鲸持仓** - CoinCarp Rich List
7. **新闻消息** - Web Search

**简报内容** (9 个章节):
- 价格概览
- 交易所盘口
- 治理投票
- 巨鲸持仓
- 链上数据
- 推特舆情
- 重大新闻
- 综合评估
- 数据来源

### 2. CFX 套利 Agent

**文件**: `cfx_arbitrage_agent.py`
**配置**: `cfx-arbitrage-config.json`

**功能**:
- 实时监控 CEX 价格差异 (Binance, OKX, Gate.io)
- 自动计算套利机会 (价差、手续费、净利润)
- 支持模拟模式和实盘模式
- 风险控制 (最小价差、最大金额、滑点保护)

**套利逻辑**:
```
净利润 = 价差 - (提币费 + Gas 费 + 交易手续费 × 2)
```

### 3. CFX 智能交易 Agent

**文件**: `cfx_trading_agent.py`
**配置**: `cfx-trading-config.json`

**功能**:
- 自动监控 CFX 价格
- 触发止盈点时自动执行交易
- 支持多级止盈策略

**止盈策略**:
- $0.15-$0.18: 卖出 30% (第一批)
- $0.22-$0.26: 卖出 40% (第二批，回本)
- $0.30+: 卖出剩余 30% (第三批)

### 4. 辅助脚本

**位置**: `scripts/`
- `fetch_orderbook.py` - 订单簿数据获取
- `fetch_axcnh_data.py` - AxCNH 稳定币数据
- `fetch_whale_data.py` - 巨鲸持仓数据

**其他工具**:
- `developer_ranking.py` - 开发者排名分析
- `cfx_orderbook_monitor.py` - 订单簿监控
- `cfx_multi_exchange_monitor.py` - 多交易所监控

## 项目文件结构

```
CFX-DWF行情/
├── .claude/
│   └── skills/
│       ├── cfx-briefing/          # 简报生成 Skill
│       │   ├── SKILL.md           # 主执行逻辑
│       │   ├── @AGENT.md          # Agent 配置
│       │   └── modules/           # 数据采集模块
│       ├── cfx-arbitrage-agent/   # 套利 Agent Skill
│       └── cfx-trading-agent/     # 交易 Agent Skill
├── scripts/                       # 辅助脚本
│   ├── fetch_orderbook.py
│   ├── fetch_axcnh_data.py
│   └── fetch_whale_data.py
├── venv/                          # Python 虚拟环境
├── .env                           # API 密钥配置
├── CLAUDE.md                      # 项目文档 (主)
├── README-arbitrage.md            # 套利 Agent 文档
├── CFX-TRADING-AGENT-README.md    # 交易 Agent 文档
├── cfx_arbitrage_agent.py         # 套利脚本
├── cfx_trading_agent.py           # 交易脚本
├── cfx-arbitrage-config.json      # 套利配置
├── cfx-trading-config.json        # 交易配置
└── CFX简报_YYYY-MM-DD.html        # 输出简报

历史简报文件 (50+ 个):
├── CFX简报_2026-03-03.html
├── CFX简报_2026-02-28.html
└── ... (更多历史简报)
```

## 投资背景

### 用户持仓信息
- **成本价**: $0.26
- **当前状态**: 浮亏
- **投资目标**: 回本并盈利

### 关键催化剂 (按重要性排序)
1. ⭐⭐⭐ **香港稳定币牌照** - 预计 2026年3月首批发放
2. ⭐⭐⭐ **Hexbit × Conflux 合作** - 支付产品、RWA、AxCNH 打通
3. ⭐⭐ **ConfluxHub 治理投票** - Round 21 (PoW温和减产-8.75%、利率翻倍6.52%)
4. ⭐ **山寨季启动** - 比特币周期驱动
5. ⭐ **DWF Labs 做市** - 链上动向监控

## Conflux 技术架构

### 双空间系统
Conflux 使用同一个 CFX 代币，但有两个独立的执行空间:

| 特性 | Core Space | eSpace |
|------|------------|--------|
| **浏览器** | confluxscan.org | evm.confluxscan.net |
| **地址格式** | `cfx:` 开头 | `0x` 开头 (EVM 兼容) |
| **总账户** | ~2500万 | ~111万 (2026-02) |
| **日增账户** | 25-75 | 25-100 |
| **DeFi 生态** | 少 | 主要集中地 |
| **稳定币** | 少 | USDT0/AxCNH |

## 数据源

### 价格与市场
- CoinGecko API: `https://api.coingecko.com/api/v3/coins/conflux-token`
- CoinCarp: `https://www.coincarp.com/currencies/confluxtoken/`
- DefiLlama: `https://defillama.com/chain/Conflux`

### 链上数据
- Core Space: `https://www.confluxscan.org/`
- eSpace: `https://evm.confluxscan.net/`
- ConfluxScan API: `https://api.confluxscan.io/`

### 交易所
- Binance: `https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT`
- OKX: `https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT`
- Gate.io: `https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT`
- MEXC: `https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT`

### 治理与社区
- ConfluxHub: `https://confluxhub.io/governance/vote/onchain-dao-voting`
- Twitter 监控: 16 个关键账号 (官方、团队、生态项目、合作伙伴)

## API 配置

### Grok API (xAI) - 推特舆情分析

**当前版本**: Agent Tools API (2026-02-05)

```bash
# Endpoint
POST https://api.x.ai/v1/responses

# 模型
grok-4-1-fast-reasoning

# 限制
- allowed_x_handles 最多 10 个账号/请求
- 需分 2 批请求获取全部 16 个监控账号
```

**已弃用**:
- ~~`/v1/chat/completions`~~ (2026-01-12 停用)
- ~~`grok-3-latest`~~ 模型

## 快速开始

### 生成 CFX 简报

```bash
# 生成 HTML 简报 (推荐)
CFX

# 生成 Markdown 简报
CFX --md
```

### 运行套利 Agent

```bash
# 运行一次检查
python cfx_arbitrage_agent.py --once

# 循环运行
python cfx_arbitrage_agent.py --loop
```

### 运行交易 Agent

```bash
# 执行一次检查
python cfx_trading_agent.py --once

# 持续监控 (每 60 秒)
python cfx_trading_agent.py
```

## 开发指南

### 修改简报生成逻辑
1. 编辑 Skill 文件: `.claude/skills/cfx-briefing/SKILL.md`
2. 测试执行: `CFX --api`
3. 检查输出: 打开生成的 HTML 文件
4. 调试失败: 查看 Agent 输出日志

### 添加新数据源
在 `SKILL.md` 中添加新 Agent，在 TaskOutput 中收集结果，在 HTML 生成中添加新章节。

### 常见问题

**Q: Agent Teams 执行失败？**
A: 检查 `mode: "bypassPermissions"` 是否设置，确保所有 Agent 在同一个 tool call 中启动

**Q: API 返回 403？**
A: 检查 `.env` 文件中的 API Key，确认 API 配额未超限

**Q: 简报缺少某个章节？**
A: 检查对应 Agent 的输出，可能是数据源失败，需要添加降级逻辑

## 性能优化

- ✅ 使用并行 Agent 而非串行执行
- ✅ 设置合理的超时时间 (120-180秒)
- ✅ 对失败的 API 调用使用降级方案
- ✅ 缓存不常变化的数据 (如治理投票)

## 项目特点

### 1. 自动化程度高
- 零确认全自动执行
- Agent Teams 并行架构
- 自动权限绕过 (bypassPermissions)

### 2. 数据源丰富
- 9 个不同类型的数据源
- 实时价格、链上数据、社交媒体、治理投票
- 多交易所价格对比

### 3. 风险控制完善
- 模拟模式测试
- 多级止盈策略
- 滑点保护
- 手续费计算

### 4. 文档完善
- 详细的 CLAUDE.md 项目文档
- 每个功能模块都有独立 README
- 包含快速开始、配置说明、故障排查

## 技术亮点

### 1. Agent Teams 架构
使用 Claude Code 的 Agent Teams 功能，实现真正的并行数据采集，大幅提升效率。

### 2. 渐进式披露
简报生成采用渐进式披露架构，模块化设计，易于扩展和维护。

### 3. 多模态输出
支持 HTML 和 Markdown 两种输出格式，满足不同场景需求。

### 4. 实时监控
套利和交易 Agent 支持持续监控模式，自动捕捉市场机会。

## 项目状态

### 已完成功能
- ✅ CFX 投资简报生成 (HTML/Markdown)
- ✅ 套利机会监控与分析
- ✅ 智能交易止盈策略
- ✅ 多数据源集成
- ✅ Agent Teams 并行架构

### 待完成功能
- ⏳ OKX API 真实交易集成
- ⏳ 邮件/Webhook 通知
- ⏳ 更多交易所支持
- ⏳ 历史数据分析

## 总结

CFX-DWF行情 是一个功能完善的加密货币投资研究与自动化交易工具，具有以下特点:

1. **技术栈现代**: Python + Bash + HTML，集成多个 API 和 MCP Servers
2. **架构先进**: Agent Teams 并行架构，零确认全自动执行
3. **功能全面**: 投资简报、套利监控、智能交易三大核心功能
4. **数据丰富**: 整合 9 个不同类型的数据源
5. **文档完善**: 详细的项目文档和使用指南
6. **风险可控**: 模拟模式、多级止盈、滑点保护

该项目展示了如何使用 Claude Code 和 Agent Teams 构建复杂的自动化投资研究工具，是一个很好的实践案例。
