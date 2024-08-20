"""
    Различные вспомогательные фукнции
"""
from core.model.functions import PhysicFunctions


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
        return getattr(PhysicFunctions, function_name)(**kwargs)

def validate_input_string(string_input):
    if string_input is None or string_input == '':
        raise Exception('Пустая строка ввода')
    else: return string_input