import tkinter as tk
from typing import Callable

from rx.subject import Subject

from data_editor.editor_config import EditorManager
from data_toolbox.data.data_operator import DataOperator


class OperatorToolbox(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='operator', width=100, height=50)
        self._observer = Subject()

        def _callback(op: DataOperator):
            def run():
                self._observer.on_next(op)

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

    def subscribe(self, on_next: Callable[[DataOperator], None]):
        self._observer.subscribe(on_next)


def _test_class_loader(cls):
    try:
        return cls()
    except:
        return None


if __name__ == '__main__':
    root = tk.Tk()
    editor = OperatorToolbox(root)
    editor.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
