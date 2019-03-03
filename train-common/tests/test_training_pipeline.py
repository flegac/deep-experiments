import keras

from hyper_search.train_parameters import TrainParameters
from monkeys_detection.prepare_monkeys import PrepareMonkeys
from mydeep_lib.models.basic_model import basic_model
from train_common.compute_submission import ComputeSubmission
from train_common.ctx.model import Model
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline
from train_common.ctx.train_context import TrainContext
from train_common.prepare_training_dataset import PrepareTrainingDataset
from train_common.search_learning_rate import SearchLearningRate
from train_common.trainer import Trainer
from train_common.validate_training import ValidateTraining

train_ctx = TrainContext(

    model_provider=lambda: Model.from_keras(
        basic_model(
            input_shape=(128, 128, 3),
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'SGD',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 64,
        'epochs': 2,
        'callbacks': []
    }),

    augmentation=TrainParameters({
        '__builder__': keras.preprocessing.image.ImageDataGenerator,
        'rescale': 1. / 255,
        'rotation_range': 40,
        'width_shift_range': 0.2,
        'height_shift_range': 0.2,
        'shear_range': 0.2,
        'zoom_range': 0.2,
        'horizontal_flip': True,
    })
)

pipe = pipeline([
    PrepareMonkeys(),
    PrepareTrainingDataset(test_size=0.1),
    SearchLearningRate(train_ctx, min_lr=0.69, max_lr=0.71),
    Trainer(train_ctx),
    ValidateTraining(train_ctx.augmentation),
    ComputeSubmission(train_ctx.augmentation, nb_pred=2, target_x='xx', target_y='yy')
])
pipe(PipelineContext(
    root_path='resources/dataset',
    project_name='test'))
