import tkinter as tk

import pandas as pd
from pandastable import Table


# https://pandastable.readthedocs.io/en/latest/examples.html


class DatasetEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str = None, path: str = None):
        super().__init__(master, text="data", width=300)
        self.table = Table(
            self,
            dataframe=pd.DataFrame(data=[
                [0, 0, 0, 0]
            ], columns=['left', 'right', 'top', 'bottom']),
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
        self.table.importCSV(path)
        self.table.redraw()


if __name__ == '__main__':
    root = tk.Tk(className=" Just another Text Editor")
    editor = DatasetEditor(root)
    editor.pack()
    root.mainloop()
