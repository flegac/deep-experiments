import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from sign_mnist.feature_dataset_creation import FeatureDatasetCreation
from sign_mnist.gradient_boosting_evaluator import GradientBoostingEvaluator
from sign_mnist.gradient_boosting_trainer import GradientBoostingTrainer
from sign_mnist.raw_dataset_creation import RawDatasetCreation
from sign_mnist.treshold_filter import extract_features
from surili_core.pipelines import pipeline, step
from surili_core.workspace import Workspace

train_ctx = GradientBoostingTrainer.create_ctx(
    params=TrainParameters({
        'learning_rate': 0.01,
        'subsample': 0.5
    }),
    augmentation=TrainParameters({
        '__builder__': keras.preprocessing.image.ImageDataGenerator,
        'rotation_range': 10,
        'width_shift_range': 0.1,
        'height_shift_range': 0.1,
        'shear_range': 0.3,
        'zoom_range': 0.1,
    }),
    preprocessing=extract_features
)

pipe = pipeline([
    step('raw_dataset',
         worker=RawDatasetCreation(train_csv_path='sign_mnist_train.csv')),
    step('features_dataset',
         worker=FeatureDatasetCreation(
             input_path='raw_dataset'
         )),
    step('dataset',
         worker=PrepareTrainingDataset(
             input_path='features_dataset',
             test_size=0.1
         )),
    step('training',
         worker=GradientBoostingTrainer(params=train_ctx, dataset_path='dataset')),
    step('validation',
         worker=GradientBoostingEvaluator(dataset_path='dataset', training_path='training'))
])
pipe(Workspace.from_path('D:/Datasets/sign-language-mnist/sign-mnist-boost', ))
