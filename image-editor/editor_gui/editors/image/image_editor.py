import tkinter as tk

from editor_gui.editors.image.image_view import ImageView
from editor_gui.editors.image.layer_editor import LayerEditor


class ImageEditor(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget, name: str, path: str = None):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # view
        self.view = ImageView(self)
        self.view.grid(row=0, column=0, sticky='nsew')

        # editors
        self.layer_editor = LayerEditor(self, self.view.on_source_change)
        self.layer_editor.grid(row=0, column=1, sticky='nsew')

        if path is not None:
            self.layer_editor.source_editor.open(path)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageEditor(root, None, None)
    editor.pack(fill='both', expand=True)
    root.mainloop()
