"""
    Физические функции для обсчетов
"""

import math

from core.entity.Gas import Gas
from core.entity.Pipeline import Pipeline
from core.entity.Vessel import Vessel


def run_calc(function, **kwargs):
    """Запуск любой функции с соответствующими ей аргументами"""
    if None in kwargs.values():
        raise Exception('Не хватает аргументов!')
    else:
        return function(**kwargs)


def calc_pipe_velocity(composition, temperature, pressure, internal_diameter, rate):
    """Рассчитывает скорость газа в трубопроводе"""

    pipe = Pipeline(internal_diameter, 0, 0)
    gas = Gas(composition, temperature, pressure, rate)
    velocity = gas.actual_rate / pipe.area / 3600
    capacity = round(25 * rate / velocity)

    return capacity, velocity


def calc_gas_density(composition, temperature, pressure, rate):
    """Рассчитывает плотность газа при рабочих, нормальных, стандартных условиях, актуальный расход газа"""

    gas = Gas(composition, temperature, pressure, rate)

    return (
        round(gas.actual_density, 2),
        round(gas.standard_density, 4),
        round(gas.actual_rate, 2),
        round(gas.molecular_mass, 2),
    )


def calc_pipe_diameter(composition, temperature, pressure, rate):
    """Рассчитывает требуемый диаметр трубопровода, чтобы скорость была в порядке"""
    velosity_limit = 25

    gas = Gas(composition, temperature, pressure, rate)
    actual_flow = gas.standard_density / gas.actual_density * rate
    internal_diameter = (actual_flow * 4 / 3600 / velosity_limit / math.pi) ** 0.5 * 1000

    return round(internal_diameter, 2)


"""Плохая функция"""
def calc_odorant_reserve(volume, rate):
    """Рассчитывает запас одоранта"""

    odorant_vessel = Vessel(0, 0, volume)
    return odorant_vessel


def calc_request_odorant_reserve(rate):
    """Рассчитывает необходимый запас одоранта"""

    request_volume = rate / 1000 * 0.016 * 60 * 24 / 830
    return round(request_volume, 2)
