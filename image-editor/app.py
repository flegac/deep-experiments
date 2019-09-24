from editor_core.editor.gui.editor_window import EditorWindow
from editor_core.editor.editor_config import EditorManager
from editor_core.image_operator_plugin import ImageFilterPlugin
from editor_core.visu_plugin import VisuPlugin


def main():
    # load all plugins
    EditorManager.plugin.extend(ImageFilterPlugin())
    EditorManager.plugin.extend(VisuPlugin())

    # create and run editor
    EditorWindow().mainloop()


if __name__ == '__main__':
    main()
