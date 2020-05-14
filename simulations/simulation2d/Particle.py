#!/usr/bin/python3.8
class Particle:
    _ID = 0

    def __init__(self, size, i, j):
        self.id = Particle._ID
        self.size = size
        self.i = i
        self.j = j
        self.energy = 0
        Particle._ID += 1

    def __str__(self):
        return str(self.energy)

    def accept(self, power, speed):
        self.energy += power
        print("%d at %d;%d accepted %dMW of power with %d of speed, energy : %d" %
              (self.id, self.i, self.j, power, speed, self.energy))

    @staticmethod
    def avoid() -> None:
        Particle._ID -= 1