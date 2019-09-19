import os
import tkinter.filedialog

from editor_gui.config import EDITOR_CONFIG


def dir_selection():
    path = tkinter.filedialog.askdirectory(
        initialdir=EDITOR_CONFIG.config.get('directory_browser_path'),
    )

    __update_browser_config('directory_browser_path', path)

    return path


def file_selection():
    paths = tkinter.filedialog.askopenfilenames(
        initialdir=EDITOR_CONFIG.config.get('file_browser_path'),
        title="Open image",
        filetypes=[
            ('tiff files', '.tif'),
            ('png files', '.png'),
            ('all files', '.*')
        ]
    )
    if len(paths) > 0:
        __update_browser_config('file_browser_path', os.path.dirname(paths[0]))

    return paths


def __update_browser_config(param: str, path: str):
    if path is None or len(path) == 0:
        return
    EDITOR_CONFIG.config[param] = path

    if not EDITOR_CONFIG.config_path_is_valid('directory_browser_path'):
        EDITOR_CONFIG.config['directory_browser_path'] = path
    if not EDITOR_CONFIG.config_path_is_valid('file_browser_path'):
        EDITOR_CONFIG.config['file_browser_path'] = path
    EDITOR_CONFIG.save_config()
