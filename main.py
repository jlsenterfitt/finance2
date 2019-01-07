"""Module to call other functions, and handle flags."""

import argparse
from collections import defaultdict
from collections import OrderedDict
from copy import deepcopy
import config
from data_cleaner import data_cleaner
from data_gatherer import data_gatherer
import datetime
import math
import numpy as np
from optimizer import optimizer
from scipy.stats.mstats import gmean
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
    default=config.TRADING_DAYS_PER_YEAR * 3)
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


def _runSingleDay(date_int, ticker_data, daily_return, required_num_days, perform_trades=True):
    start = time.time()
    (ticker_tuple, data_matrix) = data_cleaner.cleanAndConvertData(deepcopy(ticker_data), required_num_days, date_int)
    print('Cleaning data took %.2fs' % (time.time() - start))
    start = time.time()
    (best_score, allocation_map) = optimizer.findOptimalAllocation(data_matrix, ticker_tuple, daily_return)
    print('Optimization took %.2fs' % (time.time() - start))

    if not perform_trades: return allocation_map

    _printAllocMap(allocation_map)
    print('Score: %.4f' % best_score)
    small_ticker_data = {ticker: data for ticker, data in ticker_data.items() if ticker in allocation_map or ticker in config.CURRENT_ALLOCATION_DICT}
    (small_ticker_tuple, small_data_matrix) = data_cleaner.cleanAndConvertData(small_ticker_data, 1, date_int)
    trader.calculateTrades(allocation_map, config.CURRENT_ALLOCATION_DICT, small_ticker_tuple, small_data_matrix)


def _runBacktest(allocation_map, ticker_data, start_date_int, next_date_int):
    small_ticker_data = {ticker: data for ticker, data in ticker_data.items() if ticker in allocation_map}
    (small_ticker_tuple, small_data_matrix) = data_cleaner.cleanAndConvertData(
            small_ticker_data, 1, next_date_int, first_date=start_date_int)
    allocation_map = defaultdict(int, allocation_map)
    small_allocation_array = np.array([allocation_map[ticker] for ticker in small_ticker_tuple], dtype=np.float64)
    performance = gmean(np.matmul(small_data_matrix, small_allocation_array))
    return performance


def _roughScore(return_list, required_return):
    print(return_list)
    return_list = np.array(return_list, dtype=np.float64)
    mean_return = gmean(return_list)

    # Short-circuit score calculation when mean_return < required_return.
    # Otherwise, with a negative denominator, the code will push for a
    # large denominator to maximize the overall score.
    if mean_return < required_return:
        return mean_return - required_return

    filtered_returns = np.copy(return_list)
    filtered_returns -= required_return
    filtered_returns = np.clip(filtered_returns, None, 0)
    filtered_returns *= filtered_returns
    downside_risk = np.sqrt(filtered_returns.mean())

    return (mean_return - required_return) / downside_risk


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
    epoch = datetime.datetime.utcfromtimestamp(0)
    optimized_list = []
    if args.set_start_date:
        start_date_int = (datetime.datetime.strptime(args.set_start_date, '%Y-%m-%d') - epoch).days
        today_int = (datetime.datetime.now() - epoch).days
        while start_date_int < today_int:
            allocation_map = _runSingleDay(start_date_int, deepcopy(ticker_data), daily_return, args.required_num_days, perform_trades=False)
            print(datetime.date.fromtimestamp(start_date_int * 24 * 3600))
            _printAllocMap(allocation_map)
            new_perf = _runBacktest(allocation_map, deepcopy(ticker_data), start_date_int, start_date_int + 365 / 4)
            optimized_list.append(new_perf)
            # Add ~3 months of trading days.
            start_date_int += 365 / 4
        print('Score: %.4f' % _roughScore(optimized_list, daily_return))
    elif args.set_date:
        date_int = (datetime.datetime.strptime(args.set_date, '%Y-%m-%d') - epoch).days
        _runSingleDay(date_int, deepcopy(ticker_data), daily_return, args.required_num_days)
    else:
        date_int = (datetime.datetime.now() - epoch).days
        _runSingleDay(date_int, deepcopy(ticker_data), daily_return, args.required_num_days)

    # Run the backtester across all optimizations.


if __name__ == '__main__':
    main()

