#!/usr/bin/python3.8
from autre.bench.benchmark import benchmark


def get_traveled_points(origin: tuple, destination: tuple, last) -> list:
    """
    renvoie la liste de tous les points (avec à peu près les bonnes coordonnées étant donné
        que la méthode utilisée ne donne pas que des entiers) traversés entre origin et destination
    :param origin: le point de départ
    :param destination: le point d'arrivé
    :param last: si dernier trajet du schéma
    """
    points = []
    if destination[1] - origin[1] != 0:
        m = (destination[0] - origin[0]) / (destination[1] - origin[1])
        p = origin[0] - (m * origin[1])
        step = 1 if origin[1] < destination[1] else -1
        for i in range(origin[1], destination[1], step):
            points.append((round((m * i + p)), i))
    else:  # cas d'une droite parralèle à l'axe des ordonnées
        step = 1 if origin[0] < destination[0] else -1
        for i in range(origin[0], destination[0], step):
            points.append((i, origin[1]))
    if last:
        points.append(destination)
    return points


def get_traveled_points2(origin_i: int, origin_j: int, dest_i: int, dest_j: int, last) -> list:
    points = []
    if dest_j - origin_j != 0:
        m = (dest_i - origin_i) / (dest_j - origin_j)
        p = origin_i - (m * origin_j)
        step = 1 if origin_j < dest_j else -1
        for i in range(origin_j, dest_j, step):
            points.append((round((m * i + p)), i))
        else:  # cas d'une droite parralèle à l'axe des ordonnées
            step = 1 if origin_i < dest_i else -1
        for i in range(origin_i, dest_i, step):
            points.append((i, origin_i))
        if last:
            points.append((dest_i, dest_j))
    return points


def get_traveled_points3(x0, y0, x1, y1) -> list:
    deltax = x1-x0
    dxsign = int(abs(deltax)/deltax)
    deltay = y1-y0
    dysign = int(abs(deltay)/deltay)
    deltaerr = abs(deltay/deltax)
    error = 0
    y = y0
    for x in range(x0, x1, dxsign):
        yield x, y
        error = error + deltaerr
        while error >= 0.5:
            y += dysign
            error -= 1
    yield x1, y1


if __name__ == '__main__':
    benchmark(lambda: get_traveled_points((1, 5), (2999, 1567), False), "tuples", 2000)
    benchmark(lambda: get_traveled_points2(1, 5, 2999, 1567, False), "no tuple", 2000)
    benchmark(lambda: get_traveled_points3(1, 5, 2999, 1567), "no tuple", 2000)
    for p in get_traveled_points3(1, 5, 2999, 1567):
        print(p)