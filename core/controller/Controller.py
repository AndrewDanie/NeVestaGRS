from core.controller.util_functions import *
from core.model.repository import callback
from core.view.IView import IView


class Controller:

    def __init__(self, view: IView):
        self.view = view

    def run(self, function_name):
        func_parameters = get_non_default_params_of_func(function_name)

        kwargs = dict()
        for param_name in func_parameters:
            if param_name == 'composition':
                grs_name = self.view.get_data(f'input.{param_name}')
                kwargs[param_name] = callback.get_composition_set_by_grs_name(grs_name)
            elif param_name == 'outlet':
                grs_name = self.view.get_data(f'input.composition')
                kwargs[param_name] = callback.get_outlet_set_by_grs_name(grs_name)
            else:
                str_value = self.view.get_data(f'input.{param_name}')
                str_value = validate_input_string(str_value)
                value = get_validated_float(str_value)
                kwargs[param_name] = value

        result = run_func(function_name, **kwargs)
        self.view.set_data('output.__txt_field__', result)