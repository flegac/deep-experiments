import keras

from histopathologic_cancer_detection.prepare_histopathological_cancer import PrepareHistopathologicCancer
from hyper_search.train_parameters import TrainParameters
from mydeep_keras.callbacks import CyclicLR
from mydeep_keras.models.keras_application import keras_application
from mydeep_lib.worker.compute_submission import ComputeSubmission
from mydeep_keras.k_model import KModel
from mydeep_lib.worker.prepare_training_dataset import PrepareTrainingDataset
from mydeep_lib.worker.validate_training import ValidateTraining
from surili_core.pipelines import pipeline
from surili_core.pipeline_context import PipelineContext
from mydeep_lib.worker.search_learning_rate import SearchLearningRate
from mydeep_lib.worker.trainer import Trainer

train_ctx = Trainer.create_ctx(

    model_provider=lambda: KModel.from_keras(
        keras_application(
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
        'epochs': 40,
        'callbacks': [
            CyclicLR(
                base_lr=1e-5,
                max_lr=1e-4,
                step_size=5,
                mode='triangular2'
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
    SearchLearningRate(train_ctx, min_lr=1e-6, max_lr=1e-2, epochs=1),
    Trainer(train_ctx),
    ValidateTraining(train_ctx.augmentation),
    ComputeSubmission(train_ctx.augmentation, nb_pred=10, target_x='id', target_y='label')
])

pipe(PipelineContext(
    root_path='D:/Datasets/histopathologic-cancer-detection',
    project_name='resnet50_augmentation_CLR'))
