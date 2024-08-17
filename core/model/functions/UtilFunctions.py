"""
    Различные вспомогательные фукнции
"""

def get_validated_int(string_input):
    """Валидирует строку и возвращает целочисленное значение"""
    try:
        return int(string_input)
    except:
        raise Exception('Неверный формат целого числа!')


def get_validated_float(string_input : str):
    """Валидирует строку и возвращает число с плавающей точкой"""
    try:
        string_input.replace(',', '.')
        return int(string_input)
    except:
        raise Exception('Неверный формат десятичной дроби!')


def run_func(function, **kwargs):
    """Запуск любой функции с соответствующими ей аргументами"""
    if None in kwargs.values():
        raise Exception('Не хватает аргументов!')
    else:
        return function(**kwargs)
