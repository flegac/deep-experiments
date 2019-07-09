from surili_core.pipelines_v2.pipelines import pipeline, step
from surili_core.pipelines_v2.worker import Worker
from surili_core.workspace import Workspace


def test_pipeline_v2():
    class MyWorker(Worker):

        def run(self, ctx: str, ws: Workspace):
            print('my personal worker : ctx={}'.format(str(ctx)))

    pipeline(
        ctx={'a': 3},
        steps=[
            step(step_id='step_01', worker=None),
            step(step_id='step_02', worker=lambda ctx, ws: print('ok STEP 2')),
            step(step_id='step_03', worker=MyWorker())
        ]
    )(Workspace.from_path('my_workspace'))
