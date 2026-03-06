---
name: multi-api-aggregator
description: Aggregate multiple API calls with automatic retry, fallback, and error handling. Use this skill whenever the user needs to call multiple APIs in parallel, fetch data from multiple sources simultaneously, handle API failures gracefully, or aggregate results from different endpoints. Also trigger when the user mentions "call multiple APIs", "aggregate data from", "fetch from several sources", "parallel API requests", or needs to combine data from CoinGecko, Binance, OKX, or other crypto/financial APIs.
---

# Multi-API Aggregator

Efficiently call multiple APIs in parallel, automatically handle failures, retry with exponential backoff, and aggregate results into a unified format.

## When to Use

Use this skill when:
- User needs to call 2+ APIs to gather related data
- User wants to fetch the same data from multiple sources (for redundancy)
- User mentions "aggregate", "combine", "fetch from multiple", "parallel requests"
- User is working with crypto APIs (CoinGecko, Binance, OKX, etc.)
- User needs resilient API calls with automatic retry and fallback

## What This Skill Does

1. **Parallel Execution** - Calls multiple APIs simultaneously to minimize latency
2. **Automatic Retry** - Retries failed requests with exponential backoff (3 attempts by default)
3. **Graceful Degradation** - Returns partial results if some APIs fail
4. **Unified Output** - Aggregates responses into a consistent format
5. **Error Reporting** - Clear summary of which APIs succeeded/failed and why

## Configuration Methods

### Method 1: Configuration File (Recommended for Repeated Use)

Create a YAML config file defining your API sources:

```yaml
# ~/.claude/api-configs/crypto-prices.yaml
name: "Crypto Price Aggregator"
description: "Fetch CFX price from multiple exchanges"

apis:
  - name: "coingecko"
    url: "https://api.coingecko.com/api/v3/simple/price"
    method: "GET"
    params:
      ids: "conflux-token"
      vs_currencies: "usd"
    headers:
      Accept: "application/json"
    timeout: 10

  - name: "binance"
    url: "https://api.binance.com/api/v3/ticker/price"
    method: "GET"
    params:
      symbol: "CFXUSDT"
    timeout: 10

  - name: "okx"
    url: "https://www.okx.com/api/v5/market/ticker"
    method: "GET"
    params:
      instId: "CFX-USDT"
    timeout: 10

retry:
  max_attempts: 3
  backoff_factor: 2  # 1s, 2s, 4s

output:
  format: "json"  # or "markdown", "summary"
  merge_strategy: "first_success"  # or "all", "average"
```

**Usage with config file:**
```
User: "Aggregate crypto prices using my crypto-prices config"
```

### Method 2: Inline Parameters (For Ad-hoc Queries)

Specify APIs directly in the conversation:

```
User: "Call these APIs in parallel:
1. CoinGecko for CFX price
2. Binance for CFX/USDT ticker
3. OKX for CFX trading volume"
```

## Workflow

### Step 1: Parse Request

Determine which method the user is using:

**If config file mentioned:**
- Look for config in `~/.claude/api-configs/`
- Parse YAML/JSON to extract API definitions
- Validate all required fields are present

**If inline parameters:**
- Extract API endpoints from user's message
- Infer HTTP method (default: GET)
- Identify any authentication requirements
- Set reasonable defaults (timeout: 10s, retries: 3)

### Step 2: Prepare API Calls

For each API:

**Authentication Handling:**
- Check for API keys in environment variables
- Look for patterns: `{API_NAME}_API_KEY`, `{API_NAME}_TOKEN`
- If auth required but missing, warn user and skip that API
- Support multiple auth types:
  - Bearer token: `Authorization: Bearer {token}`
  - API key in header: `X-API-Key: {key}`
  - API key in query param: `?api_key={key}`

**Request Construction:**
- Build complete URL with query parameters
- Add required headers (User-Agent, Accept, etc.)
- Set timeout (default: 10 seconds)
- Prepare request body if POST/PUT

### Step 3: Execute Parallel Requests

Use Python's `concurrent.futures` or similar to call APIs in parallel:

```python
import concurrent.futures
import requests
import time

def call_api_with_retry(api_config, max_attempts=3, backoff_factor=2):
    """Call a single API with exponential backoff retry"""
    for attempt in range(max_attempts):
        try:
            response = requests.request(
                method=api_config['method'],
                url=api_config['url'],
                params=api_config.get('params'),
                headers=api_config.get('headers'),
                json=api_config.get('body'),
                timeout=api_config.get('timeout', 10)
            )
            response.raise_for_status()
            return {
                'name': api_config['name'],
                'status': 'success',
                'data': response.json(),
                'response_time': response.elapsed.total_seconds()
            }
        except requests.exceptions.Timeout:
            if attempt < max_attempts - 1:
                time.sleep(backoff_factor ** attempt)
                continue
            return {
                'name': api_config['name'],
                'status': 'timeout',
                'error': f'Request timed out after {max_attempts} attempts'
            }
        except requests.exceptions.HTTPError as e:
            return {
                'name': api_config['name'],
                'status': 'http_error',
                'error': f'HTTP {e.response.status_code}: {e.response.text[:200]}'
            }
        except Exception as e:
            return {
                'name': api_config['name'],
                'status': 'error',
                'error': str(e)
            }

def aggregate_apis(api_configs, max_workers=5):
    """Execute multiple API calls in parallel"""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(call_api_with_retry, api) for api in api_configs]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results
```

**Key Implementation Details:**
- Use ThreadPoolExecutor with max_workers=5 (adjustable)
- Each API call runs in its own thread
- Timeout applies per attempt, not total
- Exponential backoff: 1s, 2s, 4s (configurable)

### Step 4: Aggregate Results

Collect all responses and organize them:

**Success Tracking:**
```python
successful = [r for r in results if r['status'] == 'success']
failed = [r for r in results if r['status'] != 'success']

summary = {
    'total_apis': len(results),
    'successful': len(successful),
    'failed': len(failed),
    'success_rate': len(successful) / len(results) * 100
}
```

**Data Merging Strategies:**

1. **first_success** (default) - Return first successful response
   ```python
   if successful:
       return successful[0]['data']
   ```

2. **all** - Return all successful responses
   ```python
   return {api['name']: api['data'] for api in successful}
   ```

3. **average** - Average numeric values (for prices, volumes)
   ```python
   prices = [extract_price(api['data']) for api in successful]
   return {'average': sum(prices) / len(prices), 'sources': len(prices)}
   ```

4. **merge** - Deep merge all responses
   ```python
   merged = {}
   for api in successful:
       merged.update(api['data'])
   return merged
   ```

### Step 5: Format Output

Present results in user-friendly format:

**JSON Format:**
```json
{
  "summary": {
    "total_apis": 3,
    "successful": 2,
    "failed": 1,
    "success_rate": 66.67,
    "total_time": 1.23
  },
  "results": {
    "coingecko": {
      "status": "success",
      "data": {"conflux-token": {"usd": 0.145}},
      "response_time": 0.45
    },
    "binance": {
      "status": "success",
      "data": {"symbol": "CFXUSDT", "price": "0.1448"},
      "response_time": 0.38
    },
    "okx": {
      "status": "timeout",
      "error": "Request timed out after 3 attempts"
    }
  },
  "aggregated_data": {
    "price_usd": 0.1449,
    "sources": ["coingecko", "binance"],
    "confidence": "high"
  }
}
```

**Markdown Format:**
```markdown
## API Aggregation Results

✅ **2/3 APIs succeeded** (66.67% success rate)
⏱️ Total time: 1.23s

### Successful APIs

**CoinGecko** (0.45s)
- Price: $0.145

**Binance** (0.38s)
- Price: $0.1448

### Failed APIs

**OKX** ❌
- Error: Request timed out after 3 attempts

### Aggregated Data

**Average Price**: $0.1449
**Data Sources**: CoinGecko, Binance
**Confidence**: High (2/3 sources)
```

**Summary Format** (concise):
```
✅ Fetched CFX price from 2/3 sources
Average: $0.1449 (CoinGecko: $0.145, Binance: $0.1448)
⚠️ OKX timed out
```

## Error Handling

### Common Errors and Solutions

**Authentication Errors (401/403):**
- Check if API key environment variable is set
- Verify API key format and permissions
- Suggest: `export COINGECKO_API_KEY=your_key_here`

**Rate Limiting (429):**
- Respect Retry-After header if present
- Increase backoff_factor in config
- Suggest reducing request frequency

**Timeout Errors:**
- Increase timeout value in config
- Check network connectivity
- Try fewer parallel requests (reduce max_workers)

**Invalid Response (JSON parse error):**
- Log raw response for debugging
- Check if API endpoint changed
- Verify request parameters are correct

**Connection Errors:**
- Check internet connectivity
- Verify API endpoint URL is correct
- Try with curl to isolate issue

### Partial Success Handling

When some APIs succeed and others fail:

1. **Always return successful data** - Don't fail completely if 1/3 APIs work
2. **Report failures clearly** - Show which APIs failed and why
3. **Suggest fallbacks** - If primary source fails, highlight alternatives
4. **Log for debugging** - Save full error details to `~/.claude/logs/api-aggregator.log`

## Advanced Features

### Caching

Cache successful responses to avoid redundant API calls:

```python
import hashlib
import json
import time

def cache_key(api_config):
    """Generate cache key from API config"""
    key_data = f"{api_config['url']}:{json.dumps(api_config.get('params', {}))}"
    return hashlib.md5(key_data.encode()).hexdigest()

def get_cached(cache_key, max_age=300):
    """Get cached response if not expired (default: 5 minutes)"""
    cache_file = f"~/.claude/cache/api-{cache_key}.json"
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            cached = json.load(f)
            if time.time() - cached['timestamp'] < max_age:
                return cached['data']
    return None
```

**Usage:**
```
User: "Aggregate crypto prices with 5-minute cache"
```

### Response Transformation

Transform API responses to a common schema:

```python
def transform_price_response(api_name, raw_data):
    """Normalize different API response formats"""
    transformers = {
        'coingecko': lambda d: d['conflux-token']['usd'],
        'binance': lambda d: float(d['price']),
        'okx': lambda d: float(d['data'][0]['last'])
    }
    return transformers[api_name](raw_data)
```

### Conditional Requests

Only call certain APIs based on conditions:

```yaml
apis:
  - name: "backup_api"
    url: "https://backup.example.com/price"
    condition: "primary_failed"  # Only call if primary API fails
```

## Example Use Cases

### Use Case 1: CFX Investment Briefing

**Config file:** `~/.claude/api-configs/cfx-briefing.yaml`

```yaml
name: "CFX Briefing Data Sources"
apis:
  - name: "price_coingecko"
    url: "https://api.coingecko.com/api/v3/simple/price"
    params: {ids: "conflux-token", vs_currencies: "usd,btc"}

  - name: "volume_binance"
    url: "https://api.binance.com/api/v3/ticker/24hr"
    params: {symbol: "CFXUSDT"}

  - name: "orderbook_okx"
    url: "https://www.okx.com/api/v5/market/books"
    params: {instId: "CFX-USDT", sz: "20"}

output:
  format: "json"
  merge_strategy: "all"
```

**Usage:**
```
User: "Run CFX briefing aggregation"
→ Calls all 3 APIs in parallel
→ Returns combined data in <2 seconds
```

### Use Case 2: Multi-Exchange Arbitrage Check

```
User: "Check CFX price on Binance, OKX, Gate.io, and MEXC - find arbitrage opportunities"

→ Skill calls 4 exchange APIs in parallel
→ Compares prices
→ Highlights price differences >0.5%
```

### Use Case 3: Redundant Data Fetching

```
User: "Get CFX market cap from CoinGecko, CoinMarketCap, and CoinCarp - use first successful response"

→ Calls all 3 in parallel
→ Returns immediately when first succeeds
→ Cancels remaining requests (optional)
```

## Tips for Best Results

1. **Start with config files** - Easier to maintain and reuse
2. **Set realistic timeouts** - 10s for most APIs, 30s for slow ones
3. **Use environment variables for secrets** - Never hardcode API keys
4. **Test APIs individually first** - Verify each works before aggregating
5. **Monitor rate limits** - Some APIs have strict limits (e.g., 10 req/min)
6. **Cache when possible** - Reduces API calls and improves speed
7. **Handle partial failures gracefully** - 2/3 success is often good enough

## Troubleshooting

**Problem: All APIs timing out**
- Check internet connection
- Try increasing timeout values
- Test with curl to isolate issue

**Problem: Inconsistent results**
- APIs may return different data formats
- Use response transformation to normalize
- Check API documentation for schema changes

**Problem: Rate limit errors**
- Reduce max_workers (fewer parallel requests)
- Add delays between retries
- Use caching to reduce API calls

**Problem: Authentication failures**
- Verify API keys are set: `echo $COINGECKO_API_KEY`
- Check key permissions and expiration
- Review API documentation for auth requirements
