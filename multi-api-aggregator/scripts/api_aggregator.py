#!/usr/bin/env python3
"""
Multi-API Aggregator Script
Handles parallel API calls with retry, timeout, and error handling
"""

import concurrent.futures
import requests
import time
import json
import sys
from typing import List, Dict, Any

def call_api_with_retry(
    api_config: Dict[str, Any],
    max_attempts: int = 3,
    backoff_factor: int = 2
) -> Dict[str, Any]:
    """
    Call a single API with exponential backoff retry

    Args:
        api_config: API configuration dict with url, method, params, headers, etc.
        max_attempts: Maximum number of retry attempts
        backoff_factor: Exponential backoff multiplier (1s, 2s, 4s, ...)

    Returns:
        Dict with status, data/error, and response_time
    """
    api_name = api_config.get('name', 'unknown')

    for attempt in range(max_attempts):
        try:
            start_time = time.time()

            response = requests.request(
                method=api_config.get('method', 'GET'),
                url=api_config['url'],
                params=api_config.get('params'),
                headers=api_config.get('headers', {}),
                json=api_config.get('body'),
                timeout=api_config.get('timeout', 10)
            )

            response_time = time.time() - start_time
            response.raise_for_status()

            return {
                'name': api_name,
                'status': 'success',
                'data': response.json(),
                'response_time': round(response_time, 2),
                'attempt': attempt + 1
            }

        except requests.exceptions.Timeout:
            if attempt < max_attempts - 1:
                sleep_time = backoff_factor ** attempt
                time.sleep(sleep_time)
                continue
            return {
                'name': api_name,
                'status': 'timeout',
                'error': f'Request timed out after {max_attempts} attempts',
                'attempts': max_attempts
            }

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_text = e.response.text[:200] if e.response.text else 'No error message'

            # Don't retry on client errors (4xx)
            if 400 <= status_code < 500:
                return {
                    'name': api_name,
                    'status': 'http_error',
                    'error': f'HTTP {status_code}: {error_text}',
                    'status_code': status_code
                }

            # Retry on server errors (5xx)
            if attempt < max_attempts - 1:
                sleep_time = backoff_factor ** attempt
                time.sleep(sleep_time)
                continue

            return {
                'name': api_name,
                'status': 'http_error',
                'error': f'HTTP {status_code}: {error_text}',
                'status_code': status_code,
                'attempts': max_attempts
            }

        except requests.exceptions.ConnectionError as e:
            if attempt < max_attempts - 1:
                sleep_time = backoff_factor ** attempt
                time.sleep(sleep_time)
                continue
            return {
                'name': api_name,
                'status': 'connection_error',
                'error': f'Connection failed: {str(e)[:200]}',
                'attempts': max_attempts
            }

        except Exception as e:
            return {
                'name': api_name,
                'status': 'error',
                'error': f'Unexpected error: {str(e)[:200]}'
            }

    return {
        'name': api_name,
        'status': 'error',
        'error': 'Max retries exceeded'
    }


def aggregate_apis(
    api_configs: List[Dict[str, Any]],
    max_workers: int = 5,
    retry_config: Dict[str, int] = None
) -> Dict[str, Any]:
    """
    Execute multiple API calls in parallel

    Args:
        api_configs: List of API configuration dicts
        max_workers: Maximum number of parallel workers
        retry_config: Dict with max_attempts and backoff_factor

    Returns:
        Dict with summary and results
    """
    if retry_config is None:
        retry_config = {'max_attempts': 3, 'backoff_factor': 2}

    start_time = time.time()
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                call_api_with_retry,
                api,
                retry_config['max_attempts'],
                retry_config['backoff_factor']
            )
            for api in api_configs
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    'name': 'unknown',
                    'status': 'error',
                    'error': f'Future execution failed: {str(e)}'
                })

    total_time = time.time() - start_time

    # Calculate summary
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] != 'success']

    summary = {
        'total_apis': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'success_rate': round(len(successful) / len(results) * 100, 2) if results else 0,
        'total_time': round(total_time, 2)
    }

    return {
        'summary': summary,
        'results': {r['name']: r for r in results}
    }


if __name__ == '__main__':
    # Example usage
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test with public APIs
        test_apis = [
            {
                'name': 'coingecko',
                'url': 'https://api.coingecko.com/api/v3/simple/price',
                'params': {'ids': 'bitcoin', 'vs_currencies': 'usd'}
            },
            {
                'name': 'binance',
                'url': 'https://api.binance.com/api/v3/ticker/price',
                'params': {'symbol': 'BTCUSDT'}
            }
        ]

        result = aggregate_apis(test_apis)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python api_aggregator.py --test")
        print("Or import and use aggregate_apis() function")
