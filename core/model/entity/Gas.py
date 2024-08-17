import CoolProp.CoolProp as CP
import core.model.functions.constants as CONST


class Gas:
    """Класс Газ принимает в себя покомпонентный углеводородный состав,
    наименование термодинамического пакета для расчёта, одного из трех:
        '' - по умолчанию будет выбран PR - уравнение состояния Пенга-Робинсона
        SRK - уравнение состояния Соава-Редлиха-Квонга
        HEOS - уравнение состояния Гельмгольца
    При этом при первичной инициализации фактически рассчитываются самые элементарные параметры:
        состав газа в виде словарей:
            mole_composition:
                    key - углеводород
                    value - мольная доля
            mass_composition:
                key - углеводород
                value - массовая доля"""

    def __init__(self, composition: dict, fluid_pack: str=''):
        self.mole_composition = composition # состав в мольных долях компонентов
        fluid_pack_list = ['PR', 'SRK', 'HEOS']
        if fluid_pack in fluid_pack_list:
            fluid_pack += '::'
        # готовый кусок с термодинамическим пакетом и мольным составом для расчётов в CoolProp
        self.mixture = fluid_pack + '&'.join([f'{key}[{value}]' for key, value in self.mole_composition.items()])
        self.molecular_mass = CP.PropsSI('M', self.mixture)
        self.mass_composition = {key: (composition[key] * CP.PropsSI('M', key) / self.molecular_mass)
                                 for key in composition.keys()} # состав в массовых долях компонентов

    def input_temperature_pressure(self, temperature: float, pressure: float) -> tuple:
        """Метод создаёт два новых атрибута класса - температура и давление
        на входе:
            температура в °С,
            давление в МПа (изб.)
        на выходе:
            температура в К
            давление в Па (абс.)
            пока не знаю, надо ли это"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        return self.temperature, self.pressure

    def get_standard_density(self) -> float:
        """Метод возвращает плотность смеси при стандартных условиях"""
        return CP.PropsSI('D', 'T', CONST.CELSIUS_TO_KELVIN_SHIFT + 20, 'P', CONST.PASCAL_TO_ATM, self.mixture)

    def get_normal_density(self) -> float:
        """Метод возвращает плотность смеси при нормальных условиях"""
        return CP.PropsSI('D', 'T', CONST.CELSIUS_TO_KELVIN_SHIFT, 'P', CONST.PASCAL_TO_ATM, self.mixture)

    def get_actual_density(self, temperature: float, pressure: float) -> float:
        """Метод принимает температуру в °С, давление в избыточных, то есть свыше атмосферного,
        МПа (это надо будет потом пофиксить, должна быть
        вариативность единиц измерения), возвращает плотность смеси при заданных условиях"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        return CP.PropsSI('D', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def get_entalpy(self, temperature: float, pressure: float) -> float:
        """Возвращает энтальпию смеси при заданных температуре и давлении"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        return CP.PropsSI('H', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def get_rate(self, temperature: float, pressure: float, rate: float, parameter='standard') -> float:
        """Метод возвращает расход в зависимости от заданного параметра, по умолчанию стандартный расход,
        также может принимать значения:
            mass - массовый расход, кг/ч
            standard - расход при стандартных условиях, м3/ч
            normal - расход при нормальных условиях, м3/ч
            actual - расход при рабочих условиях, м3/ч"""
        mass_rate = rate * self.get_standard_density()
        standard_rate = rate
        normal_rate = mass_rate / self.get_normal_density()
        actual_rate = mass_rate / self.get_actual_density(temperature, pressure)
        rate = {'mass': mass_rate,
                'standard': standard_rate,
                'normal': normal_rate,
                'actual': actual_rate}
        return rate[parameter]

    def get_component_specific_heat(self, temperature: float, pressure: float) -> dict:
        """Метод возвращает теплоёмкость компонентов при заданных ему температуре и давлению"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        return {key: (CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, key)) for key in self.composition}

    def get_specific_heat(self, temperature: float, pressure: float) -> float:
        """Метод возвращает теплоёмкость смеси при заданных ему температуре и давлении"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        return CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def heat_stream(self, temperature: float, pressure: float) -> float:
        """Метод возвращает тепловой поток смеси"""
        return self.get_rate(temperature, pressure, parameter='mass') * self.get_specific_heat(temperature, pressure)

    def viscosity(self, temperature: float, pressure: float) -> float:
        """Метод возвращает вязкость смеси при заданных температуре и давлении"""
        self.temperature = temperature + CONST.CELSIUS_TO_KELVIN_SHIFT
        self.pressure = pressure * 1e6 + CONST.PASCAL_TO_ATM
        try:
            self.viscosity = CP.PropsSI('V', 'T', self.temperature, 'P', self.pressure, self.mixture)
        except ValueError as e:
            print(e)
        return self.viscosity