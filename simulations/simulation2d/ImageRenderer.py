from PIL import Image

from simulations.simulation2d.NumpyGrid import Grid


class ImageRenderer:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.im = Image.new("RGB", (grid.size, grid.size), "#FFFFFF")

    def POC(self):
        pixels = self.im.load()
        ######
        mx = 0
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if self.grid.particle_at((i, j)).energy > mx:
                    mx = self.grid.particle_at((i, j)).energy
        ######
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                if self.grid.particle_at((i, j)).energy > 0:
                    pixels[j, i] = (255, 0, round((self.grid.particle_at((i, j)).energy * 255) / mx))
        self.im.show()
