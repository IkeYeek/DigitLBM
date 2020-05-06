import os
from tkinter import simpledialog


class StringDialogWrapper(simpledialog._QueryString):
    def body(self, master):
        super().body(master)
        self.iconbitmap(os.path.join('.', 'conf', 'LBM_logo.ico'))

    def ask_string(title, prompt, **kargs):
        d = StringDialogWrapper(title, prompt, **kargs)
        return d.result