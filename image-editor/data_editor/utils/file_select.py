import os
import tkinter.filedialog
from typing import List, Tuple

from data_editor.editor_config import EditorManager


def ask_open_project():
    # TODO: only display project names ?
    editor = EditorManager.load()

    path = tkinter.filedialog.askopenfilename(
        initialdir=editor.root_path,
        title="Select project",
        filetypes=[
            ('project files', 'project.json'),
            ('all files', '.*'),
        ]
    )
    return os.path.basename(os.path.dirname(path))


def ask_open_image():
    return ask_open_file('Open image', [
        ('all files', '.*'),
        ('tiff files', '.tif'),
        ('png files', '.png'),
        ('Jpeg files', '.jpg'),
    ])


def ask_open_dataset():
    return ask_open_file('Open image', [
        ('all files', '.*'),
        ('csv files', '.csv'),
    ])


def ask_dir_selection():
    editor = EditorManager.load()

    path = tkinter.filedialog.askdirectory(
        initialdir=editor.browser_path,
    )

    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)

    return path


def ask_open_file(title: str = 'Open', filetypes: List[Tuple[str, str]] = None):
    if filetypes is None:
        filetypes = [('all files', '.*')]
    editor = EditorManager.load()

    path: str = tkinter.filedialog.askopenfilename(
        initialdir=editor.browser_path,
        title=title,
        filetypes=filetypes)

    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)

    return path


def ask_save_file(title: str = 'Save', filetypes: List[Tuple[str, str]] = None):
    if filetypes is None:
        filetypes = [('all files', '.*')]
    editor = EditorManager.load()

    path: str = tkinter.filedialog.asksaveasfilename(
        initialdir=editor.browser_path,
        title=title,
        filetypes=filetypes
    )

    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)

    return path


def ask_open_files(title: str, filetypes: List[Tuple[str, str]]):
    editor = EditorManager.load()

    paths = tkinter.filedialog.askopenfilenames(
        initialdir=editor.browser_path,
        title=title,
        filetypes=filetypes)
    path = paths[0]
    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)
    return paths
