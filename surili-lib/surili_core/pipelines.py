import os
import traceback
from typing import List, Callable, Any

import time

from surili_core.pipeline_context import PipelineContext
from surili_core.pipeline_worker import Worker
from surili_core.workspace import Workspace


def pipeline_step(worker: Worker) -> Callable[[PipelineContext], PipelineContext]:
    def log(msg: str):
        print('{}: {}'.format(worker.name, msg))

    def apply(ctx: PipelineContext):
        try:
            log('----- START -------------------')
            target_ws = ctx.project_ws.get_ws(worker.working_dir)

            log('check folder : {}'.format(target_ws.path))
            start = time.time()
            if os.path.exists(target_ws.path_to('.done')):
                log('SKIPPED : (nothing to do)')
                return ctx

            log('start worker...')
            worker(ctx, target_ws)
            total_time = time.time() - start
            target_ws.touch('.done', content={
                'time': total_time
            })
            return ctx
        except Exception as e:
            log('ERROR : {}'.format(e))
            raise e
        finally:
            log('----- DONE --------------------')

    return apply


def step(name: str, working_dir: str, worker: Callable[[PipelineContext, Workspace], Any]):
    return Worker(name, working_dir, worker)


def pipeline(workers: List[Worker]):
    def _pipeline(ctx: PipelineContext):
        try:
            for worker in workers:
                ctx = pipeline_step(worker)(ctx)
            return ctx
        except:
            print(traceback.format_exc())

    return _pipeline
