import json
from typing import Dict

import keras
import numpy as np
from keras import Sequential
from keras.layers import Lambda, Conv2D, BatchNormalization, Activation, MaxPooling2D, Dropout, GlobalAveragePooling2D, \
    Dense
from keras.preprocessing.image import ImageDataGenerator

from mydeep_api.api import Data
from mydeep_api.dataset.dataset import Dataset, BiDataset
from mydeep_api.dataset.numpy_dataset import NumpyDataset
from mydeep_api.model.model import Model


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

    def fit(self, dataset: BiDataset, params: Dict = None):
        params = params or {}

        flow = ImageDataGenerator().flow(
            x=np.array(list(dataset.x)),
            y=np.array(list(dataset.y))
        )
        steps_per_epoch = len(dataset)
        if params.get('batch_size'):
            steps_per_epoch /= params['batch_size']

        self.keras_model.fit_generator(
            flow,
            steps_per_epoch=steps_per_epoch
        )
        # self.keras_model.fit(x=list(dataset.x), y=list(dataset.y), **(params or {}))

    def predict(self, x: Dataset):
        yy = NumpyDataset(np.array(self.keras_model.predict(x=x)))

        return Data.from_xy(x, yy)


def test_kmodel():
    input_shape = (10, 10, 3)
    output_class_number = 10

    model = KModel.from_keras(
        keras_model=Sequential([
            Lambda(lambda x: x, input_shape=input_shape, name="input_lambda"),
            Conv2D(16, (3, 3), padding='same'),
            BatchNormalization(),
            Activation(activation='relu'),

            MaxPooling2D(),
            Dropout(.5),

            GlobalAveragePooling2D(),
            Dropout(.5),
            Dense(output_class_number, activation='softmax')
        ]),
        compile_params={
            'loss': 'binary_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        })

    model.fit(
        dataset=Data.from_xy(
            x=NumpyDataset(np.arange(1500).reshape((5, 10, 10, 3))),
            y=NumpyDataset(np.arange(50).reshape((5, 10)))
        ),
        params={})
