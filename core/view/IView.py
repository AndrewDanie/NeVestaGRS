"""
Интерфейсы view
"""

class IInput:
    def get_data(self, parameter_path):
        """
        Позволяет получить данные из вьюхи по указанному пути элемента вьюхи
        """


class IOutput:
    def set_data(self, parameter_path, output_entity):
        """
        Позволяет отдать данные во вьюху по указанному пути элемента вьюхи
        """


class IView(IInput, IOutput):
    """
    Комбинация интерфейсов ввода и вывода
    """
