import tkinter as tk
from typing import Callable

from rx.subject import Subject

from data_editor.editor_config import EditorManager
from data_toolbox.data.data_operator import DataOperator


class OperatorToolbox(tk.LabelFrame):
    def __init__(self, master: tk.Widget, callback: Callable[[DataOperator], None]):
        tk.LabelFrame.__init__(self, master, text='operator', width=100, height=50)

        def _callback(op: DataOperator):
            def run():
                callback(op)

            return run

        operators = EditorManager.plugin.operators()
        for i in range(len(operators)):
            _ = operators[i]()

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


if __name__ == '__main__':
    root = tk.Tk()
    editor = OperatorToolbox(root, lambda _: None)
    editor.pack(expand=True, fill=tk.BOTH)
    root.mainloop()