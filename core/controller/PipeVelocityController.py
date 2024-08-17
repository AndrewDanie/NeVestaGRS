from tkinter.constants import INSERT

from core.model.entity.Gas import Gas
from core.view.Window import Window
from core.model.functions.UtilFunctions import *
from core.model.functions.PhysicFunctions import velocity_calc


class PipeVelocityController:

    def __init__(self, window: Window):
        self.window = window
        self.inputs = self.window.interactive_widgets['inputs']
        self.outputs = self.window.interactive_widgets['outputs']
        self.composition = {
            'Methane': 0.7,
            'Ethane': 0.2,
            'Propane': 0.1
        }
        self.txt_window = self.window.interactive_widgets['outputs']['scrolled_window']

    def calc_pipe_velocity(self):
        pressure = get_validated_float(self.inputs['Давление, МПа'].get())
        temperature = get_validated_float(self.inputs['Температура, °С'].get())
        rate = get_validated_float(self.inputs['Расход'].get())
        diameter = get_validated_float(self.inputs['Внешний диаметр, мм'].get())
        wall = get_validated_float(self.inputs['Толщина стенки, мм'].get())


        result = run_func(velocity_calc, composition=composition, temperature=temperature, pressure=pressure, rate=rate, diameter=diameter, wall=wall)

        self.txt_window.configure(state='normal')
        self.txt_window.insert(INSERT, 'Скорость газа = ' +str(result))
        self.txt_window.configure(state='disable')

    def calc_gas_density(self):
        gas = Gas(self.composition)

        result = gas.get_normal_density(), gas.get_standard_density()

        self.txt_window.configure(state='normal')
        self.txt_window.insert(INSERT, "Плотность при н.у. = " +str(result[0]) + '\n' + 'Плотность при cт.у. = ' + str(result[1]))
        self.txt_window.configure(state='disable')