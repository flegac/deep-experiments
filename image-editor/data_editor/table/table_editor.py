import tkinter as tk

import pandas as pd
from pandastable import Table

# https://pandastable.readthedocs.io/en/latest/examples.html
from data_toolbox.table.table_source import TableSource


class TableEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str = None, source: TableSource = None):
        super().__init__(master, text="data", width=300)

        self.table = Table(
            self,
            showtoolbar=True,
            showstatusbar=True,
        )
        self.table.show()

        self.open_dataset(source)

    def ask_redraw(self, data: pd.DataFrame):
        self.table.model.df = data
        self.table.redraw()

    def open_dataset(self, source: TableSource):
        if source is not None:
            self.source = source
            self.table.model.df = self.source.get_table()
            self.table.redraw()


if __name__ == '__main__':
    root = tk.Tk(className=" Just another Text Editor")
    editor = TableEditor(root)
    editor.pack()
    root.mainloop()
