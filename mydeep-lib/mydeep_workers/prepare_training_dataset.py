from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from mydeep_api._deprecated.file_dataset import FileDataset
from mydeep_api._deprecated.train_dataset import TrainDataset
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareTrainingDataset(Worker):

    def __init__(self, input_path: str, test_size: float = 0.1, seed: int = 543263):
        super().__init__()
        self.test_size = test_size
        self.input_path = input_path
        self.seed = seed

    def run(self, ws: Workspace):
        # prepare dataset
        dataframe_path = ws.root.get_ws(self.input_path).path_to('dataset.json')
        dataset = FileDataset.from_path(dataframe_path)
        # FIXME: remove the shuffle as it is included in the train_test_split
        dataframe = shuffle(dataset.df, random_state=self.seed)
        train, test = train_test_split(
            dataframe,
            test_size=self.test_size,
            random_state=self.seed,
            stratify=dataframe[dataset.y_col]
        )

        # save dataset to disk
        train = FileDataset(train.sort_values(dataset.x_col), dataset.image_path_template)
        test = FileDataset(test.sort_values(dataset.x_col), dataset.image_path_template)

        TrainDataset(train, test).to_path(ws)
