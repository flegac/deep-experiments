import tkinter as tk
from typing import Callable

from editor.ui_tk.source_editor import SourceEditor
from editor.ui_tk.transform_editor import TransformEditor
from editor.ui_tk.visu_editor import VisuEditor


class LayerEditor(tk.LabelFrame):
    def __init__(self, master, on_update: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='layers')

        # Make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.pack(fill="both", expand=True)

        self.source_editor = SourceEditor(self, on_update)
        self.source_editor.grid(row=0, sticky='new')
        # self.source_editor.pack(fill="both", expand=True)

        self.transform_editor = TransformEditor(self, on_update)
        self.transform_editor.grid(row=1, sticky='sew')
        # self.transform_editor.pack(fill="both", expand=True)

        self.visu_editor = VisuEditor(self)
        # self.transform_editor.pack(fill="both", expand=True)
        self.visu_editor.grid(row=2, column=0, sticky='sew')

    def get_source(self):
        return self.transform_editor.get_transform()(self.source_editor.get_source()())
