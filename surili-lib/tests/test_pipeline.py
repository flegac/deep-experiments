import time

from surili_core.pipelines import pipeline
from surili_core.pipeline_worker import PipelineWorker
from surili_core.pipeline_context import PipelineContext
from surili_core.workspace import Workspace


class TestWorker(PipelineWorker):
    def __init__(self):
        super().__init__("test1", "test1")

    def apply(self, target_ws: Workspace):
        time.sleep(2)


class TestWorker2(PipelineWorker):
    def __init__(self):
        super().__init__("test2", "test2")

    def apply(self, target_ws: Workspace):
        raise ValueError('CRASH !')


def test_pipeline():
    ctx = PipelineContext("/tmp/test/pipelines", "test_project")
    pipe = pipeline([
        TestWorker(),
        TestWorker2(),
        TestWorker(),
    ])
    pipe(ctx)


test_pipeline()
