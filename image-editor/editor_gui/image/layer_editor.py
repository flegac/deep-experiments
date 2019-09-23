import tkinter as tk

from editor_gui.image.visu_editor import VisuEditor
from editor_gui.image.source_editor import SourceEditor
from editor_gui.image.operator_toolbox import OperatorToolbox
from editor_gui.image.file_toolbox import FileToolbox


class LayerEditor(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.source_editor = SourceEditor(self)
        self.source_editor.grid(row=0, sticky='new')

        self.file_box = FileToolbox(self, self.source_editor.open_image, self.source_editor.save_image)
        self.file_box.grid(row=1, sticky='sew')

        self.transform_editor = OperatorToolbox(self, self.source_editor.push_operator)
        self.transform_editor.grid(row=2, sticky='sew')

        self.visu_editor = VisuEditor(self)
        self.visu_editor.grid(row=3, column=0, sticky='sew')
        self.source_editor.source_change_bus.subscribe(on_next=lambda _: self.visu_editor.update_data('data', _))


if __name__ == '__main__':
    root = tk.Tk()
    editor = LayerEditor(root)
    editor.pack()
    root.mainloop()
