import math


class Pipeline:
    def __init__(self, pipe_diameter, wall, description=None, pipe_lenght=0):
        self.description = description
        self.diameter = pipe_diameter
        self.wall = wall
        self.lenght = pipe_lenght
        self.internal_diameter = pipe_diameter - 2 * wall
        self.area = math.pi / 4 * self.internal_diameter ** 2 / 1e6

    def pipe_pressure_drop(self):
        return