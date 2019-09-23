from typing import Tuple

import cv2


class PaintController(object):
    def __init__(self, view):
        self.view = view
        self.redraw_bus = view.redraw_bus
        self.brush_size = 8
        self.brush_func = cv2.rectangle
        self.color = (0, 255, 0)
        self.thickness = 1

        self.boxes = []

    def bind(self):
        # # linux scroll
        # self.view.canvas.bind('<Button-4>', self.brush)
        # self.view.canvas.bind('<Button-5>', self.brush)
        # # windows scroll
        # self.view.canvas.bind('<MouseWheel>', self.brush)
        self.view.canvas.bind_all('a', lambda _: self.paint(self.view.viewport_controller.get_image_coords()))

    def brush(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.brush_size += 4
        if event.num == 4 or event.delta == 120:
            self.brush_size -= 4

    def paint(self, img_coords: Tuple[int, int]):
        img_x, img_y = img_coords
        self.boxes.append((
            (img_x - self.brush_size, img_y - self.brush_size),
            (img_x + self.brush_size, img_y + self.brush_size),
        ))
        self.redraw_bus.on_next(None)

    def apply(self, view):
        for box in self.boxes:
            view.data = cv2.rectangle(
                view.data,
                *box,
                color=(0, 255, 0),
                thickness=1
            )
        view.redraw_bus.on_next(None)
