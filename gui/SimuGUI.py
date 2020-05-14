from tkinter import Label




class SimuGUI:
    """
    Classe de la fenêtre de simulation (potentiellement temporaire)
    """
    def __init__(self, master, params):
        self.master = master
        if params["pattern_file"] is None:
            pass
            # raise Exception("Le fichier patron n'est pas défini !")
        self.params = Label(self.master,
                            text="Puissance Laser: %d; Taille spot: %d; Taille moyenne grain: %d; randomisation: %d; Absorbance: %d; Energie req! %d"
                                 % (params["laser_power"], params["spot_size"], params["mean_beam_size"], params["randomness"],
                                    params["beam_absorbancy"], params["melting_point"]))
        # self.file_content = Label(self.master, text=params["pattern_file"].name)

        self.params.pack()
        # self.file_content.pack()
        self.random_pg()

    def random_pg(self):
        img = Image.new('L', (128, 128), color="#FFFFFF")
        img.show()
