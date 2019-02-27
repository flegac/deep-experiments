import os
import traceback
from typing import List, Callable

import time

from surili_core.pipeline_context import PipelineContext
from surili_core.pipeline_worker import PipelineWorker


def pipeline_step(worker: PipelineWorker) -> Callable[[PipelineContext], PipelineContext]:
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
            worker.ctx = ctx
            worker(target_ws)
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


def pipeline(steps: List[PipelineWorker]):
    def _pipeline(ctx: PipelineContext):
        try:
            for step in steps:
                ctx = pipeline_step(step)(ctx)
            return ctx
        except:
            print(traceback.format_exc())

    return _pipeline
