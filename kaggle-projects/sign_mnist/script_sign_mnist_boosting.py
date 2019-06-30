import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_train.prepare_training_dataset import PrepareTrainingDataset
from sign_mnist.prepare_sign_mnist import sign_mnist_preparator
from sign_mnist.gradient_boosting_trainer import GradientBoostingTrainer
from sign_mnist.gradient_boosting_evaluator import GradientBoostingEvaluator
from sign_mnist.treshold_filter import TresholdFilter, extract_features
from surili_core.pipelines import pipeline, step
from surili_core.pipeline_context import PipelineContext

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
    step('Prepare raw dataset', 'raw_dataset', worker=sign_mnist_preparator),
    # TresholdFilter(),
    PrepareTrainingDataset(test_size=0.1),
    GradientBoostingTrainer(train_ctx),
    GradientBoostingEvaluator()

])

pipe(PipelineContext(
    root_path='D:/Datasets/sign-language-mnist',
    project_name='sign-mnist'))
