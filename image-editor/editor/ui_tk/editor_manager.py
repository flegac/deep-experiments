import os
import tkinter as tk
from tkinter import ttk
from typing import List

from editor.ui_tk.image_editor import ImageEditor
from editor.ui_tk.utils.ui_utils import dataset_selection


class EditorManager(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="image editor")
        self.pack(fill="both", expand="yes")
        self.notebook = ttk.Notebook(self, width=1024, height=800)
        self.notebook.pack(fill="both", expand="yes")
        self.editors = []

    def new_editor(self, text: str = 'editor'):
        frame = ttk.Frame(self.notebook)
        editor = ImageEditor(frame)
        self.editors.append(editor)
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
