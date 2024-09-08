

class Vessel:
    def __init__(self, vessel_diameter, vessel_lenght, volume):
        self.diameter = vessel_diameter
        self.lenght = vessel_lenght
        self.volume = volume

    def odorant_mass(self, volume):
        return round(0.85 * 830 * volume, 2)

    def odorant_rate(self, rate):
        return round(rate * 0.016 / 1000, 2)  # расход одоранта в час

    def odorant_time(self, volume, rate):
        return round(self.odorant_mass(volume) / self.odorant_rate(rate) / 24, 1)
