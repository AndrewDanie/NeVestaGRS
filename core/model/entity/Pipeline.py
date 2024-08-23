import math


class Pipeline:
    def __init__(self, pipe_diameter, wall, description=None, pipe_length=0):
        self.description = description
        self.diameter = pipe_diameter
        self.wall = wall
        self.length = pipe_length
        self.internal_diameter = pipe_diameter - 2 * wall
        self.area = math.pi / 4 * self.internal_diameter ** 2 / 1e6

    def pipe_pressure_drop(self):
        return

    def calc_wall(self, pressure: float, pipe_qualaity: str='K48'):
        """
        This method returns pipeshell thickness
        :param pressure: pressure in MPa,
        :return: wall (float) - pipeshell thickness
        """
        tension_limits = {
            'K42': 415,
            'K48': 470,
            'K52': 510,
            'K56': 550,
            'K60': 590,
        }
        m = 1.55 # СП 36.13330.2012
        k1 = 1.55
        kn = 1.1
        n = 1.5
        R1 = tension_limits[pipe_qualaity] * m / k1 / kn
        wall = n * pressure * self.diameter / 2 / (R1 + n * pressure)
        return wall