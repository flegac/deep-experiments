import json
import random
from typing import List, Callable

import keras
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

from mydeep_api.data import Data
from mydeep_api.dataset.dataset import Dataset
from mydeep_api.dataset.bi_dataset import BiDataset
from mydeep_api.dataset.numpy_dataset import NumpyDataset
from mydeep_api.model.model import Model, FitConfig, FitReport


class KFitReport(FitReport):
    def __init__(self, history):
        self.history = history


class KFitConfig(FitConfig):
    def __init__(self,
                 epochs: int,
                 batch_size: int = 32,
                 seed: int = random.randrange(1000),
                 shuffle: bool = True,
                 callbacks: List[Callable] = None
                 ):
        super().__init__(seed)
        self.epochs = epochs
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.callbacks = callbacks or []


class KModel(Model):
    @staticmethod
    def from_keras(keras_model: keras.Model, compile_params: dict):
        if compile_params:
            keras_model.compile(**compile_params)
        return KModel(keras_model)

    @staticmethod
    def from_path(path: str):
        assert path.endswith('.h5')
        config_path = path.replace('.h5', '.json')

        try:
            with open(config_path) as _:
                keras_model = keras.Sequential.from_config(json.load(_))
        except:
            with open(config_path) as _:
                keras_model = keras.Model.from_config(json.load(_))
        keras_model.load_weights(path)
        return KModel(keras_model)

    def __init__(self, keras_model: keras.Model):
        self.keras_model = keras_model
        keras_model.summary()

    def input_shape(self):
        return self.keras_model.get_layer(index=0).input_shape[1:-1]

    def output_shape(self):
        return self.keras_model.get_layer(index=-1).output_shape[1:]

    def to_path(self, path: str):
        assert path.endswith('.h5')

        config_path = path.replace('.h5', '.json')

        with open(path.replace('.h5', '_summary.txt'), 'w') as _:
            self.keras_model.summary(print_fn=lambda x: _.write(str(x) + '\n'))

        try:
            with open(config_path, 'w') as _:
                json.dump(self.keras_model.get_config(), _, indent=2)
        except:
            print('could not serialize the model.get_congih() !')
        self.keras_model.save_weights(path)

    def fit(self, dataset: BiDataset, config: KFitConfig = None) -> KFitReport:
        config = config or {}

        history = self.keras_model.fit_generator(
            generator=ImageDataGenerator().flow(
                x=np.array(list(dataset.x)),
                y=np.array(list(dataset.y)),
                seed=config.seed
            ),
            epochs=config.epochs,
            steps_per_epoch=int(len(dataset) / config.batch_size),
            verbose=1,
            callbacks=config.callbacks,
            validation_data=None,
            validation_steps=None,
            shuffle=config.shuffle
        )

        return KFitReport(
            history=history
        )

    def predict(self, x: Dataset):
        yy = NumpyDataset(np.array(self.keras_model.predict(x=x)))

        return Data.from_xy(x, yy)
