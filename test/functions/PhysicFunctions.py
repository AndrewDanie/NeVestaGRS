from core.model.functions.PhysicFunctions import *

"""
входные данные для тестов
"""
composition = {'Methane': 0.9197, 'Ethane': 0.0446, 'Propane': 0.0192, 'Isobutane': 0.0052, 'Butane': 0.0043,
               'Isopentane': 0.0013, 'Pentane': 0.0007, 'Hexane': 0.0007, 'Oxygen': 0.0020, 'Nitrogen': 0.002,
               'CarbonDioxide': 0.0002}
temperature = 0
pressure = 5
rate = 50000
diameter = 219
wall = 10
volume = 10
kv = 100
inlet_pressure = 5.4
outlet_pressures = 0.6, 5.3
EPS = 10**(-4)
gas = Gas(composition, fluid_pack='PR')


def test_calc_pipe_velocity():

    expected_answer = 6.827795950079494
    answer = calc_pipe_velocity(composition=composition, temperature=temperature,
                                pressure=pressure, rate=rate, diameter=diameter, wall=wall)
    assert abs(answer['pipe_velocity'] - expected_answer) < EPS


def test_calc_gas_density():
    expected_answer_normal_density = gas.get_normal_density()
    expected_answer_standard_density =gas.get_standard_density()

    answer = calc_gas_density(composition=composition)
    assert abs(answer['normal_density'] - expected_answer_normal_density) < EPS
    assert abs(answer['standard_density'] - expected_answer_standard_density) < EPS
    return


def test_calc_pipe_diameter():
    answer = calc_pipe_diameter(composition, temperature, pressure, rate)
    expected_answer = 103.99760524533208
    assert abs(answer['minimal_diameter'] - expected_answer) < EPS


def test_odorant_reserve_calc():
    expected_answer = 367.4479166666667
    answer = odorant_reserve_calc(rate, volume)
    assert abs(answer['odorant_reserve'] - expected_answer) < EPS


def test_odorant_reserve_verdict():
    expected_answer = True
    answer = odorant_reserve_verdict(rate, volume)
    assert answer == expected_answer


def test_odorant_volume_request() -> dict[str, float]:
    expected_answer = 1.63288447907
    answer = odorant_volume_request(rate)
    assert abs(answer['odorant_request'] - expected_answer) < EPS


def test_valve_capacity_calc():
    expected_answers = [108084.50504532954, 28824.122093677506]
    answers = [valve_capacity_calc(composition, kv, inlet_pressure, outlet_pressure, temperature, fluid_pack='PR')['valve_rate']
              for outlet_pressure in outlet_pressures]
    for i in range(len(answers)):
        assert abs(answers[i] - expected_answers[i]) < EPS


def test_valve_kv_calc():
    expected_answers = [46.26009989038716, 173.46582087565946]
    answers = [valve_kv_calc(composition, rate, inlet_pressure, outlet_pressure, temperature)['kv']
          for outlet_pressure in outlet_pressures]
    for i in range(len(answers)):
        assert abs(answers[i] - expected_answers[i]) < EPS


#test_calc_pipe_velocity()


test_functions = {'функции расчёта скоростей в трубопроводе': test_calc_pipe_velocity,
                  'функции расчёта плотности смеси при ст.у. и н.у.': test_calc_gas_density,
                  'функции расчёта минимального диаметра трубопровода': test_calc_pipe_diameter,
                  'функции расчёта запаса одоранта': test_odorant_reserve_calc,
                  'функции определения достаточности ёмкости одоранта': test_odorant_reserve_verdict,
                  'функции расчёта минимального объёма ёмкости одоранта': test_odorant_volume_request,
                  'функции расчёта пропускной способности регулятора': test_valve_capacity_calc,
                  'функции расчёта требуемой пропускной способности регулятора': test_valve_kv_calc}


for function_name, function in test_functions.items():
    try:
        function()
    except AssertionError:
        print(f'Ошибка в тесте {function_name}!!!')
        break