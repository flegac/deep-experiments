import tkinter as tk


class HiddenScrollbar(tk.Scrollbar):
    def set(self, lo, hi):
        self.tk.call("grid", "remove", self)
        tk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise ValueError("cannot use pack with this widget")

    def place(self, **kw):
        raise ValueError("cannot use place with this widget")
