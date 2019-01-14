import argparse
import config
from data_gatherer import data_gatherer
import time


parser = argparse.ArgumentParser()
parser.add_argument(
    '--refresh_strategy',
    choices=['outdated', 'none', 'all'],
    default='all',
    help='What tickers to update.')


def main():
    args = parser.parse_args()

    start = time.time()
    ticker_data = data_gatherer.getTickerData(
        set(config.TICKER_DICT.keys()),
        config.API_KEY,
        'cache',
        args.refresh_strategy)
    print('Getting data took %.2fs' % (time.time() - start))


if __name__ == '__main__':
    main()

