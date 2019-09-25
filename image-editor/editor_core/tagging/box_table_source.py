from typing import Tuple

import cv2

from editor_api.data.buffer import Buffer
from editor_api.data.data_operator import DataOperator
from editor_api.data.data_source import TableSource


class BoxTableSource(TableSource, DataOperator):
    def __init__(self):
        super().__init__(columns=['tag', 'center_x', 'center_y', 'left', 'right', 'top', 'bottom'])

    def add_box(self, center: Tuple[int, int], radius: int, tag: int = -1):
        center_x, center_y = center
        left = center_x - radius
        right = center_x + radius
        top = center_y - radius
        bottom = center_y + radius
        self.add_row([
            tag,
            center_x, center_y,
            left, right, top, bottom,
        ])

    def apply(self, data: Buffer) -> Buffer:
        data = data.copy()
        for box in self.get_table().iterrows():
            try:
                box = box[1]
                cv2.rectangle(
                    data,
                    (box.left, box.top), (box.right, box.bottom),
                    color=(0, 255, 0),
                    thickness=1
                )
            except:
                pass
        return data
