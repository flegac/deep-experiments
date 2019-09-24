import tkinter as tk

from editor_core.stats_visus.gui.histogram_panel import HistogramPanel
from editor_core.datasource.gui.source_editor import SourceEditor
from editor_core.dataoperator.gui.operator_toolbox import OperatorToolbox
from editor_core.tagging.gui.box_tag_panel import BoxTagPanel


class ImageControlPanel(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)

        self.source_editor = SourceEditor(self)
        self.source_editor.pack(fill='both', expand=True, side=tk.TOP)

        self.transform_editor = OperatorToolbox(self, self.source_editor.push_operator)
        self.transform_editor.pack(fill='both', expand=True, side=tk.TOP)

        self.visu_editor = HistogramPanel(self)
        self.visu_editor.pack(fill='both', expand=True, side=tk.TOP)

        self.box = BoxTagPanel(self)
        self.box.pack(fill='both', expand=True, side=tk.TOP)

        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack(fill='both', expand=True, side=tk.TOP)

        self.source_editor.update_bus.subscribe(on_next=lambda _: self.text.set(self.source_editor.source_descriptor))
        self.source_editor.update_bus.subscribe(on_next=lambda _: self.visu_editor.update_data(_))


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageControlPanel(root)
    editor.pack()
    root.mainloop()
