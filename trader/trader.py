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
import heapq
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
    allocation_array = np.array(
            [allocation_map[ticker] for ticker in ticker_tuple],
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
    cov = np.cov(combined)
    std = np.std(portfolio_1_returns)
    correl = cov / pow(std, 2)
    return correl


def _addCashToDataMatrix(ticker_tuple, data_matrix):
    cash_returns = np.ones((data_matrix.shape[0], 1))
    data_matrix = np.append(data_matrix, cash_returns, 1)
    ticker_tuple = list(ticker_tuple)
    ticker_tuple.append('_CASH_')
    ticker_tuple = tuple(ticker_tuple)
    return (ticker_tuple, data_matrix)


def calculateTrades(desired_allocation_map, actual_allocation_map, ticker_tuple, data_matrix):
    """Calculate correlation for all potential trades.

    Args:
        desired_allocation_map: Map of tickers to allocation percentages.
        actual_allocation_map: Map of tickers to allocation percentages.
        data_matrix: Rows = days, columns = tickers, values = % price changes.
        ticker_tuple: Tuple of tickers in the matrix, in the same order.
    """
    trade_heap = []

    (ticker_tuple, data_matrix) = _addCashToDataMatrix(ticker_tuple, data_matrix)

    default_desired_map = defaultdict(int)
    for k, v in desired_allocation_map.items():
        if v > 0: default_desired_map[k] = v
    optimal_returns = _getBacktestedAllocationReturns(default_desired_map, ticker_tuple, data_matrix)

    default_actual_map = defaultdict(int)
    for k, v in actual_allocation_map.items():
        if v > 0: default_actual_map[k] = v
    current_returns = _getBacktestedAllocationReturns(default_actual_map, ticker_tuple, data_matrix)

    current_correl = _getPortfolioCorrelation(optimal_returns, current_returns).min()
    print('Current correl: %.4f' % current_correl)

    for sell_ticker in actual_allocation_map.keys():
        sell_delta = default_actual_map[sell_ticker] - default_desired_map[sell_ticker]
        if sell_delta <= 0: continue

        for buy_ticker in desired_allocation_map.keys():
            buy_delta = default_desired_map[buy_ticker] - default_actual_map[buy_ticker]
            if buy_delta <= 0: continue

            true_delta = min(buy_delta, sell_delta)
            trade = default_actual_map.copy()
            trade[buy_ticker] += true_delta
            trade[sell_ticker] -= true_delta
            trade_returns = _getBacktestedAllocationReturns(trade, ticker_tuple, data_matrix)

            correl = _getPortfolioCorrelation(optimal_returns, trade_returns).min()

            if correl <= current_correl: continue
    
            trade_heap.append((correl, sell_ticker, buy_ticker, '%.1f%%' % (true_delta * 100)))

    for trade in sorted(trade_heap, reverse=True):
        print('%.4f %s %s %s' % trade)
