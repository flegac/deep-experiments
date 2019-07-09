import numpy as np

from stream_lib import stream_util
from stream_lib.stream import *


def test_cache():
    sequence = list(range(3))

    # count sequence 0 and save it to a cache
    n0 = stream(sequence) \
        .apply(stream_util.cache('/tmp/stream_cache')) \
        .count()
    assert n0 == len(sequence)

    # modify stream data
    sequence.append(4)

    # check expected result
    n2 = stream(sequence).count()
    assert n2 == len(sequence)

    # count elements with cached data
    n1 = stream(sequence).apply(stream_util.cache('/tmp/stream_cache')).count()
    assert n1 == n0  # incoherent result ... but the cache is working


def test_batch():
    stream_provider = lambda: stream(range(10)) \
        .map(lambda x: np.zeros((2, 2))) \
        .apply(stream_util.batch(4)) \
        .map(lambda x: np.array(x))

    batch_of_4 = stream_provider() \
        .filter(lambda x: x.shape == (4, 2, 2)) \
        .count()

    batch_of_2 = stream_provider() \
        .filter(lambda x: x.shape == (2, 2, 2)) \
        .count()

    assert batch_of_4 == 2
    assert batch_of_2 == 1


def test_shuffle():
    stream_provider = lambda: stream(range(100)).apply(stream_util.shuffle(50))

    left = list(stream_provider().slice(start=0, stop=50))
    right = list(stream_provider().slice(start=50, stop=100))

    assert left != list(range(50))
    assert sorted(left) == list(range(50))

    assert sorted(right) == list(range(50, 100))
    assert right != list(range(50, 100))
