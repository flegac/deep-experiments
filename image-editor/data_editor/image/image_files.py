from data_editor.utils.file_select import ask_open_file


def ask_open_image():
    return ask_open_file('Open image', [
        ('all files', '.*'),
        ('tiff files', '.tif'),
        ('png files', '.png'),
        ('Jpeg files', '.jpg'),
    ])