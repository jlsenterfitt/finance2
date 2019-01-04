"""Control trading from current allocations to desired allocations.

General strategy is:
    1) Mark every ticker where current allocation is higher than desired as a
        potential sell.
    2) Mark every ticker where current allocation is lower than desired as a
        potential buy.
    3) For every combination of buys and sells, check backdated correlation
        if that trade is done.
        3.1) Trade amount is the lesser of how overweight the buy is, or how
            underweight the sell is.
    4) Return the trades in order.
"""
from collections import defaultdict
import numpy as np

def _getBacktestedAllocationReturns(allocation_map, ticker_tuple, data_matrix):
    """Create an array of backtested returns for the given allocation map.

    Args:
        allocation_map: Map of tickers to allocation percentages.
        data_matrix: Rows = days, columns = tickers, values = % price changes.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    Returns:
        return_array: Array of backtested returns.
    """
    default_allocation_map = defaultdict(int)
    for k, v in allocation_map.items():
        default_allocation_map[k] = v

    allocation_array = np.array(
            [default_allocation_map[ticker] for ticker in ticker_tuple],
            dtype=np.float64)
    return np.matmul(data_matrix, allocation_array)


def _getPortfolioCorrelation(portfolio_1_returns, portfolio_2_returns):
    """Calculate the correlation between two portfolios.

    Args:
        portfolio_1_returns: Array of backtested returns.
        portfolio_2_returns: Array of backtested returns.
    Returns:
        correlation: The correlation between the portfolios.
    """
    combined = np.stack((portfolio_1_returns, portfolio_2_returns), axis=0)
    return np.corrcoef(combined)


def calculateTrades(desired_allocation_map, actual_allocation_map, ticker_tuple, data_matrix):
    """Calculate correlation for all potential trades.

    Args:
        desired_allocation_map: Map of tickers to allocation percentages.
        actual_allocation_map: Map of tickers to allocation percentages.
        data_matrix: Rows = days, columns = tickers, values = % price changes.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    pass
