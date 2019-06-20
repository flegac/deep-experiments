import pandas as pd

from mydeep_lib.dataframe import Dataframes
from mydeep_train.ctx.dataset import Dataset
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace


class PrepareHistopathologicCancer(PipelineWorker):
    def __init__(self):
        super().__init__('Prepare raw dataset', 'raw_dataset')

    def apply(self, target_ws: Workspace):
        path = self.ctx.root_ws.path_to('train')
        df = Dataframes.from_csv(self.ctx.root_ws.path_to('train_labels.csv'))
        df = pd.DataFrame({
            'x': df['id'],
            'y': df['label']
        })

        dataset = Dataset(
            dataset=df,
            images_path=path,
            images_ext='tif')
        dataset.to_path(target_ws.path_to('dataset.json'))
