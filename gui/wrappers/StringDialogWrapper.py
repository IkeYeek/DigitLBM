import os
from tkinter import simpledialog, PhotoImage


class StringDialogWrapper(simpledialog._QueryString):
    def body(self, master):
        super().body(master)
        self.iconphoto(True, PhotoImage(file=os.path.normpath(os.path.join('.', 'conf', 'LBM_logo.png'))))

    def ask_string(title, prompt, **kargs):
        d = StringDialogWrapper(title, prompt, **kargs)
        return d.result