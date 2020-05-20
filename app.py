import os
from tkinter import Tk
from gui.DigitLBMGUI import DigitLBMGUI


def check_metal_conf_exists():
    path = (os.path.join('.', 'conf', 'metals.json'))
    if not os.path.exists(path):
        with open(path, 'w+') as metal_file:
            metal_file.write('{}')


if __name__ == '__main__':
    check_metal_conf_exists()
    app = Tk()
    gui = DigitLBMGUI(app)
    #app.iconbitmap(os.path.join('.', 'conf', 'LBM_logo.ico'))
    app.mainloop()
