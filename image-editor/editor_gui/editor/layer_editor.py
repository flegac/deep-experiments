import tkinter as tk
from typing import Callable

from editor_gui.editor.source_editor import SourceEditor
from editor_gui.editor.transform_editor import TransformEditor
from editor_gui.editor.visu_editor import VisuEditor


class LayerEditor(tk.Frame):
    def __init__(self, master, on_update: Callable[[], None]):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.source_editor = SourceEditor(self, on_update)
        self.source_editor.grid(row=0, sticky='new')

        self.transform_editor = TransformEditor(self, on_update)
        self.transform_editor.grid(row=1, sticky='sew')

        self.visu_editor = VisuEditor(self)
        self.visu_editor.grid(row=2, column=0, sticky='sew')
