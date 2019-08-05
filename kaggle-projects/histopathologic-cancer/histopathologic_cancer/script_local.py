import json

import keras
from keras.callbacks import EarlyStopping

from histopathologic_cancer.prepare_histopathologic_cancer import PrepareHistopathologicCancer
from hyper_search.train_parameters import TrainParameters
from mydeep_keras.k_model import KModel
from mydeep_keras.k_trainer import KerasTrainer
from mydeep_keras.models.keras_application import keras_application
from mydeep_workers.compute_submission import ComputeSubmission
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from mydeep_workers.validate_training import ValidateTraining
from surili_core.pipelines import pipeline, step
from surili_core.surili_io.storage_io import StorageExport, StorageImport
from surili_core.workspace import Workspace

with open('config.json') as _:
    config = json.load(_)

train_ctx = KerasTrainer.create_ctx(
    model_provider=lambda: KModel.from_keras(
        keras_application(
            input_shape=config['input_shape'],
            output_class_number=2,
            k_model=keras.applications.MobileNetV2
        ),
        compile_params={
            'loss': 'binary_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 32,
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
        'horizontal_flip': True,
        'vertical_flip': True,
        'rotation_range': 90,
        'zoom_range': 0.1,
        'width_shift_range': 0.1,
        'height_shift_range': 0.1,
    })
)

pipeline([
    step('download_dataset',
         worker=StorageImport(
             storage_path='gs://flegac_datasets/histopathologic-cancer-detection.zip'
         )),
    step('raw_dataset',
         worker=PrepareHistopathologicCancer(
             dataset_path='download_dataset'
         )),
    step('dataset',
         worker=PrepareTrainingDataset(
             input_path='raw_dataset'
         )),
    step('training',
         worker=KerasTrainer(
             dataset_path='dataset',
             params=train_ctx
         )),
    step('validation',
         worker=ValidateTraining(
             dataset_path='dataset',
             training_path='training',
             augmentation=train_ctx.augmentation
         )),
    step('submission',
         worker=ComputeSubmission(
             dataset_path='dataset',
             training_path='training',
             augmentation=train_ctx.augmentation,
             nb_pred=10,
             target_x='id',
             target_y='label'
         )),
    step('export',
         worker=StorageExport(
             storage_path='gs://deep-experiments/results'
         ))
])(ctx=Workspace.from_path('D:/Projects/histopathologic-cancer-detection/MobileNetV2_augmentation_CLR'))
