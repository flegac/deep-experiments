import keras
from keras.datasets import cifar10
from keras.layers import Dense, Conv2D, Flatten, Dropout, BatchNormalization, MaxPooling2D, Activation
from keras.utils import to_categorical

from hyper_search.train_parameters import TrainParameters

params = TrainParameters({
    'epochs': [1],
    'optimizer': [
        keras.optimizers.RMSprop,
        keras.optimizers.Adam,
        keras.optimizers.SGD,
        keras.optimizers.Adagrad
    ],
    'lr': list(map(lambda x: 10 ** -x, range(2, 5))),
    'batch_size': [32],
    'loss': ['categorical_crossentropy'],
    'callback_lr_scheduler_factor': [.5, .6, .7, .8, .9, ],
    'model_dropout': [.1, .2],
    'model_filters': [4],
    'model_last_layer': [8],
    'model': [
        lambda dropout, base_filters, last_layer: keras.models.Sequential([
            Conv2D(base_filters, (3, 3), input_shape=(32, 32, 3), padding='same'),
            BatchNormalization(),
            Activation('relu'),
            # MaxPooling2D(),
            Dropout(dropout),

            Conv2D(base_filters * 2, (3, 3), padding='same'),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(),
            Dropout(dropout),

            Flatten(),
            Dense(last_layer),
            BatchNormalization(),
            Activation('relu'),
            Dropout(dropout),
            Dense(10, activation='softmax')
        ])
    ]
})

print(params)

# (x_train, y_train), (x_test, y_test) = cifar10.load_data()
# y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)

fixed = {
    'lr': .0001,
    'model_dropout': .1,
    'model_filters': 4,
    'model_last_layer': 8,
    'callback_lr_scheduler_factor': .5,
}

for i in range(10):
    p = params.random(fixed_params=fixed).params
    print(p)
    # model = p['model'](p['model_dropout'], p['model_filters'], p['model_last_layer'])
    # model.compile(optimizer=p['optimizer'](lr=p['lr'] / p['batch_size']),
    #               loss=p['loss'],
    #               metrics=['accuracy']
    #               )
    #
    # gen = ImageDataGenerator(rescale=1. / 255)
    #
    # train_data = gen.flow(x_train, y_train, batch_size=p['batch_size'])
    # test_data = gen.flow(x_test, y_test, batch_size=p['batch_size'])
    #
    # model.fit_generator(train_data,
    #                     epochs=p['epochs'],
    #                     steps_per_epoch=int(len(x_train) / p['batch_size']),
    #                     validation_data=test_data,
    #                     validation_steps=int(len(x_test) / p['batch_size']),
    #                     verbose=2,
    #                     callbacks_libs=[
    #                         keras.callbacks_libs.ReduceLROnPlateau(monitor='val_loss',
    #                                                           factor=p['callback_lr_scheduler_factor'], patience=2,
    #                                                           min_delta=1e-5, min_lr=1e-12)
    #
    #                     ]
    #                     )
