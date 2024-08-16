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

def velocity_calc(composition: dict, temperature: float, pressure: float, diameter: int, wall: int,  fluid_pack: str = 'PR') -> float:
    """Функция возвращает реальную скорость газа в трубопроводе
    функция принимает в себя состав для формирования:
    состав смеси,
    температуру,
    давление,
    диаметр трубы,
    толщину стенки трубы,
    термодинамический пакет (по умолчанию используется уравнение состояния Пенга-Робинсона)"""
    gas = Gas(composition, fluid_pack)
    pipe = Pipeline(diameter, wall)
    return gas.actual_rate(temperature, pressure) / pipe.area

def odorant_reserve_calc(rate: float, volume: float) -> float:
    """Расчёт количество дней, на которое хватит одоранта в емкости с учётом ограничения наполнения 80%
    плотность одоранта 830 кг/м3"""
    mass_per_thousand_cubic_meters = 0.016 # кг одоранта на 1000 м3
    odorant_density = 830 # кг/м3 - плотность одоранта
    return volume * odorant_density * 0.8 * 1000 / rate / mass_per_thousand_cubic_meters / 24

def odorant_reserve_verdict(rate: float, volume:float) -> bool:
    """Функция принимает расход и объём ёмкости одоранта и выдает false или true в зависимости от результата"""
    if odorant_reserve_calc(rate, volume) >= 60:
        return True
    else:
        return False

def odorant_volume_request(rate: float) -> float:
    """Функция принимает в себя расход газа в стандартных метрах кубических
    и возвращает требуемый объём ёмкости одоранта, с учётом, что по нормативу
    запаса одоранта должно хватать на 60 дней, заполнение ёмкости должно быть
    максимум 80%, плотность одоранта 830 кг/м3"""
    return 60 * 24 * 0.016 * rate / 1000 / 830 / 0.8

def valve_capacity_calc(composition, Kv, inlet_pressure, outlet_pressure, temperature):
    """Функция принимает в себя:
    composition - состав газа, чтобы определить плотность газа
    https://dpva.ru/Guide/GuideEquipment/Valves/ControlValvesChoosingDPVA/?ysclid=lzwoz0zt3y667024699
     Kv клапана (это может быть как с рук, так и с БД)
     inlet_pressure - давление до клапана
     outlet_pressure - давление после клапана
     temperature - температура газа на входе в регулятор"""
    gas = Gas(composition)
    p1 = (inlet_pressure + 0.101325) * 1e6 / 98100
    p2 = (outlet_pressure + 0.101325) * 1e6 / 98100
    delta_pressure = p1 - p2
    if delta_pressure < p1 / 2:
        pass #dont finished yet
    gas.normal_density()


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
