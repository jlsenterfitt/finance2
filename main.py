"""Module to call other functions, and handle flags."""

import argparse
import config
from data_gatherer import data_gatherer


parser = argparse.ArgumentParser()
parser.add_argument(
    '--refresh_strategy',
    choices=['outdated', 'none', 'all'],
    default='outdated',
    help='What tickers to update.')


def main():
    args = parser.parse_args()

    ticker_data = data_gatherer.getTickerData(
        set(config.TICKER_DICT.keys()),
        config.API_KEY,
        'cache',
        args.refresh_strategy)


if __name__ == '__main__':
    main()

