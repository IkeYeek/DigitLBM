import os
from tkinter import Tk, Frame, Button, Label, IntVar, Entry, Listbox, LEFT, N, RIGHT, filedialog, Toplevel

from gui.MetalGUI import MetalGUI


class DigitLBMGUI:
    SIZE = "650x500"
    left_frame: Frame
    right_frame: Frame

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
        # on initialise la fenêtre
        self.master = master

        # caractéristiques principales de la fenêtre
        self.master.title("DigitLBM")
        self.master.geometry(self.SIZE)
        self.master.resizable(False, False)

        self.left_pane()

        self.right_pane()

    def left_pane(self) -> None:
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

        self.beam_absorbency_var = IntVar()
        self.beam_absorbency_entry = Entry(self.right_frame, textvariable=self.beam_absorbency_var)

        self.melting_point_var = IntVar()
        self.melting_point_entry = Entry(self.right_frame, textvariable=self.melting_point_var)
        # bouton Start Simulation
        self.start_simulation_button = Button(self.right_frame, text="Démarrer la simulation")

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

    def load_metals_templates(self, metals_list: list) -> None:
        for i, metal in enumerate(metals_list):
            self.metal_template_entry.insert(i, metal)

    def handle_file_dialog_button(self):
        file = filedialog.askopenfile('r', parent=self.master, title="Choisir un fichier STL", initialdir=os.path.normpath("./"), filetypes=[('Template file', '*.*')])
        # TODO handle file

    def handle_metal_dialog(self):
        dialog = Toplevel(self.master)
        MetalGUI(dialog)


