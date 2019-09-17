import os
from tkinter.filedialog import askopenfilenames

from editor.core.plugin.plugin_manager import EDITOR


def dataset_selection():
    paths = askopenfilenames(
        initialdir=EDITOR.config.get('dataset_selection_path'),
        title="Open image",
        filetypes=[
            ('tiff files', '.tif'),
            ('png files', '.png'),
            ('all files', '.*')
        ]
    )
    if len(paths) > 0:
        EDITOR.config['dataset_selection_path'] = os.path.dirname(paths[0])
    EDITOR.save_config()
    return paths
