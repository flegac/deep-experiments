import tkinter as tk

from pygments import lex
from pygments.lexers import guess_lexer_for_filename
from pygments.styles import get_style_by_name


class TextEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str, path: str):
        super().__init__(master, text="data", width=300)

        import tkinter as tk
        from tkinter.scrolledtext import ScrolledText

        self.editor = ScrolledText(self, width=100, height=80, wrap=tk.WORD)
        style = get_style_by_name('colorful')
        for k in style:
            color = k[1]['color']
            if color is not None:
                self.editor.tag_configure(str(k[0]), foreground='#' + color)

        self.editor.pack()
        if path is not None:
            self.open_text(path)

    def open_text(self, path: str):
        with open(path) as _:
            text = _.read()
        self.editor.insert('1.0', text)
        self.syn(path)

    def syn(self, path: str):
        self.editor.mark_set("range_start", "1.0")
        data = self.editor.get("1.0", "end-1c")
        lexer = guess_lexer_for_filename(path, data)
        print('using lexer : {}'.format(lexer))
        for token, content in lex(data, lexer):
            self.editor.mark_set("range_end", "range_start + %dc" % len(content))
            self.editor.tag_add(str(token), "range_start", "range_end")
            self.editor.mark_set("range_start", "range_end")
