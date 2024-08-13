class Gas:
    def __init__(self, composition, temperature, pressure, rate=0):
        self.composition = composition
        self.temperature = temperature + 273.15
        self.pressure = 1e6 * pressure + 101325
        self.rate = rate
        self.mixture = '&'.join([f'{key}[{value}]' for key, value in self.composition.items()])
        self.entalpy = CP.PropsSI('H', 'T', self.temperature, 'P', self.pressure, self.mixture)
        self.actual_density = CP.PropsSI('D', 'T', self.temperature, 'P', self.pressure, 'PR::'+self.mixture)
        self.normal_density = CP.PropsSI('D', 'T', 273.15, 'P', 101325, 'PR::'+self.mixture)
        self.standard_density = CP.PropsSI('D', 'T', 293.15, 'P', 101325, 'PR::'+self.mixture)
        self.mass_flow = self.standard_density * self.rate
        self.actual_rate = self.mass_flow / self.actual_density
        self.molecular_weights = {'Methane': 16.04, 'Ethane': 30.07, 'Propane': 44.09, 'Isobutane': 58.12, 'Butane': 58.12, 'Isopentane': 72.15,
        'Pentane': 72.15, 'Hexane': 86.18, 'Oxygen': 31.99806, 'Nitrogen': 28.01286, 'CarbonDioxide': 44.01}
        self.component_specific_heat = {key: (CP.PropsSI('C', 'T', self.temperature, 'P', self.pressure, key)) for key in self.composition}
        self.specific_heat = sum(composition[key] * self.component_specific_heat[key] for key in self.composition)
        self.heat_stream = self.specific_heat * self.mass_flow * (self.temperature - 273.15)
        total_molecular_weight = sum(composition[key]*self.molecular_weights[key] for key in self.composition)
        self.mass_fraction = {key: (composition[key]*self.molecular_weights[key]/total_molecular_weight) for key in self.composition}
        try:
            self.viscosity = CP.PropsSI('V', 'T', self.temperature, 'P', self.pressure, self.mixture)
            print(f'Расчётная вязкость газа {round(self.viscosity * 1000, 5)} сПз')
        except ValueError:
            self.vicosity = 0.000011
            print('Вязкость не была посчитана, принята примерно, и составила 0.011 сПз')

        self.molecular_mass = CP.PropsSI('M', self.mixture) * 1000 #молекулярная масса на г/моль

    def get_actual_rate(self, temperature, pressure):
        temperature += 273.15
        pressure = 1e6 * pressure + 101325
        return self.mass_flow / CP.PropsSI('D', 'T', temperature, 'P', pressure, 'PR::'+self.mixture)


    """метод определения температуры газа в результате изоэнтальпийного расширения"""

    def expansion(self, final_pressure):
        initial_pressure = self.pressure
        initial_temperature = self.temperature
        print(initial_temperature, ' ', initial_pressure, ' ', final_pressure)
        state_initial = CP.PropsSI('H', 'T', initial_temperature, 'P', initial_pressure,
                                   self.mixture)  # изоэнтальпийное расширение
        final_temperature = CP.PropsSI('T', 'H', state_initial, 'P', final_pressure, self.mixture)
        print(final_temperature, ' ', state_initial, ' ')
        delta_T = initial_temperature - final_temperature
        return delta_T

