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
import functools
import multiprocessing as mp
import numpy as np
from scipy.stats.mstats import gmean


def _initializeProcess(data):
    """Initialize a process with necessary data."""
    global data_matrix
    data_matrix = data


def _unwrapAndScore(data_dict):
    return _scoreAllocation(data_dict['allocation_array'], data_dict['required_return'])


def _scoreAllocation(allocation_array, required_return):
    """Determine the score of a given allocation.

    Args:
        data_matrix: See _convertTickerDataToMatrix.
        allocation_array: An array of percent allocations.
        required_return: What daily return is desired.
    Returns:
        score: A modified Sortino Ratio for the allocation.
    """
    daily_returns = np.matmul(data_matrix, allocation_array)
    mean_return = gmean(daily_returns)

    # Short-circuit score calculation when mean_return < required_return.
    # Otherwise, with a negative denominator, the code will push for a
    # large denominator to maximize the overall score.
    if mean_return < required_return:
        return {
                'score': mean_return - required_return,
                'allocation_array': allocation_array}

    filtered_returns = np.copy(daily_returns)
    filtered_returns -= required_return
    filtered_returns = np.clip(filtered_returns, None, 0)
    filtered_returns *= filtered_returns
    downside_risk = np.sqrt(filtered_returns.mean())

    below_desired = daily_returns < required_return
    filtered_returns = [
        data_matrix[x]
        for x in range(len(below_desired)) if below_desired[x]]
    downside_correl = np.matmul(
        np.matmul(
            allocation_array,
            np.corrcoef(filtered_returns, rowvar=False)),
        allocation_array)

    return {
            'score': (mean_return - required_return) / (downside_risk * downside_correl),
            'allocation_array': allocation_array}


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
    # Initialize global data for master.
    _initializeProcess(data_matrix)

    with mp.Pool(
            initializer=_initializeProcess,
            initargs=(data_matrix,)) as pool:

        best = np.zeros(len(ticker_tuple), dtype=np.float64)
        best[0] = 1.0
        best_score = _scoreAllocation(best, required_return)['score']

        trading_increment = 1.0

        # TODO: Remove magic number.
        while trading_increment > 1 / 1024:
            map_iterable = []
            for sell_id in range(len(ticker_tuple)):
                if best[sell_id] < trading_increment: continue

                for buy_id in range(len(ticker_tuple)):
                    if buy_id == sell_id: continue

                    curr = np.copy(best)
                    curr[sell_id] -= trading_increment
                    curr[buy_id] += trading_increment

                    map_iterable.append({'allocation_array': curr, 'required_return': required_return})

            # TODO: Test different chunksizes.
            results = pool.map(_unwrapAndScore, map_iterable, 1)
            best_result = functools.reduce(
                    lambda x, y: x if x['score'] > y['score'] else y,
                    results,
                    {'score': -float('inf')})
        
            if best_result['score'] > best_score:
                best = best_result['allocation_array']
                best_score = best_result['score']
            else:
                trading_increment /= 2.0
    
    return (best_score, best)
