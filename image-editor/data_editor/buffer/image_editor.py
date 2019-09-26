import tkinter as tk

from data_editor.buffer.image_control_panel import ImageControlPanel
from data_editor.buffer.image_view import ImageView


class ImageEditor(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget, name: str = None, path: str = None):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # view
        self.view = ImageView(self)
        self.view.grid(row=0, column=0, sticky='nsew')

        # editors
        self.control_panel = ImageControlPanel(self)
        self.control_panel.grid(row=0, column=1, sticky='nsew')
        self.control_panel.source_editor.update_bus.subscribe(on_next=self.view.request_update)

        tag_box = self.control_panel.box.source
        self.control_panel.box.update_bus.subscribe(
            on_next=lambda _: self.view.request_update(tag_box.as_source(self.control_panel.source_editor.source)))
        self.view.canvas.bind_all('a', lambda _: self.control_panel.box.create_box(self.view.mouse_image_coords()))

        if path is not None:
            self.control_panel.source_editor.open_image(path)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageEditor(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
