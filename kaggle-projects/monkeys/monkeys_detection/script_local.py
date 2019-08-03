import json

import keras
from keras.callbacks import EarlyStopping

from hyper_search.train_parameters import TrainParameters
from monkeys_detection.prepare_monkeys import PrepareMonkeys
from mydeep_keras.k_model import KModel
from mydeep_keras.k_trainer import KerasTrainer
from mydeep_keras.models.basic_model import basic_model
from mydeep_workers.compute_submission import ComputeSubmission
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from mydeep_workers.validate_training import ValidateTraining
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline, step
from surili_core.surili_io.storage_io import StorageImport

with open('config.json') as _:
    config = json.load(_)

train_ctx = KerasTrainer.create_ctx(
    model_provider=lambda: KModel.from_keras(
        basic_model(
            input_shape=config['input_shape'],
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'SGD',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 64,
        'epochs': config['epochs'],
        'callbacks': [
            EarlyStopping(
                restore_best_weights=True,
                patience=int(2 / 5 * config['patience'])
            ),
            keras.callbacks.ReduceLROnPlateau(
                factor=.75,
                min_lr=10e-6,
                patience=config['patience']
            ),
        ]
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

pipeline([
    step('00_download_dataset',
         worker=StorageImport(
             storage_path='gs://flegac_datasets/10-monkey-species.zip'
         )),
    step('01_raw_dataset',
         worker=PrepareMonkeys(
             dataset_path='00_download_dataset'
         )),
    step('02_dataset',
         worker=PrepareTrainingDataset(
             input_path='01_raw_dataset',
             test_size=0.1
         )),
    step('training',
         worker=KerasTrainer(
             dataset_path='02_dataset',
             params=train_ctx
         )),
    step('validation',
         worker=ValidateTraining(
             training_path='training',
             dataset_path='02_dataset',
             augmentation=train_ctx.augmentation
         )),
    step('submission',
         worker=ComputeSubmission(
             dataset_path='02_dataset',
             training_path='training',
             augmentation=train_ctx.augmentation,
             nb_pred=2,
             target_x='xx',
             target_y='yy'
         ))
])(ctx=PipelineContext(
    project_name='monkeys',
    root_path=config['workspace']
))
