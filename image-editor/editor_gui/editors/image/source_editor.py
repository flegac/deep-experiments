import tkinter as tk

from rx.subject import Subject

from editor_api.data.data_core import DataOperator, DataSource, PipelineOperator
from editor_api.data.data_utils import EmptySource
from editor_core.file_source import FileSource
from editor_gui.file_select import ask_open_image
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='source')
        self.source = EmptySource()
        self.pipeline: PipelineOperator = PipelineOperator([NormalizeOperator()])
        self.buttons: tk.Widget = []

        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self.redraw_pipeline)

        tk.Button(
            self,
            text='Open',
            command=lambda: self.open(ask_open_image())
        ).pack(fill="both", expand=True, side=tk.BOTTOM)

    def open(self, path: str = None):
        self.source = FileSource.from_rgb(path)
        self.update_bus.on_next(None)

    def reset(self):
        self.pipeline = PipelineOperator()
        self.update_bus.on_next(None)

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op()
        self.update_bus.on_next(None)

    def pop_operator(self):
        self.pipeline = PipelineOperator(self.pipeline.pipeline[:-1])
        self.update_bus.on_next(None)

    def remove_operator(self, op: DataOperator):
        pipe = self.pipeline.pipeline
        pipe.remove(op)
        self.pipeline = PipelineOperator(pipe)
        self.update_bus.on_next(None)

    def get_source(self) -> DataSource:
        return self.source | self.pipeline

    def redraw_pipeline(self, event=None):
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
        if len(self.buttons) > 1:
            self.buttons.append(tk.Button(self, text='Reset', command=self.reset))

        for _ in self.buttons:
            _.pack(fill="both", expand=True, side=tk.TOP)


if __name__ == '__main__':
    root = tk.Tk()
    editor = SourceEditor(root)
    editor.pack(fill="both", expand=True, side=tk.BOTTOM)

    root.mainloop()
