import collections
from functools import partial
from typing import Iterator, Callable, List, Any, TypeVar, Generic, Tuple

from tqdm import tqdm

T = TypeVar('T')
U = TypeVar('U')


class Stream(Iterator[T]):
    @staticmethod
    def stream_identity(x: 'Stream[T]') -> 'Stream[T]':
        return x

    @staticmethod
    def stream(*iterables) -> 'Stream[T]':
        raise NotImplementedError()

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        raise NotImplementedError()

    def apply(self, func: Callable[[Iterator[T]], Iterator[U]]) -> 'Stream[U]':
        new_stream = func(self)
        if isinstance(new_stream, Stream):
            return new_stream
        return self._stream(new_stream)

    def apply_partial(self, func: Callable, *args, **kwargs):
        func = _update_func(func, *args, **kwargs)
        return self.apply(func)

    def map(self, func: Callable[[T], U]) -> 'Stream[U]':
        raise NotImplementedError()

    def map_partial(self, func: Callable, *args, **kwargs):
        func = _update_func(func, *args, **kwargs)
        return self.map(func)

    def flatmap(self, func: Callable[[T], 'Stream[U]']) -> 'Stream[U]':
        raise NotImplementedError()

    def flatmap_partial(self, func: Callable, *args, **kwargs):
        func = _update_func(func, *args, **kwargs)
        return self.flatmap(func)

    def filter(self, predicate: Callable[[T], bool]) -> 'Stream[T]':
        raise NotImplementedError()

    def filter_partial(self, predicate: Callable, *args, **kwargs):
        func = _update_func(predicate, *args, **kwargs)
        return self.filter(func)

    def slice(self, start: int, stop: int, step: int = 1) -> 'Stream[T]':
        raise NotImplementedError()

    def limit(self, size: int) -> 'Stream[T]':
        return self.slice(0, size)

    def flatten(self) -> 'Stream[U]':
        return self.flatmap(Stream[U].stream_identity)

    def enumerate(self) -> 'Stream[Tuple[int,T]]':
        return self._stream(enumerate(self))

    def side_effect(self, func: Callable[[T], Any]) -> 'Stream[T]':
        def apply(data):
            func(data)
            return data

        return self.map(apply)

    def _stream(self, *iterables) -> 'Stream':
        return self.__class__.stream(*iterables)

    # terminal operations ---------------------------------
    def reduce(self, initial_value: U, reduce_func: Callable[[U, T], U]) -> U:
        acc = initial_value
        for x in tqdm(self):
            acc = reduce_func(acc, x)
        return acc

    def foreach(self, func: Callable) -> None:
        for x in tqdm(self):
            func(x)

    def to_list(self) -> List[T]:
        return [x for x in tqdm(self)]

    def count(self) -> int:
        """
        https://gist.github.com/NelsonMinar/90212fbbfc6465c8e263341b86aa01a8
        """
        d = collections.deque(enumerate(self, 1), maxlen=1)
        return d[0][0] if d else 0


class StreamProvider(Generic[T]):
    def stream(self) -> Stream[T]:
        raise NotImplementedError()

    def __call__(self):
        return self.stream()


def _update_func(func: Callable, *args, **kwargs):
    if args or kwargs:
        return partial(func, *args, **kwargs)
    return func
