import concurrent.futures

import rasterio
from rasterio._example import compute

def compute(data):
    return data

def main(infile, outfile, num_workers=4):
    with rasterio.Env():
        with rasterio.open(infile) as src:
            profile = src.profile
            profile.update(blockxsize=128, blockysize=128, tiled=True)

            with rasterio.open(outfile, "w", **profile) as dst:
                windows = [window for ij, window in dst.block_windows()]
                data_gen = (src.get_buffer(window=window) for window in windows)
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                    for window, result in zip(windows, executor.map(compute, data_gen)):
                        dst.write(result, window=window,
                                  )


in_path = 'test.tif'
out_path = 'output.tif'
if __name__ == '__main__':
    main(in_path, out_path)
