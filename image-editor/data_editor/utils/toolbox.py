import tkinter as tk
from typing import Callable, Any, Dict

from data_editor.utils.file_select import ask_open_image, ask_save_file

Action = Callable[[], Any]


class Toolbox(tk.Frame):
    def __init__(self, master: tk.Widget, actions: Dict[str, Action]):
        tk.Frame.__init__(self, master)
        for label, action in actions.items():
            tk.Button(
                self,
                text=label,
                command=action
            ).pack(fill='both', expand=True, side=tk.LEFT)


class FileToolbox(Toolbox):

    def __init__(self, master: tk.Widget, open_func: Callable[[str], Any], save_func: Callable[[str], Any]):
        super().__init__(master, {
            'Open': lambda: open_func(ask_open_image()),
            'Save': lambda: save_func(ask_save_file())
        })


if __name__ == '__main__':
    root = tk.Tk()
    editor = Toolbox(root, {
        'toto': lambda: None,
        'tata': lambda: None,
        'titi': lambda: None,

    })
    editor.pack(fill='both', expand=True)
    root.mainloop()
