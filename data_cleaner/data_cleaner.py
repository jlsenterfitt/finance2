"""Convert ticker_data to a data_matrix for processing."""


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
    pass


def _calculatePriceChanges(ticker_data):
    """Calculate data matrix from ticker data.

    Args:
        ticker_data: Data from the data_gatherer module.
    Returns:    
        data_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    pass


def convertTickerDataToMatrix(ticker_data, required_num_days, end_date):
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
    pass

