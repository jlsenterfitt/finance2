"""Module to call other functions, and handle flags."""

import argparse
import config
from data_gatherer import data_gatherer
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument(
    '--refresh_strategy',
    choices=['outdated', 'none', 'all'],
    default='outdated',
    help='What tickers to update.')
parser.add_argument(
    '--set_start_date',
    help='What date to run the optimizer every 3 months from.')
parser.add_argument(
    '--set_date',
    help='A single date to run the optimizer for.')


def main():
    args = parser.parse_args()

    # Load full, unfiltered, and less than 1 month old data.
    ticker_data = data_gatherer.getTickerData(
        set(config.TICKER_DICT.keys()),
        config.API_KEY,
        'cache',
        args.refresh_strategy)

    # Run the optimizer for required date(s).
    allocation_map = {}
    epoch = datetime.datetime.utcfromtimestamp(0)
    if args.set_start_date:
        start_date_int = (datetime.datetime.strptime(args.set_start_date, '%Y-%m-%d') - epoch).days
        today_int = (datetime.datetime.now() - epoch).days
        while start_date_int < today_int:
            # Do somoething.
            # Add ~3 months of trading days.
            start_date_int += config.TRADING_DAYS_PER_YEAR / 4
        pass
    elif args.set_date:
        date_int = (datetime.datetime.strptime(args.set_date, '%Y-%m-%d') - epoch).days
        pass
    else:
        date_int = (datetime.datetime.now() - epoch).days
        pass

    # Calculate trades for the most recent optimization.
    trades = []

    # Run the backtester across all optimizations.


if __name__ == '__main__':
    main()

