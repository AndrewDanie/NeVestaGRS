from tkinter.constants import INSERT

from core.controller.UtilFunctions import *
from core.model.functions.function_props import commands


class Controller:

    __instance = None
    @classmethod
    def getInstance(cls):
        if not cls.__instance

    def __init__(self):
        self.window = None
        self.inputs = None
        self.outputs = None
        self.txt_window = None
        self.composition = {
            'Methane': 0.7,
            'Ethane': 0.2,
            'Propane': 0.1
        }

    def bind_window(self, window):
        self.window = window

    def bind_widgets(self):
        self.inputs = self.window.interactive_widgets['inputs']
        self.outputs = self.window.interactive_widgets['outputs']
        self.txt_window = self.window.interactive_widgets['outputs']['scrolled_window']

    def run(self, command_name):
        if self.window == None:
            raise Exception(f'Нет связанного с контроллером окна!')
        if command_name not in commands:
            raise Exception(f'Нет команды {command_name}')
        command_data = commands[command_name]
        args_data = command_data['args']
        kwargs = dict()

        if 'manual_input' in args_data:
            for inpt in args_data['manual_input']:
                label = args_data['manual_input'][inpt]
                str_value = validate_input_string(self.inputs[label].get())
                value = get_validated_float(str_value)
                kwargs[inpt] = value
        if 'composition' in args_data:
            if args_data['composition']:
                kwargs['composition'] = self.composition

        result = run_func(command_data['function'], **kwargs)

        return_data = command_data['return']
        self.txt_window.configure(state='normal')
        for name in return_data:
            self.txt_window.insert(INSERT, return_data[name] + ' = ' + str(result[name]) + '\n')
        self.txt_window.configure(state='disable')