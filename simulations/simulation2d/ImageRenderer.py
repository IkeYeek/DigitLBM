import os
import time

from PIL import Image

from simulations.simulation2d.NoNumpyTest import Grid


class ImageRenderer:
    def __init__(self, grid: Grid, params, folder='./renders/'):
        self.grid = grid
        self.im = Image.new("RGB", (grid.size, grid.size), "#FFFFFF")
        self.pixels = self.im.load()
        self.folder = folder
        self.img_name = "%d_%d_%d_%d.png" % (params['grid_size'], params['spot_size'], params['speed'], params['power'])

    def POC(self):
        ######
        mx = 0
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if self.grid.particle_at(i, j).energy > mx:
                    mx = self.grid.particle_at(i, j).energy
        ######
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if self.grid.particle_at(i, j).energy > 0:
                    self.pixels[j, i] = (255, 0, round((self.grid.particle_at(i, j).energy * 255) / mx))

    def generate_path(self, prefix=''):
        return os.path.join(self.folder,  time.strftime('%d_%m_%Y_%H_%M_%S_') + self.img_name)

    def save(self):
        path = self.generate_path()
        self.im.save(path, 'PNG')

    def show(self):
        self.im.show()
