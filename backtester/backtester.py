"""Module to backtest a given strategy based on intermittent outputs.

General strategy is:
    1) Accept a list of dated allocations, and dated stock prices.
    2) Step through days in order, adjusting previous allocations based on price
        changes, and rebalancing when new allocations are encountered.
    3) From daily return data for the entire portfolio, calculate and return
        the excess return, downside risk, and Sortino Ratio of the
        allocations.
"""
