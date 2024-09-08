from core.util.ConfigCache import ConfigCache
from core.util.util_functions import parse_yaml
from core.view.TkWindow import Window, TkScreenBuilder


class TkAppContext:
    """
    Класс, осуществляющий внедрение зависимостей между графическим интерфейсом Tkinter'а и логикой приложения
    """

    def __init__(self):
        TkAppContext.singleton = self
        self.app_properties = parse_yaml('properties.yml')
        self.binding_config_list = parse_yaml('view\\binding_config.yml')
        self.template_config_list = parse_yaml('view\\template_config.yml')
        self.window = Window(self.app_properties['application_name'])
        self.builder = TkScreenBuilder(self.window)

        config_cache = ConfigCache.get_cache()
        config_cache.set('context', self)
        config_cache.set('window', self.window)
        config_cache.set('binding_config_list', self.binding_config_list)
        config_cache.set('template_config_list', self.template_config_list)

    def run_app(self):
        self.make_context('Главное меню')
        self.window.mainloop()

    def make_context(self, screen_name):
        if screen_name not in self.binding_config_list or self.binding_config_list[screen_name] is None:
            raise Exception(f'Нет окна с названием {screen_name}')
        binding_config = self.binding_config_list[screen_name]
        screen = binding_config['screen']
        screen_config = self.template_config_list[screen]
        self.builder.build_screen(screen_name, screen_config, binding_config)
        self.builder.bind_widgets()


        # if template == 'main_menu':
        #     self.builder.build_main_menu(self.window_config)
        #     buttons = self.builder.button_list
        #     for button in buttons:
        #         window_name = button.cget('text')
        #         screen_config = self.window_config[button.cget('text')]
        #         callback = None
        #         if screen_config is not None:
        #             callback = lambda e, lbl=window_name: self.make_context(lbl)
        #         button.bind('<Button-1>', callback)
        #     self.window.mainloop()
        #
        # elif template == 'default_calculator':
        #     self.builder.build_calculator(window_name, screen_config)
        #     back_to_menu_button = self.window.widgets['button']['__to_main_menu__']
        #     back_to_menu_button.bind('<Button-1>', lambda e: self.run_app())
        #
        #     widget_config = screen_config['widgets']
        #
        #     if 'entry' in widget_config:
        #         entries = widget_config['entry']
        #         for name in entries:
        #             entry = self.window.widgets['input'][name]
        #             entry.label.configure(text=name)
        #
        #     if 'combobox' in widget_config:
        #         combobox_config = widget_config['combobox']
        #         for name in combobox_config:
        #             combobox = self.window.widgets['input'][name]
        #             combobox.label.configure(text=name)
        #             combo = combobox.widget
        #             combo['values'] = getattr(clbk, combobox_config[name])()
        #             combo.current(0)
        #
        #     if 'button' in widget_config:
        #         buttons = widget_config['button']
        #         for name in buttons:
        #             button = self.window.widgets['button'][name]
        #             button.configure(text=name)
        #             callback = None
        #             if name[:2] != '__':
        #                 callback = lambda e, func=name: self.util.run(func)
        #             button.bind('<Button-1>', callback)
        #
        # elif template == 'plot':
        #
        #     def draw_plot():
        #         df = getattr(clbk, 'get_statistic_data_by_outlet_name')(self.window.widgets['input']['outlet'].widget.get())
        #         if df is not None:
        #             ax = self.window.widgets['plot']['plot']
        #             ax.cla()
        #             y_axis = self.window.widgets['input']['quantity'].widget.get()
        #             df.plot(x='date', y=y_axis, ax=ax)
        #             canvas = self.window.widgets['plot']['canvas']
        #             canvas.draw()
        #
        #     self.builder.build_plot_window(screen_config)
        #     back_to_menu_button = self.window.widgets['button']['__to_main_menu__']
        #     back_to_menu_button.bind('<Button-1>', lambda e: self.run_app())
        #
        #     widget_config = screen_config['widgets']
        #     q_combo = self.window.widgets['input']['quantity'].widget
        #     q_combo['values'] = ['day_capacity', 'hour_capacity', 'pressure', 'temperature', 'actual_flow']
        #     q_combo.current(0)
        #
        #     if 'combobox' in widget_config:
        #         combobox_config = widget_config['combobox']
        #         grs_combo = None
        #         for name in combobox_config:
        #             combobox = self.window.widgets['input'][name]
        #             combobox.label.configure(text=name)
        #             combo = combobox.widget
        #             if name == 'composition':
        #                 combo['values'] = getattr(clbk, combobox_config[name])()
        #                 combo.current(0)
        #                 grs_combo = combo
        #             elif name == 'outlet':
        #                 c_name = name
        #                 c_combo = combo
        #                 def assign_cbox(g_name):
        #                     outlets = getattr(clbk, combobox_config[c_name])(g_name)
        #                     if len(outlets) > 0:
        #                         c_combo['values'] = outlets
        #                         c_combo.current(0)
        #                         draw_plot()
        #                     else:
        #                         c_combo['values'] = []
        #                         c_combo.set('')
        #
        #                 assign_cbox(grs_combo.get())
        #                 grs_combo.bind("<<ComboboxSelected>>", lambda e: assign_cbox(grs_combo.get()))
        #                 c_combo.bind("<<ComboboxSelected>>", lambda e: draw_plot())
        #
        #             elif name == 'quantity':
        #                 combo.bind("<<ComboboxSelected>>", lambda e: draw_plot())
        #
        #
        #     if 'button' in widget_config:
        #         buttons = widget_config['button']
        #         for name in buttons:
        #             button = self.window.widgets['button'][name]
        #             button.configure(text=name)
        #             callback = None
        #             if name[:2] != '__':
        #                 callback = lambda e: draw_plot()
        #             button.bind('<Button-1>', callback)
        #     draw_plot()

    def get_window(self):
        return self.window

