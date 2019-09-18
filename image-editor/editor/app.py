from editor.core.plugin.plugin_manager import EDITOR
from editor.ui_tk.window import Win
from plugin_0.plugin_0 import Plugin0
from plugin_tiling.tiling import TilingPlugin

if __name__ == '__main__':
    win = Win()
    EDITOR.load(Plugin0())

    EDITOR.load(TilingPlugin())

    win.config_menu({
        'File': {
            'Open': win.editor.open
        },
        'Edit': {},
        'Help': {}
    })

    win.mainloop()
