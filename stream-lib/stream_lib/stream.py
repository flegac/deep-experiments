from typing import TypeVar, Iterator

from stream_lib.itertools_stream import ItertoolsStream
from stream_lib.stream_api import Stream, StreamProvider

T = TypeVar('T')


def stream(*iterables: Iterator[T]) -> Stream[T]:
    return ItertoolsStream.stream(*iterables)


__all__ = ['stream', 'Stream', 'StreamProvider']
