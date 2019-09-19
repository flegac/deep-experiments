import cv2

from editor_core.datasource.opencv_source import OpencvSource
from editor_core.datasource.rasterio_source import RasterioSource


class FileSource(object):
    @staticmethod
    def from_gray(path: str):
        return OpencvSource(path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def from_rgb(path: str):
        return OpencvSource(path, cv2.IMREAD_COLOR)
        # return RasterioSource(path)

    @staticmethod
    def from_rio(path: str):
        return RasterioSource(path)
