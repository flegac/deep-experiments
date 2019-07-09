import keras

from histopathologic_cancer_detection.prepare_histopathological_cancer import PrepareHistopathologicCancer
from hyper_search.train_parameters import TrainParameters
from mydeep_api.model.keras_model import KModel
from mydeep_lib.callbacks.cyclic_lr import CyclicLR
from mydeep_lib.models.keras_model import keras_model
from mydeep_train.compute_submission import ComputeSubmission
from mydeep_train.prepare_training_dataset import PrepareTrainingDataset
from mydeep_train.validate_training import ValidateTraining
from surili_core.pipelines import pipeline
from surili_core.pipeline_context import PipelineContext
from mydeep_train.trainer import Trainer

train_ctx = Trainer.create_ctx(

    model_provider=lambda: KModel.from_keras(
        keras_model(
            input_shape=(96, 96, 3),
            output_class_number=2,
            k_model=keras.applications.DenseNet121
        ),
        compile_params={
            'loss': 'binary_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 32,
        'epochs': 30,
        'callbacks': [
            CyclicLR(
                base_lr=1e-6,
                max_lr=2e-4,
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
    project_name='densenet121_augmentation_CLR'))
