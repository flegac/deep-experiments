import os

import pandas as pd

from mydeep_api._deprecated.file_dataset import FileDataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareHistopathologicCancer(Worker):

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        path = ctx.root_ws.path_to('train')
        df = pd.read_csv(ctx.root_ws.path_to('train_labels.csv'))
        df = pd.DataFrame({
            'x': df['id'],
            'y': df['label']
        })

        FileDataset(
            dataset=df,
            image_path_template=os.path.join(path, '{}.tif')
        ).to_path(target_ws.path_to('dataset.json'))
