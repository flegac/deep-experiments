import json
import os

import numpy as np
import pandas as pd
from keras_preprocessing.image import ImageDataGenerator


class FileDataset(object):

    @staticmethod
    def from_path(path: str):
        with open(path, 'r') as _:
            dataset = json.load(_)
        return FileDataset(
            pd.read_csv(dataset['dataset_path']),
            dataset['image_path_template'],
            dataset['x_col'],
            dataset['y_col'])

    def __init__(self, dataset: pd.DataFrame,
                 image_path_template: str,
                 x_col='x',
                 y_col='y'):
        self.df = dataset
        self.image_path_template = image_path_template
        self.x_col = x_col
        self.y_col = y_col

    def filenames(self):
        return self.df[self.x_col].apply(self.image_path_template.format)

    def size(self):
        return len(self.df)

    def steps_number(self, batch_size: int):
        return np.ceil(self.size() / batch_size)

    # TODO move to keras part
    def prepare_generator(self, batch_size, target_shape, augmentation: ImageDataGenerator, class_mode='categorical',
                          shuffle=True):
        df = self.df
        df['_filename'] = self.filenames()
        df['_labels'] = df[self.y_col].apply(str)
        classes = list(df['_labels'].unique())
        return augmentation.flow_from_dataframe(
            dataframe=df,
            x_col='_filename',
            y_col='_labels',
            classes=classes,
            directory=os.path.basename(self.image_path_template),
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
                'image_path_template': self.image_path_template,
                'x_col': self.x_col,
                'y_col': self.y_col
            }, _, sort_keys=True, indent=4, separators=(',', ': '))
        return path

    def __repr__(self) -> str:
        return json.dumps({
            'dataset': list(self.df),
            'image_path_template': self.image_path_template,
            'x_y': [self.x_col, self.y_col]
        }, sort_keys=True, separators=(',', ': '))
