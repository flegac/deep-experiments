import tkinter as tk


class TextEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str, path: str):
        super().__init__(master, text="data", width=300)

        import tkinter as tk
        from tkinter.scrolledtext import ScrolledText

        self.editor = ScrolledText(self, width=100, height=80, wrap=tk.WORD)
        self.editor.pack()
        if path is not None:
            self.open_text(path)

    def open_text(self, path: str):
        with open(path) as _:
            text = _.read()
        self.editor.insert('1.0', text)
