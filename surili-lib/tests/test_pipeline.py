from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline, step
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def test_pipeline():
    class MyWorker(Worker):

        def run(self, ctx: str, ws: Workspace):
            print('my personal worker : ctx={}'.format(str(ctx)))

    context = PipelineContext(project_name='test', root_path='generated/my_workspace')
    with context.workspace:
        pipeline(
            steps=[
                step(step_id='step_01', worker=None),
                step(step_id='step_02', worker=lambda ctx, ws: print('ok STEP 2')),
                step(step_id='step_03', worker=MyWorker())
            ]
        )(context)
