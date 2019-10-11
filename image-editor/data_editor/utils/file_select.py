import os
import tkinter.filedialog
from typing import List, Tuple

from data_editor.editor.editor_config import EditorManager


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
