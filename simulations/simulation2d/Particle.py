#!/usr/bin/python3.8
class Particle(object):
    """
    Représente une particule
    fait les calculs pour la simulation
    """
    _ID = 0
    """
    _ID sert à auto-incrémenter l'ID des particules créées
    """

    def __init__(self, size: int, i: int, j: int):
        """
        initialise la particule avec son id, sa taille et les coordonnées de son point nord ouest
        incrémente _ID pour les particules suivantes
        :param size: la taille de la particule (n => n*n)
        :param i: coordonnée i (ligne) du point nord ouest
        :param j: coordonnée j (colonne) du point nord ouest
        """
        self.id = Particle._ID
        self.size = size
        self.i = i
        self.j = j
        self.energy = 0
        Particle._ID += 1
        if self.i % 100 == 0 and self.j == 1:
            print("particle at %d:%d size: %d ref: %d" % (self.i, self.j, self.size, self.id))

    def __str__(self) -> str:
        """
        méthode tostring, aucune autre réelle utilitée que le debug
        :return: peut varier, soit l'énergie, soit le numéro, ou autre selon les besoins
        """
        return str(self.energy)

    def accept(self, power: int, speed: int) -> None:
        """
        méthode appelée quand la simulation calcule que le laser traverse cette particule
        point d'entré pour les calculs d'énergie donc
        :param power: la puissance du laser dans la simulation
        :param speed: la vitesse du laser dans la simulation
        """
        self.energy += power
        print("%d at %d;%d accepted %dMW of power with %d of speed, energy : %d" %
              (self.id, self.i, self.j, power, speed, self.energy))

    @staticmethod
    def avoid() -> None:
        """
        annule la création d'une particule en réduisant _ID (plus utilisé mais peut toujours servir)
        /!\ ne fait que rétrograder l'id /!\
        :return:
        """
        Particle._ID -= 1