import os

from editor_gui.config import EDITOR_CONFIG
from editor_gui.event_bus import PROJECT_OPEN_BUS, IMAGE_OPEN_BUS
from editor_gui.utils.ui_utils import dir_selection, file_selection
from editor_gui.window import Win
from editor_plugins.image_filter.plugin import ImageFilterPlugin
from editor_plugins.morphology.plugin import MorphologyPlugin
from editor_plugins.tiling.plugin import TilingPlugin


def open_editor():
    paths = file_selection()
    name, _ = os.path.splitext(os.path.basename(paths[0]))
    IMAGE_OPEN_BUS.on_next((name, paths[0]))


if __name__ == '__main__':

    # load all plugins
    EDITOR_CONFIG.extend(ImageFilterPlugin())
    EDITOR_CONFIG.extend(MorphologyPlugin())
    EDITOR_CONFIG.extend(TilingPlugin())

    # create window
    win = Win()

    if EDITOR_CONFIG.config_path_is_valid('project_browser_path'):
        PROJECT_OPEN_BUS.on_next(EDITOR_CONFIG.config.get('project_browser_path'))

    win.config_menu({
        'File': {
            'New': lambda: IMAGE_OPEN_BUS.on_next(('---', None)),
            'Open project': lambda: PROJECT_OPEN_BUS.on_next(dir_selection()),
            'Open image': open_editor,

            'Exit': win.destroy

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
