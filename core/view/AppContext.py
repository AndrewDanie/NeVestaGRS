from matplotlib import pyplot as plt
from core.controller.Controller import Controller
from core.controller.util_functions import parse_yaml
from core.model.repository import callback as clbk
from core.view.TkWindow import Window, TkScreenBuilder


class TkAppContext:
    """
    Класс, осуществляющий внедрение зависимостей между графическим интерфейсом Tkinter'а и логикой приложения
    """

    def __init__(self):
        self.app_properties = parse_yaml('properties.yml')
        self.window_config = parse_yaml('view\\window_config.yml')
        self.window = Window(self.app_properties['application_name'])
        self.builder = TkScreenBuilder(self.window)
        self.controller = Controller(self.window)

    def run_app(self):
        self.make_context('Главное меню')

    def make_context(self, window_name):
        """
        Внедряет зависимости между кнопками и логикой приложения
        """
        if window_name not in self.window_config or self.window_config[window_name] is None:
            raise Exception(f'Нет окна с названием {window_name}')
        screen_config = self.window_config[window_name]
        template = screen_config['gui_template']

        if template == 'main_menu':
            self.builder.build_main_menu(self.window_config)
            buttons = self.builder.button_list
            for button in buttons:
                window_name = button.cget('text')
                screen_config = self.window_config[button.cget('text')]
                callback = None
                if screen_config is not None:
                    callback = lambda e, lbl=window_name: self.make_context(lbl)
                button.bind('<Button-1>', callback)
            self.window.mainloop()

        elif template == 'default_calculator':
            self.builder.build_default_calculator(window_name, screen_config)
            back_to_menu_button = self.window.widgets['button']['__to_main_menu__']
            back_to_menu_button.bind('<Button-1>', lambda e: self.run_app())

            widget_config = screen_config['widgets']

            if 'entry' in widget_config:
                entries = widget_config['entry']
                for name in entries:
                    entry = self.window.widgets['input'][name]
                    entry.label.configure(text=name)

            if 'combobox' in widget_config:
                combobox_config = widget_config['combobox']
                for name in combobox_config:
                    combobox = self.window.widgets['input'][name]
                    combobox.label.configure(text=name)
                    combo = combobox.widget
                    combo['values'] = getattr(clbk, combobox_config[name])()
                    combo.current(0)

            if 'button' in widget_config:
                buttons = widget_config['button']
                for name in buttons:
                    button = self.window.widgets['button'][name]
                    button.configure(text=name)
                    callback = None
                    if name[:2] != '__':
                        callback = lambda e, func=name: self.controller.run(func)
                    button.bind('<Button-1>', callback)

        elif template == 'plot':
            self.builder.build_plot_window(screen_config)
            back_to_menu_button = self.window.widgets['button']['__to_main_menu__']
            back_to_menu_button.bind('<Button-1>', lambda e: self.run_app())

            widget_config = screen_config['widgets']

            if 'combobox' in widget_config:
                combobox_config = widget_config['combobox']
                grs_combo = None
                print(combobox_config)
                for name in combobox_config:
                    combobox = self.window.widgets['input'][name]
                    combobox.label.configure(text=name)
                    combo = combobox.widget
                    if name == 'composition':
                        combo['values'] = getattr(clbk, combobox_config[name])()
                        combo.current(0)
                        grs_combo = combo
                    elif name == 'outlet':
                        c_name = name
                        c_combo = combo
                        def assign_cbox(g_name):
                            outlets = getattr(clbk, combobox_config[c_name])(g_name)
                            if len(outlets) > 0:
                                c_combo['values'] = outlets
                                c_combo.current(0)
                            else:
                                c_combo['values'] = []
                                c_combo.set('')

                        assign_cbox(grs_combo.get())
                        grs_combo.bind("<<ComboboxSelected>>", lambda e: assign_cbox(grs_combo.get()))

                    elif name == 'quantity':
                        combo['values'] = ['day_capacity', 'hour_capacity', 'pressure', 'temperature', 'actual_flow']
                        combo.current(0)

            if 'button' in widget_config:
                buttons = widget_config['button']
                for name in buttons:
                    button = self.window.widgets['button'][name]
                    button.configure(text=name)
                    callback = None
                    if name[:2] != '__':
                        def draw_plot():
                            df = getattr(clbk, name)(self.window.widgets['input']['outlet'].widget.get())
                            if df is not None:
                                ax = self.window.widgets['plot']['plot']
                                ax.cla()
                                y_axis = self.window.widgets['input']['quantity'].widget.get()
                                df.plot(x='date', y=y_axis, ax=ax)
                                canvas = self.window.widgets['plot']['canvas']
                                canvas.draw()
                        callback = lambda e: draw_plot()
                    button.bind('<Button-1>', callback)

    def get_window(self):
        return self.window

