import tkinter as tk
from typing import Callable, Any, Dict

Action = Callable[[], Any]


class GenericToolbox(tk.Frame):
    def __init__(self, master: tk.Widget, actions: Dict[str, Action]):
        tk.Frame.__init__(self, master)
        for label, action in actions.items():
            tk.Button(
                self,
                text=label,
                command=action
            ).pack(fill='both', expand=True, side=tk.LEFT)


if __name__ == '__main__':
    root = tk.Tk()
    editor = GenericToolbox(root, {
        'toto': lambda: None,
        'tata': lambda: None,
        'titi': lambda: None,

    })
    editor.pack(fill='both', expand=True)
    root.mainloop()
