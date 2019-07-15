from abc import ABC
from typing import Callable, TypeVar

from surili_core.workspace import Workspace

T = TypeVar('T')


class Worker(ABC, Callable[[T, Workspace], None]):
    def __call__(self, ctx: T, ws: Workspace):
        return self.run(ctx, ws)

    def run(self, ctx: T, ws: Workspace):
        raise NotImplementedError()
