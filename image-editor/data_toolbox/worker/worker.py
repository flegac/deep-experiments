import abc
from pathlib import Path


class Worker(abc.ABC):
    def work(self, workspace: Path):
        raise NotImplementedError()


