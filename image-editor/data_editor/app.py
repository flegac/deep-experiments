from data_editor.editor.editor_window import EditorWindow
from data_editor.editor_config import EditorManager
from data_editor.plugin import ImageFilterPlugin, VisuPlugin


def main():
    # load all plugins
    EditorManager.plugin.extend(ImageFilterPlugin())
    EditorManager.plugin.extend(VisuPlugin())

    # create and run editor
    EditorWindow().mainloop()


if __name__ == '__main__':
    main()
