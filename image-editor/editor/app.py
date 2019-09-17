from editor.core.plugin.plugin_manager import EDITOR
from editor.ui_tk.window import Win
from plugin_0.plugin_0 import Plugin0

if __name__ == '__main__':
    win = Win()
    EDITOR.load(Plugin0())

    win.config_menu({
        'File': {
            'Open': win.editor.open
        },
        'Edit': {},
        'Help': {}
    })

    win.mainloop()
