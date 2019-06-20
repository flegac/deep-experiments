import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_train.prepare_training_dataset import PrepareTrainingDataset
from sign_mnist.prepare_sign_mnist import PrepareSignMnist
from sign_mnist.trainer_xgboost import TrainerXGBoost
from sign_mnist.treshold_filter import TresholdFilter, extract_features
from surili_core.pipelines import pipeline
from surili_core.pipeline_context import PipelineContext

train_ctx = TrainerXGBoost.create_ctx(
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
    PrepareSignMnist(),
    # TresholdFilter(),
    PrepareTrainingDataset(test_size=0.1),
    TrainerXGBoost(train_ctx)
])

pipe(PipelineContext(
    root_path='D:/Datasets/sign-language-mnist',
    project_name='sign-mnist'))
