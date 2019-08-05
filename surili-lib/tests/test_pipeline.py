from surili_core.pipelines import pipeline, step
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def test_pipeline():
    class MyWorker(Worker):

        def run(self, ws: Workspace):
            print('my personal worker : ws={}'.format(str(ws)))

    with Workspace.from_path('generated/my_workspace/test') as _:
        pipeline(
            steps=[
                step(step_id='step_01', worker=None),
                step(step_id='step_02', worker=lambda ws: print('ok STEP 2')),
                step(step_id='step_03', worker=MyWorker())
            ]
        )(_)
