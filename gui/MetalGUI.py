import json
import os
from tkinter import Label, IntVar, W, Entry, Button, Tk
from tkinter.messagebox import showinfo, showerror

from gui.wrappers.StringDialogWrapper import StringDialogWrapper


class MetalGUI(object):
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
        self.update_ui()

    def prepare_metals(self) -> None:
        """
        Charge le dictionnaire "self.metals" avec des IntVar et les set aux bonnes valeurs
        """
        for metal in self.metals:
            curr_metal = {'Absorbance': IntVar(), 'Point de fusion': IntVar()}
            curr_metal['Absorbance'].set(self.metals[metal]['Absorbance'])
            curr_metal['Point de fusion'].set(self.metals[metal]['Point de fusion'])
            self.metals[metal] = curr_metal

    def update_ui(self) -> None:
        """
        S'occupe de l'affichage des Label et Entry
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        for i, metal in enumerate(self.metals):
            Label(self.master, text=metal + ':').grid(row=(len(self.metals) * i), sticky=W)
            Button(self.master, text="-", command=lambda arg=metal: self.remove_metal(arg)).grid()

            for j, car in enumerate(self.metals[metal]):
                Label(self.master, text=car + ':').grid(row=(len(self.metals) * i) + j+1, column=1, sticky=W)
                Entry(self.master,
                      textvariable=self.metals[metal][car]).grid(row=(len(self.metals) * i + j+1), column=2)
        Button(self.master, text="+", command=self.add_metal).grid()
        Button(self.master, text="Sauvegarder", command=self.save).grid()
        self.master.lift()

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

    def add_metal(self) -> None:
        """
        Se charge d'ouvrir la fenêtre de dialogue pour renseigner le nom d'un nouveau métal
        L'enregistre ensuite dans la mémoire (tant que Sauvegarder n'a pas été utilisé)
        Recharge l'interface du la fenêtre des métaux pour prendre en compte les changements
        """
        metal = StringDialogWrapper.ask_string("Ajout d'un métal", "Nommez le métal (le nom doit être unique)")
        if len(metal) > 0 and metal not in self.metals:
            self.metals[metal] = {'Absorbance': IntVar(), 'Point de fusion': IntVar()}
        elif len(metal) > 0:
            showerror("Impossible de rajouter le template", "%s déjà utilisé comme nom de métal" % (metal,))
        else:
            showerror("Impossible de rajouter le template", "Le nom est vide!")
        self.update_ui()

    def remove_metal(self, metal: str) -> None:
        """
        Se charge de supprimer un métal
        :param metal: le nom du métal a supprimer
        """
        self.metals.pop(metal)
        self.update_ui()


