from editor.window import Win

if __name__ == '__main__':
    win = Win()

    win.config_menu({
        'File': {
            'Open': win.editor.open
        },
        'Edit': {},
        'Help': {}
    })

    win.mainloop()
