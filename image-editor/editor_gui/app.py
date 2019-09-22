from editor_gui.editor_window import EditorWindow
from editor_core.config.editor import EditorManager
from editor_plugins.image_filter.plugin import ImageFilterPlugin
from editor_plugins.morphology.plugin import MorphologyPlugin
from editor_plugins.tiling.plugin import TilingPlugin


def main():
    # load all plugins
    EditorManager.plugin.extend(ImageFilterPlugin())
    EditorManager.plugin.extend(MorphologyPlugin())
    EditorManager.plugin.extend(TilingPlugin())

    # create and run editor
    EditorWindow().mainloop()


if __name__ == '__main__':
    main()
