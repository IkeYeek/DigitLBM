import json
import os
from tkinter import Label, IntVar, W, Frame, Entry, N, E, Button, Tk
from tkinter.messagebox import showinfo


class MetalGUI:
    """
    Classe de la fenêtre de selections des métaux
    """
    def __init__(self, master: Tk, params: dict):
        """
        Initialise la fenêtre
        :param master: le Toplevel passé par le caller
        :param params: Un dictionnaire comprenant tous les paramètres à passer
        """
        self.master = master
        self.close_handler = params['close_handler']
        self.update_handler = params['update_handler']
        self.metals = params["metals"]
        self.metals_metadata = {}
        self.prepare_metals()
        self.show_metals()
        Button(self.master, text="Sauvegarder", command=self.save).grid()

    def prepare_metals(self) -> None:
        """
        Charge le dictionnaire "self.metals" avec des IntVar et les set aux bonnes valeurs
        """
        for metal in self.metals:
            curr_metal = {'Absorbance': IntVar(), 'Point de fusion': IntVar()}
            curr_metal['Absorbance'].set(self.metals[metal]['Absorbance'])
            curr_metal['Point de fusion'].set(self.metals[metal]['Point de fusion'])
            self.metals[metal] = curr_metal

    def show_metals(self) -> None:
        """
        S'occupe de l'affichage des Label et Entry
        """
        for i, metal in enumerate(self.metals):
            Label(self.master, text=metal + ':').grid(row=(len(self.metals) * i), sticky=W)

            for j, car in enumerate(self.metals[metal]):
                Label(self.master, text=car + ':').grid(row=(len(self.metals) * i) + j+1, column=1, sticky=W)
                Entry(self.master,
                      textvariable=self.metals[metal][car]).grid(row=(len(self.metals) * i + j+1), column=2)

    def save(self) -> None:
        """
        Sauvegarde les changements dans les template et ferme la fenêtre
        """
        metals_new_values = {}

        # on convertit les IntVar en int et on met tout dans metals_new_values
        for metal in self.metals:
            metals_new_values[metal] = {}
            for car in self.metals[metal]:
                metals_new_values[metal][car] = self.metals[metal][car].get()

        # on convertit le tout en json et on réécrit le fichier de sauvegarde des paramètres
        with open(os.path.join('.', 'conf', 'metals.json'), 'w') as json_file:
            json_file.write(json.dumps(metals_new_values, indent=True))
        showinfo("Sauvegarde des template de métaux", "Sauvegarde des templates des métaux terminée")
        self.close_handler(__class__)
        self.update_handler()


