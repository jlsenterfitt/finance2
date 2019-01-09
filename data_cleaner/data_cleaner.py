"""Convert ticker_data to a data_matrix for processing."""
import functools
import numpy as np
from scipy.stats.mstats import gmean


def _getRatios(ticker_data):
    all_scores = []
    removed_tickers = []
    for ticker in set(ticker_data.keys()):
        price_list = []
        for date_int in sorted(ticker_data[ticker]['price_data'].keys()):
            price_list.append(ticker_data[ticker]['price_data'][date_int])
        price_array = np.array(price_list, dtype=np.float64)
        return_array = price_array[1:] / price_array[:-1]
        mean_return = pow(gmean(return_array), 253)
        std = return_array.std() * pow(253, 0.5)

        downside_returns = np.copy(return_array)
        downside_returns -= pow(1.0761, 1/253)
        downside_returns = np.clip(downside_returns, None, 0)
        downside_returns *= downside_returns
        downside_risk = np.sqrt(downside_returns.mean()) * pow(253, 0.5)

        sharpe_ratio = (mean_return - 1.0) / std
        sortino_ratio = (mean_return - 1.0761) / downside_risk

        all_scores.append((ticker, max(sharpe_ratio, sortino_ratio), sharpe_ratio, sortino_ratio, mean_return, std, downside_risk))

        if max(sharpe_ratio, sortino_ratio) < 0:
            del ticker_data[ticker]
            removed_tickers.append(ticker)

    all_scores.sort()

    #for scores in all_scores:
        #print(scores)

    print('Removed %d tickers' % len(removed_tickers))
    print(removed_tickers)

def _removeFutureData(ticker_data, end_date):
    """Remove data on or after a given date in place.

    Args:
        ticker_data: Data from the data_gatherer module.
        end_date: Data on or after this date should be discarded.
    """
    for ticker in ticker_data:
        for date_int in set(ticker_data[ticker]['price_data'].keys()):
            if date_int >= end_date:
                del ticker_data[ticker]['price_data'][date_int]


def _removePastData(ticker_data, start_date):
    if not start_date:
        return

    for ticker in ticker_data:
        for date_int in set(ticker_data[ticker]['price_data'].keys()):
            if date_int < start_date:
                del ticker_data[ticker]['price_data'][date_int]


def _removeLowDataTickers(ticker_data, required_num_days):
    """Remove tickers without enough days of data in place.

    Args:
        ticker_data: Data from the data_gatherer module.
        required_num_days: How many days of data each ticker should have.
    """
    for ticker in set(ticker_data.keys()):
        if len(ticker_data[ticker]['price_data']) < required_num_days:
            del ticker_data[ticker]


def _removeLowDataDays(ticker_data):
    """Remove any days of data with one or more tickers missing, in place."""
    # Get a set of all known dates.
    date_set = set()
    for data in ticker_data.values():
        date_set = date_set.union(data['price_data'].keys())

    # Determine what dates are common to all tickers.
    for ticker, data in ticker_data.items():
        curr_date_set = set(data['price_data'].keys())
        if len(date_set.intersection(curr_date_set)) < (len(date_set) / 2):
            print(
                    'Pathological ticker found: %s %d / %d' % (
                        ticker,
                        len(date_set.intersection(curr_date_set)),
                        len(date_set)))
        date_set = date_set.intersection(curr_date_set)

    if not date_set:
        raise ValueError('No common dates left.')

    for ticker, data in ticker_data.items():
        remove_keys = set(data['price_data'].keys()) - date_set
        for remove_key in remove_keys:
            del data['price_data'][remove_key]


def _convertToMatrix(ticker_data):
    """Calculate data matrix from ticker data.

    Args:
        ticker_data: Data from the data_gatherer module.
    Returns:    
        return_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    ticker_tuple = tuple(sorted(ticker_data.keys()))

    # Generate a 2-d array of raw prices.
    raw_price_list = []
    expense_ratio_list = []
    for ticker in ticker_tuple:
        new_row = []
        for date in sorted(ticker_data[ticker]['price_data'].keys()):
            new_row.append(ticker_data[ticker]['price_data'][date])
        raw_price_list.append(new_row)
        expense_ratio_list.append(ticker_data[ticker]['expense_ratio'])
    raw_price_array = np.array(raw_price_list, dtype=np.float64).transpose()

    return_matrix = raw_price_array[1:] / raw_price_array[:-1]
    expense_array = np.array(expense_ratio_list, dtype=np.float64)
    print('Days of data %d' % len(return_matrix))

    return (ticker_tuple, return_matrix, expense_array)


def cleanAndConvertData(ticker_data, required_num_days, end_date, first_date=None):
    """Convert ticker data to a matrix for numpy processing.

    Args:
        ticker_data: Data from the data_gatherer module.
        required_num_days: How many days of data each ticker should have.
        end_date: Data on or after this date should be discarded.
        first_date: Data before this date should be discarded.

    Returns:
        data_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    _removeFutureData(ticker_data, end_date)

    _removePastData(ticker_data, first_date)

    # _getRatios(ticker_data)

    _removeLowDataTickers(ticker_data, required_num_days)

    _removeLowDataDays(ticker_data)

    (ticker_tuple, data_matrix, expense_array) = _convertToMatrix(ticker_data)

    return (ticker_tuple, data_matrix, expense_array)
