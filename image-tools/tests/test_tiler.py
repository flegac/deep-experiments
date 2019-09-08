from image_clustering.tiler import Tiler, GridTiler


def test_tiler1():
    for _ in Tiler((2, 2)).tiles((20, 20)):
        print(_)


def test_tiler2():
    for _ in GridTiler(tile_size=10, stride=5).tiles((30, 20)):
        print(_)
