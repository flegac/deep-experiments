import sklearn
from sklearn.ensemble import GradientBoostingClassifier
from tqdm import tqdm
from typing import Tuple, Callable

from hyper_search.train_parameters import TrainParameters
from mydeep_lib.tensor.tensor import Tensor
from mydeep_train.ctx.dataset import Dataset
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from mydeep_train.ctx.train_dataset import TrainDataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator


class _Preprocessing(BaseEstimator):
    def __init__(self, preprocessing: Callable[[Tensor], Tensor]):
        super().__init__()
        self.preprocessing = preprocessing or (lambda _: _)

    def transform(self, X, y=None, **fit_params):
        return np.asarray([self.preprocessing(x).flatten() for x in X])

    def fit(self, X, y=None, **fit_params):
        return self


class TrainContext(object):
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
        model_setting = dict(TrainContext.DEFAULT_PARAMS)
        model_setting.update(self.params.params)

        return sklearn.pipeline.make_pipeline(
            _Preprocessing(self.preprocessing),
            GradientBoostingClassifier(**model_setting)
        )


class TrainerGradientBoosting(PipelineWorker):
    create_ctx = TrainContext
    model_id = 1

    def __init__(self, params: TrainContext) -> None:
        super().__init__('model training', 'training')
        self.params = params

    def apply(self, target_ws: Workspace):
        dataset_ws = self.ctx.project_ws.get_ws('dataset')
        dataset = TrainDataset.from_path(dataset_ws)

        def create_dataset(data: Dataset) -> Tuple[Tensor, Tensor]:
            training_gen = data.prepare_generator(
                batch_size=1,
                target_shape=(28, 28),
                augmentation=self.params.augmentation.build()
            )

            N = len(training_gen)
            x_train = np.zeros(shape=(N, 28, 28, 3))
            y_train = np.zeros(shape=(N,))
            for i in tqdm(range(N)):
                X, Y = next(training_gen)
                x_train[i] = X.reshape(X.shape[1:])
                y_train[i] = np.argmax(Y)
            return x_train, y_train

        x_train, y_train = create_dataset(dataset.train)
        x_test, y_test = create_dataset(dataset.test)

        model = self.params.model()
        model.fit(x_train, y_train)

        plt.figure()

        # compute test set deviance
        gradient_model = model.steps[TrainerGradientBoosting.model_id][1]
        # gradient_model = model

        # x_test = model.steps[0][1].transform(x_test)
        # N = len(gradient_model.staged_decision_function(x_test))
        #
        # test_deviance = np.zeros((N,), dtype=np.float64)
        #
        # for i, y_pred in enumerate(gradient_model.staged_decision_function(x_test)):
        #     test_deviance[i] = gradient_model.loss_(y_test, y_pred)

        # plt.plot((np.arange(test_deviance.shape[0]) + 1)[::5], test_deviance[::5],
        #          '-', color='blue', label='training XG Boost')

        # plt.legend(loc='upper left')
        # plt.xlabel('Boosting Iterations')
        # plt.ylabel('Test Set Deviance')

        # plt.show()

        return None
