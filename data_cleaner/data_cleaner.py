"""Convert ticker_data to a data_matrix for processing."""
import functools
import numpy as np

def _removeFutureData(ticker_data, end_date):
    """Remove data on or after a given date in place.

    Args:
        ticker_data: Data from the data_gatherer module.
        end_date: Data on or after this date should be discarded.
    """
    for ticker in ticker_data:
        for date_int in set(ticker_data[ticker]['price_data'].keys()):
            if int(date_int) >= end_date:
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
    # Initialize dates as whatever an arbitrary ticker has.
    date_set = set(list(ticker_data.values())[0]['price_data'].keys())

    # Determine what dates are common to all tickers.
    for ticker, data in ticker_data.items():
        curr_date_set = set(data['price_data'].keys())
        date_set = date_set.intersection(curr_date_set)

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
    # TODO: This should incorporate expense ratios.
    ticker_tuple = tuple(sorted(ticker_data.keys()))

    # Generate a 2-d array of raw prices.
    raw_price_list = []
    for ticker in ticker_tuple:
        new_row = []
        for date in sorted(ticker_data[ticker]['price_data'].keys()):
            new_row.append(ticker_data[ticker]['price_data'][date])
        raw_price_list.append(new_row)
    raw_price_array = np.array(raw_price_list, dtype=np.float64).transpose()

    return_matrix = raw_price_array[1:] / raw_price_array[:-1]

    return (ticker_tuple, return_matrix)


def cleanAndConvertData(ticker_data, required_num_days, end_date):
    """Convert ticker data to a matrix for numpy processing.

    Args:
        ticker_data: Data from the data_gatherer module.
        required_num_days: How many days of data each ticker should have.
        end_date: Data on or after this date should be discarded.
    Returns:
        data_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    _removeFutureData(ticker_data, end_date)

    _removeLowDataTickers(ticker_data, required_num_days)

    _removeLowDataDays(ticker_data)

    return _convertToMatrix(ticker_data)
