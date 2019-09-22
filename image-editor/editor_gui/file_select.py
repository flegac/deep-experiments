import os
import tkinter.filedialog
from typing import List, Tuple

from editor_core.config.editor import Editor, EditorManager


def ask_open_project(editor: Editor):
    path = tkinter.filedialog.askopenfilename(
        initialdir=editor.root_path,
        title="Select project",
        filetypes=[
            ('project files', 'project.json'),
            ('all files', '.*'),
        ]
    )
    return os.path.basename(os.path.dirname(path))


def ask_open_image(editor: Editor):
    return ask_open_file(editor, 'Open image', [
        ('all files', '.*'),
        ('tiff files', '.tif'),
        ('png files', '.png'),
        ('Jpeg files', '.jpg'),
    ])


def ask_open_dataset(editor: Editor):
    return ask_open_file(editor, 'Open image', [
        ('all files', '.*'),
        ('csv files', '.csv'),
    ])


def ask_dir_selection(editor: Editor):
    path = tkinter.filedialog.askdirectory(
        initialdir=editor.browser_path,
    )

    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)

    return path


def ask_open_file(editor: Editor, title: str, filetypes: List[Tuple[str, str]]):
    path: str = tkinter.filedialog.askopenfilename(
        initialdir=editor.browser_path,
        title=title,
        filetypes=filetypes)

    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)

    return path


def ask_open_files(editor: Editor, title: str, filetypes: List[Tuple[str, str]]):
    paths = tkinter.filedialog.askopenfilenames(
        initialdir=editor.browser_path,
        title=title,
        filetypes=filetypes)
    path = paths[0]
    if path is not None and len(path) > 0:
        editor.browser_path = os.path.dirname(path)
        EditorManager.save(editor)
    return paths
