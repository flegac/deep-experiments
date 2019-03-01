import keras

from histopathologic_cancer_detection.prepare_histopathological_cancer import PrepareHistopathologicCancer
from hyper_search.train_parameters import TrainParameters
from mydeep_lib.callbacks.cyclic_lr import CyclicLR
from mydeep_lib.models.keras_model import keras_model
from surili_core.pipelines import pipeline
from train_common.compute_submission import ComputeSubmission
from train_common.ctx.model import Model
from train_common.ctx.train_context import TrainContext
from surili_core.pipeline_context import PipelineContext
from train_common.prepare_training_dataset import PrepareTrainingDataset
from train_common.trainer import Trainer
from train_common.validate_training import ValidateTraining

train_ctx = TrainContext(

    model_provider=lambda: Model.from_keras(
        keras_model(
            input_shape=(96, 96, 3),
            output_class_number=2,
            weights=None,
            k_model=keras.applications.resnet50.ResNet50
        ),
        compile_params={
            'loss': 'binary_crossentropy',
            'optimizer': 'SGD',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 64,
        'epochs': 30,
        'callbacks': [
            CyclicLR(
                base_lr=5e-5,
                max_lr=1e-3,
                # TODO : try with 6189 x 4 = 24756
                step_size=18567.,  # N=2 : N *(len(train) / batch_size) = 2N epochs per cycles
                mode='triangular'
            ),
        ]
    }),

    augmentation=TrainParameters({
        '__builder__': keras.preprocessing.image.ImageDataGenerator,
        'rescale': 1. / 255,
        'horizontal_flip': True,
        'vertical_flip': True,
        'rotation_range': 90,
        'zoom_range': 0.05,
        'width_shift_range': 0.1,
        'height_shift_range': 0.1,
    })
)

pipe = pipeline([
    PrepareHistopathologicCancer(),
    PrepareTrainingDataset(),
    Trainer(train_ctx),
    ValidateTraining(train_ctx.augmentation),
    ComputeSubmission(train_ctx.augmentation, nb_pred=10, target_x='id', target_y='label')
])

pipe(PipelineContext(
    root_path='D:/Datasets/histopathologic-cancer-detection',
    project_name='resnet50_augmentation_CLR'))