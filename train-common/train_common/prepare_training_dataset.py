from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset, TrainingDataset


class PrepareTrainingDataset(PipelineWorker):

    def __init__(self, test_size: float = 0.1):
        super().__init__('prepare training dataset', 'dataset')
        self.test_size = test_size

    def apply(self, target_ws: Workspace):
        seed = self.ctx.seed

        # prepare dataset
        dataframe_path = self.ctx.project_ws.path_to('raw_dataset/dataset.json')
        dataset = Dataset.from_path(dataframe_path)
        dataframe = shuffle(dataset.df, random_state=seed)
        train, test = train_test_split(dataframe, test_size=self.test_size, random_state=seed,
                                       stratify=dataframe[dataset.y_col])

        # save dataset to disk
        train = Dataset(train.sort_values(dataset.x_col), dataset.img_path, dataset.img_ext)
        test = Dataset(test.sort_values(dataset.x_col), dataset.img_path, dataset.img_ext)

        TrainingDataset(train, test).to_path(target_ws)
