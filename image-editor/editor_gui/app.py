import os

from editor_gui.config import EDITOR_CONFIG
from editor_gui.utils.ui_utils import dir_selection, file_selection
from editor_gui.window import Win


def opopen_project():
    path = dir_selection()
    win.browser.open(path)


def open_editor():
    paths = file_selection()
    name, _ = os.path.splitext(os.path.basename(paths[0]))
    win.editor.create(name, paths)


if __name__ == '__main__':
    win = Win()

    win.config_menu({
        'Open project': opopen_project,

        'File': {
            'New': lambda: win.editor.create('editor'),
            'Open': open_editor

        },
        'Edit': {},
        'View': {},

        'Operator': {
            str(_()): {}
            for _ in EDITOR_CONFIG.operators()
        },
        'Help': {
            'Help': win.help,
            'About': {}
        }
    })

    win.mainloop()
