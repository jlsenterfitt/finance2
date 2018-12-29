"""Optimize allocations for a given date.

General strategy is:
    1) Fork several worker processes with copies of the filtered data.
    2) From some arbitrary starting point, create a queue of all potential
        single trade deviations.
    3) Have workers process the queue, and send results back via queue.
    4) Have the master process the results, choosing the best one.
    5a) If a better allocation is found, restart #3 with that allocation as the
        starting point.
    5b) If no better allocation is found, halve the trading amount and restart
        #2 with the current allocation and new trade amount.
    6) Once a lower limit of trade amount is found, return the allocaiton.
"""
import multiprocessing as mp
import numpy as np

def _initializeProcess(data):
    """Initialize a process with necessary data."""
    global data_matrix
    data_matrix = data


def _scoreAllocation(allocation_array, required_return):
    """Determine the score of a given allocation.

    Args:
        data_matrix: See _convertTickerDataToMatrix.
        allocation_array: An array of percent allocations.
        required_return: What daily return is desired.
    Returns:
        score: A modified Sortino Ratio for the allocation.
    """
    pass


def findOptimalAllocation(data_matrix, ticker_tuple, required_return):
    """Find the optimal allocation.

    Args:
         data_matrix: Rows = days, columns = tickers, values = % price changes.
            Tickers are ordered alphabetically.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
        required_return: What daily return is desired.
    Returns:
        allocations: Dict of percent allocations by ticker.
    """
    _initializeProcess(data_matrix)

    with mp.Pool(
            initializer=_initializeProcess,
            initArgs=(data_matrix,)) as pool:

        best = np.zeros(len(ticker_tuple), dtype=float64)
        best[0] = 1.0
        best_score = _scoreAllocation(ticker_tuple, required_return)

        # Create deviations from starting point, filter them, send through queues.
        # Collect results, keep best.
        # If no improvement, halve trade amount.
        # Repeat until trade amount is exhausted.
    
