import json

import numpy as np
import pandas as pd
from keras_preprocessing.image import ImageDataGenerator


class Dataset(object):

    @staticmethod
    def from_path(path: str):
        with open(path, 'r') as _:
            dataset = json.load(_)
        return Dataset(
            pd.read_csv(dataset['dataset_path']),
            dataset['images_path'],
            dataset['images_ext'],
            dataset['x_col'],
            dataset['y_col'])

    def __init__(self, dataset: pd.DataFrame, images_path: str, images_ext: str,
                 x_col='x', y_col='y'):
        self.df = dataset
        self.img_path = images_path
        self.img_ext = images_ext
        self.x_col = x_col
        self.y_col = y_col

    def filenames(self):
        image_path = '{}.' + self.img_ext
        return self.df[self.x_col].apply(image_path.format)

    def size(self):
        return len(self.df)

    def steps_number(self, batch_size: int):
        return np.ceil(self.size() / batch_size)

    def prepare_generator(self, batch_size, target_shape, augmentation: ImageDataGenerator, class_mode='categorical',
                          shuffle=True):
        df = self.df
        df['_filename'] = self.filenames()

        return augmentation.flow_from_dataframe(
            dataframe=df,
            x_col='_filename', y_col=self.y_col,
            classes=list(df[self.y_col].unique()),
            directory=self.img_path,
            target_size=target_shape,
            batch_size=batch_size,
            class_mode=class_mode,
            shuffle=shuffle
        )

    def to_path(self, path: str):
        assert path.endswith('.json'), path
        dataset_path = path.replace('.json', '.csv')
        self.df.to_csv(dataset_path, index=False)
        with open(path, 'w') as _:
            json.dump({
                'dataset_path': dataset_path,
                'images_path': self.img_path,
                'images_ext': self.img_ext,
                'x_col': self.x_col,
                'y_col': self.y_col
            }, _, sort_keys=True, indent=4, separators=(',', ': '))
        return path

    def __repr__(self) -> str:
        return json.dumps({
            'dataset': list(self.df),
            'img_path': '{}__id__.{}'.format(self.img_path, self.img_ext),
            'x_y': [self.x_col, self.y_col]
        }, sort_keys=True, separators=(',', ': '))
