from data_editor.utils.file_select import ask_open_file


def ask_open_table():
    return ask_open_file('Open image', [
        ('all files', '.*'),
        ('csv files', '.csv'),
    ])