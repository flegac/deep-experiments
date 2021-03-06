import tkinter as tk
from typing import List, Dict, Callable, Any, Set

from rx.subject import Subject

from data_editor.utils.toolbox import Toolbox
from data_toolbox.image.mixer.blend_mixer import BlendMixer
from data_toolbox.image.mixer.compare_mixer import CompareMixer
from data_toolbox.image.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource
from data_toolbox.model.model_source import ModelSource
from data_toolbox.table.table_source import TableSource


class SourceBrowser(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)
        self._observer = Subject()

        self._sources: Set[DataSource] = set()

        # action box
        Toolbox(self, {
            'merge': self.merge_action,
            'compare': self.compare_action,
            'close': self.close_action,
            'view': lambda: None,
        }).pack(expand=False, fill=tk.X, side=tk.BOTTOM)

        self._widgets: List[tk.Widget] = []
        self._checkboxes: Dict[DataSource, tk.IntVar] = dict()
        self._redraw()

    def subscribe(self, on_next=Callable[[Any], None]):
        self._observer.subscribe(on_next)

    def add_source(self, source: DataSource):
        if source is None:
            return
        self._sources.add(source)
        self._redraw()

    def get_selection(self):
        selected = []
        for source, var in self._checkboxes.items():
            if var.get() > 0:
                selected.append(source)
        return selected

    def close_action(self):
        selected = self.get_selection()
        for _ in selected:
            self._sources.remove(_)
        if len(selected) > 0:
            self._redraw()

    def merge_action(self):
        selected = self.get_selection()
        if len(selected) > 0:
            source = BlendMixer().as_source(selected)
            self.add_source(source)

    def compare_action(self):
        selected = self.get_selection()
        if len(selected) > 0:
            source = CompareMixer().as_source(selected)
            self.add_source(source)

    def _redraw(self):
        for _ in self._widgets:
            _.destroy()
        self._widgets.clear()
        self._checkboxes.clear()

        buffers = list(filter(lambda _: isinstance(_, BufferSource), self._sources))
        tables = list(filter(lambda _: isinstance(_, TableSource), self._sources))
        models = list(filter(lambda _: isinstance(_, ModelSource), self._sources))

        unknown = list(filter(lambda _: _ not in buffers and _ not in tables and _ not in models, self._sources))
        self._create_source_group('images', buffers)
        self._create_source_group('tables', tables)
        self._create_source_group('models', models)
        self._create_source_group('unknown', unknown)

    def _create_source_group(self, label: str, sources: List[DataSource]):
        frame = tk.LabelFrame(self, text=label, width=100, height=25)
        frame.pack(fill=tk.X, expand=False, side=tk.TOP)
        for source in sources:
            widget, var = self._create_source_widget(frame, source)
            self._checkboxes[source] = var
        self._widgets.append(frame)
        import os
        os.path.abspath(os.path.curdir)

    def _create_source_widget(self, parent: tk.Frame, source: BufferSource):
        var = tk.IntVar()

        def open_source_callback(source: BufferSource):
            def run():
                self._observer.on_next(source)

            return run

        widget = tk.Frame(parent)
        tk.Checkbutton(widget, command=lambda: None, variable=var).pack(fill="both", expand=False, side=tk.LEFT)
        tk.Button(widget, text=str(source), command=open_source_callback(source)).pack(fill="both", expand=True,
                                                                                       side=tk.RIGHT)
        widget.pack(fill="both", expand=True, side=tk.TOP)
        return widget, var


if __name__ == '__main__':
    root = tk.Tk()
    SourceBrowser(root).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
