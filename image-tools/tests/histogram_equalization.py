import glob
import os
import uuid
from time import time

import cv2

from image_clustering.image_utils import contrast_stretching, img_stats, match_hist


def timing(f):
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('Elapsed time: {}'.format(end - start))
        return result

    return wrapper


@timing
def hist_equalizer():
    os.makedirs('tiles', exist_ok=True)
    images = [contrast_stretching(cv2.imread(_)) for _ in list(sorted(glob.glob('../image_editor/tiles/**/*.png')))]
    for _ in images:
        img_stats([_], 'tiles/{}.png'.format(str(uuid.uuid4())))

    dataset = '20190802_export_s2_it1'
    images = list(sorted(
        glob.glob('/home/flegac/.change-detection/local_campaign/00_data_raw/{}/images/*_0.tif'.format(dataset))))
    for _ in ['stats', 'source', 'cs']:
        os.makedirs(os.path.join(dataset, _), exist_ok=True)

    for _ in images:
        name = os.path.basename(_).replace('_0.tif', '')
        source1 = cv2.imread(_)
        source2 = cv2.imread(_.replace('_0.tif', '_1.tif'))
        source2 = match_hist(source2, source1)

        cs1 = contrast_stretching(source1, percentiles=1)
        cs2 = contrast_stretching(source2, percentiles=1)

        cv2.imwrite('{}/source/{}_0.png'.format(dataset, name), source1)
        cv2.imwrite('{}/source/{}_1.png'.format(dataset, name), source2)

        cv2.imwrite('{}/cs/{}_0.png'.format(dataset, name), cs1)
        cv2.imwrite('{}/cs/{}_1.png'.format(dataset, name), cs2)

        img_stats([source1, source2], '{}/stats/{}_source.png'.format(dataset, name))
        img_stats([cs1, cs2], '{}/stats/{}_cs.png'.format(dataset, name))


if __name__ == '__main__':
    hist_equalizer()
