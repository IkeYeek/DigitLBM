import os
from tkinter import Tk, PhotoImage
from gui.DigitLBMGUI import DigitLBMGUI


def check_metal_conf_exists() -> None:
    """
    vérifie l'existance du fichier metals.json, sinon le crée
    """
    path = (os.path.join('.', 'conf', 'metals.json'))
    if not os.path.exists(path):
        with open(path, 'w+') as metal_file:
            metal_file.write('{}')



if __name__ == '__main__':
    # on s'assure que metals.json existe
    check_metal_conf_exists()
    # on initie l'app
    app = Tk()
    # on passe la fenêtre principale
    gui = DigitLBMGUI(app)
    # on définit l'icon
    app.iconphoto(True, PhotoImage(file=os.path.normpath(os.path.join('.', 'conf', 'LBM_logo.gif'))))
    # on lance l'app
    app.mainloop()

