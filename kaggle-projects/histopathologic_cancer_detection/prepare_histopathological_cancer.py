import pandas as pd

from mydeep_lib.dataframe import Dataframes
from mydeep_lib.dataset import Dataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareHistopathologicCancer(Worker):
    def __init__(self):
        super().__init__('Prepare raw dataset', 'raw_dataset')

    def apply(self, ctx: PipelineContext, target_ws: Workspace):
        path = ctx.root_ws.path_to('train')
        df = Dataframes.from_csv(ctx.root_ws.path_to('train_labels.csv'))
        df = pd.DataFrame({
            'x': df['id'],
            'y': df['label']
        })

        dataset = Dataset(
            dataset=df,
            images_path=path,
            images_ext='tif')
        dataset.to_path(target_ws.path_to('dataset.json'))
