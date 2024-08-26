from gc import callbacks
from tkinter.constants import INSERT

from core.model.functions.variables import cache_variable_dict
from core.controller.util_functions import *
from core.model.repository import callback
from core.view.Window import Window


class Controller:

    __instance = None
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            return 

    def __init__(self, window: Window):
        self.window = window
        self.properties = parse_yaml('view\\window_config.yml')

    def run_application(self):
        self.window.build_window_menu(self.properties)
        buttons = self.window.button_list
        for button in buttons:
            window_name = button.cget('text')
            window_data = self.properties[button.cget('text')]
            callback = None
            if window_data is not None:
                callback = lambda e, lbl=window_name: self.configure_gui(lbl)
            button.bind('<Button-1>', callback)
        self.window.mainloop()

    def configure_gui(self, window_name):
        if window_name not in self.properties or self.properties[window_name] is None:
            raise Exception(f'Нет окна с названием {window_name}')
        window_data = self.properties[window_name]
        if window_data['gui_template'] == 'default_calculator':
            self.window.build_default_calculator(window_name, window_data)
            back_to_menu_button = self.window.root.nametowidget('to_main_menu_button')
            back_to_menu_button.bind('<Button-1>', lambda e: self.run_application())
            buttons = window_data['widgets']['button']
            for name in buttons:
                button = self.window.root.nametowidget(f'right_frame.{name}_button_wrapper.{name}')
                callback = None
                if name[:2] != '__':
                    callback = lambda e, func=name: self.run(func)
                button.bind('<Button-1>', callback)

    def get_input(self, name):
        input_widget = self.window.root.nametowidget(f'right_frame.{name}_input_wrapper.{name}')
        return input_widget.get()

    def run(self, function_name):
        func_parameters = get_non_default_params_of_func(function_name)

        kwargs = dict()
        for param_name in func_parameters:
            if param_name == 'composition':
                grs_name = self.get_input(param_name)
                kwargs[param_name] = callback.get_composition_set_by_grs_name(grs_name)
            else:
                str_value = self.get_input(param_name)
                str_value = validate_input_string(str_value)
                value = get_validated_float(str_value)
                kwargs[param_name] = value

        result = run_func(function_name, **kwargs)
        output_txt_field = self.window.root.nametowidget('left_frame.!frame.output_txt_field')
        output_txt_field.configure(state='normal')
        for name in result:
            output_txt_field.insert(INSERT, cache_variable_dict[name] + ' = ' + str(result[name]) + '\n')
        output_txt_field.configure(state='disable')