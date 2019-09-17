import tkinter as tk

from editor.core.datasource.rgb_source import RGBSource


class MultiBandEditor(tk.Frame):
    def __init__(self, master, multi_band: RGBSource):
        tk.Frame.__init__(self, master)
        self.multi_band = multi_band
        self.variables = None

        self.buttons = []

    def update(self):
        self.variables = [tk.BooleanVar(value=_.is_active) for _ in self.multi_band.bands]

        def updater(band, var):
            band.is_active = not var.get()

        for _ in self.buttons:
            _.destroy()
        self.buttons = [
            tk.Checkbutton(self,
                           text=band.name,
                           variable=var,
                           command=lambda: updater(band, var))
            for var, band in zip(self.variables, self.multi_band.bands)
        ]
        for _ in self.buttons:
            _.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    multi_band = RGBSource('')
    multi_band.open('../tests/test.jpg')
    widget = MultiBandEditor(root, multi_band)
    widget.pack()

    root.mainloop()
