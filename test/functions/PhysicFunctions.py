from core.model.functions.PhysicFunctions import *



EPS = 10**(-4)
def test_velocity_calc():
    composition = {
        'Methane': 0.7,
        'Ethane': 0.2,
        'Propane': 0.1
    }
    temperature = 0
    pressure = 5
    rate = 50000
    diameter = 219
    wall = 10

    expected_answer = 1807585.092213786
    answer = velocity_calc(composition=composition, temperature=temperature, pressure=pressure, rate=rate, diameter=diameter, wall=wall)
    print(answer)
    assert abs(answer - expected_answer) < EPS