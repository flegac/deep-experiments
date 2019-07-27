import pandas as pd

from mydeep_api._deprecated.file_dataset import FileDataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareHistopathologicCancer(Worker):
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        dataset_ws = target_ws.parent.get_ws(self.dataset_path)

        target_ws.get_ws('train').extract(dataset_ws.path_to('train.zip'))
        target_ws.get_ws('test').extract(dataset_ws.path_to('test.zip'))

        df = pd.read_csv(dataset_ws.path_to('train_labels.csv'))
        df = pd.DataFrame({
            'x': df['id'],
            'y': df['label']
        })

        FileDataset(
            dataset=df,
            image_path_template=target_ws.path_to('train/{}.tif')
        ).to_path(target_ws.path_to('dataset.json'))
