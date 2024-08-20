

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
            'kv' : 'Расход, м3/ч',
        }
    }
}