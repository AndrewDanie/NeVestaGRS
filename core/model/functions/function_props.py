

commands = {
    "calc_pipe_velocity" : {
        'function' : 'calc_pipe_velocity',
        'args' : {
            'manual_input' : {
                'pressure': 'Давление, МПа',
                'temperature': 'Температура, °С',
                'rate': 'Расход',
                'diameter': 'Внешний диаметр, мм',
                'wall': 'Толщина стенки, мм',
            },
            'composition' : True
        },
        'return' : {
            'pipe_velocity' : 'Скорость газа'
        }
    },
    'calc_gas_density' : {
        'function' : 'calc_gas_density',
        'args' : {
            'composition' : True
        },
        'return' : {
            'normal_density' : 'Плотность при н.у.',
            'standard_density' : 'Плотность при ст.у.'
        }
    },
    'calc_odorant_reserve' : {
        'function' : 'calc_odorant_reserve',
        'args' : {
            'manual_input' : {
                'rate': 'Расход газа в ст. м3',
                'volume': 'Вместимость ёмкости',
            },
        },
        'return' : {
            'odorant_reserve' : 'Число дней, на которые хватит запаса',
        }
    },
    'calc_odorant_volume_request' : {
        'function' : 'calc_odorant_volume_request',
        'args' : {
            'manual_input' : {
                'rate': 'Расход газа в ст. м3',
            },
        },
        'return' : {
            'odorant_request' : 'Необходимый объем',
        }
    },
    'calc_valve_capacity' : {
        'function' : 'calc_valve_capacity',
        'args' : {
            'manual_input' : {
                'kv': 'Kv, м3/ч',
                'inlet_pressure': 'Давление до клапана, МПа',
                'outlet_pressure': 'Давление после клапана, МПа',
                'temperature': 'Температура, °С',
            },
            'composition' : True,
        },
        'return' : {
            'valve_rate' : 'Расход, ст м3/ч',
        }
    },
    'calc_valve_kv' : {
        'function' : 'calc_valve_kv',
        'args' : {
            'manual_input' : {
                'rate': 'Расход, м3/ч',
                'inlet_pressure': 'Давление до клапана, МПа',
                'outlet_pressure': 'Давление после клапана, МПа',
                'temperature': 'Температура, °С',
            },
            'composition' : True,
        },
        'return' : {
            'kv' : 'Kv, м3/ч',
        }
    },
    'calc_capacity_ppk' : {
        'function' : 'calc_capacity_ppk',
        'args' : {
            'manual_input' : {
                'inlet_pressure': 'Давление, МПа',
                'temperature': 'Температура, °С',
                'alpha': 'Коэффициент расхода',
                'valve_area': 'Площадь седла, мм',
            },
            'composition' : True,
        },
        'return' : {
            'capacity_mass': 'Расход, кг/ч',
            'capacity_normal': 'Расход, нм3/ч',
            'capacity_standard': 'Расход, ст.м3/ч'
        }
    },
    'calc_valve_area_ppk': {
        'function': 'calc_valve_area_ppk',
        'args': {
            'manual_input': {
                'inlet_pressure': 'Давление, МПа',
                'temperature': 'Температура, °С',
                'alpha': 'Коэффициент расхода',
                'rate': 'Расход, ст. м3/ч',
            },
            'composition' : True,
        },
        'return' : {
            'valve_area': 'Площадь седла, мм2'
        }
    }
}