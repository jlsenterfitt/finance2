import basicMain
import multiprocessing as mp
import time


output = []


def _poolMain(kwargs):
    score = basicMain.actualMain(
            kwargs['desired_return'],
            'none',
            kwargs['num_days'],
            '2007-01-01',
            None,
            kwargs['use_downside_correl'])
    output.append('%.4f %d %s %.4f' % (
        kwargs['desired_return'],
        kwargs['num_days'],
        kwargs['use_downside_correl'],
        score))


def main():
    output = []
    start = time.time()
    try:
        with mp.Pool() as pool:
            arg_list = []
            for desired_return in [1.0561, 1.0661, 1.0761, 1.0861, 1.0961]:
                for num_years in range(8, 0, -1):
                    for use_downside_correl in [False]:
                        kwargs = {
                            'desired_return': desired_return,
                            'num_days': 253 * num_years,
                            'use_downside_correl': use_downside_correl
                            }
                        arg_list.append(kwargs)
            pool.map(_poolMain, arg_list, 1)
    finally:
        print('Return Years Correl Score')
        print('\n'.join(output))
        print('Took %.2fs' % (time.time() - start))


if __name__ == '__main__':
    main()
