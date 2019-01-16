import basicMain
import datetime
import multiprocessing as mp
from random import shuffle
import time


index = mp.Value('d', 0)


def _poolMain(kwargs):
    try:
        score = basicMain.actualMain(
            kwargs['desired_return'],
            'none',
            kwargs['num_days'],
            kwargs['date'],
            None,
            kwargs['use_downside_correl'])
    except Exception as e:
        score = -100
        print(kwargs)
        print(e)
        raise e
    with index.get_lock():
        index.value += 1
        print('\n\nFinished %d' % index.value)
    return_str = '%.4f %d %s %.4f' % (
        kwargs['desired_return'],
        kwargs['num_days'],
        kwargs['use_downside_correl'],
        score)
    print(return_str)
    print('\n')
    return return_str


def main():
    output = []
    start = time.time()
    try:
        with mp.Pool() as pool:
            num_years = 1
            quarter = 0
            arg_list = []
            while num_years < 14:
                date_str = '%d-%d-01' % (2004 + num_years, (12 * quarter) + 1)
                num_days = 253 * (num_years + quarter)
                arg_list.append({
                    'desired_return': 1.0747,
                    'num_days': num_days,
                    'use_downside_correl': False,
                    'date': date_str})
                quarter += 0.25
                if quarter == 1:
                    quarter = 0
                    num_years += 1
            
            shuffle(arg_list)
            print('Running %d experiments.' % len(arg_list))
            output = pool.map(_poolMain, arg_list, 1)
    finally:
        print('Return Years Correl Score')
        print('\n'.join(sorted(output)))
        print('Took %.2fs' % (time.time() - start))


if __name__ == '__main__':
    main()
