from typing import Tuple

from editor_api.data.data_source import TableSource


class BoxTableSource(TableSource):
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
