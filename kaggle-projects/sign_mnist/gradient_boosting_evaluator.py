import keras
import numpy as np
from matplotlib import pyplot as plt
from sklearn.externals import joblib

from hyper_search.train_parameters import TrainParameters
from mydeep_lib.train_dataset import TrainDataset
from sign_mnist.gradient_boosting_trainer import create_dataset
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class GradientBoostingEvaluator(Worker):

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        dataset_ws = ctx.project_ws.get_ws('dataset')
        dataset = TrainDataset.from_path(dataset_ws)

        training_ws = ctx.project_ws.get_ws('training')
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
        plt.savefig(target_ws.path_to('eval.png'))
        return None
