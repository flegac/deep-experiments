import os
import shutil

import pandas as pd

from mydeep_lib.dataframe import Dataframes
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset


class PrepareMonkeys(PipelineWorker):

    def __init__(self, col_x='x', col_y='y'):
        super().__init__('Prepare raw dataset', 'raw_dataset')
        self.col_x = col_x
        self.col_y = col_y

    def apply(self, target_ws: Workspace):
        path = self.ctx.root_ws.path_to('training')
        training = Dataframes.from_directory_structure(self.col_x, self.col_y)(path)
        path = self.ctx.root_ws.path_to('validation')
        validation = Dataframes.from_directory_structure(self.col_x, self.col_y)(path)
        df = pd.concat([training, validation], axis=0, ignore_index=True)

        for x in df[self.col_x]:
            target_path = target_ws.get_ws('images').path_to(os.path.basename(x))
            shutil.copyfile(x, target_path)
        df[self.col_x] = df[self.col_x].apply(lambda x: os.path.splitext(os.path.basename(x))[0])

        dataset = Dataset(
            dataset=df,
            images_path=target_ws.path_to('images'),
            images_ext='jpg')
        dataset.to_path(target_ws.path_to('dataset.json'))
