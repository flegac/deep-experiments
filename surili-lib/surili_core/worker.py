from abc import ABC
from typing import Callable

from surili_core.workspace import Workspace


class Worker(ABC, Callable[[Workspace], None]):
    def __call__(self, ws: Workspace):
        return self.run(ws)

    def run(self, ws: Workspace):
        raise NotImplementedError()
