# from functional import seq

import concurrent.futures
import time

import rx

seconds = [5, 1, 2, 4, 3]


def sleep(tm):
    time.sleep(tm)
    return tm


def output(result):
    print('%d seconds' % result)


with concurrent.futures.ProcessPoolExecutor(5) as executor:
    rx.from_(seconds).pipe(
        rx.operators.flat_map(lambda s: executor.submit(sleep, s))
    ).subscribe(output)
