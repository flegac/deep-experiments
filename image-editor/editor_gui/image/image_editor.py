import tkinter as tk

from editor_gui.image.layer_editor import LayerEditor
from editor_gui.image.view.image_view import ImageView


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
        self.layer_editor = LayerEditor(self)
        self.layer_editor.grid(row=0, column=1, sticky='nsew')
        self.layer_editor.source_editor.source_change_bus.subscribe(on_next= self.view.on_source_change)

        if path is not None:
            self.layer_editor.source_editor.open_image(path)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageEditor(root, None, None)
    editor.pack(fill='both', expand=True)
    root.mainloop()
