from core.view.Window import Window


class Controller:

    def __init__(self, window: Window):
        self.window = window
        self.commands = dict()

    def bind_command(self, gui_element, command):
        pass

    def subscribe_on(self, model):
        model.set_subscriber(self)

