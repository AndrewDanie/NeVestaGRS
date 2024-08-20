

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
                'Требуемый объём' : 'calc_odorant_reserve',
                'Запас' : 'calc_odorant_volume_request',
            }
        }
    },
    'Пропускная способность клапанов': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'combobox': 'Доступные ГРС',
            'input_labels': [
                'Давление до клапана, МПа',
                'Давление после клапана, МПа',
                'Температура, °С',
                'Kv, м3/ч',
                'Расход, м3/ч',
            ],
            'buttons' : {
                'Полный расчёт' : None,
                'Расчёт Kv' : 'calc_valve_kv',
                'Выполнить расчёт' : 'calc_valve_capacity',
            }
        }
    },
    'Расчет подогревателя газа': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'combobox': 'Доступные ГРС',
            'input_labels': [
                'Расход газа, ст. м3/ч',
                'Давление на входе ГРС, МПа',
                'Давление на выходе ГРС, МПа',
                'Температура газа на входе ГРС, °С',
                'Минимальная тем-ра на выходе, °С',
            ],
            'buttons' : {
                'Выполнить расчёт' : None,
            }
        }
    },
    'Расчёт предохранительных клапанов ГРС': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'combobox': 'Доступные ГРС',
            'input_labels': [
                'Давление до клапана, МПа',
                'Температура, °С',
                'Альфа',
                'Расход газа, ст. м3/ч'
            ],
            'buttons' : {
                'Выполнить расчёт' : None,
                'Расчет седла' : None,
            }
        }
    },
    'Расчёт ТВПС': {
        'default_gui': True,
        'left_frame' : {
            'output_block': 'TOP'
        },
        'right_frame': {
            'combobox': 'Доступные ГРС',
            'input_labels': [
                'Минимальное давление',
                'Максимальное давление',
                'Шаг по давлению',
                'Минимальная температура',
                'Максимальная температура',
                'Число точек по температуре',
                'Масштаб подписей данных'
            ],
            'buttons' : {
                'Таблица' : None,
                'Расчёт' : None,
                'Вставить секцию ТВПС' : None,
                'График ТВПС' : None,
                'Показать ТВПС' : None
            }
        }
    }
}