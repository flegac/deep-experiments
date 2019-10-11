import os
import tkinter.filedialog

from data_editor.editor.editor_config import EditorManager


def ask_open_project():
    # TODO: only display project names ?
    editor = EditorManager.load()
    path = tkinter.filedialog.askdirectory(
        initialdir=editor.root_path,
    )
    return os.path.basename(path)
