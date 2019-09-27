import tkinter as tk

from data_editor.utils.my_list_box import MyListBox

master = tk.Tk()
list_model = lambda: list(range(100))
MyListBox(master, list_model).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

master.mainloop()
