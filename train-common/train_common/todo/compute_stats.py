import numpy as np
import pandas as pd

from mydeep_lib.dataframe import Dataframes
from surili_core.pipeline_worker import PipelineWorker
from surili_core.pipeline_context import PipelineContext
from mydeep_lib.tensor.tensor_util import tensor_from_path, tensor_scale, tensor_centered_window
from surili_core.workspace import Workspace
from stream_lib.stream import stream


def compute_stats(df: pd.DataFrame):
    columns = ['id', 'label', 'amin', 'amax', 'average', 'std', 'mean', 'var']
    regions = [(24, 24), (32, 32), (48, 48), (72, 72), (96, 96)]

    def _compute_stats(item):
        path, name, label = item
        img = tensor_from_path(path)
        img = tensor_scale(1. / 255)(img)

        def compute_region_stats(region):
            _ = tensor_centered_window(*region)(img)
            return region, name, label, np.amin(_), np.amax(_), np.average(_), np.mean(_), np.std(_), np.var(_)

        stream(regions).map(compute_region_stats).to_list()

        return [compute_region_stats(r) for r in regions]

    stats = stream(df['filename'], df['id'], df['label']) \
        .flatmap(_compute_stats) \
        .to_list()

    def compute_item(region):
        region_stats = stream(stats).filter(lambda x: x[0] == region).map(lambda x: x[1:]).to_list()
        region_stats = pd.DataFrame.from_records(region_stats, columns=columns)
        return region_stats

    records = {r: compute_item(r) for r in regions}
    # big_dataframe = pd.DataFrame.from_records(stats, columns=columns)
    # records = [x for _, x in big_dataframe.groupby('region')]
    return records


def load_dataframe(ctx: PipelineContext):
    df = Dataframes.from_csv(ctx.root_ws.path_to('train_labels.csv'))
    df['filename'] = df['id'].apply(lambda x: '{}/train/{}.tif'.format(ctx.root_ws.path, x))
    return df


class ComputeStats(PipelineWorker):
    def __init__(self, region=tuple) -> None:
        super().__init__('scan dataset', '')
        self.region = region

    def apply(self, target_ws: Workspace):
        dataset = load_dataframe(self.ctx)
        datasets = compute_stats(dataset)

        for r in datasets:
            print('region: {}'.format(r))
            datasets[r].to_csv(target_ws.path_to('dataset_{}.csv'.format(r)), index=False)
