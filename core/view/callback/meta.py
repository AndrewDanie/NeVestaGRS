from core.util.ConfigCache import ConfigCache
from core.util.util_functions import *
from core.view.callback import db, window


def get_yaml_variable(name):
    name = name[1:].split('.')
    var_type = name[0]

    variable = None
    if var_type == 'custom':
        raise Exception('Префикс $custom не определен!')
    else:
        raise Exception(f'Префикс {name} не существует!')
    # return variable


def get_yaml_callback(name):
    """
    :param name: имя из binding_config.yml
    :return: соответствующий колбэк
    """
    name = name[1:].split('.')
    callback_type = name[0]
    callback_name = name[1]
    callback = None
    if callback_type == 'window':
        return getattr(window, callback_name)
    elif callback_type == 'db':
        return getattr(db, callback_name)
    elif callback_type == 'cache':
        return getattr(db, callback_name)
    elif callback_type == 'logic':
        return lambda e, c_name = callback_name: run_logic_func(c_name)
    elif callback_type == 'meta':
        return globals()[callback_name]
    elif callback_type == 'custom':
        raise Exception(f'Кастомные колбэки не реализованы!')
    else:
        raise Exception(f'Тип колбэка {callback_type} не найден!')


def get_move_to_screen_callbacks():
    """
    :return: Возвращает СПИСОК колбэков для запуска разных экранов из меню по ключам из binding_config.yml
    """
    context = ConfigCache.get_cache().get('context')
    callback_list = []
    for name in parse_yaml('view\\binding_config.yml').keys():
        if name != 'Главное меню':
            callback_list.append([name, lambda e, sc_name=name: context.make_context(sc_name)])
    return callback_list


def run_logic_func(function_name):
    window = ConfigCache.get_cache().get('window')
    func_parameters = get_non_default_params_of_func(function_name)
    kwargs = dict()
    for param_name in func_parameters:
        if param_name == 'composition':
            grs_name = window.get_data(f'combobox.{param_name}')
            kwargs[param_name] = db.get_composition_set_by_grs_name(grs_name)
        elif param_name == 'outlet':
            grs_name = window.get_data(f'combobox.outlet')
            kwargs[param_name] = db.get_outlet_set_by_grs_name(grs_name)
        else:
            str_value = window.get_data(f'entry.{param_name}')
            str_value = validate_input_string(str_value)
            value = get_validated_float(str_value)
            kwargs[param_name] = value
    result = run_func(function_name, **kwargs)
    window.set_data('output.__txt_field__', result)