from keras import Model
from keras.layers import *


def keras_model(input_shape, output_class_number, k_model, **k_model_args) -> Model:
    inputs = Input(input_shape)
    base_model = k_model(include_top=False, input_shape=input_shape, **k_model_args)
    x = base_model(inputs)

    out1 = GlobalMaxPooling2D()(x)
    out2 = GlobalAveragePooling2D()(x)
    out3 = Flatten()(x)
    out = Concatenate(axis=-1)([out1, out2, out3])
    out = Dropout(0.5)(out)
    out = Dense(output_class_number, activation="sigmoid", name="output_full_3")(out)

    model = Model(inputs, out)

    model.summary()
    return model
