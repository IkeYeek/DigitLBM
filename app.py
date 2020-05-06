import os
from tkinter import Tk, PhotoImage
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
    app.iconphoto(True, PhotoImage(file=os.path.normpath(os.path.join('.', 'conf', 'LBM_logo.png'))))
    app.mainloop()
