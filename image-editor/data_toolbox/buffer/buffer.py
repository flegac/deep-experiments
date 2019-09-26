from typing import Callable, Tuple

import numpy as np

Buffer = np.ndarray

BufferProvider = Callable[[Tuple[int, int], Tuple[int, int]], Buffer]
