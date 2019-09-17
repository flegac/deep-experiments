import tkinter as tk
from typing import Callable

from editor.core.plugin.plugin_manager import EDITOR
from editor.core.transformer.pipeline import PipelineTransform


class TransformEditor(tk.LabelFrame):
    def __init__(self, master, callback: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='transform')

        def class_loader(cls):
            try:
                return cls()
            except:
                return None

        # toolbox
        self.transforms = list(filter(None, [class_loader(cls) for cls in EDITOR.transformers]))

        self.variables = [tk.BooleanVar() for _ in self.transforms]

        for var, transform in zip(self.variables, self.transforms):
            tk.Checkbutton(self,
                           text=type(transform).__name__,
                           variable=var,
                           command=callback).pack(fill="both", expand=True)

    def get_transform(self):
        pipeline = [
            self.transforms[i]
            if self.variables[i].get()
            else None
            for i in range(len(self.transforms))
        ]

        return PipelineTransform(pipeline)


if __name__ == "__main__":
    root = tk.Tk()
    widget = TransformEditor(root, lambda: None)
    widget.pack()

    root.mainloop()
