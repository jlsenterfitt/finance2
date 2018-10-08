"""Control the gathering and caching of stock data.

General strategy is:
    1) For every given ticker, check the cache folder for that ticker's file.
    2) Add all tickers to a priority queue, sorted by modification timestamp..
    3) For all tickers that are outdated (or 1% of tickers, whichever is
        greater), load them async via the API and re-write them.
    4) For all other tickers, async load their files.
"""

import datetime
import requests
import time


def _callApi(request, required_key):
    """Call a given AlphaVantage API with controlled retries until successful.

    Args:
        request: String request to make.
        required_key: A key that must be present in the response.
    Returns:
        result: A partially validated response.
    """
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

        return result


def _callSearchApi(tickers, api_key):
    """Call the AlphaVantage Search API for a list of tickers.

    Args:
        tickers: Iterable of ticker strings.
        api_key: String API key for authentication.
    Returns:
        ticker_data: Dict of tickers to asset names.
    """
    base_request = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=%s&apikey=%s'

    ticker_data = {}
    for ticker in tickers:
        request = base_request % (ticker, api_key)
        result = _callApi(request, 'bestMatches')

        for match in result['bestMatches']:
            if match['1. symbol'] == ticker:
                ticker_data[ticker] = match['2. name']

        if ticker not in ticker_data:
            raise IOError('Couldn\'t find ticker %s' % ticker)

    return ticker_data


def _callDailyAdjustedApi(tickers, api_key):
    """Call the AlphaVantage Daily Adjusted API for a list of tickers.

    Args:
        tickers: Iterable of ticker strings.
        api_key: String API key for authentication.
    Returns:
        ticker_data: Dict of tickers (strings) to integer dates (days since
            epoch), to prices (floats).
    """
    base_request = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s'
    epoch = datetime.datetime.utcfromtimestamp(0)

    ticker_data = {}
    for ticker in tickers:
        request = base_request % (ticker, api_key)
        result = _callApi(request, 'Time Series (Daily)')

        date_dict = {}
        for date_str, data in result['Time Series (Daily)'].items():
            date_int = (datetime.datetime.strptime(date_str, '%Y-%m-%d') - epoch).days
            price_float = float(data['5. adjusted close'])
            date_dict[date_int] = price_float

        ticker_data[ticker] = date_dict

    return ticker_data
