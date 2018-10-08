"""Control the gathering and caching of stock data.

General strategy is:
    1) For every given ticker, check the cache folder for that ticker's file.
    2) Add all tickers to a priority queue, sorted by modification timestamp..
    3) For all tickers that are outdated (or 1% of tickers, whichever is
        greater), load them async via the API and re-write them.
    4) For all other tickers, async load their files.
"""
