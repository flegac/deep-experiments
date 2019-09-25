import tkinter as tk

import pandas as pd
from pandastable import Table

# https://pandastable.readthedocs.io/en/latest/examples.html
from editor_api.data.data_source import TableSource


class TableEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str = None, path: str = None):
        super().__init__(master, text="data", width=300)

        self.source = TableSource(columns=['A', 'B', 'C', 'D'])
        self.source.add_row([0, 0, 0, 0])

        self.table = Table(
            self,
            dataframe=self.source.get_table(),
            showtoolbar=True,
            showstatusbar=True,
        )
        self.table.show()

        if path is not None:
            self.open_dataset(path)

    def ask_redraw(self, data: pd.DataFrame):
        self.table.model.df = data
        self.table.redraw()

    def open_dataset(self, path: str):
        self.source.load(path)
        self.table.model.df = self.source.get_table()
        self.table.redraw()


if __name__ == '__main__':
    root = tk.Tk(className=" Just another Text Editor")
    editor = TableEditor(root)
    editor.pack()
    root.mainloop()
