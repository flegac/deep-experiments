from typing import Tuple, Callable

from matplotlib.colors import to_rgb

from image_clustering.tiler import Box


class Flag(object):
    @staticmethod
    def from_name(box: Box, color: str):
        r, g, b = to_rgb(color)

        return Flag(box, (r * 255, g * 255, b * 255))

    def __init__(self, box: Box, color: Tuple[int, int, int]):
        self.box = box
        self.color = color


FlagComputer = Callable[[Box], Flag]