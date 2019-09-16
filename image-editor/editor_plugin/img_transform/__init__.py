from editor_plugin.img_transform.contrast_stretching import ContrastStretchingTransform
from editor_plugin.img_transform.edge_detection import EdgeDetectionTransform
from editor_plugin.img_transform.normalize import NormalizeTransform


def plugin_init():
    ContrastStretchingTransform()
    EdgeDetectionTransform()
    NormalizeTransform()
