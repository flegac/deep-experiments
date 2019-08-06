import os

from surili_core.pipelines import pipeline, step
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def test_pipeline():
    class MyWorker(Worker):

        def run(self, ws: Workspace):
            assert ws.path != ws.root.path
            assert ws.path.startswith(ws.root.path)

            print('my personal worker : ws={}'.format(str(ws)))

    with Workspace.from_path('generated/my_workspace/test') as _:
        assert os.path.exists(_.path)

        pipeline(
            steps=[
                step(step_id='step_01', worker=None),
                step(step_id='step_02', worker=lambda ws: print('ok STEP 2')),
                step(step_id='step_03', worker=MyWorker())
            ]
        )(_)
        assert os.path.exists(_.path_to('out.txt'))
        assert os.path.exists(_.path_to('err.txt'))

    assert not os.path.exists(_.path)
