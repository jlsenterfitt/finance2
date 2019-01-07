import basicMain
import time


def main():
    output = []
    start = time.time()
    for desired_return in [1.0561, 1.0661, 1.0761, 1.0861, 1.0961]:
        for num_years in range(1, 4):
            for use_downside_correl in [True, False]:
                score = basicMain.actualMain(desired_return, 'none', 253 * num_years, '2007-01-01', None, use_downside_correl=use_downside_correl)
                output.append('%.4f %d %s %.4f' % (desired_return, num_years, use_downside_correl, score))
    print('Return Years Correl Score')
    print('\n'.join(output))
    print('Took %.2fs' % (time.time() - start))


if __name__ == '__main__':
    main()
