import os
import tkinter as tk
from tkinter import ttk
from typing import List

from editor.gui.editor.image_editor import ImageEditor
from editor.gui.utils.ui_utils import dataset_selection


class EditorManager(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="editor")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand="yes")

    def new_editor(self, text: str = 'editor'):
        frame = ttk.Frame(self.notebook)
        editor = ImageEditor(frame)
        editor.pack(fill="both", expand=True)

        self.notebook.add(frame, text=text)
        self.notebook.select(frame)
        return editor

    def open(self):
        paths = dataset_selection()
        self.open_files(paths)

    def open_files(self, paths: List[str]):
        for path in paths:
            editor = self.new_editor(os.path.basename(path))
            editor.layer_editor.source_editor.open([path])
