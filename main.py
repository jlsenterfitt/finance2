"""Module to call other functions, and handle flags."""

import config
from data_gatherer import data_gatherer


def main():
    data_gatherer.getTickerData(
        set(config.TICKER_DICT.keys()), config.API_KEY, 'cache/')


if __name__ == '__main__':
    main()

