import basicMain
import multiprocessing as mp
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
    except:
        score = -100
    with index.get_lock():
        index.value += 1
        print('\n\nFinished %d\n\n' % index.value)
    return '%.4f %d %s %.4f' % (
        kwargs['desired_return'],
        kwargs['num_days'],
        kwargs['use_downside_correl'],
        score)


def main():
    output = []
    start = time.time()
    try:
        with mp.Pool() as pool:
            arg_list = []
            """
            for desired_return in [1.0761]:
                for num_years in range(20, 0, -1):
                    for use_downside_correl in [False]:
                        kwargs = {
                            'desired_return': desired_return,
                            'num_days': 253 * num_years,
                            'use_downside_correl': use_downside_correl,
                            }
                        arg_list.append(kwargs)
            """
            arg_list = [
                {'desired_return': 1.0561, 'num_days': 253 * 1, 'use_downside_correl': False, 'date': '2000-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 2, 'use_downside_correl': False, 'date': '2001-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 3, 'use_downside_correl': False, 'date': '2002-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 4, 'use_downside_correl': False, 'date': '2003-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 5, 'use_downside_correl': False, 'date': '2004-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 6, 'use_downside_correl': False, 'date': '2005-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 7, 'use_downside_correl': False, 'date': '2006-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 8, 'use_downside_correl': False, 'date': '2007-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 9, 'use_downside_correl': False, 'date': '2008-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 10, 'use_downside_correl': False, 'date': '2009-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 11, 'use_downside_correl': False, 'date': '2010-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 12, 'use_downside_correl': False, 'date': '2011-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 13, 'use_downside_correl': False, 'date': '2012-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 14, 'use_downside_correl': False, 'date': '2013-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 15, 'use_downside_correl': False, 'date': '2014-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 16, 'use_downside_correl': False, 'date': '2015-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 17, 'use_downside_correl': False, 'date': '2016-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 18, 'use_downside_correl': False, 'date': '2017-01-01'},
                {'desired_return': 1.0561, 'num_days': 253 * 19, 'use_downside_correl': False, 'date': '2018-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 1, 'use_downside_correl': False, 'date': '2000-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 2, 'use_downside_correl': False, 'date': '2001-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 3, 'use_downside_correl': False, 'date': '2002-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 4, 'use_downside_correl': False, 'date': '2003-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 5, 'use_downside_correl': False, 'date': '2004-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 6, 'use_downside_correl': False, 'date': '2005-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 7, 'use_downside_correl': False, 'date': '2006-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 8, 'use_downside_correl': False, 'date': '2007-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 9, 'use_downside_correl': False, 'date': '2008-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 10, 'use_downside_correl': False, 'date': '2009-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 11, 'use_downside_correl': False, 'date': '2010-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 12, 'use_downside_correl': False, 'date': '2011-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 13, 'use_downside_correl': False, 'date': '2012-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 14, 'use_downside_correl': False, 'date': '2013-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 15, 'use_downside_correl': False, 'date': '2014-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 16, 'use_downside_correl': False, 'date': '2015-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 17, 'use_downside_correl': False, 'date': '2016-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 18, 'use_downside_correl': False, 'date': '2017-01-01'},
                {'desired_return': 1.0661, 'num_days': 253 * 19, 'use_downside_correl': False, 'date': '2018-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 1, 'use_downside_correl': False, 'date': '2000-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 2, 'use_downside_correl': False, 'date': '2001-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 3, 'use_downside_correl': False, 'date': '2002-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 4, 'use_downside_correl': False, 'date': '2003-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 5, 'use_downside_correl': False, 'date': '2004-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 6, 'use_downside_correl': False, 'date': '2005-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 7, 'use_downside_correl': False, 'date': '2006-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 8, 'use_downside_correl': False, 'date': '2007-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 9, 'use_downside_correl': False, 'date': '2008-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 10, 'use_downside_correl': False, 'date': '2009-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 11, 'use_downside_correl': False, 'date': '2010-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 12, 'use_downside_correl': False, 'date': '2011-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 13, 'use_downside_correl': False, 'date': '2012-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 14, 'use_downside_correl': False, 'date': '2013-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 15, 'use_downside_correl': False, 'date': '2014-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 16, 'use_downside_correl': False, 'date': '2015-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 17, 'use_downside_correl': False, 'date': '2016-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 18, 'use_downside_correl': False, 'date': '2017-01-01'},
                {'desired_return': 1.0761, 'num_days': 253 * 19, 'use_downside_correl': False, 'date': '2018-01-01'},
                ]
            print('Running %d experiments.' % len(arg_list))
            output = pool.map(_poolMain, arg_list, 1)
    finally:
        print('Return Years Correl Score')
        print('\n'.join(sorted(output)))
        print('Took %.2fs' % (time.time() - start))


if __name__ == '__main__':
    main()
