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
