import imghdr
import tkinter as tk

from data_editor.editor.control_panel import ImageControlPanel
from data_editor.buffer.image_view import ImageView
from data_editor.table.table_view import TableView
from data_editor.text.text_view import TextView
from data_toolbox.buffer.buffer_factory import ImageFactory
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource
from data_toolbox.data_types import DataType
from data_toolbox.table.table_source import TableSource


class EditorPanel(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget, name: str = None, source: BufferSource = None):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # view
        self.views = {
            DataType.BUFFER: ImageView(self),
            DataType.TABLE: TableView(self),
            DataType.TEXT: TextView(self)
        }

        self.view = self.views[DataType.TABLE]
        self.view.grid(row=0, column=0, sticky='nsew')

        # editors
        self.control_panel = ImageControlPanel(self)
        self.control_panel.grid(row=0, column=1, sticky='nsew')
        self.control_panel.source.update_bus.subscribe(on_next=self.request_view_update)

        tag_box = self.control_panel.box.source
        self.control_panel.box.update_bus.subscribe(
            on_next=lambda _: self.request_view_update(tag_box.as_source(self.control_panel.source.source)))
        self.views[DataType.BUFFER].canvas.bind_all('a', lambda _: self.control_panel.box.create_box(
            self.view.mouse_image_coords()))

        self.control_panel.source.open_image(source)

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
            source = self.control_panel.source.operator.as_source(source)
            source = self.control_panel.box.source.as_source(source)

            self.view = self.views[DataType.BUFFER]
            self.view.request_update(source)
        if isinstance(source, str):
            self.view = self.views[DataType.TEXT]
            self.view.open_text(source)
        self.view.grid(row=0, column=0, sticky='nsew')


if __name__ == '__main__':
    root = tk.Tk()
    editor = EditorPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
