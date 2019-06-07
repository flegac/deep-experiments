from sklearn.ensemble import GradientBoostingClassifier
from tqdm import tqdm
from typing import List, Tuple

from hyper_search.train_parameters import TrainParameters
from mydeep_lib.tensor.tensor import Tensor
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset
from train_common.ctx.train_dataset import TrainDataset
import numpy as np
import matplotlib.pyplot as plt


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

    def __init__(self, params: TrainParameters, augmentation: TrainParameters) -> None:
        super().__init__()
        self.params = params
        self.augmentation = augmentation

    def model(self):
        model_setting = dict(TrainContext.DEFAULT_PARAMS)
        model_setting.update(self.params.params)
        return GradientBoostingClassifier(**model_setting)


class TrainerXGBoost(PipelineWorker):
    create_ctx = TrainContext

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
            x_train = np.zeros(shape=(N, 784*3))
            y_train = np.zeros(shape=(N,))
            for i in tqdm(range(N // 100)):
                X, Y = next(training_gen)
                x_train[i] = X.reshape(X.size)
                y_train[i] = np.argmax(Y)
            return x_train, y_train

        x_train, y_train = create_dataset(dataset.train)
        x_test, y_test = create_dataset(dataset.test)

        plt.figure()

        model = self.params.model()
        model.fit(x_train, y_train)

        # compute test set deviance
        N = len(model.staged_decision_function(x_test))
        test_deviance = np.zeros((N,), dtype=np.float64)

        for i, y_pred in enumerate(model.staged_decision_function(x_test)):
            test_deviance[i] = model.loss_(y_test, y_pred)

        plt.plot((np.arange(test_deviance.shape[0]) + 1)[::5], test_deviance[::5],
                 '-', color='blue', label='training XG Boost')

        plt.legend(loc='upper left')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Test Set Deviance')

        plt.show()

        return None
