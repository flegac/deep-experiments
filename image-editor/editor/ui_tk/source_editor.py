import tkinter as tk
from typing import Callable, List

from editor.api.data import DataSource
from editor.plugins.core.datasource.multi_source import MultiSource
from editor.plugins.core.datasource.file_source import FileSource
from editor.ui_tk.utils.ui_utils import dataset_selection


class SourceEditor(tk.LabelFrame):
    def __init__(self, master, on_update: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='sources')
        self.layers = MultiSource()
        self.variables = None
        self.buttons = []
        self.on_update = on_update

        tk.Button(
            self,
            text='Open',
            command=self.open
        ).pack(fill="both", expand=True, side=tk.BOTTOM)

    def open(self, paths: List[str] = None):
        if paths is None:
            paths = dataset_selection()
        for _ in paths:
            self.layers.add_layer(FileSource.from_rgb(_))
        self._on_update()

    def get_source(self) -> DataSource:
        return self.layers

    def _on_update(self):
        self.on_update()

        self.variables = [tk.BooleanVar() for _ in self.layers.layers]

        for _ in self.buttons:
            _.destroy()
        self.buttons = [
            tk.Checkbutton(self, text=band.name, command=lambda: None)
            for var, band in zip(self.variables, self.layers.layers)
        ]
        for _ in self.buttons:
            _.pack(fill="both", expand=True, side=tk.TOP)
