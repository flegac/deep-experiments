import numpy as np
from keras import Sequential
from keras.layers import Lambda, Conv2D, BatchNormalization, Activation, MaxPooling2D, Dropout, GlobalAveragePooling2D, \
    Dense

from mydeep_api.data import Data
from mydeep_api.dataset.numpy_dataset import NumpyDataset
from mydeep_keras.keras_model import KModel, KFitConfig


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
            x=NumpyDataset(np.arange(100*10*10*3).reshape((100, 10, 10, 3))),
            y=NumpyDataset(np.arange(100*10).reshape((100, 10)))
        ),
        config=KFitConfig(
            epochs=3,

        ))
