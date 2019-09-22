import random
from typing import Optional

import numpy as np
import yaml


class TrainParameters(object):
    @staticmethod
    def from_yaml(path: str):
        with open(path, 'r') as _:
            params = yaml.load(_)
        return TrainParameters(params)

    def to_yaml(self, path: str):
        with open(path, 'w') as _:
            yaml.dump(self.params, _, default_flow_style=False)
        return path

    def __init__(self, params: Optional[dict] = None):
        self.params = params if params else dict()

    def get(self, name: str):
        return TrainParameters(self.params[name])

    def set_builder(self, builder):
        self.params['__builder__'] = builder

    def build(self):
        args = self.params.copy()
        del args['__builder__']
        return self.params['__builder__'](**args)

    def to_path(self, path: str):
        with open(path, 'w') as _:
            _.write(str(self))
        return path

    def random(self, fixed_params=None):
        if fixed_params is None:
            fixed_params = {}
        result = TrainParameters()
        for k, v in self.params.items():
            result.params[k] = fixed_params.get(k, v)
            if isinstance(v, list):
                result.params[k] = random.choice(v)
        return result

    def hyper_space_size(self):
        size = 1
        for x in self.params:
            if isinstance(self.params[x], list):
                size *= len(self.params[x])
        return size

    def __repr__(self) -> str:
        return 'parameters[{}]: {}'.format(self.hyper_space_size(), str(self.params))

    def compute_steps(self, dataset):
        return np.ceil(len(dataset) / self.params['batch_size'])

    def train_config(self):
        return {
            'optimizer': self.params['optimizer'](self.params['lr'] / self.params['batch_size']),
            'loss': self.params['loss'],
            'metrics': ['accuracy']
        }
