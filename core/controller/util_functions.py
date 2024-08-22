"""
    Различные вспомогательные фукнции
"""
import inspect
import yaml


from core.model.functions import physic_functions


def get_validated_int(string_input):
    """Валидирует строку и возвращает целочисленное значение"""
    try:
        return int(string_input)
    except:
        raise Exception('Неверный формат целого числа!')


def get_validated_float(string_input : str):
    """Валидирует строку и возвращает число с плавающей точкой"""
    try:
        string_input = string_input.replace(u',', u'.')
        return float(string_input)
    except:
        raise Exception(f'Неверный формат десятичной дроби! {string_input}')


def run_func(function_name, **kwargs):
    """Запуск любой функции с соответствующими ей аргументами"""
    if None in kwargs.values():
        raise Exception('Не хватает аргументов!')
    else:
        return getattr(physic_functions, function_name)(**kwargs)

def get_non_default_params_of_func(function_name):
    sig = inspect.signature(getattr(physic_functions, function_name))
    return (p for p in sig.parameters if sig.parameters[p].default == inspect.Parameter.empty)

def validate_input_string(string_input):
    if string_input is None or string_input == '':
        raise Exception('Пустая строка ввода')
    else: return string_input

def parse_yaml(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data