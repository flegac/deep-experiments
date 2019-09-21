import tkinter as tk
from typing import Callable

from editor_gui.editors.image.operator_toolbox import OperatorToolbox
from editor_gui.editors.image.source_editor import SourceEditor
from editor_gui.editors.image.visu_editor import VisuEditor


class LayerEditor(tk.Frame):
    def __init__(self, master: tk.Widget, on_update: Callable[[], None]):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.source_editor = SourceEditor(self)
        self.source_editor.grid(row=0, sticky='new')
        self.source_editor.update_bus.subscribe(on_next=lambda _: on_update())

        self.transform_editor = OperatorToolbox(self, self.source_editor.push_operator)
        self.transform_editor.grid(row=1, sticky='sew')

        self.visu_editor = VisuEditor(self)
        self.visu_editor.grid(row=2, column=0, sticky='sew')
