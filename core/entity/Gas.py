import CoolProp.CoolProp as CP

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
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        return self.temperature, self.pressure

    def standard_density(self) -> float:
        """Метод возвращает плотность смеси при стандартных условиях"""
        return CP.PropsSI('D', 'T', 293.15, 'P', 101325, self.mixture)

    def normal_density(self) -> float:
        """Метод возвращает плотность смеси при нормальных условиях"""
        return CP.PropsSI('D', 'T', 273.15, 'P', 101325, self.mixture)

    def actual_density(self, temperature: float, pressure: float) -> float:
        """Метод принимает температуру в °С, давление в избыточных, то есть свыше атмосферного,
        МПа (это надо будет потом пофиксить, должна быть
        вариативность единиц измерения), возвращает плотность смеси при заданных условиях"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        return CP.PropsSI('D', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def entalpy(self, temperature: float, pressure: float) -> float:
        """Возвращает энтальпию смеси при заданных температуре и давлении"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        return CP.PropsSI('H', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def rate(self, temperature: float, pressure: float, rate, parameter='standard') -> float:
        """Метод возвращает расход в зависимости от заданного параметра, по умолчанию стандартный расход
        также может принимать значения:
            mass - массовый расход, кг/ч
            standard - расход при стандартных условиях, м3/ч
            normal - расход при нормальных условиях, м3/ч
            actual - расход при рабочих условиях, м3/ч"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        self.mass_rate = rate * self.standard_density()
        self.standard_rate = rate
        self.normal_rate = self.mass_rate / self.normal_density()
        self.actual_rate = self.mass_rate / self.actual_density(temperature, pressure)
        rate = {'mass': self.mass_rate,
                'standard': self.standard_rate,
                'normal': self.normal_rate,
                'actual': self.actual_rate}
        return rate[parameter]

    def component_specific_heat(self, temperature: float, pressure: float) -> dict:
        """Метод возвращает теплоёмкость компонентов при заданных ему температуре и давлению"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        return {key: (CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, key)) for key in self.composition}

    def specific_heat(self, temperature: float, pressure: float) -> float:
        """Метод возвращает теплоёмкость смеси при заданных ему температуре и давлении"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        return CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, self.mixture)

    def heat_stream(self, temperature: float, pressure: float) -> float:
        """Метод возвращает тепловой поток смеси"""
        return self.rate(temperature, pressure, parameter='mass') * self.specific_heat(temperature, pressure)

    def viscosity(self, temperature: float, pressure: float) -> float:
        """Метод возвращает вязкость смеси при заданных температуре и давлении"""
        self.temperature = temperature + 273.15
        self.pressure = pressure * 1e6 + 101325
        try:
            self.viscosity = CP.PropsSI('V', 'T', self.temperature, 'P', self.pressure, self.mixture)
        except ValueError as e:
            print(e)
            return
        return self.viscosity