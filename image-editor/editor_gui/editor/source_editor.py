import os
import tkinter as tk
from typing import Callable, List

from editor_api.data import DataSource, PipelineOperator
from editor_core.file_source import FileSource
from editor_gui.utils.ui_utils import file_selection
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master, on_update: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='sources')
        self.source = None
        self.transform = PipelineOperator() | NormalizeOperator()
        self.buttons = []
        self.on_update = on_update

        tk.Button(
            self,
            text='Open',
            command=self.open
        ).pack(fill="both", expand=True, side=tk.BOTTOM)

    def open(self, paths: List[str] = None):
        if paths is None:
            paths = file_selection()
        self.source = FileSource.from_rgb(paths[0])

        self.on_update()

        for _ in self.buttons:
            _.destroy()

        self.buttons = [
            tk.Label(self, text=os.path.basename(paths[0]))
        ]
        for _ in self.buttons:
            _.pack(fill="both", expand=True, side=tk.TOP)

    def get_source(self) -> DataSource:
        return self.transform(self.source)
