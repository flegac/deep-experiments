from typing import Tuple, Callable

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline
from tqdm import tqdm

from hyper_search.train_parameters import TrainParameters
from mydeep_api.tensor import Tensor
from mydeep_lib.dataset import Dataset
from mydeep_lib.train_dataset import TrainDataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def create_dataset(data: Dataset, augmentation: TrainParameters = None) -> Tuple[Tensor, Tensor]:
    training_gen = data.prepare_generator(
        batch_size=1,
        target_shape=(28, 28),
        augmentation=augmentation.build()
    )

    N = len(training_gen)
    x_train = np.zeros(shape=(N, 28, 28, 3))
    y_train = np.zeros(shape=(N,))
    for i in tqdm(range(N)):
        X, Y = next(training_gen)
        x_train[i] = X.reshape(X.shape[1:])
        y_train[i] = np.argmax(Y)
    return x_train, y_train


class _Preprocessing(BaseEstimator):
    def __init__(self, preprocessing: Callable[[Tensor], Tensor]):
        super().__init__()
        self.preprocessing = preprocessing or (lambda _: _)

    def transform(self, X, y=None, **fit_params):
        return np.asarray([self.preprocessing(x).flatten() for x in X])

    def fit(self, X, y=None, **fit_params):
        return self


class GradientBoostingContext(object):
    DEFAULT_PARAMS = {
        'learning_rate': 0.1,
        'n_estimators': 200,
        'max_leaf_nodes': 4,
        'max_depth': None,
        'random_state': 2,
        'min_samples_split': 5,
        'verbose': 1
    }

    def __init__(self, params: TrainParameters, augmentation: TrainParameters, preprocessing: Callable = None) -> None:
        super().__init__()
        self.params = params
        self.augmentation = augmentation
        self.preprocessing = preprocessing

    def model(self):
        model_setting = dict(GradientBoostingContext.DEFAULT_PARAMS)
        model_setting.update(self.params.params)

        return make_pipeline(
            _Preprocessing(self.preprocessing),
            GradientBoostingClassifier(**model_setting)
        )


class GradientBoostingTrainer(Worker):
    create_ctx = GradientBoostingContext

    def __init__(self, params: GradientBoostingContext) -> None:
        super().__init__()
        self.params = params

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        dataset_ws = ctx.project_ws.get_ws('dataset')
        dataset = TrainDataset.from_path(dataset_ws)

        x_train, y_train = create_dataset(
            data=dataset.train,
            augmentation=self.params.augmentation)

        model = self.params.model()
        model.fit(x_train, y_train)

        joblib.dump(model, target_ws.path_to('model.sav'))
        return None
