from typing import List

from editor.core.data import DataTransformer, Buffer


class Pipeline(DataTransformer):
    def __init__(self, pipeline: List[DataTransformer] = None):
        self.pipeline: List[DataTransformer] = []
        if pipeline is not None:
            for step in pipeline:
                self.add_transform(step)

    def add_transform(self, step: DataTransformer):
        if step is not None:
            self.pipeline.append(step)

    def clear(self):
        self.pipeline.clear()

    def __call__(self, data: Buffer) -> Buffer:
        for step in self.pipeline:
            data = step(data)
        return data
