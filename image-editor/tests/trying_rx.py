import multiprocessing
import time

import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler


def toto():
    rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon").pipe(
        ops.map(lambda s: len(s)),
        ops.filter(lambda i: i >= 5)
    ).subscribe(lambda value: print("Received {0}".format(value)))

    rx.from_([1, 2]).subscribe(lambda value: print("Received {0}".format(value)))

    def generator(observer, scheduler):
        while True:
            time.sleep(1)
            observer.on_next('toto')

    rx.create(generator).subscribe(lambda value: print("Received {0}".format(value)))

    # rx.interval(.1).pipe(
    #     # ops.debounce(2),
    #     ops.throttle_first(1.2)
    # ).subscribe(lambda value: print("Received {0}".format(value)))

    while True:
        pass


optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)


def create(label):
    def generator(observer, scheduler):
        while True:
            time.sleep(.7)
            observer.on_next(label)

    return generator


rx.create(create('toto')).pipe(
    ops.subscribe_on(pool_scheduler),

    ops.merge(rx.create(create('tata'))),

).subscribe(print)

while True:
    pass
