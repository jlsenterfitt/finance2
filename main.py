"""Module to call other functions, and handle flags."""

import argparse
from collections import OrderedDict
from copy import deepcopy
import config
from data_cleaner import data_cleaner
from data_gatherer import data_gatherer
import datetime
import math
from optimizer import optimizer
import time
from trader import trader


parser = argparse.ArgumentParser()
parser.add_argument(
    '--refresh_strategy',
    choices=['outdated', 'none', 'all'],
    default='outdated',
    help='What tickers to update.')
parser.add_argument(
    '--required_num_days',
    type=int, help='How many days are required.',
    default=config.TRADING_DAYS_PER_YEAR * 14)
parser.add_argument(
    '--required_return',
    type=float,
    help='What return to require.')
parser.add_argument(
    '--set_start_date',
    help='What date to run the optimizer every 3 months from.')
parser.add_argument(
    '--set_date',
    help='A single date to run the optimizer for.')


def _printAllocMap(allocation_map):
    filtered_map = {k: v for k, v in allocation_map.items() if v > 0}
    ordered_map = OrderedDict(sorted(filtered_map.items()))
    print(ordered_map)


def main():
    args = parser.parse_args()

    if not args.required_return:
        raise ValueError('Need to set required return')
    daily_return = math.pow(args.required_return, 1 / config.TRADING_DAYS_PER_YEAR)

    # Load full, unfiltered, and less than 1 month old data.
    start = time.time()
    ticker_data = data_gatherer.getTickerData(
        set(config.TICKER_DICT.keys()),
        config.API_KEY,
        'cache',
        args.refresh_strategy)
    print('Getting data took %.2fs' % (time.time() - start))

    # Run the optimizer for required date(s).
    allocation_map = {}
    epoch = datetime.datetime.utcfromtimestamp(0)
    optimized_list = []
    start = time.time()
    if args.set_start_date:
        start_date_int = (datetime.datetime.strptime(args.set_start_date, '%Y-%m-%d') - epoch).days
        today_int = (datetime.datetime.now() - epoch).days
        while start_date_int < today_int:
            (ticker_tuple, data_matrix) = data_cleaner.cleanAndConvertData(deepcopy(ticker_data), args.required_num_days, start_date_int)
            (best_score, allocation_map) = optimizer.findOptimalAllocation(data_matrix, ticker_tuple, daily_return)
            optimized_list.append((start_date_int, allocation_map))
            print(datetime.date.fromtimestamp(start_date_int * 24 * 3600))
            _printAllocMap(allocation_map)
            # Add ~3 months of trading days.
            start_date_int += 365 / 4
    elif args.set_date:
        date_int = (datetime.datetime.strptime(args.set_date, '%Y-%m-%d') - epoch).days
        (ticker_tuple, data_matrix) = data_cleaner.cleanAndConvertData(deepcopy(ticker_data), args.required_num_days, date_int)
        print('Cleaning data took %.2fs' % (time.time() - start))
        (best_score, allocation_map) = optimizer.findOptimalAllocation(data_matrix, ticker_tuple, daily_return)
        _printAllocMap(allocation_map)
        print('Score: %.4f' % best_score)
        trader.calculateTrades(allocation_map, config.CURRENT_ALLOCATION_DICT, ticker_tuple, data_matrix)
    else:
        date_int = (datetime.datetime.now() - epoch).days
        (ticker_tuple, data_matrix) = data_cleaner.cleanAndConvertData(deepcopy(ticker_data), args.required_num_days, date_int)
        print('Cleaning data took %.2fs' % (time.time() - start))
        (best_score, allocation_map) = optimizer.findOptimalAllocation(data_matrix, ticker_tuple, daily_return)
        _printAllocMap(allocation_map)
        print('Score: %.4f' % best_score)
        trader.calculateTrades(allocation_map, config.CURRENT_ALLOCATION_DICT, ticker_tuple, data_matrix)

    # Run the backtester across all optimizations.


if __name__ == '__main__':
    main()

