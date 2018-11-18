"""Optimize allocations for a given date.

General strategy is:
    1) Filter given prices data based on date.
        1.1) Remove tickers w/o enough data.
        1.2) Remove days w/o all tickers.
    2) Fork several worker processes with copies of the filtered data.
    3) From some arbitrary starting point, create a queue of all potential
        single trade deviations.
    4) Have workers process the queue, and send results back via queue.
    5) Have the master process the results, choosing the best one.
    6a) If a better allocation is found, restart #3 with that allocation as the
        starting point.
    6b) If no better allocation is found, halve the trading amount and restart
        #2 with the current allocation and new trade amount.
    7) Once a lower limit of trade amount is found, return the allocaiton.
"""


def _scoreAllocation(data_matrix, allocation_array, required_return):
    """Determine the score of a given allocation.

    Args:
        data_matrix: See _convertTickerDataToMatrix.
        allocation_array: An array of percent allocations.
        required_return: What daily return is desired.
    Returns:
        score: A modified Sortino Ratio for the allocation.
    """
    pass


def _findOptimalAllocation(data_matrix, ticker_tuple, required_return):
    """Find the optimal allocation.

    Args:
         data_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
        required_return: What daily return is desired.
    Returns:
        allocations: Dict of percent allocations by ticker.
    """
    pass


def getOptimalAllocation(data_matrix, required_return):
    """Find the optimal allocation based on requirements.   

    Args:
        data_matrix: See _convertTickerDataToMatrix.
        required_return: What daily return is desired.
    Returns:
        allocations: Dict of percent allocations by ticker.
    """
    pass
