from editor.core.plugin.plugin_manager import PLUGIN_MANAGER
from editor.ui_tk.window import Win
from editor_plugin.img_transform import Plugin0

if __name__ == '__main__':
    win = Win()
    PLUGIN_MANAGER.load(Plugin0())

    win.config_menu({
        'File': {
            'Open': win.editor.open
        },
        'Edit': {},
        'Help': {}
    })

    win.mainloop()
