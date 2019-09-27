import tkinter as tk
from typing import Callable, List


class MyListBox(tk.Frame):

    def __init__(self, master, list_model: Callable[[], List]):
        tk.Frame.__init__(self, master)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.list = tk.Listbox(self, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.list_model = list_model

        self.current = None
        self._redraw()

    def selected(self):
        return self.list.curselection()

    def _redraw(self):
        self.list.delete(0, self.list.size())

        for item in self.list_model():
            self.list.insert(tk.END, item)


if __name__ == '__main__':
    root = tk.Tk()
    MyListBox(root, lambda: list(range(100))).pack(fill='both', expand=True)
    root.mainloop()
