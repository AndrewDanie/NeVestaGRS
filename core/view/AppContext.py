from core.controller.Controller import Controller
from core.controller.util_functions import parse_yaml
from core.view.TkWindow import Window, TkGuiBuilder


class TkAppContext:
    """
    Класс, осуществляющий внедрение зависимостей между графическим интерфейсом Tkinter'а и логикой приложения
    Имеет доступ к объектам Window, не должен иметь доступа к WindowBuilder
    """

    def __init__(self):
        self.app_properties = parse_yaml('properties.yml')
        self.window_config = parse_yaml('view\\window_config.yml')
        print(self.app_properties)
        self.window = Window(self.app_properties['application_name'])
        self.builder = TkGuiBuilder(self.window)
        self.controller = Controller(self.window)

    def run_app(self):
        self.make_context('Главное меню')

    def make_context(self, window_name):
        """
        Внедряет зависимости между кнопками и логикой приложения
        """
        if window_name not in self.window_config or self.window_config[window_name] is None:
            raise Exception(f'Нет окна с названием {window_name}')
        window_data = self.window_config[window_name]
        template = window_data['gui_template']

        if template == 'main_menu':
            self.builder.build_main_menu(self.window_config)
            buttons = self.builder.button_list
            for button in buttons:
                window_name = button.cget('text')
                window_data = self.window_config[button.cget('text')]
                callback = None
                if window_data is not None:
                    callback = lambda e, lbl=window_name: self.make_context(lbl)
                button.bind('<Button-1>', callback)
            self.window.mainloop()

        elif template == 'default_calculator':
            self.builder.build_default_calculator(window_name, window_data)
            back_to_menu_button = self.window.widgets['button']['__to_main_menu__']
            back_to_menu_button.bind('<Button-1>', lambda e: self.run_app())
            buttons = window_data['widgets']['button']
            for name in buttons:
                button = self.window.widgets['button'][name]
                callback = None
                if name[:2] != '__':
                    callback = lambda e, func=name: self.controller.run(func)
                button.bind('<Button-1>', callback)

        elif template == 'plot':
            self.builder.build_plot_window()

    def get_window(self):
        return self.window