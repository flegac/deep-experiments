import os
import tkinter as tk
import tkinter.filedialog
from typing import Mapping, Union, Callable

from editor_gui.config import EDITOR_CONFIG

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


def build_menu(parent, config: MenuConfig) -> tk.Menu:
    menu = tk.Menu(parent)
    for label, commands in config.items():
        if isinstance(commands, Callable):
            menu.add_command(label=label, command=commands)
        else:
            sub_menu = tk.Menu(menu, tearoff=0)
            for cmd_label, command in commands.items():
                sub_menu.add_command(label=cmd_label, command=command)
            menu.add_cascade(label=label, menu=sub_menu)
    return menu


def add_popup(widget, menu: tk.Menu):
    def popup(event):
        try:
            menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            menu.grab_release()

    widget.bind('<Button-3>', popup)


def dir_selection():
    path = tkinter.filedialog.askdirectory(
        initialdir=EDITOR_CONFIG.config.get('project_browser_path'),
    )

    __update_browser_config('project_browser_path', path)

    return path


def file_selection():
    paths = tkinter.filedialog.askopenfilenames(
        initialdir=EDITOR_CONFIG.config.get('file_browser_path'),
        title="Open image",
        filetypes=[
            ('all files', '.*'),
            ('csv files', '.csv'),
            ('tiff files', '.tif'),
            ('png files', '.png'),
            ('Jpeg files', '.jpg'),

        ]
    )
    if len(paths) > 0:
        __update_browser_config('file_browser_path', os.path.dirname(paths[0]))

    return paths


def __update_browser_config(param: str, path: str):
    if path is None or len(path) == 0:
        return
    EDITOR_CONFIG.config[param] = path

    if not EDITOR_CONFIG.config_path_is_valid('project_browser_path'):
        EDITOR_CONFIG.config['project_browser_path'] = path
    if not EDITOR_CONFIG.config_path_is_valid('file_browser_path'):
        EDITOR_CONFIG.config['file_browser_path'] = path
    EDITOR_CONFIG.save_config()
