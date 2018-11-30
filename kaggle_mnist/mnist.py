import pandas as pd
from keras.utils.np_utils import to_categorical

from keras.models import Sequential
from keras.layers import *
from keras_preprocessing.image import ImageDataGenerator

from sklearn.model_selection import train_test_split

train = pd.read_csv("input/train.csv")
test = pd.read_csv("input/test.csv")

x_train = train.iloc[:, 1:].values.astype('float32')
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
y_train = train.iloc[:, 0].values.astype('int32')
y_train = to_categorical(y_train)
x_test = test.values.astype('float32')
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

print(x_train.shape, y_train.shape)
print(x_test.shape)

mean_px = x_train.mean().astype(np.float32)
std_px = x_train.std().astype(np.float32)


def standardize(x):
    return (x - mean_px) / std_px


model = Sequential([
    Lambda(standardize, input_shape=(28, 28, 1)),
    Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'),
    Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'),
    MaxPooling2D(),

    Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'),
    Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'),
    MaxPooling2D(),

    Flatten(),
    BatchNormalization(),
    Dense(units=64, activation='relu'),
    Dense(units=10, activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

gen = ImageDataGenerator(rotation_range=8,
                         width_shift_range=0.08,
                         shear_range=0.3,
                         height_shift_range=0.08,
                         zoom_range=0.08)

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.10, random_state=None)

batches = gen.flow(x_train, y_train, batch_size=2048)
val_batches = gen.flow(x_val, y_val, batch_size=2048)

history = model.fit_generator(generator=batches,
                              # steps_per_epoch=batches.n,
                              epochs=10,
                              validation_data=val_batches,
                              # validation_steps=val_batches.n
                              )

predictions = model.predict_classes(x_test, verbose=0)

submissions = pd.DataFrame({"ImageId": list(range(1, len(predictions) + 1)),
                            "Label": predictions})
submissions.to_csv("submission.csv", index=False, header=True)
