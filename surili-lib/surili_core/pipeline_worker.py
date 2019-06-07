from surili_core.pipeline_context import PipelineContext
from surili_core.workspace import Workspace


class PipelineWorker(object):
    def __init__(self, name: str, working_dir: str):
        self._ctx = None
        self.name = name
        self.working_dir = working_dir

    def __call__(self, target_ws: Workspace):
        return self.apply(target_ws)

    def apply(self, target_ws: Workspace):
        raise NotImplementedError()

    @property
    def ctx(self) -> PipelineContext:
        return self._ctx

    @ctx.setter
    def ctx(self, ctx: PipelineContext):
        self._ctx = ctx
