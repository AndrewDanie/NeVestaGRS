

class InputEntity:

    def __init__(self):
        self._inputs = dict()

    def get_type(self):
        pass

    def get_input_value(self, input_name):
        pass

    def set_input(self, input_name, input_block):
        self._inputs[input_name] = input_block

