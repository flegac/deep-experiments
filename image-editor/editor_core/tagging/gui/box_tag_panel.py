import tkinter as tk


from editor_core.tagging.tag_box_manager import TagBoxManager
from editor_core.files.gui.file_select import ask_open_image, ask_save_file


class BoxTagPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='tags')

        self.tag_box = TagBoxManager()
        self.tag_box.update_bus.subscribe(on_next=self._redraw)

        self.text = tk.StringVar()
        label = tk.Label(self, textvariable=self.text)
        label.pack(fill='both', expand=True, side=tk.TOP)

        button = tk.Button(
            self,
            text='Open',
            command=lambda: self.tag_box.load_dataset(ask_open_image())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Save',
            command=lambda: self.tag_box.source.save(ask_save_file())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Clear',
            command=self.tag_box.clear
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Refresh',
            command=self.tag_box.request_update
        )
        button.pack(fill='both', expand=True, side=tk.BOTTOM)
        self._redraw()

    def _redraw(self, event=None):
        self.text.set('{} items'.format(self.tag_box.source.get_table().shape[0]))


if __name__ == '__main__':
    root = tk.Tk()
    editor = BoxTagPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
