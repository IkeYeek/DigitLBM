import json
import os
from io import TextIOWrapper
from tkinter import Tk, Frame, Button, Label, IntVar, Entry, Listbox, LEFT, N, RIGHT, filedialog, Toplevel, Event, END, \
    PhotoImage
from tkinter.messagebox import showerror

from gui.MetalGUI import MetalGUI
from gui.SimuGUI import SimuGUI


class DigitLBMGUI:
    """
    Classe de la fenêtre principale
    """
    MAXW=650
    MAXH=500
    SIZE = "%dx%d" % (MAXW, MAXH)
    left_frame: Frame
    right_frame: Frame

    pattern_file: TextIOWrapper

    opened_gui: list
    metals_template: dict

    random_in_beam_size_var: IntVar
    beam_absorbency_var: IntVar
    melting_point_var: IntVar
    mean_beam_size_var: IntVar
    spot_size_var: IntVar
    laser_power_var: IntVar

    mean_beam_size_entry: Entry
    random_in_beam_size_entry: Entry
    beam_absorbency_entry: Entry
    melting_point_entry: Entry
    spot_size_entry: Entry
    laser_power_entry: Entry
    metal_template_entry: Listbox

    melting_point_label: Label
    beam_absorbency_label: Label
    metal_template_label: Label
    random_in_beam_size_label: Label
    mean_beam_size_label: Label
    spot_size_label: Label
    laser_power_label: Label
    params_label: Label
    pattern_file_label: Label

    pattern_file_dialog_button: Button
    metal_dialog_button: Button
    start_simulation_button: Button

    def __init__(self, master: Tk):
        """
        Initialise la fenêtre
        :param master: le root de l'app
        """
        self.master = master
        self.opened_gui = {}
        self.pattern_file = None
        # caractéristiques principales de la fenêtre
        self.master.title("DigitLBM")
        self.master.geometry(self.SIZE)
        # self.master.resizable(False, False)

        self.left_pane()

        self.right_pane()

        self.load_metals_templates()

    def left_pane(self) -> None:
        """
        initialise la partie gauche de l'interface
        """
        self.left_frame = Frame(self.master)
        self.pattern_file_label = Label(self.left_frame, text="Fichier Patron")
        self.pattern_file_dialog_button = Button(self.left_frame, text="Choisir un fichier",
                                                 command=self.handle_file_dialog_button)
        self.metal_dialog_button = Button(self.left_frame, text="Gérer les templates de métaux",
                                          command=self.handle_metal_dialog)

        self.left_frame.pack(side=LEFT, anchor=N, padx=(50, 0), pady=20)
        self.pattern_file_label.grid(row=1)
        self.pattern_file_dialog_button.grid(row=2, pady=20)
        self.metal_dialog_button.grid(row=3)

    def right_pane(self) -> None:
        """
        initialise la partie droite de l'interface
        """
        self.right_frame = Frame(self.master)
        # labels
        self.params_label = Label(self.right_frame, text="Paramètres de la simulation", font=(11))
        self.laser_power_label = Label(self.right_frame, text="Puissance du laser (Watt)")
        self.spot_size_label = Label(self.right_frame, text="Taille du spot (mm3)")
        self.mean_beam_size_label = Label(self.right_frame, text="Taille moyenne d'un grain (µ)")
        self.random_in_beam_size_label = Label(self.right_frame, text="Randomisation de la taille (%)")
        self.metal_template_label = Label(self.right_frame, text="Template du métal utilisé")
        self.beam_absorbency_label = Label(self.right_frame, text="Absorbtion de la poudre (x/100Watts)")
        self.melting_point_label = Label(self.right_frame, text="Energie requise pour atteindre un état fondu (?)")
        # inputs
        self.laser_power_var = IntVar()
        self.laser_power_entry = Entry(self.right_frame, textvariable=self.laser_power_var)

        self.spot_size_var = IntVar()
        self.spot_size_entry = Entry(self.right_frame, textvariable=self.spot_size_var)

        self.mean_beam_size_var = IntVar()
        self.mean_beam_size_entry = Entry(self.right_frame, textvariable=self.mean_beam_size_var)

        self.random_in_beam_size_var = IntVar()
        self.random_in_beam_size_entry = Entry(self.right_frame, textvariable=self.random_in_beam_size_var)

        self.metal_template_entry = Listbox(self.right_frame)
        self.metal_template_entry.bind('<<ListboxSelect>>', self.metal_template_entry_change)

        self.beam_absorbency_var = IntVar()
        self.beam_absorbency_entry = Entry(self.right_frame, textvariable=self.beam_absorbency_var)

        self.melting_point_var = IntVar()
        self.melting_point_entry = Entry(self.right_frame, textvariable=self.melting_point_var)
        # bouton Start Simulation
        self.start_simulation_button = Button(self.right_frame, text="Démarrer la simulation", command=self.handle_start_simulation)

        # placements
        self.right_frame.pack(side=RIGHT, anchor=N, padx=20)
        self.params_label.grid(row=1, column=1, pady=(10, 20))

        self.spot_size_label.grid(row=2, column=1, pady=(10, 0))
        self.spot_size_entry.grid(row=2, column=2)

        self.laser_power_label.grid(row=3, column=1, pady=(10, 0))
        self.laser_power_entry.grid(row=3, column=2)

        self.spot_size_label.grid(row=4, column=1, pady=(10, 0))
        self.spot_size_entry.grid(row=4, column=2)

        self.mean_beam_size_label.grid(row=5, column=1, pady=(10, 0))
        self.mean_beam_size_entry.grid(row=5, column=2)

        self.random_in_beam_size_label.grid(row=6, column=1, pady=(10, 0))
        self.random_in_beam_size_entry.grid(row=6, column=2)

        self.metal_template_label.grid(row=7, column=1, pady=(10, 0))
        self.metal_template_entry.grid(row=7, column=2)

        self.beam_absorbency_label.grid(row=8, column=1, pady=(10, 0))
        self.beam_absorbency_entry.grid(row=8, column=2)

        self.melting_point_label.grid(row=9, column=1, pady=(10, 0))
        self.melting_point_entry.grid(row=9, column=2)

        self.start_simulation_button.grid(row=10, column=2, pady=(50, 0))

    def load_metals_templates(self) -> None:
        self.metal_template_entry.delete(0, END)
        with open(os.path.join('.', 'conf', 'metals.json')) as metals_json:
            self.metals_template = json.loads(metals_json.read())
        for i, metal in enumerate(self.metals_template.keys()):
            self.metal_template_entry.insert(i, metal)

    def metal_template_entry_change(self, event: Event) -> None:
        """
        event handler d'un changement dans le template de métal séléctionné
        :param event:
        """
        w = event.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            new_metal = self.metals_template[value]
            self.beam_absorbency_var.set(new_metal['Absorbance'])
            self.melting_point_var.set(new_metal['Point de fusion'])

    def handle_file_dialog_button(self) -> None:
        """
        handler du filedialog permettant d'aller chercher le fichier patron
        """
        file = filedialog.askopenfile('r', parent=self.master, title="Choisir un fichier STL", initialdir=os.path.normpath(
            "/"), filetypes=[('Template file', '*.*')])
        self.pattern_file_label['text'] = file.name
        self.pattern_file = file
        # TODO handle file

    def handle_metal_dialog(self) -> None:
        """
        handler du bouton pour accéder à la fenêtre de gestion des templates de métaux
        """
        self.open_unique(MetalGUI, {'update_handler': self.load_metals_templates, 'close_handler': self.close, 'metals': dict(self.metals_template)})

    def handle_start_simulation(self) -> None:
        """
        handler du bouton pour lancer la simulation
        :return:
        """
        self.open_unique(SimuGUI,
                             {"laser_power": self.laser_power_var.get(), "spot_size": self.spot_size_var.get(), "mean_beam_size": self.mean_beam_size_var.get(),
                              "randomness": self.random_in_beam_size_var.get(), "beam_absorbancy": self.beam_absorbency_var.get(),
                              "melting_point": self.melting_point_var.get(), "pattern_file": self.pattern_file})


    def open_unique(self, gui_class: type, params={}) -> None:
        """
        permet de prévenir de l'ouverture multiples d'une même sous fenêtre (ex: ouvrir 2x la fenêtre des templates de
         métaux), en cas d'ouverture d'une fenêtre déjà ouverte, celle-ci est remontée
        :param gui_class:
        :param params:
        :return:
        """
        if gui_class not in self.opened_gui:
            """dialog = Toplevel(self.master)
            self.opened_gui[gui_class] = dialog
            dialog.protocol("WM_DELETE_WINDOW", lambda arg=gui_class: self.close(arg))
            gui_class(dialog, params)
            """
            try:
                dialog = Toplevel(self.master)
                dialog.iconphoto(True, PhotoImage(file=os.path.normpath(os.path.join('.', 'conf', 'LBM_logo.png'))))
                self.opened_gui[gui_class] = dialog
                dialog.protocol("WM_DELETE_WINDOW", lambda arg=gui_class: self.close(arg))
                gui_class(dialog, params)
                return self.opened_gui[gui_class]
            except Exception as e:
                self.close(gui_class)
                showerror("Erreur lors de l'ouverture de %s" % (gui_class.__name__,), str(e))
        else:
            opened_window = self.opened_gui[gui_class]
            opened_window.lift()
            return self.opened_gui[gui_class]

    def close(self, gui_class):
        """
        handler de la fermeture d'une fenêtre (la retire de la liste des fenêtres ouvertes)
        :param gui_class:
        :return:
        """
        if gui_class in self.opened_gui:
            dialog = self.opened_gui.pop(gui_class).destroy()





