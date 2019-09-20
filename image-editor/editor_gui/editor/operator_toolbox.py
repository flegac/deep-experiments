import tkinter as tk
from typing import Callable

from editor_api.data import DataOperator
from editor_gui.config import EDITOR_CONFIG


class OperatorToolbox(tk.LabelFrame):
    def __init__(self, master, callback: Callable[[DataOperator], None], undo_callback: Callable[[], None]):
        tk.LabelFrame.__init__(self, master, text='operator')

        operators = list(filter(None, [_test_class_loader(cls) for cls in EDITOR_CONFIG.operators()]))
        for i in range(len(operators)):
            def _callback(step: DataOperator):
                def run():
                    callback(step)

                return run

            button = tk.Button(
                self,
                text=str(operators[i]),
                command=_callback(operators[i])
            )
            button.pack(fill='both', expand=True, side=tk.TOP)

        tk.Button(
            self,
            text='undo',
            command=undo_callback
        ).pack(fill='both', expand=True, side=tk.BOTTOM)


def _test_class_loader(cls):
    try:
        return cls()
    except:
        return None


if __name__ == "__main__":
    root = tk.Tk()
    widget = OperatorToolbox(root, lambda: None)
    widget.pack()

    root.mainloop()
