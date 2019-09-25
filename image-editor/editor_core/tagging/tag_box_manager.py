from typing import Tuple, Dict

import cv2
from rx.subject import Subject

from editor_api.data.buffer import Buffer
from editor_api.data.data_operator import DataOperator
from editor_api.data.data_source import TableSource
from editor_core.tagging.box_table_source import BoxTableSource


class TagBoxManager(DataOperator):
    def __init__(self, tag_colors: Dict[int, Tuple[int, int, int]] = None):
        self.source = BoxTableSource()
        self.update_bus = Subject()

        self.brush_size = 8
        self.brush_tag: int = -1

        self.tag_colors = tag_colors or {
            -1: (0, 255, 0)
        }
        self.draw_thickness = 1

    def request_update(self):
        self.update_bus.on_next(self.source)

    def clear(self):
        self.source.clear()
        self.request_update()

    def load_dataset(self, path: str):
        self.source.load(path)
        self.request_update()

    def replace_dataset(self, source: TableSource):
        self.source = source
        self.request_update()

    def create_box(self, center: Tuple[int, int]):
        self.source.add_box(center, self.brush_size, self.brush_tag)
        self.request_update()

    def apply(self, data: Buffer) -> Buffer:
        data = data.copy()
        for box in self.source.get_table().iterrows():
            try:
                box = box[1]
                cv2.rectangle(
                    data,
                    (box.left, box.top), (box.right, box.bottom),
                    color=self.tag_colors[box.tag],
                    thickness=self.draw_thickness
                )
            except:
                pass
        return data
