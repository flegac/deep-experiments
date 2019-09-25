from editor_core.image.opencv_source import OpencvSource
from editor_core.image.rasterio_source import RasterioSource


class FileSource(object):
    @staticmethod
    def from_gray(path: str):
        return OpencvSource.from_gray(path)

    @staticmethod
    def from_rgb(path: str):
        return OpencvSource.from_rgb(path)
        # return RasterioSource(path)

    @staticmethod
    def from_rio(path: str):
        return RasterioSource(path)
