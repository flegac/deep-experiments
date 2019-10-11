from data_editor.utils.file_select import ask_open_file


def ask_open_model():
    return ask_open_file('Open model', [
        ('all files', '.*'),
        ('h5', '.h5'),
    ])
