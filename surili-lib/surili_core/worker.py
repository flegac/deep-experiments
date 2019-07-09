from typing import Any, Callable

from surili_core.pipeline_context import PipelineContext
from surili_core.workspace import Workspace


class Worker(object):
    def __init__(self, name: str, working_dir: str, worker: Callable[[PipelineContext, Workspace], Any] = None):
        self.name = name
        self.working_dir = working_dir
        self.worker = worker

    def __call__(self, ctx: PipelineContext, target_ws: Workspace):
        return self.apply(ctx, target_ws)

    def apply(self, context: PipelineContext, target_ws: Workspace):
        if not self.worker:
            raise NotImplementedError()
        return self.worker(context, target_ws)
