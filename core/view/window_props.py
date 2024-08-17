

windows = {
    'Расчет скорости в трубопроводах': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'combobox': 'Доступные ГРС',
            'input_labels': [
                'Давление, МПа',
                'Температура, °С',
                'Расход',
                'Внешний диаметр, мм',
                'Толщина стенки, мм'
            ],
            'buttons' : {
                'Подбор диаметра': None,
                'Плотность газа': 'calc_gas_density',
                'Скорость газа': 'calc_pipe_velocity'
            }
        }
    },
    'Ёмкость одоранта': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'input_labels': [
                'Вместимость ёмкости',
                'Расход газа в ст. м3',
            ],
            'buttons' : {
                'Требуемый объём' : None,
                'Запас' : None,
            }
        }
    }
}