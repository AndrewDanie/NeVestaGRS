

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
    }
}