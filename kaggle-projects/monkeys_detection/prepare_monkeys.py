import os
import shutil

import pandas as pd

from mydeep_lib.dataframe import Dataframes
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset


class PrepareMonkeys(PipelineWorker):

    def __init__(self):
        super().__init__('Prepare raw dataset', 'raw_dataset')

    def apply(self, target_ws: Workspace):
        path = self.ctx.root_ws.path_to('training')
        training = Dataframes.from_directory_structure('x', 'y')(path)
        path = self.ctx.root_ws.path_to('validation')
        validation = Dataframes.from_directory_structure('x', 'y')(path)
        df = pd.concat([training, validation], axis=0, ignore_index=True)

        for x in df['x']:
            shutil.copyfile(x, target_ws.get_ws('images').path_to(os.path.basename(x)))
            df['x'] = df['x'].apply(lambda x: os.path.splitext(os.path.basename(x))[0])

        dataset = Dataset(
            dataset=df,
            images_path=target_ws.path_to('images'),
            images_ext='jpg')
        dataset.to_path(target_ws.path_to('dataset.json'))
