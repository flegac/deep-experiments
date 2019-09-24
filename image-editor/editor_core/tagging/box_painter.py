from typing import Tuple

import cv2
import pandas as pd
from rx.subject import Subject

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataOperator


class TagBoxManager(DataOperator):
    def __init__(self, canvas):
        self.canvas = canvas
        self.brush_size = 8
        self.brush_func = cv2.rectangle
        self.color = (0, 255, 0)
        self.thickness = 1

        self.boxes = pd.DataFrame(columns=['center_x', 'center_y', 'left', 'right', 'top', 'bottom'])
        self.update_bus = Subject()

    def brush(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.brush_size += 4
        if event.num == 4 or event.delta == 120:
            self.brush_size -= 4

    def clear(self):
        self.boxes.drop()

    def save_dataset(self, path: str):
        self.boxes.to_csv(path, index=False)

    def load_dataset(self, dataset: pd.DataFrame):
        self.boxes = dataset
        self.update_bus.on_next(self.boxes)

    def create_box(self, center: Tuple[int, int]):
        img_x, img_y = center
        left = img_x - self.brush_size
        right = img_x + self.brush_size
        top = img_y - self.brush_size
        bottom = img_y + self.brush_size
        self.boxes = self.boxes.append({
            'center_x': center[0],
            'center_y': center[1],
            'left': left,
            'right': right,
            'top': top,
            'bottom': bottom,
        }, ignore_index=True)
        self.update_bus.on_next(self.boxes)

    def apply(self, data: Buffer) -> Buffer:
        data = data.copy()
        for box in self.boxes.iterrows():
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
