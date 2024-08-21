
properties = {
    'Расчет скорости в трубопроводах': {
        'gui_template': 'default_calculator',
        'widgets': {
            'combobox': {
                'composition',
            },
            'entry': [
                'pressure',
                'temperature',
                'rate',
                'diameter',
                'wall',
            ],
            'button' : [
                '__Подбор диаметра',
                'calc_gas_density',
                'calc_pipe_velocity',
            ]
        }

    },
    'Ёмкость одоранта': {
        'gui_template': 'default_calculator',
        'widgets': {
            'entry': [
                'rate',
                'volume',
            ],
            'button' : [
                'calc_odorant_reserve',
                'calc_odorant_volume_request',
            ],
        }
    },
    'Пропускная способность клапанов': {
        'gui_template': 'default_calculator',
        'widgets': {
            'combobox': [
                'composition',
            ],
            'entry': [
                'kv',
                'inlet_pressure',
                'outlet_pressure',
                'temperature',
                'rate',
            ],
            'button' : [
                '__Полный расчёт',
                'calc_valve_kv',
                'calc_valve_capacity',
            ]
        }
    },
    'Расчет подогревателя газа': {
        'gui_template': 'default_calculator',
        'widgets': {
            'combobox': [
                'composition',
            ],
            'entry': [
                'rate',
                '__Давление на входе ГРС, МПа',
                '__Давление на выходе ГРС, МПа',
                '__Температура газа на входе ГРС, °С',
                '__Минимальная тем-ра на выходе, °С',
            ],
            'button' : [
                '__Выполнить расчёт',
            ]
        }
    },
    'Расчёт предохранительных клапанов': {
        'gui_template': 'default_calculator',
        'widgets': {
            'combobox': [
                'composition',
            ],
            'entry': [
                'inlet_pressure',
                'temperature',
                'alpha',
                'valve_area',
                'rate',
            ],
            'button' : [
                'calc_capacity_ppk',
                'calc_valve_area_ppk',
            ]
        }
    },
    'Расчёт ТВПС': {
        'gui_template': 'default_calculator',
        'widgets': {
            'combobox': [
                'composition',
            ],
            'entry': [
                '__Минимальное давление',
                '__Максимальное давление',
                '__Шаг по давлению',
                '__Минимальная температура',
                '__Максимальная температура',
                '__Число точек по температуре',
                '__Масштаб подписей данных'
            ],
            'button': [
                '__Таблица',
                '__Расчёт',
                '__Вставить секцию ТВПС',
                '__График ТВПС',
                '__Показать ТВПС',
            ]
        }
    },
    'Толщина стенок трубопроводов': None,
    'Схема': None,
    'Статистика': None,
    'База данных ГРС': None,
}

