import tkinter as tk
from typing import Callable

from editor_api.data.data_core import DataOperator, DataSource, PipelineOperator
from editor_api.data.data_utils import EmptySource, DataUtils
from editor_core.file_source import FileSource
from editor_gui.utils.ui_utils import file_selection
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, on_update: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='sources')
        self.source = EmptySource()
        self.pipeline: PipelineOperator = DataUtils.identity | NormalizeOperator()
        self.buttons: tk.Widget = []
        self._on_update = on_update

        tk.Button(
            self,
            text='Open',
            command=self.open
        ).pack(fill="both", expand=True, side=tk.BOTTOM)

    def open(self, path: str = None):
        if path is None:
            path = file_selection()[0]
        self.source = FileSource.from_rgb(path)
        self.on_update()

    def on_update(self):
        self._on_update()

        for _ in self.buttons:
            _.destroy()

        editor = self

        def _callback(step: DataOperator):
            def run():
                editor.remove_operator(step)

            return run

        self.buttons = [
            tk.Label(self, text=str(self.source)),
            *[
                tk.Button(self, text=str(step), command=_callback(step))
                for step in self.pipeline.pipeline
            ]
        ]
        for _ in self.buttons:
            _.pack(fill="both", expand=True, side=tk.TOP)

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op()
        self.on_update()

    def pop_operator(self):
        self.pipeline = PipelineOperator(self.pipeline.pipeline[:-1])
        self.on_update()

    def remove_operator(self, op: DataOperator):
        pipe = self.pipeline.pipeline
        pipe.remove(op)
        self.pipeline = PipelineOperator(pipe)
        self.on_update()

    def get_source(self) -> DataSource:
        return self.pipeline(self.source)
