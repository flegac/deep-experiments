from typing import Callable, List

import numpy as np

Buffer = np.ndarray
DataSource = Callable[[], Buffer]
DataTransformer = Callable[[Buffer], Buffer]
DataCombiner = Callable[[List[Buffer]], Buffer]
