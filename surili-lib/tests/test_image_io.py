import numpy as np

from surili_core.surili_io.image_io import OpencvIO
from surili_core.workspace import Workspace

io = OpencvIO()


def test_image_io():
    with Workspace.temporary() as ws:
        img = np.zeros((20, 20, 3))
        for i in range(20):
            img[i, i, :] = 255
        path = io.write(ws.path_to('toto.png'), img)

        img2 = io.read(path)
        assert np.array_equal(img, img2)
