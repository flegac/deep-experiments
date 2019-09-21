from typing import Callable, Any, Dict

from editor_api.data.data_core import DataSource

ProcessUpdater = Callable[[float], Any]
DataProcess = Callable[[ProcessUpdater], None]
DataProcessFactory = Callable[[DataSource], DataProcess]


# TODO: make it multithread / asynchronous
class ProcessManager(object):
    def __init__(self):
        self.processes: Dict[DataProcess, float] = dict()

    def run(self, factory: DataProcessFactory, data: DataSource):
        process = factory(data)
        self.processes[process] = 0.
        process(self.create_updater(process))

    def create_updater(self, process):
        def updater(progress: float):
            self.processes[process] = progress

        return updater
