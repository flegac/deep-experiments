import tkinter as tk
from typing import Callable

from editor_api.data import DataOperator, PipelineOperator
from editor_gui.config import EDITOR_CONFIG


class TransformEditor(tk.LabelFrame):
    def __init__(self, master, callback: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='transform')

        self.pipeline = PipelineOperator()

        transformers = list(filter(None, [_test_class_loader(cls) for cls in EDITOR_CONFIG.operators()]))
        for i in range(len(transformers)):
            def _callback(step: DataOperator):
                def run():
                    self.pipeline.add_transform(step)
                    callback()

                return run

            button = tk.Button(
                self,
                text=type(transformers[i]).__name__,
                command=_callback(transformers[i])
            )
            button.pack(fill='both', expand=True, side=tk.TOP)

        def _callback():
            self.pipeline.clear()
            callback()

        tk.Button(
            self,
            text='reset',
            command=_callback
        ).pack(fill='both', expand=True, side=tk.BOTTOM)

    def get_transform(self):
        return self.pipeline


def _test_class_loader(cls):
    try:
        return cls()
    except:
        return None


if __name__ == "__main__":
    root = tk.Tk()
    widget = TransformEditor(root, lambda: None)
    widget.pack()

    root.mainloop()
