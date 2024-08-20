"""
    Физические функции для обсчетов
"""

import math
from typing import Dict, Any

from core.model.entity.Gas import Gas
from core.model.entity.Pipeline import Pipeline
import core.model.functions.constants as CONST


def calc_pipe_velocity(composition: dict, temperature: float,
                       pressure: float, rate: float, diameter: float,
                       wall: float, fluid_pack: str = 'PR'):
    """
    This function calculates the velocity of fluid in pipe.

    :param composition: per component molar composition of fluid;
    :param temperature: temperature of fluid, °C;
    :param pressure: fluid pressure over atmospheric, MPa;
    :param rate: fluid volume rate in standard cubic meters per hour;
    :param diameter: external diameter of pipe, mm;
    :param wall: pipeshell thickness, mm;
    :param fluid_pack: fluid thermodynamic pack:
    :return velocity (float): the velocity of fluid in pipe
    """
    gas = Gas(composition, fluid_pack)
    pipe = Pipeline(diameter, wall)
    velocity = gas.get_rate(temperature, pressure, rate, parameter='actual') / pipe.area / 3600
    return {
        'pipe_velocity': velocity
    }


def calc_gas_density(composition: dict, fluid_pack: str = 'PR'):
    """
    This function calculates the density of fluid for normal and standard conditions

    :param composition: per component molar composition of fluid;
    :param fluid_pack: fluid thermodynamic pack:
    :return normal_density, standard_density (float): densities for normal and standard conditions
    """
    gas = Gas(composition, fluid_pack)
    result = {
        'normal_density': gas.get_normal_density(),
        'standard_density': gas.get_standard_density()
    }
    return result


def calc_pipe_diameter(composition: dict, temperature: float, pressure: float, rate: float, fluid_pack: str = 'PR'):
    """
    This function calculates minimal requests diameter of pipe for current volume rate of fluid for velocity=25 mps

    :param composition: per component molar composition of fluid;
    :param temperature: temperature of fluid, °C;
    :param pressure: fluid pressure over atmospheric, MPa;
    :param rate: fluid volume rate in standard cubic meters per hour;
    :param fluid_pack: fluid thermodynamic pack:
    :return minimal_diameter (float): minimal requests pipeshell diameter
    """
    gas = Gas(composition, fluid_pack)
    minimal_diameter = 1000 * (gas.get_rate(temperature, pressure, rate, parameter='actual') / 3600 / 25 * 4 / math.pi) ** 0.5
    return  {
        'minimal_diameter': minimal_diameter
    }


def calc_odorant_reserve(rate: float, volume: float):
    """
    This function calculates numbers of days for maximal rate of gas to odorate gas

    :param rate: fluid volume rate in standard cubic meters per hour;
    :param volume: volume of odorant vessel
    :return odorant_reserve (float): numbers of days for maximal rate of gas to odorate gas
    """
    mass_per_thousand_cubic_meters = 0.016 # кг одоранта на 1000 м3
    odorant_density = 830 # кг/м3 - плотность одоранта
    reserve = volume * odorant_density * 0.85 * 1000 / rate / mass_per_thousand_cubic_meters / 24
    return {
        'odorant_reserve': reserve
    }


def calc_odorant_reserve_verdict(rate: float, volume:float):
    """
    This function return final verdict for odorant vessel
    :param rate: fluid volume rate in standard cubic meters per hour;
    :param volume: volume of odorant vessel
    :return (bool):
    """

    verdict = calc_odorant_reserve(rate, volume)['odorant_reserve'] >= 60
    return  {
        'verdict' :verdict
    }


def calc_odorant_volume_request(rate: float):
    """
    This function calculates requested odorant volume
    :param rate: fluid volume rate in standard cubic meters per hour;
    60 - number of days
    24 - hours in day
    0.016 - odorant mass rate per thousand cubic meters of gas СТО Газпром 2-3.5-051-2006, пункт 9.7.6
    830 - odorant density
    0.85 - 85% retard of odorant vessel
    :return:
    """
    odorant_request = 60 * 24 * 0.016 * rate / 1000 / 830 / 0.85
    return {
        'odorant_request': odorant_request
    }


def calc_valve_capacity(composition: dict, kv: int, inlet_pressure: float, outlet_pressure: float, temperature: float, fluid_pack ='PR'):
    """
    This function calculates capacity of valve by this fashion:
        https://dpva.ru/Guide/GuideEquipment/Valves/ControlValvesChoosingDPVA/?ysclid=lzwoz0zt3y667024699
    :param composition: per component molar composition of fluid;
    :param kv: volume of liquid of density 1000 with pressure drop 1 bar
    :param inlet_pressure: pressure before valve
    :param outlet_pressure: pressure after valve
    :param temperature: temperature of fluid, °C;
    :param fluid_pack: fluid thermodynamic pack:
    :return rate (float):
    """
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
    return {
        'valve_rate': standard_rate
    }


def calc_valve_kv(composition: dict, rate: float, inlet_pressure: float, outlet_pressure: float, temperature: float, fluid_pack='PR'):
    """
    This function calculates requests kv for gas rate
    :param composition: per component molar composition of fluid;
    :param rate: fluid volume rate in standard cubic meters per hour;
    :param inlet_pressure: pressure before valve
    :param outlet_pressure: pressure after valve
    :param fluid_pack: fluid thermodynamic pack:
    :return kv (float): volume of liquid of density 1000 with pressure drop 1 bar
    """
    gas = Gas(composition, fluid_pack)
    temperature += CONST.CELSIUS_TO_KELVIN_SHIFT
    inlet_pressure = (inlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    outlet_pressure = (outlet_pressure + CONST.PASCAL_TO_ATM / 1e6) * 1e6 / 98100
    gas_density = gas.get_normal_density()
    mass_rate = rate * gas.get_standard_density()
    delta_pressure = inlet_pressure - outlet_pressure

    if delta_pressure < inlet_pressure / 2:
        kv = mass_rate * temperature / 529 / (delta_pressure * outlet_pressure
                * gas_density * temperature) ** 0.5
    else:
        kv = mass_rate / 265 / inlet_pressure * (temperature / gas_density) ** 0.5
    return {
        'kv': kv
    }
