import tkinter as tk

from data_editor.editor.control_panel import ImageControlPanel
from data_editor.buffer.image_view import ImageView
from data_editor.table.table_view import TableView
from data_editor.text.text_view import TextView
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data_types import DataType


class ImageEditor(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget, name: str = None, source: BufferSource = None):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # view
        self.view = ImageView(self)
        self.view.grid(row=0, column=0, sticky='nsew')

        # editors
        self.control_panel = ImageControlPanel(self)
        self.control_panel.grid(row=0, column=1, sticky='nsew')
        self.control_panel.source.update_bus.subscribe(on_next=self.view.request_update)

        tag_box = self.control_panel.box.source
        self.control_panel.box.update_bus.subscribe(
            on_next=lambda _: self.view.request_update(tag_box.as_source(self.control_panel.source.source)))
        self.view.canvas.bind_all('a', lambda _: self.control_panel.box.create_box(self.view.mouse_image_coords()))

        self.control_panel.source.open_image(source)

    def show_buffer(self, source: BufferSource):
        self.view.destroy()
        self.view = ImageEditor(self)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageEditor(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
