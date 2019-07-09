from typing import Tuple

from keras import Model
from keras.layers import *


def model_v2(input_shape,
             output_class_number: int,
             kernel_size: Tuple[int, int] = (3, 3),
             base_filters: int = 16,
             dropout_rate=0.25,
             activation='relu',
             layer_batch_size=2,
             layer_batch_number=2) -> Model:
    inputs = Input(shape=input_shape)
    x = inputs

    for k in range(layer_batch_number):
        for i in range(layer_batch_size):
            x = Conv2D((2 ** k) * base_filters, kernel_size, padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation(activation=activation)(x)
        x = MaxPooling2D()(x)
        x = Dropout(dropout_rate)(x)

    # final layer
    out = Concatenate(axis=-1)([
        GlobalMaxPooling2D()(x),
        GlobalAveragePooling2D()(x),
        Flatten()(x)
    ])
    out = Dropout(0.5)(out)
    out = Dense(output_class_number, activation='sigmoid', name='output_final')(out)

    model = Model(inputs, out)
    model.summary()
    return model
