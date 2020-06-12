import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class LaserMoovesBridge:
    def __init__(self, file_path, grid):
        self.f_path = os.path.normpath(file_path)
        self.grid = grid

    def get_moves(self):
        lines = []
        with open(self.f_path) as carre:
            for l in carre:
                lines.append(l.replace('\n', '').replace('[', '').replace(']', '').replace(';', ',').split(','))
        temp_np = np.asarray(lines)
        mms = MinMaxScaler(feature_range=(0 + 50, self.grid.size - 1 - 50))
        temp_np = mms.fit_transform(temp_np)
        temp_np = temp_np.astype('int')
        mooves = []

        for t in temp_np:
            mooves.append(
                [
                    (round(t[3]), round(t[4])), (round(t[0]), round(t[1]))]
            )
        return mooves
