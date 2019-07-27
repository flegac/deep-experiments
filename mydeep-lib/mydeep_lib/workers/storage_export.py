from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class StorageExport(Worker):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def run(self, ctx: PipelineContext, ws: Workspace):
        ctx.workspace.to_storage(self.storage_path)
