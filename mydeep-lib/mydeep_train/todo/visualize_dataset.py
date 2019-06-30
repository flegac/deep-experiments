from sklearn.utils import shuffle

from mydeep_lib.dataframe import Dataframes
from surili_core.pipeline_context import PipelineContext
from surili_core.pipeline_worker import Worker
from mydeep_lib.tensor.tensor_util import tensor_from_path, tensor_scale

from mydeep_lib.visualize.visualize import Visualize
from surili_core.workspace import Workspace
from stream_lib.stream import stream


class VisualizeDataset(Worker):
    def __init__(self, nb_images: int) -> None:
        super().__init__('visualize dataset', 'visualize')
        self.nb_images = nb_images

    def apply(self, ctx: PipelineContext, target_ws: Workspace):
        df = Dataframes.from_csv(ctx.project_ws.path_to('dataset/train.csv')).head(self.nb_images)
        df = shuffle(df)

        images = df['id'] \
            .apply(lambda x: '{}/train/{}.tif'.format(ctx.root_ws.path, x)) \
            .apply(tensor_from_path) \
            .apply(tensor_scale(1. / 255))

        stream(images, df['label']) \
            .apply(Visualize.show_dataset('view'))
