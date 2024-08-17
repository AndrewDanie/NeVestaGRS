"""
    Физические функции для обсчетов
"""

import math

from core.model.entity.Gas import Gas
from core.model.entity.Pipeline import Pipeline
import core.model.functions.constants as CONST


def velocity_calc(composition: dict, temperature: float, pressure: float, rate: float, diameter: int, wall: int,  fluid_pack: str = 'PR') -> float:
    """Функция возвращает реальную скорость газа в трубопроводе
    функция принимает в себя состав для формирования:
    состав смеси,
    температуру,
    расход, ст. м3/ч,
    давление,
    диаметр трубы,
    толщину стенки трубы,
    термодинамический пакет (по умолчанию используется уравнение состояния Пенга-Робинсона)"""
    gas = Gas(composition, fluid_pack)
    pipe = Pipeline(diameter, wall)
    velocity = gas.get_rate(temperature, pressure, rate, parameter='actual') / pipe.area / 3600
    return velocity


def calc_pipe_diameter(composition: dict, temperature: float, pressure: float, rate: float, fluid_pack: str = 'PR') -> float:
    gas = Gas(composition, fluid_pack)
    return (gas.get_rate(temperature, pressure, rate, parameter='actual') / 25 * 4 / math.pi) ** 0.5 # 25 метров в секунду - слишком тупо цифрами писать


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


def valve_capacity_calc(composition: dict, kv: int, inlet_pressure: float, outlet_pressure: float, temperature: float, fluid_pack = 'PR') -> float:
    """Пропускная способность клапанов
    Функция принимает в себя:
    composition - состав газа, чтобы определить плотность газа
    https://dpva.ru/Guide/GuideEquipment/Valves/ControlValvesChoosingDPVA/?ysclid=lzwoz0zt3y667024699
        Kv клапана (это может быть как с рук, так и с БД)
        inlet_pressure - давление до клапана
        outlet_pressure - давление после клапана
        temperature - температура газа на входе в регулятор"""
    gas = Gas(composition, fluid_pack)
    temperature += CONST.CELSIUS_TO_KELVIN_SHIFT
    inlet_pressure = (inlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    outlet_pressure = (outlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    gas_density = gas.get_normal_density()
    delta_pressure = inlet_pressure - outlet_pressure
    if delta_pressure < inlet_pressure / 2:
        mass_rate = (529 / temperature) * kv * (delta_pressure * outlet_pressure * gas_density * temperature) ** 0.5
    else:
        mass_rate = 265 * inlet_pressure * kv * (gas_density / temperature) ** 0.5
    standard_rate = mass_rate / gas.get_standard_density()
    return standard_rate


def valve_kv_calc(composition: dict, rate: float, inlet_pressure: float, outlet_pressure: float, temperature: float, fluid_pack='PR') -> float:
    """Функция принимает в себя состав, расход в стандартных метрах кубических в час,
    давления на входе и выходе из регулятора в МПа (изб.),
    температуру газа на входе в регулятор.
    Возвращает требуемый для такой пропускной способности Kv без учёта запаса
    рекомендуемый запас по регуляторам - 20-50%"""
    gas = Gas(composition, fluid_pack)
    temperature += CONST.CELSIUS_TO_KELVIN_SHIFT
    inlet_pressure = (inlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    outlet_pressure = (outlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    gas_density = gas.get_normal_density()
    delta_pressure = inlet_pressure - outlet_pressure
    if delta_pressure < inlet_pressure / 2:
        kv = rate * gas.get_standard_density() * temperature / 529 / (delta_pressure * outlet_pressure * gas_density * temperature) ** 0.5
    else:
        kv = rate * gas.get_standard_density() / 265 / inlet_pressure / (gas_density / temperature) ** 0.5
    return kv
