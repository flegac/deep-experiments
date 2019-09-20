import time

import rx
from rx import operators as ops


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
