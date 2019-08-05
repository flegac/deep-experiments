import keras
import numpy as np
from matplotlib import pyplot as plt
from sklearn.externals import joblib

from hyper_search.train_parameters import TrainParameters
from mydeep_api._deprecated.train_dataset import TrainDataset
from sign_mnist.gradient_boosting_trainer import create_dataset
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class GradientBoostingEvaluator(Worker):
    def __init__(self, dataset_path: str, training_path: str):
        self.training_path = training_path
        self.dataset_path = dataset_path

    def run(self, ws: Workspace):
        dataset_ws = ws.root.get_ws(self.dataset_path)
        dataset = TrainDataset.from_path(dataset_ws)

        training_ws = ws.root.get_ws(self.training_path)
        model = joblib.load(training_ws.path_to('model.sav'))

        plt.figure()
        x_test, y_test = create_dataset(
            data=dataset.test,
            augmentation=TrainParameters({
                '__builder__': keras.preprocessing.image.ImageDataGenerator,
            }))
        preprocessing = model.steps[0][1]
        gradient_model = model.steps[1][1]

        # compute test set deviance
        x_test = preprocessing.transform(x_test)
        N = len(x_test)
        test_deviance = np.zeros((N,), dtype=np.float64)
        for i, y_pred in enumerate(gradient_model.staged_decision_function(x_test)):
            test_deviance[i] = gradient_model.loss_(y_test, y_pred)
        plt.plot((np.arange(test_deviance.shape[0]) + 1)[::5], test_deviance[::5],
                 '-', color='blue', label='training Boosting')
        plt.legend(loc='upper left')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Test Set Deviance')
        # plt.show()
        plt.savefig(ws.path_to('eval.png'))
        return None
