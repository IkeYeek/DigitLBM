import os
from tkinter import simpledialog, PhotoImage, Tk


class StringDialogWrapper(simpledialog._QueryString):
    """
    Wrapper pour ask_string afin d'afficher le favicon
    """
    def body(self, master: Tk) -> None:
        super().body(master)
        self.iconphoto(True, PhotoImage(file=os.path.normpath(os.path.join('', 'conf', 'LBM_logo.gif'))))

    @staticmethod
    def ask_string(title, prompt, **kargs):
        d = StringDialogWrapper(title, prompt, **kargs)
        return d.result