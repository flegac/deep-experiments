import tkinter as tk

import pandas as pd
from pandastable import Table

# https://pandastable.readthedocs.io/en/latest/examples.html

class DataBrowser(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="data", width=300)

        self.table = Table(
            self,
            dataframe=pd.DataFrame({
                'x': ['file_path'],
                'y': ['file_path']
            }),
            showtoolbar=True,
            showstatusbar=True,
        )

        self.table.show()
