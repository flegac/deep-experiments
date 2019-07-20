from keras import Model
from keras.layers import *


def keras_application(input_shape, output_class_number, k_model, **k_model_args) -> Model:
    inputs = Input(input_shape)
    base_model = k_model(include_top=False, input_shape=input_shape, **k_model_args)
    x = base_model(inputs)

    out = Concatenate(axis=-1)([
        GlobalMaxPooling2D()(x),
        GlobalAveragePooling2D()(x),
        Flatten()(x)
    ])
    out = Dropout(0.5)(out)
    out = Dense(output_class_number, activation="sigmoid", name="output_full_3")(out)

    model = Model(inputs, out)

    model.summary()
    return model
