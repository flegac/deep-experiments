import tkinter as tk
from typing import Callable

from editor_api.data.data_core import DataOperator
from editor_model.editor import EditorManager


class OperatorToolbox(tk.LabelFrame):
    def __init__(self, master: tk.Widget, callback: Callable[[DataOperator], None]):
        tk.LabelFrame.__init__(self, master, text='operator')

        operators = EditorManager.plugin.operators()

        for i in range(len(operators)):
            _ = operators[i]()

            def _callback(op: DataOperator):
                def run():
                    callback(op)

                return run

            button = tk.Button(
                self,
                text=str(_),
                command=_callback(operators[i])
            )
            button.pack(fill='both', expand=True, side=tk.TOP)


def _test_class_loader(cls):
    try:
        return cls()
    except:
        return None
