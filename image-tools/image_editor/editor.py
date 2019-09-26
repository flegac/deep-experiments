import glob

from image_editor.image_manager import ImageManager

images = glob.glob('../../feat-detection/detection/images/*_?.png')

for _ in images:
    ImageManager(_).start()
