import tkinter as tk
from typing import Callable, Any

from data_editor.image.histogram_panel import HistogramPanel
from data_editor.image.image_source_panel import BufferSourcePanel
from data_editor.operator.operator_panel import OperatorPanel
from data_editor.operator.operator_toolbox import OperatorToolbox
from data_editor.tagging.box_tag_panel import BoxTagPanel
from data_toolbox.image.source.buffer_source import BufferSource


class ImageControlPanel(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)

        self.source = BufferSourcePanel(self)
        self.source.pack(fill=tk.X, expand=False, side=tk.TOP)

        self.operator = OperatorPanel(self)
        self.operator.pack(fill=tk.X, expand=False, side=tk.TOP)

        self.operator_toolbox = OperatorToolbox(self)
        self.operator_toolbox.pack(fill=tk.X, expand=False, side=tk.TOP)

        self.box = BoxTagPanel(self)
        self.box.pack(fill=tk.X, expand=False, side=tk.TOP)

        self.visu_editor = HistogramPanel(self)
        self.visu_editor.pack(fill='both', expand=False, side=tk.BOTTOM)

        # events
        self.operator_toolbox.subscribe(self.operator.push_operator)
        self.subscribe(on_next=lambda _: self.visu_editor.update_data(self.get_processed_source()))

    def get_processed_source(self) -> BufferSource:
        raw_source = self.source.source
        processed_source = self.operator.operator.as_source(raw_source)
        return processed_source

    def get_full_source(self) -> BufferSource:
        processed_source = self.get_processed_source()
        tagged_source = self.box.source.as_source(processed_source)
        return tagged_source

    def subscribe(self, on_next: Callable[[Any], None]):
        self.source.subscribe(on_next)
        self.operator.subscribe(on_next)
        self.box.subscribe(on_next)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageControlPanel(root)
    editor.pack()
    root.mainloop()
