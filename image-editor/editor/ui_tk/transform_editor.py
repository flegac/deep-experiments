import tkinter as tk
from typing import Callable

from editor.core.api.data_pipeline import DataTransform
from editor.core.transform.pipeline import PipelineTransform


class TransformEditor(tk.Frame):
    def __init__(self, master, callback: Callable[[], None]):
        tk.Frame.__init__(self, master)

        def class_loader(cls):
            try:
                return cls()
            except:
                return None

        print([cls.__name__ for cls in DataTransform.__subclasses__()])

        # toolbox
        self.transforms = list(filter(None, [class_loader(cls) for cls in DataTransform.__subclasses__()]))

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
