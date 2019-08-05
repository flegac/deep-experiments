import filecmp
import inspect
import os
import shutil
import time
from typing import Callable, Optional, List

from surili_core.worker import Worker
from surili_core.workspace import Workspace

StepWorker = Callable[[Workspace], None]


def step(step_id: str, worker: Optional[Worker]) -> StepWorker:
    def log(msg: str):
        print('{}: {}'.format(step_id, msg))

    def run(ws: Workspace):
        try:
            log('----- START {} -------------------'.format(step_id))
            current_ws = ws.get_ws(step_id)

            log('check folder : {}'.format(current_ws.path))
            start = time.time()
            if os.path.exists(current_ws.path_to('.done')):
                log('SKIPPED : rm {}'.format(current_ws.path_to('.done')))
                return

            log('start worker...')
            if worker is not None:
                worker(current_ws)
            total_time = time.time() - start
            current_ws.create_file('.done', content={
                'time': total_time
            })
            log('SUCCESS !'.format(step_id))
            return
        except Exception as e:
            log('FAILLED : {}'.format(e))
            raise e
        finally:
            log('----- DONE {} --------------------'.format(step_id))

    return run


def pipeline(steps: List[StepWorker]):
    def run(ws: Workspace):
        running_script_path = _get_running_script_path()
        script_destination_path = ws.path_to('script.py.txt')
        if not os.path.exists(script_destination_path):
            shutil.copyfile(running_script_path, script_destination_path)
        elif not filecmp.cmp(running_script_path, script_destination_path, shallow=False):
            raise ValueError('Existing project, but running script has changed : rm {}'.format(script_destination_path))

        for step in steps:
            step(ws)

    return run


def _get_running_script_path():
    return os.path.abspath(inspect.stack()[-1][1])
