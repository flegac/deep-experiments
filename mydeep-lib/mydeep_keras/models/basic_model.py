from keras import Sequential
from keras.layers import *


def basic_model(input_shape, output_class_number):
    kernel_size = (3, 3)
    filters = 16
    dropout_rate = 0.1

    def conv_layer(layer_filters):
        return [
            Conv2D(layer_filters, kernel_size, padding='same'),
            BatchNormalization(),
            Activation(activation='relu'),
        ]

    model = Sequential([
        Lambda(lambda x: x, input_shape=input_shape, name="input_lambda"),
        *conv_layer(filters),
        *conv_layer(filters),
        *conv_layer(filters),
        MaxPooling2D(),
        Dropout(dropout_rate),

        *conv_layer(filters * 2),
        *conv_layer(filters * 2),
        MaxPooling2D(),
        Dropout(dropout_rate),

        *conv_layer(filters * 4),
        MaxPooling2D(),
        Dropout(dropout_rate),

        GlobalAveragePooling2D(),
        Dropout(dropout_rate),
        Dense(output_class_number, activation='softmax')
    ])

    model.summary()
    return model
