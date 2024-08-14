from typing import Dict

from core.gui.InputEntity import InputEntity


class CalculateManager:

    def __init__(self):
        self.current_inputs = []
        self.current_functions = []
        self.current_outputs = []

    def add_input(self, input_entity):
        self.current_inputs.append(input_entity)

    def add_inputs(self, input_entity_list):
        for entity in input_entity_list:
            self.add_input(self, entity)

    def remove_all_inputs(self):
        self.current_inputs = []

    def add_function(self, function_entity):
        self.current_functions.append(function_entity)

    def add_functions(self, function_entity_list):
        for entity in function_entity_list:
            self.add_function(self, entity)

    def remove_all_functions(self):
        self.current_functions = []

    def add_output(self, output_entity):
        self.current_outputs.append(output_entity)

    def add_outputs(self, output_entity_list):
        for entity in output_entity_list:
            self.add_output(self, entity)

    def remove_all_outputs(self):
        self.current_outputs = []

    def calculate(self, input_entities : Dict[InputEntity], function, outputs):
        for entity in input_entities:
            input_block_list = input_entities[entity]
            for name in input_block_list:
                entity.get_input_value(name)