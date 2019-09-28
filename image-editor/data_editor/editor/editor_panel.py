import imghdr
import tkinter as tk

from data_editor.image.image_view import ImageView
from data_editor.editor.control_panel import ImageControlPanel
from data_editor.table.table_view import TableView
from data_editor.text.text_view import TextView
from data_toolbox.image.buffer_factory import ImageFactory
from data_toolbox.image.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource
from data_toolbox.data_types import DataType
from data_toolbox.table.table_source import TableSource


class EditorPanel(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget,  source: BufferSource = None):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # view
        self.views = {
            DataType.BUFFER: ImageView(self),
            DataType.TABLE: TableView(self),
            DataType.TEXT: TextView(self)
        }

        self.view = self.views[DataType.BUFFER]
        self.view.grid(row=0, column=0, sticky='nsew')

        # editors
        self.control_panel = ImageControlPanel(self)
        self.control_panel.grid(row=0, column=1, sticky='nsew')
        # self.control_panel.subscribe(on_next=self.request_view_update)

        self.control_panel.subscribe(
            on_next=lambda _: self.view.set_source(self.control_panel.get_full_source()))
        self.views[DataType.BUFFER].canvas.bind_all('a', lambda _: self.control_panel.box.create_box(
            self.view.mouse_image_coords()))

        self.control_panel.source.set_source(source)

    def request_view_update(self, source: DataSource):
        self.view.grid_forget()
        if isinstance(source, str):
            path = source
            if path.endswith('.csv'):
                source = TableSource().load(path)
            elif imghdr.what(path) is not None:
                source = ImageFactory.from_rgb(path)
            elif path.endswith('.txt') or path.endswith('.json') or path.endswith('.py'):
                # TODO create TextSource
                pass
            else:
                print('unsupported file format !')
        if isinstance(source, TableSource):
            self.view = self.views[DataType.TABLE]
            self.view.open_dataset(source)
        if isinstance(source, BufferSource):
            self.view = self.views[DataType.BUFFER]
            # self.view.request_update(source)
            self.control_panel.source.set_source(source)

        if isinstance(source, str):
            self.view = self.views[DataType.TEXT]
            self.view.open_text(source)
        self.view.grid(row=0, column=0, sticky='nsew')


if __name__ == '__main__':
    root = tk.Tk()
    editor = EditorPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
