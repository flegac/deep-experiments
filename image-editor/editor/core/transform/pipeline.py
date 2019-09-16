from typing import List

import numpy as np

from editor.core.api.data_pipeline import DataTransform


class PipelineTransform(DataTransform):
    def __init__(self, pipeline: List[DataTransform]):
        self.pipeline = pipeline

    def apply(self, data: np.ndarray) -> np.ndarray:
        for step in self.pipeline:
            if step is not None:
                data = step.apply(data)
        return data
