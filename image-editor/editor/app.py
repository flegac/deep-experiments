from editor.ui_tk.window import Win
from editor_plugin import img_transform

if __name__ == '__main__':
    img_transform.plugin_init()

    win = Win()

    win.config_menu({
        'File': {
            'Open': win.editor.open
        },
        'Edit': {},
        'Help': {}
    })

    win.mainloop()
