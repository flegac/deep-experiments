import keras

from histopathologic_cancer_detection.prepare_histopathological_cancer import PrepareHistopathologicCancer
from hyper_search.train_parameters import TrainParameters
from mydeep_keras.callbacks.cyclic_lr import CyclicLR
from mydeep_keras.k_model import KModel
from mydeep_keras.models.keras_application import keras_application
from mydeep_workers.compute_submission import ComputeSubmission
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from mydeep_workers.search_learning_rate import SearchLearningRate
from mydeep_keras.keras_trainer import KerasTrainer
from mydeep_workers.validate_training import ValidateTraining
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline, step

train_ctx = KerasTrainer.create_ctx(
    model_provider=lambda: KModel.from_keras(
        keras_application(
            input_shape=(96, 96, 3),
            output_class_number=2,
            k_model=keras.applications.DenseNet169
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
        'rotation_range': 45,
        'zoom_range': 0.1,
        'width_shift_range': 0.1,
        'height_shift_range': 0.1,
    })
)

ctx = PipelineContext(
    root_path='D:/Datasets/histopathologic-cancer-detection',
    project_name='densenet169_augmentation_CLR'
)

pipe = pipeline(
    ctx=ctx,
    steps=[
        step('raw_dataset',
             worker=PrepareHistopathologicCancer()),
        step('dataset',
             worker=PrepareTrainingDataset(input_path='raw_dataset')),
        step('lr_finder',
             worker=SearchLearningRate(train_ctx, min_lr=1e-6, max_lr=1e-2, epochs=1)),
        step('training',
             worker=KerasTrainer(train_ctx)),
        step('validation',
             worker=ValidateTraining(train_ctx.augmentation)),
        step('submission',
             worker=ComputeSubmission(train_ctx.augmentation, nb_pred=10, target_x='id', target_y='label')),

    ])

pipe(ctx.project_ws)