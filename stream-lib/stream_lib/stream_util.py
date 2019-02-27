import os
import pickle
import random
from typing import TypeVar, Callable

from stream_lib.stream import stream, Stream

IN = TypeVar('IN')
OUT = TypeVar('OUT')


def cache(path: str, invalidate=False):
    def apply(flow: Stream[IN]) -> Stream[IN]:
        if not os.path.exists(path) or invalidate:
            with open(path, 'wb') as _:
                for x in flow:
                    pickle.dump(x, _)

        def file_stream():
            with open(path, 'rb') as _:
                while True:
                    yield pickle.load(_)

        return stream(file_stream())

    return apply


def batch(batch_size: int):
    def apply(flow: Stream[IN]) -> Stream[IN]:
        def new_stream():
            buffer = []
            for x in flow:
                buffer.append(x)
                if len(buffer) == batch_size:
                    yield buffer
                    buffer = []
            if len(buffer) > 0:
                yield buffer

        return stream(new_stream())

    return apply


def shuffle(buffer_size):
    def apply(flow: Stream[IN]) -> Stream[IN]:
        if buffer_size is None or buffer_size <= 0:
            return flow

        def new_stream():
            buffer = []
            for x in flow:
                buffer.append(x)
                if len(buffer) == buffer_size:
                    random.shuffle(buffer)
                    for y in buffer:
                        yield y
                    buffer = []
            for x in buffer:
                yield x

        return stream(new_stream())

    return apply


def to_stream(func: Callable[[IN], OUT]) -> Callable[[Stream[IN]], Stream[OUT]]:
    def apply(flux: Stream[IN]) -> Stream[OUT]:
        return flux.map(func)

    return apply
