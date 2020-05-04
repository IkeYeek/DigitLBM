from tkinter import Tk
from gui.DigitLBMGUI import DigitLBMGUI


if __name__ == '__main__':
    metals = ["Alluminium", "Tungstene", "Fer"]
    app = Tk()
    my_gui = DigitLBMGUI(app)
    my_gui.load_metals_templates(metals)
    app.mainloop()
