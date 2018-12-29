"""Control the gathering and caching of stock data.

General strategy is:
    1) For every given ticker, check the cache folder for that ticker's file.
    2) Add all tickers to a priority queue, sorted by modification timestamp..
    3) For all tickers that are outdated (or 1% of tickers, whichever is
        greater), load them async via the API and re-write them.
    4) For all other tickers, async load their files.
"""

import bz2
import datetime
from copy import deepcopy
import json
import math
from multiprocessing.dummy import Pool
import os
import requests
import time


local_cache = {}


def _callApi(request, required_key):
    """Call a given AlphaVantage API with controlled retries until successful.

    Args:
        request: String request to make.
        required_key: A key that must be present in the response.
    Returns:
        result: A partially validated response.
    """
    if request in local_cache:
        return local_cache[request]

    attempts = 0
    aggregated_results = {}
    while True:
        time.sleep(1)

        attempts += 1
        if attempts >= 120:
            print(aggregated_results)
            raise IOError('Too many attempts for request %s' % request)

        raw_result = requests.get(request)

        # Retry w/o error if server is swamped.
        if raw_result.status_code == 503:
            continue

        if raw_result.status_code != 200:
            print(request)
            print(raw_result)
            raise IOError('Recived %d status code for request %s.' % (
                raw_result.status_code, request))

        try:
            result = raw_result.json()
        except ValueError as e:
            print(request)
            print(raw_result)
            raise e

        if 'Error Message' in result:
            raise IOError('Received error %s for request %s.' % (
                result['Error Message'], request))

        if required_key not in result:
            aggregated_results.update(result)
            continue

        local_cache[request] = result

        return result


def _callSearchApi(ticker, api_key):
    """Call the AlphaVantage Search API for a list of tickers.

    Args:
        ticker: Ticker string.
        api_key: String API key for authentication.
    Returns:
        name: String name of this ticker.
    """
    base_request = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=%s&apikey=%s'

    request = base_request % (ticker, api_key)
    result = _callApi(request, 'bestMatches')

    for match in result['bestMatches']:
        if match['1. symbol'] == ticker:
            return match['2. name']

    print(result)
    raise IOError('Couldn\'t find ticker %s' % ticker)



def _callDailyAdjustedApi(ticker, api_key):
    """Call the AlphaVantage Daily Adjusted API for a list of tickers.

    Args:
        ticker: Ticker string.
        api_key: String API key for authentication.
    Returns:
        price_data: Dict of integer dates (days since epoch), to prices
            (floats).
    """
    base_request = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s'
    epoch = datetime.datetime.utcfromtimestamp(0)

    request = base_request % (ticker, api_key)
    result = _callApi(request, 'Time Series (Daily)')

    price_data = {}
    for date_str, data in result['Time Series (Daily)'].items():
        date_int = (datetime.datetime.strptime(date_str, '%Y-%m-%d') - epoch).days
        price_float = float(data['5. adjusted close'])
        price_data[date_int] = price_float

    return price_data


def _getAllApiData(ticker, api_key):
    """Get data from AlphaVantage APIs.

    Args:
        ticker: Ticker string.
        api_key: String API key for authentication.
    Returns:
        ticker_data: Nested dict of data about this ticker.
            {
                ticker<string>: {
                    'name': name<string>,
                    'price_data': {
                        date<int>: price<float>
                    }
                }
            }
    """
    name = _callSearchApi(ticker, api_key)
    price_data = _callDailyAdjustedApi(ticker, api_key)

    ticker_data = {
        ticker: {
            'name': name,
            'price_data': price_data}}

    return ticker_data


def _getAndCacheApiData(tickers, api_key, cache_folder):
    """Get API data for all tickers, cache it, and return it.

    Args:
        tickers: Iterable of ticker strings.
        api_key: String API key for authentication.
        cache_folder: Where to store cache files.
    Returns:
        ticker_data: See _getAllApiData for format.
    """
    ticker_data = {}
    for t, ticker in enumerate(tickers):
        print('Getting ticker %s (%d/%d)' % (ticker, t + 1, len(tickers)))
        data = _getAllApiData(ticker, api_key)
        data_encoded = json.dumps(data)
        filename = cache_folder + '/' + ticker + '.encoded.bz2'
        with bz2.BZ2File(filename, 'wb') as f:
            f.write(data_encoded.encode())
        ticker_data.update(data)

    return ticker_data


def _readCacheFile(filename):
    """Read a single cached file.

    Args:
        filename: String name of a file to read.
    Returns:
        ticker_data: See _getAllApiData for format.
    """
    with bz2.BZ2File(filename, 'rb') as f:
        byte_data = f.read()
    decoded_data = byte_data.decode()
    ticker_data = json.loads(decoded_data)

    # JSON cannot have non-string keys, so convert dates back to int.
    for ticker in ticker_data:
        date_strings = set(ticker_data[ticker]['price_data'].keys())
        
        price_data = ticker_data[ticker]['price_data']
        for date_string in date_strings:
            price_data[int(date_string)] = price_data[date_string]
            del price_data[date_string]

    return ticker_data


def _getCachedFiles(tickers, cache_folder, max_age):
    """Get a sorted list of cache files newer than max_age.

    Args:
        tickers: Iterable of ticker strings.
        cache_folder: Where to read cache files.
        max_age: Max number of days to allow for cache, or None for no max age.
    Returns:
        cached_ticker_list: List of ticker strings with a valid cache.
    """
    unsorted_list = []
    for ticker in tickers:
        filename = cache_folder + '/' + ticker + '.encoded.bz2'

        if not os.path.isfile(filename):
            continue

        days_since_modified = (
            time.time() - os.path.getmtime(filename)) / (24 * 60 * 60)

        if max_age == None or days_since_modified < max_age:
            unsorted_list.append((days_since_modified, ticker))

    sorted_list = sorted(unsorted_list)

    cached_ticker_list = []
    for _, ticker in sorted_list:
        cached_ticker_list.append(ticker)

    return cached_ticker_list


def _readCacheFiles(tickers, cache_folder):
    """Read all cached files.

    Args:
        tickers: Iterable of ticker strings.
        cache_folder: Where to store cache files.
    Returns:
        ticker_data: See _getAllApiData for format.
    """
    ticker_data = {}
    print('Reading %d files from cache.' % len(tickers))
    for ticker in tickers:
        print('Reading %s from cache.' % ticker)
        ticker_data.update(
            _readCacheFile(cache_folder + '/' + ticker + '.encoded.bz2'))

    return ticker_data


def getTickerData(tickers, api_key, cache_folder, refresh_strategy):
    """Get data from APIs or caches for ticker data.

    Args:
        tickers: Iterable of ticker strings.
        api_key: String API key for authentication.
        cache_folder: Where to store cache files.
        refresh_strategy: Whether to updated "outdated", "all", or "none" of
            the tickers.
    Returns:
        ticker_data: See _getAllApiData for format.
    """
    ticker_data = None
    cached_files = []
    if refresh_strategy == 'all':
        return _getAndCacheApiData(tickers, api_key, cache_folder)
    elif refresh_strategy == 'none':
        cached_files = _getCachedFiles(tickers, cache_folder, None)
    else:
        cached_files = _getCachedFiles(tickers, cache_folder, 30)

        # Assume we will run daily.
        # Ensure at least 1/25 of tickers are refreshed with each call.
        min_refresh = math.ceil(len(tickers) / 25)
        min_refresh -= (len(tickers) - len(cached_files))
        min_refresh = max(min_refresh, 0)
        for _ in range(min_refresh):
            if cached_files:
                cached_files.pop()

    uncached_files = set(tickers) - set(cached_files)

    pool1 = Pool(1)
    pool2 = Pool(2)
    api_result = pool1.apply_async(
        _getAndCacheApiData, (uncached_files, api_key, cache_folder))
    file_result = pool2.apply_async(
        _readCacheFiles, (cached_files, cache_folder))
    pool1.close()
    pool2.close()

    ticker_data = api_result.get()
    ticker_data.update(file_result.get())

    return ticker_data
