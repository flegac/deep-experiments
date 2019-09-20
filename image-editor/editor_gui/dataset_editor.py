import tkinter as tk

from pandastable import Table


# https://pandastable.readthedocs.io/en/latest/examples.html


class DatasetEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str, path: str):
        super().__init__(master, text="data", width=300)

        self.table = Table(
            self,
            showtoolbar=True,
            showstatusbar=True,
        )
        self.table.show()
        if path is not None:
            self.open_dataset(path)

    def open_dataset(self, path: str):
        self.table.importCSV(path)
        self.table.redraw()


