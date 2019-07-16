import os

import numpy as np
import pandas as pd

from surili_core.workspace import Workspace


class Dataframes:

    @staticmethod
    def from_directory_structure(x_key: str = 'x', y_key: str = 'y'):
        def apply(path: str):
            data = Workspace.from_path(path) \
                .folders \
                .flatmap(lambda fs: fs.files) \
                .map(lambda f: (f, os.path.basename(os.path.dirname(f)))) \
                .to_list()
            data = np.array(data)
            data = pd.DataFrame(data, columns=[x_key, y_key])
            return data

        return apply
