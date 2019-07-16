import numpy as np
import sklearn
from skimage import filters
from skimage.measure import block_reduce

from mydeep_api.tensor import Tensor
from mydeep_utils.tensor_util import tensor_from_path, tensor_save
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def extract_features(rgb: Tensor):
    if len(rgb.shape) == 3:
        rgb = rgb[..., :3]
        gray = np.dot(rgb, [0.2989, 0.5870, 0.1140])
    else:
        gray = rgb
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    # gray = gaussian_filter(gray, sigma=1)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    gray = (gray - np.mean(gray)) / np.std(gray)
    gray = sklearn.preprocessing.normalize(gray)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    gray = block_reduce(gray, block_size=(2, 2), func=np.mean)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    val = filters.threshold_otsu(gray)
    mask = gray < val
    # plt.imshow(mask, cmap='gray', interpolation='nearest').figure.show()
    mask = mask.astype('uint8')
    mask *= 255
    mask = np.stack([mask, mask, mask])
    mask = np.moveaxis(mask, 0, 2)
    return mask


class TresholdFilter(Worker):

    def __init__(self):
        super().__init__()
        self.col_x = 'x'
        self.col_y = 'y'

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        ctx.project_ws \
            .get_ws('raw_dataset/images') \
            .files \
            .map(tensor_from_path) \
            .map(extract_features) \
            .enumerate() \
            .foreach(tensor_save(target_ws.path_to('images')))