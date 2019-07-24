import os
import shutil

import pandas as pd

from mydeep_api._deprecated.dataframe import Dataframes
from mydeep_api._deprecated.file_dataset import FileDataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareMonkeys(Worker):

    def __init__(self, col_x='x', col_y='y'):
        super().__init__()
        self.col_x = col_x
        self.col_y = col_y

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        path = ctx.root_ws.path_to('training')
        training = Dataframes.from_directory_structure(self.col_x, self.col_y)(path)
        path = ctx.root_ws.path_to('validation')
        validation = Dataframes.from_directory_structure(self.col_x, self.col_y)(path)
        df = pd.concat([training, validation], axis=0, ignore_index=True)

        for x in df[self.col_x]:
            target_path = target_ws.get_ws('images').path_to(os.path.basename(x))
            shutil.copyfile(x, target_path)
        df[self.col_x] = df[self.col_x].apply(lambda x: os.path.splitext(os.path.basename(x))[0])

        FileDataset(
            dataset=df,
            image_path_template=os.path.join(target_ws.path_to('images'), '{}.jpg')
        ).to_path(target_ws.path_to('dataset.json'))
