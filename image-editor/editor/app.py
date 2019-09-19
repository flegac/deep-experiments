from tkinter import messagebox

from editor.config import EDITOR
from editor.plugins.image_filter.plugin import ImageFilterPlugin
from editor.plugins.tiling.plugin import TilingPlugin
from editor.gui.window import Win

if __name__ == '__main__':
    win = Win()
    EDITOR.load(ImageFilterPlugin())

    EDITOR.load(TilingPlugin())

    win.config_menu({
        'File': {
            'New': win.editor.new_editor,
            'Open': win.editor.open

        },
        'Edit': {},
        'Help': win.help
    })

    win.mainloop()
