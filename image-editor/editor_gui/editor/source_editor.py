import tkinter as tk
from typing import Callable, List

from editor_api.data import DataSource, IdentityOperator, EmptySource, PipelineOperator, DataOperator
from editor_core.file_source import FileSource
from editor_gui.utils.ui_utils import file_selection
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master, on_update: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='sources')
        self.source = EmptySource()
        self.pipeline: PipelineOperator = IdentityOperator() | NormalizeOperator()
        self.buttons = []
        self._on_update = on_update

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

    def on_update(self):
        self._on_update()

        for _ in self.buttons:
            _.destroy()

        self.buttons = [
                           tk.Label(self, text=str(self.source))
                       ] + [
                           tk.Label(self, text=str(step))
                           for step in self.pipeline.pipeline
                       ]
        for _ in self.buttons:
            _.pack(fill="both", expand=True, side=tk.TOP)

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op
        self.on_update()

    def pop_operator(self):
        self.pipeline = PipelineOperator(self.pipeline.pipeline[:-1])
        self.on_update()

    def get_source(self) -> DataSource:
        return self.pipeline(self.source)
