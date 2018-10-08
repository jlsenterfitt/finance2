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
