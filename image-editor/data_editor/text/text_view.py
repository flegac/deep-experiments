import tkinter as tk

try:
    from pygments import lex
    from pygments.lexers import guess_lexer_for_filename, guess_lexer
    from pygments.styles import get_style_by_name

    SYNTAXIC_COLORING = True
    print('syntax coloring is OK')

except Exception as e:
    print(e)
    print('syntax coloring is not active')

    SYNTAXIC_COLORING = False


class TextView(tk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master, width=300)

        import tkinter as tk
        from tkinter.scrolledtext import ScrolledText

        self.editor = ScrolledText(self, width=100, height=80, wrap=tk.WORD)
        style = get_style_by_name('colorful')
        for k in style:
            color = k[1]['color']
            if color is not None:
                self.editor.tag_configure(str(k[0]), foreground='#' + color)

        self.editor.pack()

    def open_text(self, path: str):
        with open(path) as _:
            text = _.read()
        self.editor.insert('1.0', text)
        if SYNTAXIC_COLORING:
            self.syn(path)

    def syn(self, path: str):
        self.editor.mark_set("range_start", "1.0")
        data = self.editor.get("1.0", "end-1c")
        # lexer = guess_lexer_for_filename(path, data)
        lexer = guess_lexer(data)
        print('using lexer : {}'.format(lexer))
        for token, content in lex(data, lexer):
            self.editor.mark_set("range_end", "range_start + %dc" % len(content))
            self.editor.tag_add(str(token), "range_start", "range_end")
            self.editor.mark_set("range_start", "range_end")
