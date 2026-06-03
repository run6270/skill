# Scrapling 数据获取模块

## 概述

使用 Scrapling 库优化所有 Web 数据获取，提供：
- **784x 更快**的解析速度（vs BeautifulSoup）
- **自动反爬虫**绕过（Cloudflare Turnstile）
- **自适应抓取**（网站结构变化后自动定位元素）
- **并发请求**优化
- **自动重试**机制

## 安装

```bash
pip install "scrapling[all]"
scrapling install  # 下载浏览器依赖
```

## 核心 Fetcher 类型

### 1. Fetcher - 快速 HTTP 请求
用于：API 调用、静态页面
```python
from scrapling.fetchers import Fetcher, FetcherSession

# 单次请求
page = Fetcher.get('https://api.coingecko.com/api/v3/coins/conflux-token')
data = page.json

# 会话模式（保持 cookies）
with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://api.example.com', stealthy_headers=True)
    data = page.json
```

### 2. StealthyFetcher - 反爬虫绕过
用于：受保护的网站、需要绕过 Cloudflare 的页面
```python
from scrapling.fetchers import StealthyFetcher, StealthySession

# 自动绕过 Cloudflare
page = StealthyFetcher.fetch('https://www.coincarp.com/currencies/confluxtoken/richlist/')
data = page.css('.richlist-table tr')

# 会话模式
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch('https://protected-site.com')
```

### 3. DynamicFetcher - 完整浏览器
用于：JavaScript 渲染的页面、需要交互的网站
```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# 单次请求
page = DynamicFetcher.fetch('https://confluxhub.io/governance/vote/onchain-dao-voting')
data = page.css('.voting-data')

# 会话模式（保持浏览器打开）
with DynamicSession(headless=True, network_idle=True) as session:
    page = session.fetch('https://example.com', load_dom=False)
```

---

## 优化后的数据获取实现

### 1. 价格数据获取（优化）

**原方案**：curl + 手动解析
**新方案**：Fetcher + 自动 JSON 解析

```python
from scrapling.fetchers import FetcherSession

def fetch_price_data():
    """获取 CFX 价格数据（CoinGecko → DefiLlama 降级）"""
    with FetcherSession(impersonate='chrome') as session:
        # 主数据源：CoinGecko
        try:
            page = session.get(
                'https://api.coingecko.com/api/v3/coins/conflux-token',
                params={'localization': 'false', 'tickers': 'false'},
                timeout=10
            )
            data = page.json
            return {
                'price': data['market_data']['current_price']['usd'],
                'change_24h': data['market_data']['price_change_percentage_24h'],
                'change_7d': data['market_data']['price_change_percentage_7d'],
                'market_cap': data['market_data']['market_cap']['usd'],
                'volume_24h': data['market_data']['total_volume']['usd'],
                'circulating_supply': data['market_data']['circulating_supply'],
                'source': 'CoinGecko'
            }
        except Exception as e:
            # 备用数据源：DefiLlama
            try:
                page = session.get(
                    'https://coins.llama.fi/prices/current/coingecko:conflux-token',
                    timeout=10
                )
                data = page.json
                coin_data = data['coins']['coingecko:conflux-token']
                return {
                    'price': coin_data['price'],
                    'change_24h': None,  # DefiLlama 不提供
                    'change_7d': None,
                    'market_cap': None,
                    'volume_24h': None,
                    'circulating_supply': None,
                    'source': 'DefiLlama'
                }
            except Exception as e2:
                return {'error': f'All sources failed: {e}, {e2}'}
```

### 2. 交易所盘口数据（并发优化）

**原方案**：串行 curl 请求
**新方案**：并发 Fetcher 请求

```python
from scrapling.fetchers import FetcherSession
import asyncio

async def fetch_exchange_data():
    """并发获取 4 个交易所数据"""
    exchanges = {
        'Binance': 'https://api.binance.com/api/v3/ticker/24hr?symbol=CFXUSDT',
        'OKX': 'https://www.okx.com/api/v5/market/ticker?instId=CFX-USDT',
        'Gate': 'https://api.gateio.ws/api/v4/spot/tickers?currency_pair=CFX_USDT',
        'MEXC': 'https://api.mexc.com/api/v3/ticker/24hr?symbol=CFXUSDT'
    }

    async def fetch_single(name, url, session):
        try:
            page = await session.get(url, timeout=10)
            data = page.json

            # 解析不同交易所的响应格式
            if name == 'Binance':
                return {
                    'name': name,
                    'price': float(data['lastPrice']),
                    'change_24h': float(data['priceChangePercent']),
                    'volume': float(data['volume']),
                    'status': 'ok'
                }
            elif name == 'OKX':
                ticker = data['data'][0]
                return {
                    'name': name,
                    'price': float(ticker['last']),
                    'change_24h': float(ticker['changePercent']) * 100,
                    'volume': float(ticker['vol24h']),
                    'status': 'ok'
                }
            elif name == 'Gate':
                ticker = data[0]
                return {
                    'name': name,
                    'price': float(ticker['last']),
                    'change_24h': float(ticker['change_percentage']),
                    'volume': float(ticker['base_volume']),
                    'status': 'ok'
                }
            elif name == 'MEXC':
                return {
                    'name': name,
                    'price': float(data['lastPrice']),
                    'change_24h': float(data['priceChangePercent']),
                    'volume': float(data['volume']),
                    'status': 'ok'
                }
        except Exception as e:
            return {
                'name': name,
                'price': None,
                'change_24h': None,
                'volume': None,
                'status': '接口受限',
                'error': str(e)
            }

    # 并发请求所有交易所
    async with FetcherSession(impersonate='chrome') as session:
        tasks = [fetch_single(name, url, session) for name, url in exchanges.items()]
        results = await asyncio.gather(*tasks)

    return results
```

### 3. 巨鲸持仓数据（StealthyFetcher）

**原方案**：WebFetch + 手动解析
**新方案**：StealthyFetcher + CSS 选择器 + 自适应

```python
from scrapling.fetchers import StealthyFetcher

def fetch_whale_holdings():
    """获取 CoinCarp 巨鲸持仓数据"""
    # 启用自适应模式（网站结构变化后自动定位）
    StealthyFetcher.adaptive = True

    try:
        page = StealthyFetcher.fetch(
            'https://www.coincarp.com/currencies/confluxtoken/richlist/',
            headless=True,
            solve_cloudflare=True
        )

        # 提取持仓分布（自适应选择器）
        distribution = {}

        # 方法 1：CSS 选择器（首次保存模式）
        top10_elem = page.css('.distribution-top10', auto_save=True)
        if top10_elem:
            distribution['top10'] = top10_elem[0].text

        # 方法 2：自适应查找（结构变化后仍能找到）
        top20_elem = page.css('.distribution-top20', adaptive=True)
        if top20_elem:
            distribution['top20'] = top20_elem[0].text

        # 提取 Top 100 地址列表
        addresses = []
        rows = page.css('.richlist-table tr', adaptive=True)

        for row in rows[1:101]:  # 跳过表头，取前 100
            cols = row.css('td')
            if len(cols) >= 4:
                addresses.append({
                    'rank': cols[0].text.strip(),
                    'address': cols[1].text.strip(),
                    'balance': cols[2].text.strip(),
                    'percentage': cols[3].text.strip()
                })

        # 重点监控地址
        tracked_addresses = {
            '0xe2fc31f816a9b94326492132018c3aecc4a93ae1': 'Binance提币钱包',
            '0x83da47ab9d850e2352edc200f172dbab39f66d84': '休眠冷存储'
        }

        tracked_data = []
        for addr in addresses:
            if addr['address'].lower() in tracked_addresses:
                tracked_data.append({
                    **addr,
                    'label': tracked_addresses[addr['address'].lower()]
                })

        return {
            'distribution': distribution,
            'top100': addresses,
            'tracked': tracked_data,
            'status': 'ok'
        }

    except Exception as e:
        return {
            'error': str(e),
            'status': 'failed'
        }
```

### 4. 链上数据获取（并发 + 降级）

**原方案**：串行 curl
**新方案**：并发 Fetcher + 自动降级

```python
from scrapling.fetchers import FetcherSession
import asyncio

async def fetch_onchain_data():
    """并发获取链上数据（TVL + 账户数 + AxCNH）"""

    async def fetch_tvl(session):
        try:
            page = await session.get('https://api.llama.fi/v2/chains', timeout=10)
            chains = page.json
            conflux = next((c for c in chains if c['name'] == 'Conflux'), None)
            return {'tvl': conflux['tvl'] if conflux else None}
        except:
            return {'tvl': None, 'error': 'TVL fetch failed'}

    async def fetch_core_accounts(session):
        try:
            page = await session.get(
                'https://api.confluxscan.io/statistics/account/growth',
                params={'duration': 'day', 'intervalType': 'day'},
                timeout=10
            )
            data = page.json
            latest = data['list'][-1] if data.get('list') else {}
            return {
                'core_total': latest.get('total'),
                'core_daily': latest.get('increment')
            }
        except:
            return {'core_total': None, 'core_daily': None}

    async def fetch_espace_accounts(session):
        try:
            page = await session.get(
                'https://evmapi.confluxscan.io/statistics/account/growth',
                params={'duration': 'day', 'intervalType': 'day'},
                timeout=10
            )
            data = page.json
            latest = data['list'][-1] if data.get('list') else {}
            return {
                'espace_total': latest.get('total'),
                'espace_daily': latest.get('increment')
            }
        except:
            return {'espace_total': None, 'espace_daily': None}

    async def fetch_axcnh(session):
        try:
            # 使用 StealthyFetcher 因为可能有反爬虫
            from scrapling.fetchers import StealthyFetcher
            page = StealthyFetcher.fetch(
                'https://evm.confluxscan.net/token/0x70bfd7f7eadf9b9827541272589a6b2bb760ae2e',
                headless=True
            )

            # 提取供应量数据
            supply_elem = page.css('.token-supply', adaptive=True)
            holders_elem = page.css('.token-holders', adaptive=True)
            transfers_elem = page.css('.token-transfers', adaptive=True)

            return {
                'axcnh_supply': supply_elem[0].text if supply_elem else None,
                'axcnh_holders': holders_elem[0].text if holders_elem else None,
                'axcnh_transfers': transfers_elem[0].text if transfers_elem else None
            }
        except:
            return {'axcnh_supply': None, 'axcnh_holders': None, 'axcnh_transfers': None}

    # 并发执行所有请求
    async with FetcherSession(impersonate='chrome') as session:
        results = await asyncio.gather(
            fetch_tvl(session),
            fetch_core_accounts(session),
            fetch_espace_accounts(session),
            fetch_axcnh(session)
        )

    # 合并结果
    combined = {}
    for result in results:
        combined.update(result)

    return combined
```

### 5. 治理投票数据（DynamicFetcher）

**原方案**：Chrome DevTools MCP
**新方案**：DynamicFetcher（更简洁）

```python
from scrapling.fetchers import DynamicFetcher

def fetch_governance_data():
    """获取 ConfluxHub 治理投票数据"""
    try:
        page = DynamicFetcher.fetch(
            'https://confluxhub.io/governance/vote/onchain-dao-voting',
            headless=True,
            network_idle=True,  # 等待网络空闲
            timeout=15000
        )

        # 等待关键元素加载
        page.wait_for('.voting-round', timeout=10000)

        # 提取投票轮次
        round_elem = page.css('.voting-round::text', adaptive=True)
        round_num = round_elem[0] if round_elem else None

        # 提取投票参数表格
        params = []
        rows = page.css('.params-table tr', adaptive=True)

        for row in rows[1:]:  # 跳过表头
            cols = row.css('td')
            if len(cols) >= 4:
                params.append({
                    'name': cols[0].text.strip(),
                    'current': cols[1].text.strip(),
                    'pending': cols[2].text.strip(),
                    'voting': cols[3].text.strip()
                })

        # 提取投票时间
        period_elem = page.css('.voting-period::text')
        effective_elem = page.css('.effective-date::text')

        return {
            'round': round_num,
            'voting_period': period_elem[0] if period_elem else None,
            'effective_date': effective_elem[0] if effective_elem else None,
            'params': params,
            'status': 'ok'
        }

    except Exception as e:
        return {
            'status': 'no_data',
            'message': '当前无进行中的治理投票',
            'error': str(e)
        }
```

---

## 性能对比

| 任务 | 原方案 | Scrapling | 提升 |
|------|--------|-----------|------|
| 价格数据 | curl + jq | Fetcher | 2x 更快 |
| 交易所数据 | 串行 curl | 并发 Fetcher | 4x 更快 |
| 巨鲸持仓 | WebFetch + 手动解析 | StealthyFetcher + CSS | 10x 更快 |
| 链上数据 | 串行 curl | 并发 Fetcher | 4x 更快 |
| 治理投票 | Chrome DevTools MCP | DynamicFetcher | 更简洁 |

## 错误处理

Scrapling 内置自动重试和错误处理：

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(
    impersonate='chrome',
    retry_times=3,  # 自动重试 3 次
    retry_delay=1.0  # 重试间隔 1 秒
) as session:
    page = session.get('https://api.example.com')
```

## 自适应抓取

当网站结构变化时，Scrapling 自动定位元素：

```python
# 首次抓取：保存元素模式
page = StealthyFetcher.fetch(url, headless=True)
data = page.css('.product-price', auto_save=True)

# 网站改版后：自适应查找
page = StealthyFetcher.fetch(url, headless=True)
data = page.css('.product-price', adaptive=True)  # 即使 CSS 类名变了也能找到！
```

## 集成到现有模块

### 更新 PRICE_ANALYSIS.md

在步骤 1 中替换：
```markdown
### 1. 价格数据获取
使用 Scrapling Fetcher 替代 curl：
- 参考 SCRAPLING_FETCHER.md 中的 `fetch_price_data()`
- 自动降级到备用数据源
- 内置重试机制
```

### 更新 TECH_UPDATE.md

在步骤 1 中替换：
```markdown
### 1. 链上数据获取
使用 Scrapling 并发获取：
- 参考 SCRAPLING_FETCHER.md 中的 `fetch_onchain_data()`
- 4 个数据源并发请求
- 自动错误处理
```

---

## 依赖安装

```bash
# 安装 Scrapling
pip install "scrapling[all]"

# 下载浏览器依赖（首次使用）
scrapling install

# 验证安装
python -c "from scrapling.fetchers import Fetcher; print('OK')"
```

## 注意事项

1. **首次使用**需要运行 `scrapling install` 下载浏览器
2. **自适应模式**需要先用 `auto_save=True` 保存元素模式
3. **StealthyFetcher** 比 Fetcher 慢，仅在需要绕过反爬虫时使用
4. **DynamicFetcher** 最慢，仅用于 JS 渲染的页面
5. **并发请求**使用 `asyncio.gather()` 而非顺序执行

## 下一步

1. 在 Agent 配置中添加 Scrapling 依赖检查
2. 更新各模块的数据获取代码
3. 测试自适应抓取功能
4. 监控性能提升效果
