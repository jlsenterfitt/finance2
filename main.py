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
    '--set_dates',
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


if __name__ == '__main__':
    main()

