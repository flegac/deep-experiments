import os

from surili_core.worker import Worker, T
from surili_core.workspace import Workspace


class StorageImport(Worker):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def run(self, ctx: T, ws: Workspace):
        ws.from_storage(self.storage_path)
        archive_name = os.path.basename(self.storage_path)
        ws.extract(ws.path_to(archive_name))
